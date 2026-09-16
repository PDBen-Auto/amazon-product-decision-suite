from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "release_provenance.py"
SPEC = importlib.util.spec_from_file_location("release_provenance", SCRIPT_PATH)
assert SPEC and SPEC.loader
PROVENANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROVENANCE)


@unittest.skipUnless(importlib.util.find_spec("cryptography"), "cryptography is not installed")
class ProvenanceTests(unittest.TestCase):
    def create_release(self, root: Path):
        private_key = root / "publisher-private.pem"
        public_key = root / "publisher-public.pem"
        manifest = root / "PUBLIC_MANIFEST.sha256"
        provenance = root / "RELEASE_PROVENANCE.json"
        signature = root / "RELEASE_PROVENANCE.sig"
        manifest.write_text("0" * 64 + "  synthetic.txt\n", encoding="utf-8")
        PROVENANCE.command_generate_key(
            Namespace(
                private_key=private_key,
                public_key=public_key,
                passphrase_env="TEST_UNUSED_PASSPHRASE",
                allow_unencrypted_private_key=True,
            )
        )
        PROVENANCE.command_sign_release(
            Namespace(
                manifest=manifest,
                private_key=private_key,
                public_key=public_key,
                provenance=provenance,
                signature=signature,
                skill_name="amazon-product-decision-gateway",
                release_version="test-1",
                origin_id="origin-test",
                repository=None,
                passphrase_env="TEST_UNUSED_PASSPHRASE",
            )
        )
        return private_key, public_key, manifest, provenance, signature

    def test_signed_release_verifies(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            _, public_key, manifest, provenance, signature = self.create_release(Path(temp_dir))
            result = PROVENANCE.verify_release(
                manifest, provenance, signature, public_key, expected_origin_id="origin-test"
            )
            self.assertTrue(result["verified"])

    def test_modified_manifest_fails_verification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            _, public_key, manifest, provenance, signature = self.create_release(Path(temp_dir))
            manifest.write_text("modified\n", encoding="utf-8")
            with self.assertRaises(PROVENANCE.ProvenanceError):
                PROVENANCE.verify_release(manifest, provenance, signature, public_key)

    def test_challenge_signature_verifies(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            private_key, public_key, _, _, _ = self.create_release(Path(temp_dir))
            private = PROVENANCE.load_private_key(private_key, "TEST_UNUSED_PASSPHRASE")
            public = PROVENANCE.load_public_key(public_key)
            payload = PROVENANCE.challenge_payload("origin-test", "nonce-123", public)
            signature = private.sign(PROVENANCE.canonical_json_bytes(payload))
            public.verify(signature, PROVENANCE.canonical_json_bytes(payload))
            self.assertEqual(payload["challenge"], "nonce-123")

    def test_provenance_json_contains_no_private_material(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            _, _, _, provenance, _ = self.create_release(Path(temp_dir))
            value = json.loads(provenance.read_text(encoding="utf-8"))
            self.assertNotIn("private_key", value)
            self.assertEqual(value["origin_id"], "origin-test")


if __name__ == "__main__":
    unittest.main()

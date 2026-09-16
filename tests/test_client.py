from __future__ import annotations

import copy
import base64
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLIENT_PATH = ROOT / "scripts" / "decision_client.py"
VALID_REQUEST_PATH = ROOT / "tests" / "fixtures" / "valid_request.json"
INVALID_REQUEST_PATH = ROOT / "tests" / "fixtures" / "invalid_request.json"

SPEC = importlib.util.spec_from_file_location("decision_client", CLIENT_PATH)
assert SPEC and SPEC.loader
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class DecisionClientTests(unittest.TestCase):
    def setUp(self):
        self.valid_request = read_json(VALID_REQUEST_PATH)

    def test_valid_request_passes(self):
        self.assertEqual(CLIENT.validate_request(self.valid_request), [])

    def test_invalid_fixture_reports_multiple_contract_errors(self):
        errors = CLIENT.validate_request(read_json(INVALID_REQUEST_PATH))
        self.assertGreaterEqual(len(errors), 8)
        self.assertTrue(any("duplicate" in error for error in errors))
        self.assertTrue(any("currency" in error for error in errors))

    def test_sensitive_key_is_rejected(self):
        request = copy.deepcopy(self.valid_request)
        request["evidence_bundle"]["api_key"] = "synthetic-value"
        errors = CLIENT.validate_request(request)
        self.assertTrue(any("sensitive key" in error for error in errors))

    def test_local_user_path_is_rejected(self):
        request = copy.deepcopy(self.valid_request)
        request["evidence_bundle"]["evidence"][0]["source"]["locator"] = "/home/" + "demo/private/file.json"
        errors = CLIENT.validate_request(request)
        self.assertTrue(any("local user path" in error for error in errors))

    def test_canonical_hash_is_stable_across_key_order(self):
        first = {"b": 2, "a": 1}
        second = {"a": 1, "b": 2}
        self.assertEqual(CLIENT.sha256_hex(first), CLIENT.sha256_hex(second))

    def test_valid_response_binds_to_request(self):
        request_hash = CLIENT.sha256_hex(self.valid_request)
        response = {
            "schema_version": "1.0",
            "result_id": "result-demo-001",
            "engine_version": "engine-demo-001",
            "request_sha256": request_hash,
            "status": "partial",
            "verdict": "CONDITIONAL_GO",
            "confidence": "medium",
            "stage_matrix": [],
            "conditions": [],
            "gaps": [],
        }
        response["result_sha256"] = CLIENT.sha256_hex(CLIENT.response_payload(response))
        self.assertEqual(CLIENT.validate_response(response, request_hash), [])

    def test_response_request_mismatch_fails(self):
        response = {
            "schema_version": "1.0",
            "result_id": "result-demo-001",
            "engine_version": "engine-demo-001",
            "request_sha256": "0" * 64,
            "status": "complete",
            "verdict": "GO",
            "confidence": "high",
            "stage_matrix": [],
            "conditions": [],
            "gaps": [],
        }
        response["result_sha256"] = CLIENT.sha256_hex(CLIENT.response_payload(response))
        errors = CLIENT.validate_response(response, "1" * 64)
        self.assertTrue(any("does not match" in error for error in errors))

    def test_http_endpoint_is_rejected(self):
        with self.assertRaises(CLIENT.ClientError):
            CLIENT.validate_endpoint("http://example.invalid/v1/decisions")

    @unittest.skipUnless(importlib.util.find_spec("cryptography"), "cryptography is not installed")
    def test_ed25519_signature_verifies(self):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        request_hash = CLIENT.sha256_hex(self.valid_request)
        response = {
            "schema_version": "1.0",
            "result_id": "result-demo-signed",
            "engine_version": "engine-demo-signed",
            "request_sha256": request_hash,
            "status": "complete",
            "verdict": "CONDITIONAL_GO",
            "confidence": "medium",
            "stage_matrix": [],
            "conditions": [],
            "gaps": [],
        }
        response["result_sha256"] = CLIENT.sha256_hex(CLIENT.response_payload(response))
        private_key = Ed25519PrivateKey.generate()
        response["signature_alg"] = "ed25519"
        response["signature"] = base64.b64encode(
            private_key.sign(CLIENT.canonical_json_bytes(CLIENT.response_payload(response)))
        ).decode("ascii")
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            key_path = Path(temp_dir) / "public.pem"
            key_path.write_bytes(public_pem)
            CLIENT.verify_signature(response, key_path)

    def test_cli_validate_writes_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "validation.json"
            completed = subprocess.run(
                [sys.executable, str(CLIENT_PATH), "validate", str(VALID_REQUEST_PATH), "--report", str(report)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(report.exists())
            self.assertTrue(read_json(report)["valid"])

    def test_submit_requires_explicit_acknowledgement(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "response.json"
            completed = subprocess.run(
                [sys.executable, str(CLIENT_PATH), "submit", str(VALID_REQUEST_PATH), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 3)
            self.assertIn("acknowledge-external-processing", completed.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallSmokeTest(unittest.TestCase):
    def test_release_zip_has_one_installable_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            package = work / "amazon-product-decision-gateway"
            for name in (
                "SKILL.md",
                "agents",
                "references",
                "scripts",
                "requirements.txt",
                "LICENSE",
                "SECURITY.md",
                ".well-known",
                "PUBLISHER_PUBLIC_KEY.pem",
                "PUBLIC_MANIFEST.sha256",
                "RELEASE_PROVENANCE.json",
                "RELEASE_PROVENANCE.sig",
            ):
                source = ROOT / name
                target = package / name
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)

            archive = work / "skill.zip"
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
                for path in package.rglob("*"):
                    if path.is_file():
                        handle.write(path, path.relative_to(work).as_posix())

            extracted = work / "extracted"
            with zipfile.ZipFile(archive) as handle:
                handle.extractall(extracted)

            skill_files = list(extracted.rglob("SKILL.md"))
            self.assertEqual([Path("amazon-product-decision-gateway/SKILL.md")], [p.relative_to(extracted) for p in skill_files])
            self.assertTrue((extracted / "amazon-product-decision-gateway/agents/openai.yaml").is_file())
            self.assertTrue((extracted / "amazon-product-decision-gateway/scripts/decision_client.py").is_file())
            self.assertTrue((extracted / "amazon-product-decision-gateway/references/request-schema.md").is_file())
            self.assertFalse((extracted / "amazon-product-decision-gateway/amazon-product-decision-gateway").exists())


if __name__ == "__main__":
    unittest.main()

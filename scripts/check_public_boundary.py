#!/usr/bin/env python3
"""Fail when private-core files, secrets, or real-case data enter the public repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/decision_client.py",
    "scripts/check_public_boundary.py",
    "scripts/build_release_manifest.py",
    "scripts/release_provenance.py",
    "references/request-schema.md",
    "references/response-schema.md",
    "references/security-model.md",
    "docs/provenance.md",
    ".well-known/skill-provenance.json",
    "tests/test_client.py",
    "tests/test_provenance.py",
    "tests/trigger-cases.md",
    "tests/fixtures/valid_request.json",
    "tests/fixtures/invalid_request.json",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".gitattributes",
    "README.md",
    "README.en.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "LICENSE",
    "requirements.txt",
    "PUBLIC_MANIFEST.sha256",
    "PUBLISHER_PUBLIC_KEY.pem",
    "RELEASE_PROVENANCE.json",
    "RELEASE_PROVENANCE.sig",
}
FORBIDDEN_BASENAMES = {
    "decision-gates.md",
    "pipeline-contract.md",
    "method.md",
    "output-contract.md",
    "feasibility-framework.md",
    "supplier-intake.md",
    "input-schema.md",
    "metric-definitions.md",
    "calculate_unit_economics.py",
    "score_feasibility.py",
    "validate_evidence.py",
}
FORBIDDEN_PARTS = {"private", "private-core", "server", ".env", "real-data", "production-data"}
FORBIDDEN_TEXT = (
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("bearer token", re.compile(r"(?i)authorization:\s*bearer\s+\S+")),
    ("real case ASIN", re.compile("B0CF" + "QFMC4F")),
    ("real case brand", re.compile("REAL" + "INN", re.IGNORECASE)),
    ("local user path", re.compile(r"(?i)C:\\Users\\S" + "YZ")),
)
ALLOWED_PUBLIC_KEY_FILES = {"PUBLISHER_PUBLIC_KEY.pem"}
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".toml", ".pem"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}


def scan(root: Path) -> list[str]:
    errors: list[str] = []
    present = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    for required in sorted(REQUIRED_FILES - present):
        errors.append(f"missing required public file: {required}")

    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=str):
        relative = path.relative_to(root)
        relative_posix = relative.as_posix()
        if any(part in SKIP_PARTS for part in relative.parts):
            continue
        if path.name.lower() in FORBIDDEN_BASENAMES:
            errors.append(f"private-core filename is forbidden: {relative_posix}")
        if any(part.lower() in FORBIDDEN_PARTS for part in relative.parts):
            errors.append(f"private or secret path is forbidden: {relative_posix}")
        if path.suffix.lower() in {".key", ".p12", ".pfx"} or (
            path.suffix.lower() == ".pem" and path.name not in ALLOWED_PUBLIC_KEY_FILES
        ):
            errors.append(f"key material is forbidden: {relative_posix}")
        if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 2 * 1024 * 1024:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"text file is not UTF-8: {relative_posix}")
            continue
        if path.name in ALLOWED_PUBLIC_KEY_FILES:
            if "BEGIN PUBLIC KEY" not in text or "PRIVATE KEY" in text:
                errors.append(f"allowed PEM is not a public key: {relative_posix}")
        for label, pattern in FORBIDDEN_TEXT:
            if pattern.search(text):
                errors.append(f"{label} detected in {relative_posix}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors = scan(root)
    if errors:
        print("Public boundary check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Public boundary check passed: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

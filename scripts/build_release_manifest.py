#!/usr/bin/env python3
"""Write or verify a deterministic SHA-256 manifest for public release files."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


MANIFEST_NAME = "PUBLIC_MANIFEST.sha256"
SIGNED_METADATA_NAMES = {"RELEASE_PROVENANCE.json", "RELEASE_PROVENANCE.sig"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}


def release_files(root: Path):
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
        relative = path.relative_to(root)
        if path.name == MANIFEST_NAME or path.name in SIGNED_METADATA_NAMES or any(
            part in SKIP_PARTS for part in relative.parts
        ):
            continue
        yield path, relative.as_posix()


def build(root: Path) -> str:
    lines = []
    for path, relative in release_files(root):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {relative}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = root / MANIFEST_NAME
    expected = build(root)
    if args.write:
        manifest_path.write_text(expected, encoding="utf-8", newline="\n")
        print(f"Wrote {manifest_path}")
        return 0
    if not manifest_path.exists():
        print(f"Missing {manifest_path}", file=sys.stderr)
        return 1
    actual = manifest_path.read_text(encoding="utf-8")
    if actual != expected:
        print("Release manifest does not match repository files", file=sys.stderr)
        return 1
    print(f"Release manifest verified: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

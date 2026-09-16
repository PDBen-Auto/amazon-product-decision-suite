#!/usr/bin/env python3
"""Create and verify publisher-signed release provenance for this public Skill."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SIGNATURE_ALG = "ed25519"
DEFAULT_PASSPHRASE_ENV = "AMAZON_GATEWAY_PUBLISHER_KEY_PASSPHRASE"


class ProvenanceError(RuntimeError):
    """Expected provenance failure with a concise user-facing message."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ProvenanceError(f"cannot read '{path}': {exc}") from exc


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProvenanceError(f"cannot read JSON '{path}': {exc}") from exc
    if not isinstance(value, dict):
        raise ProvenanceError(f"'{path}' must contain a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def crypto_modules():
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    except ImportError as exc:
        raise ProvenanceError("release provenance requires the Python 'cryptography' package") from exc
    return InvalidSignature, serialization, Ed25519PrivateKey, Ed25519PublicKey


def load_public_key(path: Path):
    _, serialization, _, Ed25519PublicKey = crypto_modules()
    try:
        key = serialization.load_pem_public_key(read_bytes(path))
    except ValueError as exc:
        raise ProvenanceError(f"invalid public key '{path}'") from exc
    if not isinstance(key, Ed25519PublicKey):
        raise ProvenanceError("publisher public key must be Ed25519")
    return key


def public_key_der(key) -> bytes:
    _, serialization, _, _ = crypto_modules()
    return key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def public_key_fingerprint(key) -> str:
    return sha256_bytes(public_key_der(key))


def load_private_key(path: Path, passphrase_env: str):
    _, serialization, Ed25519PrivateKey, _ = crypto_modules()
    passphrase = os.environ.get(passphrase_env)
    password = passphrase.encode("utf-8") if passphrase else None
    try:
        key = serialization.load_pem_private_key(read_bytes(path), password=password)
    except (TypeError, ValueError) as exc:
        raise ProvenanceError(
            f"cannot unlock publisher key; set {passphrase_env} when the key is encrypted"
        ) from exc
    if not isinstance(key, Ed25519PrivateKey):
        raise ProvenanceError("publisher private key must be Ed25519")
    return key


def command_generate_key(args: argparse.Namespace) -> int:
    _, serialization, Ed25519PrivateKey, _ = crypto_modules()
    if args.private_key.exists() or args.public_key.exists():
        raise ProvenanceError("refusing to overwrite an existing publisher key")
    passphrase = os.environ.get(args.passphrase_env)
    if not passphrase and not args.allow_unencrypted_private_key:
        raise ProvenanceError(
            f"set {args.passphrase_env} or explicitly use --allow-unencrypted-private-key"
        )
    encryption = (
        serialization.BestAvailableEncryption(passphrase.encode("utf-8"))
        if passphrase
        else serialization.NoEncryption()
    )
    private_key = Ed25519PrivateKey.generate()
    args.private_key.parent.mkdir(parents=True, exist_ok=True)
    args.public_key.parent.mkdir(parents=True, exist_ok=True)
    args.private_key.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption,
        )
    )
    args.public_key.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    print(
        json.dumps(
            {
                "private_key": str(args.private_key),
                "public_key": str(args.public_key),
                "public_key_sha256": public_key_fingerprint(private_key.public_key()),
                "private_key_encrypted": bool(passphrase),
            },
            indent=2,
        )
    )
    return 0


def release_payload(args: argparse.Namespace, public_key) -> dict[str, Any]:
    payload = {
        "schema_version": "1.0",
        "signature_alg": SIGNATURE_ALG,
        "scope": "public-skill-package",
        "skill_name": args.skill_name,
        "release_version": args.release_version,
        "origin_id": args.origin_id,
        "manifest_sha256": sha256_bytes(read_bytes(args.manifest)),
        "publisher_public_key_sha256": public_key_fingerprint(public_key),
        "prompt_neutral": True,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    if args.repository:
        payload["repository"] = args.repository
    return payload


def command_sign_release(args: argparse.Namespace) -> int:
    private_key = load_private_key(args.private_key, args.passphrase_env)
    public_key = load_public_key(args.public_key)
    if public_key_der(private_key.public_key()) != public_key_der(public_key):
        raise ProvenanceError("private key does not match PUBLISHER_PUBLIC_KEY.pem")
    payload = release_payload(args, public_key)
    signature = private_key.sign(canonical_json_bytes(payload))
    write_json(args.provenance, payload)
    args.signature.write_text(
        base64.b64encode(signature).decode("ascii") + "\n",
        encoding="ascii",
        newline="\n",
    )
    print(json.dumps({"signed": True, **payload}, indent=2))
    return 0


def verify_release(
    manifest: Path,
    provenance_path: Path,
    signature_path: Path,
    public_key_path: Path,
    expected_origin_id: str | None = None,
    expected_fingerprint: str | None = None,
) -> dict[str, Any]:
    InvalidSignature, _, _, _ = crypto_modules()
    payload = read_json(provenance_path)
    public_key = load_public_key(public_key_path)
    fingerprint = public_key_fingerprint(public_key)
    if payload.get("signature_alg") != SIGNATURE_ALG:
        raise ProvenanceError("unsupported release signature algorithm")
    if payload.get("manifest_sha256") != sha256_bytes(read_bytes(manifest)):
        raise ProvenanceError("release manifest hash does not match signed provenance")
    if payload.get("publisher_public_key_sha256") != fingerprint:
        raise ProvenanceError("publisher public-key fingerprint mismatch")
    if expected_origin_id and payload.get("origin_id") != expected_origin_id:
        raise ProvenanceError("publisher origin ID mismatch")
    if expected_fingerprint and fingerprint.lower() != expected_fingerprint.lower():
        raise ProvenanceError("publisher key does not match the trusted external fingerprint")
    try:
        signature = base64.b64decode(signature_path.read_text(encoding="ascii").strip(), validate=True)
        public_key.verify(signature, canonical_json_bytes(payload))
    except (OSError, ValueError) as exc:
        raise ProvenanceError(f"cannot read release signature: {exc}") from exc
    except InvalidSignature as exc:
        raise ProvenanceError("release provenance signature verification failed") from exc
    return {
        "verified": True,
        "skill_name": payload.get("skill_name"),
        "release_version": payload.get("release_version"),
        "origin_id": payload.get("origin_id"),
        "publisher_public_key_sha256": fingerprint,
        "manifest_sha256": payload.get("manifest_sha256"),
    }


def command_verify_release(args: argparse.Namespace) -> int:
    result = verify_release(
        args.manifest,
        args.provenance,
        args.signature,
        args.public_key,
        args.expected_origin_id,
        args.expected_fingerprint,
    )
    print(json.dumps(result, indent=2))
    return 0


def challenge_payload(origin_id: str, challenge: str, public_key) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "signature_alg": SIGNATURE_ALG,
        "origin_id": origin_id,
        "challenge": challenge,
        "publisher_public_key_sha256": public_key_fingerprint(public_key),
    }


def command_sign_challenge(args: argparse.Namespace) -> int:
    private_key = load_private_key(args.private_key, args.passphrase_env)
    payload = challenge_payload(args.origin_id, args.challenge, private_key.public_key())
    payload["signature"] = base64.b64encode(private_key.sign(canonical_json_bytes(payload))).decode("ascii")
    write_json(args.output, payload)
    print(json.dumps({"signed": True, "output": str(args.output), "origin_id": args.origin_id}, indent=2))
    return 0


def command_verify_challenge(args: argparse.Namespace) -> int:
    InvalidSignature, _, _, _ = crypto_modules()
    payload = read_json(args.input)
    signature_text = payload.pop("signature", None)
    if not isinstance(signature_text, str):
        raise ProvenanceError("challenge signature is missing")
    public_key = load_public_key(args.public_key)
    if payload.get("publisher_public_key_sha256") != public_key_fingerprint(public_key):
        raise ProvenanceError("challenge public-key fingerprint mismatch")
    if args.expected_origin_id and payload.get("origin_id") != args.expected_origin_id:
        raise ProvenanceError("challenge origin ID mismatch")
    if args.expected_challenge and payload.get("challenge") != args.expected_challenge:
        raise ProvenanceError("challenge text mismatch")
    try:
        public_key.verify(base64.b64decode(signature_text, validate=True), canonical_json_bytes(payload))
    except (ValueError, InvalidSignature) as exc:
        raise ProvenanceError("challenge signature verification failed") from exc
    print(json.dumps({"verified": True, **payload}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate-key", help="Create a publisher Ed25519 key pair")
    generate.add_argument("--private-key", type=Path, required=True)
    generate.add_argument("--public-key", type=Path, required=True)
    generate.add_argument("--passphrase-env", default=DEFAULT_PASSPHRASE_ENV)
    generate.add_argument("--allow-unencrypted-private-key", action="store_true")
    generate.set_defaults(handler=command_generate_key)

    sign_release = subparsers.add_parser("sign-release", help="Sign one public release manifest")
    sign_release.add_argument("--manifest", type=Path, required=True)
    sign_release.add_argument("--private-key", type=Path, required=True)
    sign_release.add_argument("--public-key", type=Path, required=True)
    sign_release.add_argument("--provenance", type=Path, required=True)
    sign_release.add_argument("--signature", type=Path, required=True)
    sign_release.add_argument("--skill-name", required=True)
    sign_release.add_argument("--release-version", required=True)
    sign_release.add_argument("--origin-id", required=True)
    sign_release.add_argument("--repository")
    sign_release.add_argument("--passphrase-env", default=DEFAULT_PASSPHRASE_ENV)
    sign_release.set_defaults(handler=command_sign_release)

    verify = subparsers.add_parser("verify-release", help="Verify manifest, provenance, and publisher signature")
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--provenance", type=Path, required=True)
    verify.add_argument("--signature", type=Path, required=True)
    verify.add_argument("--public-key", type=Path, required=True)
    verify.add_argument("--expected-origin-id")
    verify.add_argument("--expected-fingerprint")
    verify.set_defaults(handler=command_verify_release)

    sign_challenge = subparsers.add_parser("sign-challenge", help="Prove current possession of the publisher key")
    sign_challenge.add_argument("--challenge", required=True)
    sign_challenge.add_argument("--origin-id", required=True)
    sign_challenge.add_argument("--private-key", type=Path, required=True)
    sign_challenge.add_argument("--output", type=Path, required=True)
    sign_challenge.add_argument("--passphrase-env", default=DEFAULT_PASSPHRASE_ENV)
    sign_challenge.set_defaults(handler=command_sign_challenge)

    verify_challenge = subparsers.add_parser("verify-challenge", help="Verify a publisher challenge response")
    verify_challenge.add_argument("--input", type=Path, required=True)
    verify_challenge.add_argument("--public-key", type=Path, required=True)
    verify_challenge.add_argument("--expected-origin-id")
    verify_challenge.add_argument("--expected-challenge")
    verify_challenge.set_defaults(handler=command_verify_challenge)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.handler(args))
    except ProvenanceError as exc:
        print(json.dumps({"verified": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

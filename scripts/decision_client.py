#!/usr/bin/env python3
"""Validate and submit sanitized requests to a protected decision engine."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
ALLOWED_OUTPUTS = {
    "stage_matrix",
    "verdict",
    "conditions",
    "gaps",
    "economics_summary",
    "validation_plan",
}
ALLOWED_STATUS = {"complete", "partial", "blocked"}
ALLOWED_VERDICTS = {"GO", "CONDITIONAL_GO", "NO_GO", "INSUFFICIENT_EVIDENCE"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", "unknown"}
SENSITIVE_KEY = re.compile(
    r"(?:password|passwd|secret|api[_-]?key|access[_-]?key|private[_-]?key|"
    r"authorization|bearer|cookie|session[_-]?id|refresh[_-]?token|access[_-]?token)$",
    re.IGNORECASE,
)
SENSITIVE_TEXT = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(?:x-amz-signature|x-amz-credential|access_token|refresh_token|api_key)=([^&\s]+)"),
    re.compile(r"(?i)authorization:\s*bearer\s+\S+"),
    re.compile(r"(?i)\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_RESPONSE_BYTES = 5 * 1024 * 1024


class ClientError(RuntimeError):
    """Expected client failure with a stable exit category."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent bearer tokens from following redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        raise urllib.error.HTTPError(req.full_url, code, "Redirect blocked", headers, fp)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def find_sensitive_content(value: Any, path: str = "root") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if SENSITIVE_KEY.search(str(key)):
                findings.append(f"{child}: sensitive key is not allowed")
            findings.extend(find_sensitive_content(item, child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(find_sensitive_content(item, f"{path}[{index}]"))
    elif isinstance(value, str):
        for pattern in SENSITIVE_TEXT:
            if pattern.search(value):
                findings.append(f"{path}: credential or private-key pattern detected")
                break
        if re.search(r"(?i)(?:[a-z]:\\users\\|/users/|/home/)[^\s]+", value):
            findings.append(f"{path}: local user path is not allowed")
    return findings


def validate_request(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root: expected a JSON object"]

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version: expected '1.0'")
    if not isinstance(data.get("request_id"), str) or not data["request_id"].strip():
        errors.append("request_id: required non-empty string")

    project = data.get("project")
    if not isinstance(project, dict):
        errors.append("project: required object")
        project = {}
    for key in ("decision_question", "marketplace", "currency", "as_of_date"):
        if not isinstance(project.get(key), str) or not project[key].strip():
            errors.append(f"project.{key}: required non-empty string")
    if project.get("currency") and not re.fullmatch(r"[A-Z]{3}", project["currency"]):
        errors.append("project.currency: expected three uppercase letters")
    if project.get("as_of_date") and not is_iso_date(project["as_of_date"]):
        errors.append("project.as_of_date: expected YYYY-MM-DD")

    scope = data.get("product_scope")
    if not isinstance(scope, dict):
        errors.append("product_scope: required object")
        scope = {}
    target = scope.get("target")
    if not isinstance(target, dict):
        errors.append("product_scope.target: required object")
        target = {}
    for key in ("product_id", "id_type", "label"):
        if not isinstance(target.get(key), str) or not target[key].strip():
            errors.append(f"product_scope.target.{key}: required non-empty string")
    competitors = scope.get("competitors", [])
    if not isinstance(competitors, list):
        errors.append("product_scope.competitors: expected an array when present")

    bundle = data.get("evidence_bundle")
    if not isinstance(bundle, dict):
        errors.append("evidence_bundle: required object")
        bundle = {}
    for key in ("evidence", "assumptions", "gaps"):
        if not isinstance(bundle.get(key), list):
            errors.append(f"evidence_bundle.{key}: required array")
    evidence_ids: set[str] = set()
    for index, item in enumerate(bundle.get("evidence", [])):
        if not isinstance(item, dict):
            errors.append(f"evidence_bundle.evidence[{index}]: expected object")
            continue
        evidence_id = item.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            errors.append(f"evidence_bundle.evidence[{index}].evidence_id: required")
        elif evidence_id in evidence_ids:
            errors.append(f"evidence_bundle.evidence[{index}].evidence_id: duplicate '{evidence_id}'")
        else:
            evidence_ids.add(evidence_id)

    constraints = data.get("business_constraints", {})
    if not isinstance(constraints, dict):
        errors.append("business_constraints: expected an object when present")

    requested = data.get("requested_outputs")
    if not isinstance(requested, list) or not requested:
        errors.append("requested_outputs: required non-empty array")
    else:
        invalid = sorted({item for item in requested if item not in ALLOWED_OUTPUTS})
        if invalid:
            errors.append(f"requested_outputs: unsupported values {invalid}")

    errors.extend(find_sensitive_content(data))
    return errors


def response_payload(data: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(data)
    for key in ("result_sha256", "signature_alg", "signature", "signature_verification"):
        payload.pop(key, None)
    return payload


def validate_response(data: Any, expected_request_sha256: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["response: expected a JSON object"]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("response.schema_version: expected '1.0'")
    for key in ("result_id", "engine_version", "request_sha256"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"response.{key}: required non-empty string")
    if data.get("status") not in ALLOWED_STATUS:
        errors.append("response.status: invalid value")
    if data.get("verdict") not in ALLOWED_VERDICTS:
        errors.append("response.verdict: invalid value")
    if data.get("confidence") not in ALLOWED_CONFIDENCE:
        errors.append("response.confidence: invalid value")
    for key in ("stage_matrix", "conditions", "gaps"):
        if not isinstance(data.get(key), list):
            errors.append(f"response.{key}: required array")
    request_hash = data.get("request_sha256")
    if isinstance(request_hash, str) and not HEX64.fullmatch(request_hash):
        errors.append("response.request_sha256: expected 64 lowercase hex characters")
    if expected_request_sha256 and request_hash != expected_request_sha256:
        errors.append("response.request_sha256: does not match submitted request")

    result_hash = data.get("result_sha256")
    if not isinstance(result_hash, str) or not HEX64.fullmatch(result_hash):
        errors.append("response.result_sha256: expected 64 lowercase hex characters")
    elif result_hash != sha256_hex(response_payload(data)):
        errors.append("response.result_sha256: content hash mismatch")
    return errors


def verify_signature(data: dict[str, Any], public_key_path: Path) -> None:
    if data.get("signature_alg") != "ed25519":
        raise ClientError("response.signature_alg must be 'ed25519'")
    signature_text = data.get("signature")
    if not isinstance(signature_text, str) or not signature_text:
        raise ClientError("response.signature is required")
    try:
        signature = base64.b64decode(signature_text, validate=True)
    except ValueError as exc:
        raise ClientError("response.signature is not valid base64") from exc

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature
    except ImportError as exc:
        raise ClientError("signature verification requires the Python 'cryptography' package") from exc

    try:
        public_key = serialization.load_pem_public_key(public_key_path.read_bytes())
    except (OSError, ValueError) as exc:
        raise ClientError(f"cannot load public key: {exc}") from exc
    if not isinstance(public_key, Ed25519PublicKey):
        raise ClientError("public key is not an Ed25519 key")
    try:
        public_key.verify(signature, canonical_json_bytes(response_payload(data)))
    except InvalidSignature as exc:
        raise ClientError("response signature verification failed") from exc


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ClientError(f"cannot read JSON '{path}': {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_endpoint(endpoint: str) -> None:
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ClientError("endpoint must be an absolute HTTPS URL")
    if parsed.username or parsed.password:
        raise ClientError("endpoint must not contain credentials")


def submit(endpoint: str, token: str, data: dict[str, Any], timeout: float) -> dict[str, Any]:
    validate_endpoint(endpoint)
    request_hash = sha256_hex(data)
    request = urllib.request.Request(
        endpoint,
        data=canonical_json_bytes(data),
        method="POST",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "amazon-product-decision-gateway/1.0",
            "X-Request-SHA256": request_hash,
        },
    )
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" not in content_type.lower():
                raise ClientError(f"service returned non-JSON content type '{content_type}'")
            payload = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise ClientError(f"service returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ClientError(f"network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise ClientError("network request timed out") from exc
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ClientError("service response exceeds 5 MiB limit")
    try:
        result = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClientError("service response is not valid UTF-8 JSON") from exc
    errors = validate_response(result, request_hash)
    if errors:
        raise ClientError("invalid service response: " + "; ".join(errors))
    return result


def command_validate(args: argparse.Namespace) -> int:
    data = read_json(args.input)
    errors = validate_request(data)
    result = {
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
        "request_sha256": sha256_hex(data) if isinstance(data, dict) else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.report:
        write_json(args.report, result)
    return 0 if not errors else 2


def command_inspect_response(args: argparse.Namespace) -> int:
    request_data = read_json(args.request)
    response_data = read_json(args.response)
    request_errors = validate_request(request_data)
    if request_errors:
        raise ClientError("request is invalid: " + "; ".join(request_errors))
    errors = validate_response(response_data, sha256_hex(request_data))
    result = {"valid": not errors, "errors": errors, "signature_verification": "not_run"}
    if not errors and args.public_key:
        verify_signature(response_data, args.public_key)
        result["signature_verification"] = "verified"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 5


def command_submit(args: argparse.Namespace) -> int:
    if not args.acknowledge_external_processing:
        raise ClientError("submission requires --acknowledge-external-processing after user confirmation")
    data = read_json(args.input)
    errors = validate_request(data)
    if errors:
        raise ClientError("request validation failed: " + "; ".join(errors))

    endpoint = args.endpoint or os.environ.get("AMAZON_DECISION_API_URL", "")
    token = os.environ.get(args.token_env, "")
    if not endpoint:
        raise ClientError("AMAZON_DECISION_API_URL or --endpoint is required")
    if not token:
        raise ClientError(f"environment variable {args.token_env} is required")

    result = submit(endpoint, token, data, args.timeout)
    key_value = args.public_key or os.environ.get("AMAZON_DECISION_PUBLIC_KEY")
    if key_value:
        verify_signature(result, Path(key_value))
        result["signature_verification"] = "verified"
    elif args.allow_unverified_response:
        result["signature_verification"] = "not_run_diagnostic_only"
    else:
        raise ClientError(
            "AMAZON_DECISION_PUBLIC_KEY or --public-key is required; "
            "use --allow-unverified-response only for diagnostics"
        )
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "valid": True,
                "output": str(args.output),
                "result_id": result.get("result_id"),
                "engine_version": result.get("engine_version"),
                "verdict": result.get("verdict"),
                "signature_verification": result.get("signature_verification"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate and hash a request without network access")
    validate_parser.add_argument("input", type=Path)
    validate_parser.add_argument("--report", type=Path)
    validate_parser.set_defaults(handler=command_validate)

    inspect_parser = subparsers.add_parser("inspect-response", help="Validate a saved response against its request")
    inspect_parser.add_argument("request", type=Path)
    inspect_parser.add_argument("response", type=Path)
    inspect_parser.add_argument("--public-key", type=Path)
    inspect_parser.set_defaults(handler=command_inspect_response)

    submit_parser = subparsers.add_parser("submit", help="Submit one authorized HTTPS request")
    submit_parser.add_argument("input", type=Path)
    submit_parser.add_argument("--output", type=Path, required=True)
    submit_parser.add_argument("--endpoint", help="HTTPS endpoint; defaults to AMAZON_DECISION_API_URL")
    submit_parser.add_argument("--token-env", default="AMAZON_DECISION_API_TOKEN")
    submit_parser.add_argument("--public-key", type=Path)
    submit_parser.add_argument("--timeout", type=float, default=60.0)
    submit_parser.add_argument("--acknowledge-external-processing", action="store_true")
    submit_parser.add_argument("--allow-unverified-response", action="store_true")
    submit_parser.set_defaults(handler=command_submit)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.handler(args))
    except ClientError as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

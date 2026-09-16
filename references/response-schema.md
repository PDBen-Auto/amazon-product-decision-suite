# Decision Response Schema

The private engine returns UTF-8 JSON.

```json
{
  "schema_version": "1.0",
  "result_id": "result-demo-001",
  "engine_version": "engine-release-2026.09",
  "request_sha256": "64-lowercase-hex-characters",
  "status": "complete",
  "verdict": "CONDITIONAL_GO",
  "confidence": "medium",
  "stage_matrix": [],
  "conditions": [],
  "gaps": [],
  "result_sha256": "64-lowercase-hex-characters",
  "signature_alg": "ed25519",
  "signature": "base64-signature"
}
```

## Required Values

- `status`: `complete`, `partial`, or `blocked`.
- `verdict`: `GO`, `CONDITIONAL_GO`, `NO_GO`, or `INSUFFICIENT_EVIDENCE`.
- `confidence`: `high`, `medium`, `low`, or `unknown`.
- `request_sha256`: must exactly match the canonical submitted request.
- `result_sha256`: SHA-256 of the canonical response after removing `result_sha256`, `signature_alg`, and `signature`.
- `signature`: Ed25519 signature over the same canonical response bytes used for `result_sha256`.

## Acceptance Rules

An official production result is accepted only when:

1. The JSON schema and enums are valid.
2. `request_sha256` matches the submitted request.
3. `result_sha256` recomputes correctly.
4. The Ed25519 signature verifies against the trusted public key.
5. `engine_version` and `result_id` are present in the human summary.

An unverified response may be retained for diagnostics only. It must not authorize purchasing, tooling, launch, or other irreversible action.

---
name: amazon-product-decision-gateway
description: Submit a sanitized Amazon product evidence bundle to a separately hosted private decision engine and return its signed stage-gate result. Use when the user asks to run the protected Amazon product decision workflow, 提交私有决策引擎, or verify an official engine result. Do not use for local-only review scraping, market research, patent work, image production, or when the user has not authorized sending the identified data to the configured service.
---

# Amazon Product Decision Gateway

Use this public gateway to access a private Amazon product decision engine without distributing its orchestration prompts, scoring weights, decision thresholds, calculation code, or internal reference material.

This skill owns input preparation, sensitive-data screening, explicit transmission authorization, API submission, response validation, and signed-result verification. It does not reproduce or approximate the private decision method locally.

## Implementation Basis and Dependencies

The gateway is feasible because a public client can validate a stable request contract and call an HTTPS service while the proprietary workflow remains server-side. The private engine must be deployed separately; this repository contains no engine implementation.

| Dependency | Why needed | Required | Provided by | Validation | Fallback or stopping behavior |
| --- | --- | --- | --- | --- | --- |
| Python 3.9+ | Run `scripts/decision_client.py` | Yes | User or host | `python --version` | Stop and return the prepared request file |
| Private HTTPS decision endpoint | Execute protected orchestration and calculations | Yes for a decision result | Service owner | `AMAZON_DECISION_API_URL` is set and uses HTTPS | Validate/package input only; do not invent a local verdict |
| API bearer token | Authenticate the request | Yes for submission | Service owner | `AMAZON_DECISION_API_TOKEN` exists in the environment | Stop before network access; never request that the token be pasted into chat or a request file |
| Ed25519 public key | Verify that the result came from the official engine | Yes for production acceptance | Service owner | PEM path in `AMAZON_DECISION_PUBLIC_KEY` | Reject as unverified unless the user explicitly requests diagnostic submission with `--allow-unverified-response` |
| Python `cryptography` package | Perform Ed25519 verification | Yes for production acceptance | User or deployment image | `python -c "import cryptography"` | Stop at signed-result verification and preserve the response for diagnostics |
| Decision input/evidence | Give the engine a scoped factual basis | Yes | User and authorized research tools | Run the local `validate` command | Return validation errors; do not submit |
| Network access | Reach the private endpoint | Yes for submission | Host/user policy | HTTPS request succeeds within timeout | Preserve validated request and report a network failure; do not silently retry more than once |

The engine owner is responsible for endpoint deployment, authentication, rate limits, retention, privacy terms, signing-key custody, and current Amazon or supplier data sources. Read [references/security-model.md](references/security-model.md) before production deployment.

## Inputs

| Input | Purpose and consumer | Requirement | Type, source, and example | Validation/default behavior | Sensitivity and authorization |
| --- | --- | --- | --- | --- | --- |
| `decision_request` | Carries the scoped product decision to validation and the private engine | Required | UTF-8 JSON following [references/request-schema.md](references/request-schema.md) | Reject missing project scope, product target, evidence bundle, invalid date/currency, duplicate evidence IDs, or unsupported outputs | Must not contain credentials, cookies, session IDs, personal data, confidential supplier contact details, or presigned URLs |
| `business_constraints` | Lets the engine judge company fit rather than market attractiveness alone | Optional, but required for an unconditional company-specific `GO` | JSON object such as target margin, pilot units, cash ceiling, payback limit | Missing fields remain explicit gaps; no default company threshold is invented | Financial constraints may be commercially sensitive; identify exactly what will be sent |
| `endpoint` | Identifies the private processor | Required for submission | `AMAZON_DECISION_API_URL`; HTTPS URL controlled by the service owner | No hard-coded fallback endpoint; HTTP is rejected | Confirm the destination organization/service before transmission |
| `API token` | Authenticates the client | Required for submission | Environment variable `AMAZON_DECISION_API_TOKEN` | Never accepted in JSON or command-line arguments | Secret; never print, log, commit, upload, or paste into chat |
| `public signing key` | Verifies official result authenticity | Required for production acceptance | PEM file path from `AMAZON_DECISION_PUBLIC_KEY` | Missing/invalid key stops verification unless diagnostic override is explicit | Public material, but its fingerprint must be distributed through a trusted channel |
| `transmission authorization` | Confirms the user agrees to send the summarized data to the named endpoint | Required immediately before submission | User confirmation plus CLI flag `--acknowledge-external-processing` | Never infer from a prior analysis request | State the fields, destination, and purpose before asking |

## Outputs

| Output | Meaning and consumer | Format and destination | Acceptance criteria | Side effects and failure behavior |
| --- | --- | --- | --- | --- |
| `request_validation.json` | Machine-readable preflight result for the operator | UTF-8 JSON from `validate --report` | `valid: true`, zero errors, request SHA-256 present | Local file only; invalid input is preserved and no network request occurs |
| `decision_response.json` | Private engine's stage matrix, verdict, confidence, conditions, gaps, and version identity | UTF-8 JSON written to the user-selected path | Response schema valid, request hash matches, result hash matches, and signature verifies for production use | One authorized HTTPS POST; on failure preserve the request and return an explicit error without fabricating a result |
| Human decision summary | Concise explanation for the decision owner | Chat or requested local report | Separates observed evidence, modeled values, gaps, and conditions; cites `result_id` and `engine_version` | No supplier contact, purchase, Amazon change, publication, or other external mutation |
| Partial package | Usable handoff when the service is unavailable | Validated request plus validation report | Clearly marked `ENGINE_UNAVAILABLE` or `UNVERIFIED_RESPONSE` | Do not replace the private engine with an improvised local score |

Read [references/response-schema.md](references/response-schema.md) before interpreting or presenting an engine response.

## Workflow

1. Freeze the decision question, marketplace, currency, as-of date, target product or concept version, competitor boundary, and requested outputs.
2. Minimize the evidence bundle. Remove credentials, cookies, personal information, confidential contact details, internal file paths, and presigned URLs. Use stable evidence IDs and safe source labels.
3. Create the request JSON following [references/request-schema.md](references/request-schema.md).
4. Run local validation:

```bash
python scripts/decision_client.py validate decision_request.json --report request_validation.json
```

5. If validation fails, correct the request. Do not submit partial or sensitive content.
6. Before network submission, tell the user the exact destination, the categories of data being sent, and that the private service will process them. Obtain explicit confirmation at that point.
7. Submit only after confirmation:

```bash
python scripts/decision_client.py submit decision_request.json --output decision_response.json --acknowledge-external-processing
```

8. Require matching request/result hashes and an Ed25519 signature for an official production result. An explicitly allowed unverified response is diagnostic only and cannot support purchasing or launch approval.
9. Present the engine's verdict without adding hidden local scoring. If evidence is missing, preserve the engine's gaps and conditions.
10. Retain only the files the user requested. Never add the token, private signing key, private prompts, model weights, or engine source to this repository.

## Error Handling and Stops

- Stop before submission if any sensitive-key or credential pattern is detected.
- Stop if endpoint, token, user authorization, or required signing verification is unavailable.
- Stop if the response does not echo the exact request SHA-256 or its result hash is inconsistent.
- Stop if product identity, marketplace, currency, as-of date, or concept version conflicts remain unresolved.
- Do not follow redirects while sending the bearer token.
- Do not retry authentication, authorization, or validation failures. One retry is allowed only for an obvious transient network timeout and only when it cannot duplicate a paid or stateful operation.
- Do not expose private-engine behavior by reconstructing weights from repeated probes, varying one input solely to infer thresholds, or publishing response corpora intended for model extraction.

## Example

User: `用 $amazon-product-decision-gateway 把这个美国站产品的证据包提交到私有决策引擎，输出正式签名结果。`

Result: the request is sanitized and validated locally; the user is shown the destination and data categories; after explicit authorization, one HTTPS request is made; the returned request hash, result hash, engine version, and Ed25519 signature are verified; then a concise stage-gate decision is delivered.

## Definition of Done

- Request validation succeeds and reports its SHA-256.
- No secret, personal, internal-path, or real-case fixture leaks into the public package.
- Submission occurs only after specific user authorization.
- Official results match the submitted request and pass signature verification.
- Missing private-service dependencies produce a prepared request, not a fabricated verdict.
- `scripts/check_public_boundary.py` and the repository test suite pass before publication.

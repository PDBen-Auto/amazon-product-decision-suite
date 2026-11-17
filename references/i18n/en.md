# Amazon product decision gateway

`amazon-product-decision-gateway` · English

## Purpose and scope

Submit a minimized evidence package to a separately hosted private decision engine and verify its signed result. This public client does not contain the engine.

## Implementation Basis and Dependencies

Python 3.9+, cryptography, a configured HTTPS endpoint, bearer token and trusted Ed25519 public key. Service access, retention and charges belong to the service owner; missing service access permits local preparation only.

## Inputs

Required: scoped decision_request JSON, product, marketplace, currency and evidence date. Conditional: business constraints for company-specific GO, endpoint and explicit permission for the identified transmission. Tokens stay in environment variables.

## Outputs

Local request_validation.json; after authorized submission, decision_response.json and a summary separating evidence, modeled values, gaps and conditions. Verify matching request/result hashes and signature.

## Workflow

1. Freeze scope and concept version.
2. Remove secrets, personal data and internal paths.
3. Validate the schema locally.
4. Describe destination and data categories
5. obtain specific transmission permission.
6. Submit once, then verify hashes, signature and engine version.
7. Preserve unavailable or diagnostic status.

## Boundaries and stopping conditions

Never reconstruct private weights or invent a local verdict. Stop on sensitive input, missing permission, invalid signature or mismatched hashes. No token-bearing redirects. A diagnostic override is not an official decision.

## Example request

Use `$amazon-product-decision-gateway` — Prepare the US phone-mount evidence request locally; submit only after destination-specific approval and return the verified result; respond in English and preserve evidence, unknowns and action boundaries.

## Complete specification

[Skill entrypoint and detailed references](../../SKILL.md).

Use the user's explicitly requested output language; otherwise follow the request language. Keep commands, skill IDs, JSON keys, enum values, units and source quotations unchanged. Separate translations from originals. Never infer country, currency or jurisdiction from language. Read the relevant detailed references in the complete specification and retain all existing validation and authorization gates.

Before delivery reconcile inputs, evidence, missing values, files and the original completion criteria. Mark unexecuted steps unverified; a successful script exit is not business validation.

## Language coverage and validation

This localized operating guide covers purpose, prerequisites, inputs, outputs, workflow, examples and boundaries; it is not a line-by-line translation of every reference. Detailed technical references, historical cases, script errors, example interfaces and images retain their original language. The assistant can explain them in the requested language. Structural, link and key-constraint checks are performed; native-speaker editorial review for each language is not claimed.


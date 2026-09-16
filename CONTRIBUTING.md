# Contributing

Thank you for helping improve the public Amazon Product Decision Gateway. This repository accepts narrowly scoped contributions to the public client, schemas, synthetic tests, documentation, release verification, and security hardening.

## Public Boundary

Do not submit or request any of the following:

- private-engine prompts, orchestration, model configuration, weights, thresholds, formulas, or internal reference material;
- attempts to infer protected decision logic through repeated probing or response-corpus collection;
- real product cases, ASIN research bundles, supplier records, customer data, Amazon account data, production requests, or production responses;
- API tokens, cookies, credentials, presigned URLs, signing private keys, local absolute paths, or confidential contact details;
- code or documentation that presents a modified build as an official release.

Use synthetic fixtures only. Run `python scripts/check_public_boundary.py .` before opening a pull request.

## Before Opening an Issue

1. Search existing issues.
2. Reproduce the problem with the included synthetic fixtures or a newly created synthetic example.
3. Remove secrets, personal data, supplier identities, internal paths, and business-sensitive values.
4. Use GitHub private vulnerability reporting for security issues; do not open a public issue for a suspected data leak, authentication flaw, or signing-key problem.

## Pull Requests

Keep each pull request focused. Explain the public behavior being changed, why the change is needed, and how it was tested. A pull request should pass:

```bash
python scripts/decision_client.py validate tests/fixtures/valid_request.json
python -m unittest discover -s tests -v
python scripts/check_public_boundary.py .
python scripts/build_release_manifest.py . --check
```

Changes to signed release files are maintained by the publisher. Do not manually edit `PUBLIC_MANIFEST.sha256`, `RELEASE_PROVENANCE.json`, or `RELEASE_PROVENANCE.sig` in a feature pull request.

## Licensing and Official Status

Submitting a contribution does not change the repository license or grant permission to publish a modified version as an official release. Only releases signed by the publisher key and published through the official repository should be treated as official.


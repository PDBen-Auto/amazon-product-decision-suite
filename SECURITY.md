# Security Policy

## Supported Surface

Security reports should cover the public gateway, request validation, accidental data disclosure, authentication handling, redirect behavior, response integrity, or repository-boundary failures.

The private engine is maintained and reported through its separate private channel. Do not publish private-engine findings, credentials, customer data, supplier data, tokens, signing keys, or production request/response bodies in a public issue.

## Reporting

Use GitHub private vulnerability reporting when enabled for the official repository. Otherwise contact the repository owner through a private channel listed in the repository profile. Include a minimal synthetic reproduction and remove all secrets or real business data.

## Operational Rules

- Rotate a token immediately if it appears in logs, commits, issues, or build output.
- Revoke and replace the signing key if the private key may have been exposed.
- Treat the publisher provenance key and the private engine result-signing key as separate keys with separate custody and rotation procedures.
- If the publisher key is exposed, publish a revocation notice through the same independently trusted channels that carried its fingerprint, then sign future releases with a new key.
- Treat unsigned or hash-mismatched results as invalid.
- Do not enable public Actions workflows that can read private-engine secrets on pull requests from forks.
- Do not upload real decision bundles as issue attachments or test fixtures.

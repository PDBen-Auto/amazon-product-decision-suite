# Changelog

All notable public Gateway changes are documented here. Private Engine changes are tracked separately and are intentionally excluded.

## [0.1.0] - 2026-09-16

### Added

- Installable `amazon-product-decision-gateway` Codex Skill.
- Request and response contracts for evidence-driven Amazon product decisions.
- Local sensitive-data screening, validation, canonical request hashing, and HTTPS submission.
- Ed25519 verification for official private-engine responses.
- Synthetic fixtures, unit tests, GitHub Actions validation, and public-boundary checks.
- Bilingual repository overview and public/private architecture documentation.
- Prompt-neutral origin record, signed release provenance, and publisher public-key fingerprint.

### Security

- Private decision methods, weights, thresholds, formulas, business cases, credentials, and private keys are excluded from the public package.
- External processing requires an HTTPS endpoint, a scoped token, and explicit user authorization at submission time.


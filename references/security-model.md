# Security and Publication Model

## What This Design Protects

- Core prompts, orchestration, scoring weights, thresholds, formulas, internal references, and model configuration remain in a private service or private repository.
- Public clients can submit a documented request but cannot inspect the engine implementation.
- Request/result hashes bind a response to the exact input.
- Ed25519 signatures distinguish official engine results from locally modified or fabricated output.
- Repository boundary checks reduce accidental publication of secrets, private source files, internal paths, and real case fixtures.
- Publisher provenance signatures bind an official release to a stable origin ID and a separately anchored publisher key.

## What It Cannot Prevent

- Anyone can modify a local clone of public files.
- A restrictive license creates a legal boundary; it does not make source technically immutable.
- Branch protection protects the official repository, not forks.
- Obfuscation, compiled Python, or bytecode raises effort but does not reliably protect a method distributed to an untrusted machine.
- A malicious client can skip its own checks. It still cannot produce a valid official server signature without the private signing key.
- A low-salience origin ID can be copied or removed and is supporting evidence only. It is not a substitute for signed provenance and an externally anchored public-key fingerprint.

## Recommended Split

Keep private:

- all five current engine Skill entrypoints and internal references;
- stage routing and handoff logic;
- evidence confidence and conflict-resolution heuristics;
- differentiation scoring weights and elimination rules;
- supply-chain weights, blocker logic, and supplier evaluation playbooks;
- economics calculators, proprietary assumptions, and scenario policies;
- prompts, model configuration, datasets, real cases, supplier records, credentials, and signing keys.

Publish:

- the gateway `SKILL.md`;
- request and response transport schemas;
- the sanitized client and boundary checker;
- the public publisher key, signed release provenance, and non-executable origin ID;
- synthetic fixtures, tests, CI, security policy, and restrictive license notice.

## Required Private-Service Controls

- HTTPS only; no token-bearing redirects.
- Short-lived scoped tokens, server-side rate limiting, request-size limits, and audit logs.
- Data minimization and documented retention/deletion policy.
- Private signing key stored in a managed secret or key service, never in GitHub source or Actions variables exposed to pull requests.
- Version every engine release and preserve the engine version with each result.
- Do not expose threshold-probing endpoints or unlimited evaluation access that enables method extraction.

## Official GitHub Repository Controls

Use repository rulesets to require pull requests, approvals, status checks, signed commits where practical, and to block force pushes and branch deletion. Enable secret scanning where the repository/account plan supports it. Publish releases from protected tags and include the generated public-boundary scan and test result.

Use a dedicated offline publisher key for release provenance. Do not reuse the private engine result-signing key. Publish the publisher public-key fingerprint on an independent identity channel, because a public key included only in the repository can be replaced by someone distributing a modified clone.

Authoritative references:

- [GitHub repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
- [Secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

The included license notice is a conservative publication default, not legal advice. Have counsel review commercial distribution, reverse-engineering, warranty, privacy, export, and governing-law terms before a public launch.

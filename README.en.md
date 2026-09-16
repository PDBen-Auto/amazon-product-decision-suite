# Amazon Product Decision Suite

English | [中文](README.md)

An evidence-driven product decision system for Amazon physical-product opportunities. It is designed for product managers who need to turn fragmented market, customer, product, supply-chain, and financial evidence into an actionable, auditable, and veto-capable launch decision.

This public repository provides an installable Codex Gateway Skill that validates and submits structured evidence to a separately hosted private decision engine.

> This repository is the public Gateway, not the proprietary Engine. Local validation, sensitive-data screening, hashing, and signature verification work without the service. Official product decisions require the private endpoint.

## The Product-Management Problem

Product teams rarely lack reports. They lack a defensible decision chain. Market research may show demand, reviews may reveal pain, patent work may flag risk, suppliers may claim feasibility, and a spreadsheet may show margin, but those conclusions often use different dates, definitions, and assumptions.

The suite connects evidence quality, customer problems, testable differentiation, supply-chain feasibility, unit economics, cash constraints, and explicit launch conditions. Its intended result is not another opportunity summary, but `GO / CONDITIONAL_GO / NO_GO / INSUFFICIENT_EVIDENCE`, a stage matrix, blockers, conditions, evidence gaps, and a next-validation plan.

## How It Differs From Single-Purpose Skills

| Skill category | What it does well | Where it normally stops |
| --- | --- | --- |
| Market BI and product research | Demand, trends, price bands, competitors, and keyword opportunity | Market attractiveness, not buildability, profitability, or company fit |
| Review collection and VOC | Customer language, pain themes, use cases, and complaints | Insight, not specifications, BOM impact, prototype tests, or kill criteria |
| Patent and design-around research | Preliminary rights risk and design boundaries | Risk guidance, not supply-chain or investment approval |
| Supplier and cost tools | Quotes, MOQ, tooling, lead time, and direct cost | Supplier claims may remain unverified and disconnected from demand or return risk |
| Margin calculators | Contribution margin, break-even ACoS, and scenarios | Clear math, but not necessarily evidence-backed inputs or hard compliance blockers |
| Generic product frameworks | Positioning, SWOT, strategy, and opportunity framing | Useful discussion, but usually no machine-validated evidence contract or stage gates |
| Amazon image workflows | Concepts, listing images, A+, and creative QA | A downstream production activity that should follow product approval |

The suite does not claim to replace specialist tools for narrow tasks. Its advantage appears when a product manager must make one cross-functional investment decision from all of them.

## Product Advantages

1. **Decision output, not report output:** moves from research findings to explicit stage-gate outcomes.
2. **One evidence language:** separates observed facts, calculations, models, inferences, and assumptions.
3. **Testable differentiation:** converts VOC into mechanisms, specifications, process/BOM impact, experiments, pass thresholds, and kill criteria.
4. **Hard blockers outrank average scores:** safety, mandatory compliance, rights, and critical-process failures cannot be hidden by market demand.
5. **Company fit, not market appeal alone:** includes contribution targets, ads, returns, MOQ, first-order cash, and payback constraints.
6. **Auditable handoffs:** links decisions back to evidence IDs, source dates, calculations, and unresolved gaps across product, sourcing, and finance.
7. **Protected method with verifiable results:** keeps proprietary thresholds and orchestration server-side while the Gateway binds request hashes and verifies signed responses.

This is most useful for formal product approval, concept comparison, prototype or sourcing gates, and management review. For a single review scrape, patent lookup, or image-generation task, the relevant specialist Skill remains the more direct choice.

## Public Architecture

```text
Evidence + business constraints
              |
              v
Public Gateway Skill
  - minimize and validate data
  - require transmission authorization
  - bind request SHA-256
              |
              | HTTPS + scoped token
              v
Private Decision Engine
  - proprietary orchestration and methods
  - versioned stage-gate result
  - server-side Ed25519 signature
              |
              v
Gateway verifies request hash, result hash, and signature
```

See [Suite Overview](docs/SUITE_OVERVIEW.en.md), [Architecture](docs/ARCHITECTURE.md), and [Private Engine Deployment](docs/PRIVATE_ENGINE_DEPLOYMENT.md).

## Included

- `amazon-product-decision-gateway` Codex Skill
- Request and response JSON contracts
- Sensitive-data checks, canonical hashing, and HTTPS submission
- Ed25519 verification of official engine responses
- Synthetic fixtures, unit tests, GitHub Actions, and boundary scanning
- Prompt-neutral release provenance and signed manifests

## Kept Private

- Engine prompts, orchestration, weights, thresholds, and model configuration
- Evidence conflict-resolution heuristics
- Differentiation, supplier-evaluation, and scenario policies
- Proprietary economics assumptions and internal calculators
- Real cases, supplier records, production data, credentials, and private keys

## Install

```bash
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git ~/.codex/skills/amazon-product-decision-gateway
cd ~/.codex/skills/amazon-product-decision-gateway
python -m pip install -r requirements.txt
```

An official signed package can also be downloaded from [GitHub Releases](https://github.com/PDBen-Auto/amazon-product-decision-suite/releases) and extracted into the same location.

## Validate Locally

```bash
python scripts/decision_client.py validate tests/fixtures/valid_request.json
python -m unittest discover -s tests -v
python scripts/check_public_boundary.py .
python scripts/build_release_manifest.py . --check
```

All included fixtures are synthetic. Never post customer, supplier, Amazon-account, credential, or production request data in public issues.

## Configure the Private Service

Set `AMAZON_DECISION_API_URL`, `AMAZON_DECISION_API_TOKEN`, and `AMAZON_DECISION_PUBLIC_KEY` outside the repository. The Gateway accepts HTTPS only, blocks token-bearing redirects, and requires explicit authorization immediately before external processing.

## Publisher Provenance

Publisher public-key SHA-256:

```text
d64d7ebc963fdaa86a44573bd226e8bb135d9d95818c5f39df88e0a45e886596
```

The origin record is outside prompt-bearing Skill files and does not change model behavior or transmit telemetry. The signed manifest, repository history, and independently trusted fingerprint provide the meaningful evidence.

## License

This public repository is source-available, not OSI open source. The current notice permits inspection and use of unmodified official releases but does not grant modification, derivative-work, redistribution, or official-representation rights. Review [LICENSE](LICENSE) and obtain legal advice before commercial distribution.

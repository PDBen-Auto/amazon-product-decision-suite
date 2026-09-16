# Amazon Product Decision Suite Overview

The public Gateway connects five private modules through stable contracts. These descriptions explain responsibility and handoffs without publishing prompts, weights, thresholds, or formulas.

| Private module | Responsibility | Main inputs | Main outputs |
| --- | --- | --- | --- |
| Decision Pipeline | Orchestrate market, customer, rights, supply-chain, differentiation, finance, and decision gates | Decision question, evidence bundle, business constraints | Stage matrix, verdict, conditions, blockers, validation plan |
| Evidence Contract | Normalize heterogeneous research into traceable evidence | Market reports, reviews, quotes, policy sources | Typed observed, calculated, modeled, inferred, and assumed records |
| Differentiation | Convert customer problems into testable product definitions | VOC, competitor facts, constraints | Mechanisms, specifications, BOM impact, experiments, elimination criteria |
| Supply Chain Feasibility | Test supplier, MOQ, tooling, process, quality, compliance, and lead-time feasibility | Product definition, quotes, process and compliance evidence | PASS, CONDITIONAL, or BLOCK with required evidence |
| Unit Economics & Cashflow | Test complete contribution economics and first-order cash constraints | Price, fees, sourcing, logistics, ads, returns, payment terms | Contribution margin, break-even ACoS, scenarios, cash constraints |

The suite does not replace market BI, review collection, VOC analysis, patent screening, or Amazon image production. Those capabilities collect and interpret evidence; the decision suite owns normalization, handoffs, gates, and the final conditional decision.

Gate principles:

- Market attractiveness cannot override safety, mandatory-compliance, or rights blockers.
- A high numeric score cannot override an infeasible critical process.
- Assumptions and modeled values remain distinct from observed facts.
- Missing company-specific profit and cash thresholds prevent an unconditional `GO`.
- When the private Engine is unavailable, the Gateway does not imitate proprietary scoring locally.

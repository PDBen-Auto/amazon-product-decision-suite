# Decision Request Schema

Use UTF-8 JSON. The public gateway intentionally validates only the transport contract; private decision methods remain server-side.

## Shape

```json
{
  "schema_version": "1.0",
  "request_id": "demo-organizer-001",
  "project": {
    "decision_question": "Should this concept advance to a 500-unit pilot?",
    "marketplace": "amazon.com",
    "currency": "USD",
    "as_of_date": "2026-09-15"
  },
  "product_scope": {
    "target": {
      "product_id": "DEMO-ORGANIZER-001",
      "id_type": "concept",
      "label": "Synthetic organizer concept",
      "variant": "v1"
    },
    "competitors": []
  },
  "evidence_bundle": {
    "schema_version": "1.0",
    "evidence": [],
    "assumptions": [],
    "gaps": []
  },
  "business_constraints": {
    "initial_inventory_units": 500,
    "target_contribution_margin_rate": 0.18
  },
  "requested_outputs": [
    "stage_matrix",
    "verdict",
    "conditions",
    "gaps"
  ]
}
```

## Required Fields

- `schema_version`: exactly `1.0`.
- `request_id`: caller-generated stable identifier; do not use an email address or customer name.
- `project.decision_question`: one bounded decision.
- `project.marketplace`: Amazon marketplace domain or country-specific identifier.
- `project.currency`: three-letter uppercase currency code.
- `project.as_of_date`: `YYYY-MM-DD`.
- `product_scope.target`: object containing `product_id`, `id_type`, and `label`.
- `evidence_bundle`: object containing arrays `evidence`, `assumptions`, and `gaps`.
- `requested_outputs`: non-empty subset of `stage_matrix`, `verdict`, `conditions`, `gaps`, `economics_summary`, and `validation_plan`.

## Evidence Transport Rules

- Each evidence item needs a unique `evidence_id`.
- Include the fact, unit, claim type, confidence, date, and a safe source locator or label when available.
- Remove local absolute paths and replace them with neutral source labels or uploaded artifact IDs issued by the private service.
- Do not include cookies, authorization headers, API keys, login URLs, presigned URLs, customer identities, or supplier personal contact information.
- User-provided confidential commercial numbers may be included only after the user is told they will be transmitted to the configured private service.

## Invalid or Partial Input

Invalid required fields stop submission. Missing business constraints remain explicit gaps and normally prevent an unconditional company-specific `GO`. Missing optional outputs are not inferred beyond the documented default set.

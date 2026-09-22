# Compatibility

| Surface | Supported | Notes |
| --- | --- | --- |
| Codex / Agent Skills | Yes | Install with `npx skills add` or copy the Skill directory. |
| Python | 3.10+ | CI validates with Python 3.12. |
| Inputs | Sanitized JSON evidence bundles | Validate against `references/request-schema.md`. |
| Outputs | Local validation, request hash, bounded handoff, verified signed response | A formal decision requires the separately hosted private engine. |
| Network | Optional for local validation; HTTPS required for external submission | Explicit user authorization is required before submission. |
| Windows / Linux | Supported | Keep signing keys and private engine credentials outside the repository. |

When the endpoint, token, contract version, or evidence is unavailable, return a bounded validation or handoff result and do not imitate the private engine.

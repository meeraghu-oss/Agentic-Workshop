---
title: 'Story 1.1: Triage decision schema'
type: 'feature'
created: '2026-09-26'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Epic 1 needs a strict, reusable JSON contract so later agent and evaluation code can trust every triage decision's shape and values.

**Approach:** Add an immutable Pydantic decision model with the supported category, priority, and route values, a one-sentence rationale rule, and a validation helper that accepts dictionaries or JSON while returning clear errors for invalid input.

</frozen-after-approval>

## Implementation Notes

- Added `triage.schema` with the stable `Category`, `Priority`, `Route`, `TriageDecision`, `TriageValidationError`, and `validate_decision` public API required by later epics.
- Kept category and route as independent strict enums; policy pairing remains outside this story. The model forbids extra fields, is immutable, trims rationale whitespace, and rejects empty or multi-sentence rationales.
- Added schema coverage in `tests/test_schema.py` plus `tests/conftest.py` to make the repository package importable through the required `uv run pytest` entry point.
- Verification: `uv run pytest` passed all 16 tests. The first run exposed the missing test import bootstrap; adding the checkpoint-compatible `tests/conftest.py` resolved collection.
- Review patch: parameterized positive coverage now proves every supported category, priority, and route value is accepted; final verification passed all 30 tests.

## Review Triage Log

- `false` — category/route pairing is intentionally policy logic, not part of CAP-1's independent enum schema; the canonical spec and downstream `ToolStrategy(TriageDecision)` contract require the existing model semantics.
- `false` — `Money is at stake.Apply P2.` is malformed prose rather than two grammatically separated sentences, so accepting it does not disprove the documented single-sentence check.
- `low` (rejected) — abbreviation-shaped prose such as `Inc. was` can trigger the lightweight sentence-break heuristic, but this is rare in policy rationales and robust natural-language sentence segmentation would add disproportionate complexity.
- `false` — semantic proof that a rationale names the applied policy rule belongs to the agent/policy layer; CAP-1 requires a nonempty one-sentence rationale, which the schema enforces.
- `low` (rejected) — Python's JSON parser resolves duplicate object keys to the final value; duplicate-key detection is outside the contract, uncommon for generated decisions, and would complicate parsing for negligible benefit.
- `low` (patched) — positive tests covered only one enum member; parameterized coverage now exercises all supported category, priority, and route values. The suggested pairing assertion was rejected because pairing is intentionally out of scope.
- `low` (deferred) — the pre-existing untracked `.DS_Store` can be accidentally added, but repository ignore hygiene predates this story; recorded in `_bmad-output/implementation-artifacts/deferred-work.md`.

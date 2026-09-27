---
id: SPEC-epic-3
companions:
  - ../../../cases/expense/POLICY.md
  - ../spec-epic-2/SPEC.md
---

# Epic 3: Reviewer Release Readiness

## Why

Epic 2 produces policy-grounded line decisions. Epic 3 makes the result usable by a finance reviewer by showing the approved-only reimbursable total and separating approved items over $500 that still require human release.

## Capabilities

- **CAP-1:** A claim review returns every line item with its decision, clause, explanation, amount, and release status.
- **CAP-2:** Reimbursable total equals the sum of approved items only; rejected and flagged items are excluded and remain visible.
- **CAP-3:** An approved item over $500 remains approved but has `requires_human_release: true`; no payout is released by the agent.

## Constraints

- Preserve Epic 2 decisions and clause citations.
- Human release applies only to approved items over $500.
- No payout API or automatic release.

## Non-goals

- Changing policy decisions.
- Recalculating or hiding rejected or flagged line items.

## Success signal

The labelled Case A examples produce a reviewer-ready decision table, an approved-only total, and explicit human-release status.

---
id: SPEC-epic-2
companions:
  - ../../../cases/expense/POLICY.md
  - ../spec-epic-1/tool-contracts.md
sources:
  - ../../planning-artifacts/prds/prd-agents-workshop-2026-09-27/prd.md
  - ../../planning-artifacts/epics.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Epic 2: Policy-Grounded Line Item Decisions

## Why

Epic 1 made Case A claim context and decision storage available. Epic 2 turns that context into finance-review work: every line item receives one auditable policy decision with the exact deciding clause and a short explanation.

## Capabilities

- **CAP-1**
  - **intent:** The workflow can decide every line item as `approve`, `flag`, or `reject` using the precedence rules in `POLICY.md`.
  - **success:** Labelled examples covering non-reimbursable items, duplicates, stale expenses, IT approval, limits, and receipt follow-up match their expected decisions.

- **CAP-2**
  - **intent:** The workflow cites the exact policy clause that determined each line item decision.
  - **success:** Labelled examples in `cases/expense/eval/labelled.csv` match their expected clause values.

- **CAP-3**
  - **intent:** The workflow records each decision with a short line-item-grounded explanation for reviewer inspection.
  - **success:** Running a claim review writes every line item decision through `record_decision` and returns rows with `line_id`, `decision`, `clause`, and `explanation`.

## Constraints

- `POLICY.md` is read-only and is the single source of policy truth.
- Policy precedence is section 3, then 5.1, then 1.2, then 4.1, then sections 2 and 6 limits, then 1.3.
- Epic 2 must not calculate final reimbursable totals or implement human-release behavior; those belong to Epic 3.
- Existing Epic 1 tool contracts remain the integration surface.

## Non-goals

- No payout behavior.
- No human-release gate for approved items over `$500`.
- No UI beyond returned data structures and testable outputs.

## Success signal

Against the labelled examples, line item decisions and cited clauses match expected values, and a claim review records explainable decisions without calculating payout totals or releasing money.

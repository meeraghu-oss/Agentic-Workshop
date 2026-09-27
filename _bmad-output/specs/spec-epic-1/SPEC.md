---
id: SPEC-epic-1
companions:
  - tool-contracts.md
  - data-fixtures.md
sources:
  - ../../planning-artifacts/prds/prd-agents-workshop-2026-09-27/prd.md
  - ../../planning-artifacts/epics.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Epic 1: Claim Review Context and Tooling

## Why

The expense reviewer agent cannot make auditable policy decisions until it can load the full claim context: the claim, line items, employee level and city, and applicable limits. This epic gives workshop builders the runnable context and tool surface that later decision, citation, and reviewer-table work depends on.

## Capabilities

- **CAP-2**
  - **intent:** A workshop builder can make Case A seed data and labelled examples available before implementing context tools.
  - **success:** The seed CSVs and `cases/expense/eval/labelled.csv` are present at the expected paths and loadable for tests.

- **CAP-1**
  - **intent:** A finance reviewer or workflow can provide a `claim_id` and retrieve the complete claim context needed before line item decisions are made.
  - **success:** Given a valid `claim_id`, the workflow has the claim, line items, employee level and city, and category limits available for downstream policy review.

## Constraints

- Tool contracts are load-bearing and must match `tool-contracts.md`.
- Data fixtures are load-bearing and must match `data-fixtures.md`.
- Epic 1 prepares context and recording capability only; it must not perform policy decisions, clause citation, reimbursement totals, or payout release.
- `POLICY.md` remains the read-only source of policy truth for later epics.

## Non-goals

- No line item `approve`, `flag`, or `reject` decisions.
- No policy precedence evaluation.
- No reimbursable total calculation.
- No human-release or payout behavior.

## Success signal

The Case A seed data and labelled examples are loadable, and given a valid `claim_id`, the agent workflow can load every input required by later policy review and expose the required tool contracts without making any line item decision.

---
title: "Case A Expense Claim Reviewer MVP"
status: "final"
created: "2026-09-27"
updated: "2026-09-27"
---

# PRD: Case A Expense Claim Reviewer MVP

## 0. Purpose
This PRD is for workshop builders implementing the Case A demo from the product brief. It defines one MVP agent that reviews expense claim line items against `cases/expense/POLICY.md`, uses the seeded case data, records decisions, and demonstrates a policy-grounded agentic workflow. Source brief: `_bmad-output/planning-artifacts/briefs/brief-agents-workshop-2026-09-27/brief.md`.

## 1. Vision
Finance reviewers should move from manual cross-checking across claim data, employee data, limits, receipts, duplicates, and policy clauses to a decision table they can audit. The MVP agent simplifies expense review by deciding each line item, explaining the reason, and citing the exact policy clause behind the decision. Approved items over `$500` remain approved but require human release before payout.

## 2. Target User and Journey
Primary user: a finance reviewer processing claims during a workshop demo.

**UJ-1. Finance reviewer audits one claim.** Given a `claim_id`, the reviewer runs the expense reviewer agent. The agent reviews every line item, records decisions, and returns a table with `line_id`, description, amount, decision, clause, explanation, reimbursable amount, and `human_release_required`. The reviewer can scan rejected, flagged, and awaiting-release items first, then confirm the reimbursable total.

## 3. Glossary
- **Claim** — One employee expense submission.
- **Line item** — One expense inside a claim; each receives exactly one decision and one clause.
- **Decision** — `approve`, `flag`, or `reject`.
- **Clause** — The `POLICY.md` section that determines the line item decision.
- **Human release** — Required payout approval for approved items over `$500`; it does not change the item decision.

## 4. MVP Requirements
### Feature: One Expense Reviewer Agent
**Description:** One agent reviews claims using `get_claim`, `get_employee`, `get_policy_limits`, and `record_decision`. It applies `POLICY.md` precedence: section 3 non-reimbursable items, then 5.1 duplicates, 1.2 stale expenses, 4.1 IT approval, limits under sections 2 and 6, then 1.3 receipt follow-up. If no rule rejects or flags an item, it approves under the category clause.

#### FR-1: Load claim context
The agent can retrieve a claim, its line items, the employee's level and city, and applicable limits before deciding any line item.

Required tool contracts:
- `get_claim(claim_id)` returns the employee ID and line items.
- `get_employee(employee_id)` returns employee level and city.
- `get_policy_limits(level, city)` returns limits by category.
- `record_decision(line_id, decision, clause)` writes one line item decision.

#### FR-2: Decide every line item
The agent assigns exactly one `approve`, `flag`, or `reject` decision to every line item, including mixed claims where different line items receive different decisions.

The MVP must cover the policy precedence categories in `POLICY.md`: section 3 non-reimbursable items, 5.1 duplicates, 1.2 stale expenses, 4.1 IT pre-approval, sections 2 and 6 limits, and 1.3 receipt follow-up.

#### FR-3: Cite the deciding clause
The agent records the exact clause that determined each line item decision. Clause accuracy is the primary trust anchor.

#### FR-4: Explain and record review output
The agent provides a short explanation for each decision grounded in the line item and cited clause. It writes each line item decision and clause through `record_decision(line_id, decision, clause)` so the reviewer can inspect a decision table.

#### FR-5: Preserve human control for high-value approvals
For approved items over `$500`, the output clearly shows that the item remains approved but awaits human release before payout.

#### FR-6: Calculate reimbursable total
The workflow shows a reimbursable total equal to the sum of approved items only, while rejected items and approved items awaiting human release remain visible as separate line-level outcomes.

## 5. Non-Goals
- No multi-agent workflow.
- No payments, agent-released payouts, or email sending.
- No policy editing or policy authoring.
- No polished production UI beyond a demo-visible decision table.
- No replacement of final finance accountability.

## 6. Success Metrics
- **SM-1:** Against the labelled examples in `cases/expense/eval/labelled.csv`, every evaluated line item matches the expected decision. Validates FR-2.
- **SM-2:** Against the labelled examples in `cases/expense/eval/labelled.csv`, every evaluated line item cites the expected policy clause. Validates FR-3.
- **SM-3:** For each evaluated claim represented in the labelled examples, reimbursable total matches the expected sum of approved items only. Validates FR-6.
- **SM-4:** Demo reviewer can see decisions, clauses, and human-release status in one table. Validates FR-4 and FR-5.
- **Guardrail:** No payout is released by the agent; approved items over `$500` must require human release.

## 7. Assumptions
- Seed CSVs in `cases/expense/seed/` are available and loaded into the workshop data store.
- `POLICY.md` is read-only and is the single source of policy truth.
- `cases/expense/eval/labelled.csv` defines MVP acceptance for the first 30 claims; the final 10 claims are holdout demo-scoring cases, not the MVP acceptance source.
- The MVP uses one expense reviewer agent.

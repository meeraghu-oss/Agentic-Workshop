# Case A Workshop Handoff

This file is a continuation brief for a new Codex account/session.

## Repository

- Workspace: `/Users/craghave@cisco.com/Desktop/agents-workshop/day2`
- Remote: `origin`
- Current branch: `main`
- Latest pushed commit: `0329a70`
- The unrelated `.DS_Store` files are untracked and should be ignored.

## Product

Case A is a workshop demo for a policy-grounded expense-review workflow. The primary user is a finance reviewer; employees and managers are secondary users. The workflow makes complex policy review simple, cites the exact policy clause for every line item, and keeps mixed outcomes visible.

Important rules:

- Every line item gets exactly one decision: `approve`, `flag`, or `reject`.
- Policy precedence is sections 3, 5.1, 1.2, 4.1, limits in sections 2/6, then 1.3.
- Duplicate detection is policy clause 5.1: same employee, date, merchant, and amount; reject the later item.
- Reimbursable total is the sum of approved items only.
- Approved items over `$500` remain approved but require human release before payout.
- The agent never releases payout automatically.

## Completed epics

### Epic 1: Case A Data and Decision Storage

- Story 1.1: Add Case A data and labelled examples
- Story 1.2: Implement claim context lookup tools
- Story 1.3: Implement decision recording contract

### Epic 2: Policy-Grounded Line Item Decisions

- Story 2.1: Implement policy precedence decisions
- Story 2.2: Validate decisions and clauses against labelled examples
- Story 2.3: Record explainable claim review decisions

### Epic 3: Reviewer Release Readiness

- Story 3.1: Build the reviewer decision table and total
- Story 3.2: Add human release status for high-value approvals

## Key files

- `cases/expense/POLICY.md`: read-only policy source
- `cases/expense/seed/*.csv`: claims, line items, employees, and limits
- `cases/expense/eval/labelled.csv`: labelled acceptance examples
- `expense/tools.py`: context lookup and decision persistence
- `expense/policy.py`: policy precedence and duplicate detection
- `expense/review.py`: explainable claim review, approved-only totals, release status
- `mcp/expense_server.py`: MCP tool registrations
- `_bmad-output/specs/spec-epic-{1,2,3}/`: canonical specs and story lists

## Verification

From the repository root:

```bash
/Users/craghave@cisco.com/.local/bin/uv run pytest -q
```

Current result: `46 passed`.

## Resume instruction

Start by running `git status --short --branch`, reading this file and the Epic 3 spec, then run the test suite. Continue implementation from `main`; do not recreate completed stories or reset existing changes.

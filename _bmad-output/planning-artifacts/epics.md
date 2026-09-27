---
stepsCompleted:
  - step-01-validate-prerequisites
inputDocuments:
  - /Users/craghave@cisco.com/Desktop/agents-workshop/_bmad-output/planning-artifacts/prds/prd-agents-workshop-2026-09-27/prd.md
---

# agents-workshop - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for agents-workshop, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: The agent can retrieve a claim, its line items, the employee's level and city, and applicable limits before deciding any line item.

FR2: The agent assigns exactly one `approve`, `flag`, or `reject` decision to every line item, including mixed claims where different line items receive different decisions. The MVP must cover the policy precedence categories in `POLICY.md`: section 3 non-reimbursable items, 5.1 duplicates, 1.2 stale expenses, 4.1 IT pre-approval, sections 2 and 6 limits, and 1.3 receipt follow-up.

FR3: The agent records the exact clause that determined each line item decision; clause accuracy is the primary trust anchor.

FR4: The agent provides a short explanation for each decision grounded in the line item and cited clause, and writes each line item decision and clause through `record_decision(line_id, decision, clause)` so the reviewer can inspect a decision table.

FR5: For approved items over `$500`, the output clearly shows that the item remains approved but awaits human release before payout.

FR6: The workflow shows a reimbursable total equal to the sum of approved items only, while rejected items and approved items awaiting human release remain visible as separate line-level outcomes.

### NonFunctional Requirements

NFR1: The workflow must preserve finance accountability by ensuring no payout is released by the agent.

NFR2: The demo-visible decision table must make decisions, clauses, explanations, reimbursable amounts, and human-release status easy for a finance reviewer to inspect.

NFR3: The implementation must use `POLICY.md` as a read-only single source of policy truth.

NFR4: MVP acceptance must be measured against the labelled examples in `cases/expense/eval/labelled.csv` for the first 30 claims.

### Additional Requirements

- No architecture document was found in planning artifacts, so no architecture-specific requirements were extracted.
- Required tool contracts from the PRD:
  - `get_claim(claim_id)` returns the employee ID and line items.
  - `get_employee(employee_id)` returns employee level and city.
  - `get_policy_limits(level, city)` returns limits by category.
  - `record_decision(line_id, decision, clause)` writes one line item decision.

### UX Design Requirements

- No UX design handoff was found in planning artifacts, so no UX design requirements were extracted.

### FR Coverage Map

{{requirements_coverage_map}}

## Epic List

{{epics_list}}

<!-- Repeat for each epic in epics_list (N = 1, 2, 3...) -->

## Epic {{N}}: {{epic_title_N}}

{{epic_goal_N}}

<!-- Repeat for each story (M = 1, 2, 3...) within epic N -->

### Story {{N}}.{{M}}: {{story_title_N_M}}

As a {{user_type}},
I want {{capability}},
So that {{value_benefit}}.

**Acceptance Criteria:**

<!-- for each AC on this story -->

**Given** {{precondition}}
**When** {{action}}
**Then** {{expected_outcome}}
**And** {{additional_criteria}}

<!-- End story repeat -->

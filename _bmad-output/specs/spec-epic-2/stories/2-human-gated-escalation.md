---
title: 'Human-gated escalation'
type: 'feature'
created: '2026-09-26'
status: 'draft'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/specs/spec-epic-2/SPEC.md'
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/TRIAGE_POLICY.md'
  - '{project-root}/.agents/skills/langchain-middleware/SKILL.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The triage agent must not escalate a high-priority Enterprise ticket without a person's explicit approval.

**Approach:** Add a local `escalate_to_human` tool protected by LangChain's human-in-the-loop middleware. When the policy's final outcome is P1 for an Enterprise customer, pause at the terminal for a yes/no decision; approval executes escalation, while rejection completes without escalation. Keep the Epic 1 decision schema unchanged.

## Boundaries & Constraints

**Always:** Use LangChain `create_agent` and `HumanInTheLoopMiddleware`, with a checkpointer and thread ID so the run can resume. Expose escalation as a local agent tool, never through the read-only MCP server. Require explicit yes before the escalation tool executes. Preserve the `run_agent.py` MLflow setup and the Epic 1 decision output shape.

**Never:** Change `triage/schema.py`, its loader, `mcp/triage_server.py`, `TRIAGE_POLICY.md`, or files under `seed/`. Do not add an alternate MCP server, hand-rolled agent loop, UI, or deployment work. Do not expand this story into unrelated Epic 2 capabilities.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Escalation approved | Final decision is P1; customer is Enterprise; person answers yes | Run resumes, local escalation tool executes, and the unchanged triage decision is returned | Approval interruption must not be treated as a tool failure |
| Escalation declined | Final decision is P1; customer is Enterprise; person answers no | Run resumes without executing the escalation tool and returns the unchanged triage decision | Rejection is a completed non-escalated run |
| No escalation rule | Final decision is not P1 or customer is not Enterprise | No approval prompt and no escalation tool call | N/A |

</frozen-after-approval>

## Open Questions

- **Missing prerequisites:** Epic 2 story 1 (“The triage agent”) is not implemented on `main`, and this checkout also lacks Epic 1's loader/database setup required by the agent's MCP tools. Should this branch include those prerequisite implementations so Story 2 can be integrated and exercised end to end, or should Story 2 wait until they land separately? Including them makes this branch larger than the requested story; waiting leaves this story unimplementable in the current checkout.

## Code Map

- `_bmad-output/specs/spec-epic-2/SPEC.md` -- canonical CAP-5 behavior, agent integration constraints, protected files, and terminal yes/no contract.
- `_bmad-output/specs/spec-epic-2/stories.yaml` -- identifies story ID `2` as “Human-gated escalation”; its story ID is authoritative (the generated epic context numbers this capability differently).
- `TRIAGE_POLICY.md` -- escalation condition is final priority P1 plus Enterprise; explicit approval is required.
- `run_agent.py` -- integration point imports `triage`, runs it with `asyncio.run`, and prints the schema-shaped decision; preserve MLflow setup.
- `.agents/skills/langchain-middleware/SKILL.md` -- HITL requires a checkpointer and thread ID; resumes through LangGraph `Command` decisions.
- `triage/schema.py` -- unchanged output schema; there is no escalation field, so approval state belongs to tool execution/run behavior.
- `mcp/triage_server.py` -- read-only MCP implementation; do not add escalation there.
- `tests/` -- currently only schema tests; add isolated agent/HITL coverage after prerequisites are resolved.
- `origin/stage-3:agent.py` and `origin/stage-3:tests/test_agent.py` -- read-only reference for the repository's later end-to-end design, including local tool and approval/rejection flow; do not copy the unrelated Epic 2 story 1 implementation into this story without resolving the open question.

## Tasks & Acceptance

**Execution:**
- [ ] Add a local `escalate_to_human` tool and gate it with `HumanInTheLoopMiddleware` so it cannot execute before an explicit approval.
- [ ] Resume approved and rejected interruptions correctly, preserving the existing triage decision schema and `run_agent.py` MLflow wiring.
- [ ] Add tests covering all I/O matrix cases, including proof that rejection never executes the escalation tool.

**Acceptance Criteria:**
- Given a final P1 decision for an Enterprise customer, when the person answers yes at the terminal, then the run resumes, the escalation tool executes, and the run returns a valid Epic 1 decision.
- Given the same escalation condition, when the person answers no, then the run completes without executing escalation and still returns a valid Epic 1 decision.
- Given any other decision/customer-plan combination, when triage completes, then there is no approval prompt and no escalation call.
- The agent's approval path uses LangChain's HITL middleware and a resumable checkpointer/thread ID; no change is made to the protected Epic 1, MCP, policy, or seed files.

## Implementation Notes


## Spec Change Log


## Review Triage Log


## Design Notes

Successful tool execution represents the workshop's escalation action; the repo has no external paging endpoint and the Epic 1 schema has no escalation field. An approval records escalation in the agent/tool trace while the returned decision remains schema-compatible.

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass, including the new approval, rejection, and no-escalation coverage.

**Manual checks (if no CLI):**
- Run the agent with a P1 Enterprise ticket and verify the terminal prompt blocks until a yes/no response.

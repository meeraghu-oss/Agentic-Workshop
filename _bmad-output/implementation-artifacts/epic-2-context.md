# Epic 2 Context: the triage agent

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

This epic delivers the workshop's first end-to-end triage agent: a LangChain agent that reads a support ticket through MCP tools, retrieves the related customer history, applies `TRIAGE_POLICY.md`, and returns a trustworthy decision using the Epic 1 structured schema. The planning artifacts directory was missing, so this context is compiled from the Epic 2 SPEC only; no additional PRD, architecture, UX/design, or product-brief constraints were available.

## Stories

- Story 2.1: Runnable triage agent entrypoint
- Story 2.2: Provider switching by environment
- Story 2.3: Ticket and customer lookup flow
- Story 2.4: Policy-based structured decision output
- Story 2.5: Human-approved escalation
- Story 2.6: Prompt-injection resistant ticket handling

## Requirements & Constraints

The command `uv run python run_agent.py <ticket_id>` must execute the triage flow and print a JSON decision that conforms to the Epic 1 triage-decision schema. `T-1042` must resolve to category `billing`, priority `P2`, route `billing-team`, with a rationale. `T-1099` must resolve to `bug` / `P4`, proving that instructions embedded in ticket text are treated as untrusted data rather than agent instructions.

The agent must retrieve the ticket first and then retrieve the customer history using the `customer_id` returned by that ticket lookup. MLflow traces must show the tool-call order and the exact customer ID handoff.

The decision must be policy-driven and schema-valid. If structured output fails validation, the agent retries once; if the retry also fails, the run stops with a clear error. The Enterprise priority bump must follow policy behavior, including leaving `T-1042` at P2 because Northwind is below the bump threshold.

Escalation is approval-gated. When a policy outcome requires escalation for a P1 Enterprise customer, the run must pause at the terminal for a yes/no approval. A "yes" completes the run as escalated; a "no" completes it without escalation. No run may escalate without explicit human approval.

The following assets are read-only and must not be changed: the Epic 1 triage-decision schema and loader, `mcp/triage_server.py`, `TRIAGE_POLICY.md`, and everything under `seed/`. The eval harness, LLM judge, UI work, hosting, and deployment are out of scope.

## Technical Decisions

Build the agent with LangChain's `create_agent`; do not implement a custom tool loop. MCP access must use only `mcp/triage_server.py` over stdio through `langchain-mcp-adapters`.

Provider selection is controlled entirely by environment variables. The default path uses `ChatGoogleGenerativeAI`, reading the model from `MODEL` with default `gemini-3.8-flash` and the API key from `GEMINI_API_KEY`. When `PROVIDER=groq`, the agent uses `ChatGroq`, reading the model from `MODEL` with default `openai/gpt-oss-120b` and the API key from `GROQ_API_KEY`. Both providers must work through the same `run_agent.py` invocation.

`run_agent.py` is the integration point: it imports `triage` from an `agent` module, calls it with `asyncio.run`, and prints `json.dumps(decision, indent=2)`. Its MLflow setup must remain in place: tracking URI `sqlite:///mlflow.db`, experiment `triage-agent`, and `mlflow.langchain.autolog()`.

`escalate_to_human` must be a local tool exposed by the agent rather than a tool added to `mcp/triage_server.py`. It must be gated end to end by LangChain's human-in-the-loop middleware so escalation always pauses for approval.

## Cross-Story Dependencies

Epic 2 depends on Epic 1's schema and loader for structured decision validation and output shape. The provider-switching, MCP lookup, policy, validation, and escalation behavior all converge in the same `run_agent.py` command, so each story must preserve that single execution path. Epic 3 depends on Epic 2 producing real, traceable end-to-end agent runs that an evaluation harness can later measure.

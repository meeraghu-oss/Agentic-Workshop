---
id: SPEC-epic-1
companions: []
sources: [../../../INTENT.md]
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Epic 1: Triage Data and Schema

## Why

The support-ticket triage system needs trustworthy local data and a strict decision contract before an agent can make or evaluate decisions. Epic 1 establishes that foundation so later components can consume a stable SQLite schema and produce consistently validated JSON.

## Capabilities

- **CAP-1**
  - **intent:** The system can represent every triage decision as a validated JSON object with a category, priority, route, and one-sentence rationale.
  - **success:** A valid decision accepts category `billing`, `bug`, `access`, `performance`, or `how-to`; priority `P1` through `P4`; route `billing-team`, `bug-team`, `access-team`, `performance-team`, or `how-to-team`; and a one-sentence rationale. Any other shape or value is rejected with a clear error.

- **CAP-2**
  - **intent:** A developer can load the supplied ticket and customer seed data into the local database with one repeatable command.
  - **success:** `uv run python load_seed.py` creates `app.db` with a `tickets` table containing `ticket_id`, `customer_id`, `created_at`, and `text`, and a `customers` table containing `customer_id`, `name`, `plan`, and `open_tickets`. Running the command twice leaves the same rows and values as running it once.

## Constraints

- Use Python 3.12 or newer with uv.
- Treat every file under `seed/` as read-only input.
- Make no network calls and require no API keys.
- Preserve the `app.db` table and column names consumed by `mcp/triage_server.py`; do not modify that consumer.

## Non-goals

- Building or changing the agent, MCP tools, evaluations, or any user interface.

## Success signal

The seed loader can be run repeatedly to produce the same MCP-compatible local database, and triage decisions with exactly the supported fields and values validate while invalid decisions fail with a clear error.

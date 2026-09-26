# Epic 1 Context: Triage Data and Schema

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish the trustworthy local foundation required by later triage-agent work: a strict, validated contract for triage decisions and a repeatable way to populate an MCP-compatible SQLite database from the supplied seed data. No separate planning-artifacts directory was available, so this context is limited to the canonical Epic 1 spec and its story list.

## Stories

- Story 1.1: Triage decision schema
- Story 1.2: Repeatable seed data loader

## Requirements & Constraints

- A triage decision must contain exactly a category, priority, route, and one-sentence rationale, and invalid shapes or values must fail with a clear error.
- Supported categories are `billing`, `bug`, `access`, `performance`, and `how-to`.
- Supported priorities are `P1`, `P2`, `P3`, and `P4`.
- Supported routes are `billing-team`, `bug-team`, `access-team`, `performance-team`, and `how-to-team`.
- `uv run python load_seed.py` must create `app.db` from the supplied ticket and customer seed data.
- The `tickets` table must expose `ticket_id`, `customer_id`, `created_at`, and `text`. The `customers` table must expose `customer_id`, `name`, `plan`, and `open_tickets`.
- Seed loading must be idempotent: running the loader twice must leave the same rows and values as running it once.
- Use Python 3.12 or newer with uv. The implementation must run locally without network access or API keys.
- Treat all files under `seed/` as read-only inputs.
- Do not build or change the agent, MCP tools, evaluations, or user interface as part of this epic.

## Technical Decisions

- Persist seed data in the local SQLite database named `app.db`.
- Preserve the database table and column contract consumed by `mcp/triage_server.py`; that consumer must remain unchanged.
- Validation is strict: only the four supported decision fields and their enumerated values are accepted, and the rationale must be one sentence.
- Seed ingestion must converge on the same database contents on every run rather than accumulating duplicate or divergent records.

## Cross-Story Dependencies

Implement Story 1.1 before Story 1.2. Both stories establish independent parts of the same foundation; together they provide the stable decision contract and local data required by later agent and MCP work.

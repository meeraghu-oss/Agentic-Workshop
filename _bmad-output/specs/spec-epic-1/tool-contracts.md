# Tool Contracts

These contracts are required for Epic 1: Claim Review Context and Tooling.

| Tool | Required behavior |
|---|---|
| `get_claim(claim_id)` | Returns the employee ID and line items for the claim. |
| `get_employee(employee_id)` | Returns the employee level and city. |
| `get_policy_limits(level, city)` | Returns limits by category for the employee level and city. |
| `record_decision(line_id, decision, clause)` | Writes one line item decision for later reviewer inspection. |

Epic 1 must make these contracts available, but it does not need to implement policy decision logic beyond enabling later use of `record_decision`.

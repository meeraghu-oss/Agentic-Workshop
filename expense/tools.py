"""CSV-backed context lookup tools for Case A expense claims."""

import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent.parent / "cases" / "expense" / "seed"
DECISIONS_DB_PATH = ROOT / "expense.db"
DECISIONS = {"approve", "flag", "reject"}


def _read_csv(name: str) -> list[dict[str, str]]:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing expense seed file: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def _money(value: str) -> float:
    return float(value)


def _receipt(value: str) -> bool:
    return value.strip().lower() == "yes"


def get_claim(claim_id: str) -> dict:
    """Return a claim's employee ID and line items."""
    claims = _read_csv("claims.csv")
    claim = next((row for row in claims if row["claim_id"] == claim_id), None)
    if claim is None:
        raise ValueError(f"No claim with ID {claim_id}")

    line_items = [
        {
            **row,
            "amount": _money(row["amount"]),
            "has_receipt": _receipt(row["has_receipt"]),
        }
        for row in _read_csv("line_items.csv")
        if row["claim_id"] == claim_id
    ]
    return {**claim, "line_items": line_items}


def get_employee(employee_id: str) -> dict:
    """Return an employee's level and city."""
    employee = next((row for row in _read_csv("employees.csv") if row["employee_id"] == employee_id), None)
    if employee is None:
        raise ValueError(f"No employee with ID {employee_id}")
    return employee


def get_policy_limits(level: str, city: str) -> dict[str, float]:
    """Return category limits for an employee level and city."""
    limits = {
        row["category"]: _money(row["limit_cad"])
        for row in _read_csv("limits.csv")
        if row["level"] == level and row["city"] == city
    }
    if not limits:
        raise ValueError(f"No policy limits for {level} in {city}")
    return limits


def record_decision(line_id: str, decision: str, clause: str) -> dict[str, str]:
    """Write one line item decision for later reviewer inspection."""
    if not line_id.strip():
        raise ValueError("Line ID is required")
    if decision not in DECISIONS:
        raise ValueError(f"Decision must be one of {sorted(DECISIONS)}")
    if not clause.strip():
        raise ValueError("Clause is required")

    with sqlite3.connect(DECISIONS_DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                line_id TEXT PRIMARY KEY,
                decision TEXT NOT NULL,
                clause TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT INTO decisions (line_id, decision, clause)
            VALUES (?, ?, ?)
            ON CONFLICT(line_id) DO UPDATE SET
                decision = excluded.decision,
                clause = excluded.clause
            """,
            (line_id, decision, clause),
        )
        conn.commit()
    return {"line_id": line_id, "decision": decision, "clause": clause}

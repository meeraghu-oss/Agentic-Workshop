"""CSV-backed context lookup tools for Case A expense claims."""

import csv
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "cases" / "expense" / "seed"


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

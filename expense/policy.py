"""Read-only Case A policy evaluation for individual expense line items."""

from datetime import date

from .tools import _read_csv, get_employee, get_policy_limits


PRECEDENCE = ("3.1", "3.2", "3.3", "5.1", "1.2", "4.1", "limits", "1.3")
CATEGORY_CLAUSES = {
    "meals": "2.1",
    "hotel": "2.2",
    "flight": "2.3",
    "ground": "6.1",
}


def _parse_day(value: str) -> date:
    return date.fromisoformat(value)


def _all_items() -> list[dict[str, str]]:
    return _read_csv("line_items.csv")


def _is_duplicate(item: dict[str, str]) -> bool:
    items = _all_items()
    claims = {row["claim_id"]: row["employee_id"] for row in _read_csv("claims.csv")}
    current_employee = claims[item["claim_id"]]
    for candidate in items:
        if candidate["line_id"] == item["line_id"]:
            return False
        if (
            claims[candidate["claim_id"]] == current_employee
            and candidate["date"] == item["date"]
            and candidate["merchant"] == item["merchant"]
            and round(float(candidate["amount"]), 2) == round(float(item["amount"]), 2)
        ):
            return True
    return False


def decide_line_item(item: dict, claim: dict, employee: dict | None = None) -> dict[str, str]:
    """Return exactly one decision and the first applicable policy clause."""
    employee = employee or get_employee(claim["employee_id"])
    category = item["category"].lower()
    description = item.get("description", "").lower()
    merchant = item.get("merchant", "").lower()

    if category == "alcohol" or "alcohol" in description or "beer" in description or "wine" in description:
        return {"decision": "reject", "clause": "3.1"}
    if category in {"personal", "gym", "entertainment", "clothing"} or any(
        word in description or word in merchant for word in ("gym", "entertainment", "clothing")
    ):
        return {"decision": "reject", "clause": "3.2"}
    if category in {"parking_ticket", "traffic_fine", "fine"} or "ticket" in description or "fine" in description:
        return {"decision": "reject", "clause": "3.3"}
    if _is_duplicate(item):
        return {"decision": "reject", "clause": "5.1"}
    if (_parse_day(claim["submitted_at"]) - _parse_day(item["date"])).days > 60:
        return {"decision": "reject", "clause": "1.2"}
    if category in {"software", "equipment"}:
        if __import__("re").search(r"ITA-\d+", item.get("description", "")):
            return {"decision": "approve", "clause": "4.1"}
        return {"decision": "reject", "clause": "4.1"}

    limits = get_policy_limits(employee["level"], item["city"])
    if category in {"meals", "ground"}:
        total = sum(
            float(other["amount"])
            for other in claim["line_items"]
            if other["date"] == item["date"] and other["category"].lower() == category
        )
    else:
        total = float(item["amount"])
    if category in limits:
        limit = limits[category]
        if total > limit * 1.2:
            return {"decision": "reject", "clause": CATEGORY_CLAUSES[category]}
        if total > limit:
            return {"decision": "flag", "clause": CATEGORY_CLAUSES[category]}
    if float(item["amount"]) > 25 and not item["has_receipt"]:
        return {"decision": "flag", "clause": "1.3"}
    return {"decision": "approve", "clause": CATEGORY_CLAUSES.get(category, "1.1")}


def decide_claim(claim: dict, employee: dict | None = None) -> list[dict[str, str]]:
    employee = employee or get_employee(claim["employee_id"])
    return [
        {"line_id": item["line_id"], **decide_line_item(item, claim, employee)}
        for item in claim["line_items"]
    ]

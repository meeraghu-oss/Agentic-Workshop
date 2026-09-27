"""Claim review orchestration for finance reviewers."""

from .policy import decide_claim
from .tools import get_claim, record_decision


def _explanation(result: dict[str, str]) -> str:
    if result["decision"] == "approve":
        return f"Approved under policy clause {result['clause']}."
    if result["decision"] == "flag":
        return f"Flagged for reviewer follow-up under policy clause {result['clause']}."
    return f"Rejected under policy clause {result['clause']}."


def review_claim(claim_id: str) -> list[dict[str, str]]:
    claim = get_claim(claim_id)
    rows = []
    for result in decide_claim(claim):
        explanation = _explanation(result)
        item = next(item for item in claim["line_items"] if item["line_id"] == result["line_id"])
        rows.append({**record_decision(**result, explanation=explanation), "amount": item["amount"]})
    return rows


def review_claim_summary(claim_id: str) -> dict:
    rows = review_claim(claim_id)
    return {
        "claim_id": claim_id,
        "line_items": rows,
        "reimbursable_total": round(sum(row["amount"] for row in rows if row["decision"] == "approve"), 2),
    }

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
    return [
        record_decision(**result, explanation=_explanation(result))
        for result in decide_claim(claim)
    ]

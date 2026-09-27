import csv

from expense.policy import decide_claim, validate_labelled_examples
from expense.tools import get_claim


def test_labelled_examples_match_policy_decisions_and_clauses():
    with open("cases/expense/eval/labelled.csv", newline="") as handle:
        labels = list(csv.DictReader(handle))
    claims = {row["claim_id"]: get_claim(row["claim_id"]) for row in labels}
    actual = {
        result["line_id"]: result
        for claim in claims.values()
        for result in decide_claim(claim)
    }
    mismatches = [
        row for row in labels
        if actual[row["line_id"]]["decision"] != row["expected_decision"]
        or actual[row["line_id"]]["clause"] != row["expected_clause"]
    ]
    assert mismatches == []


def test_labelled_validator_returns_no_mismatches():
    assert validate_labelled_examples() == []

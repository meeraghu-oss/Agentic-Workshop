import pytest

from expense.tools import get_claim, get_employee, get_policy_limits


def test_get_claim_returns_employee_id_and_line_items():
    claim = get_claim("CL-2001")

    assert claim["employee_id"] == "E-101"
    assert len(claim["line_items"]) == 4
    assert claim["line_items"][0]["line_id"] == "L-3001"
    assert claim["line_items"][0]["amount"] == 546.57
    assert claim["line_items"][0]["has_receipt"] is True


def test_get_employee_returns_level_and_city():
    employee = get_employee("E-101")

    assert employee["level"] == "L2"
    assert employee["city"] == "Toronto"


def test_get_policy_limits_returns_category_limits():
    limits = get_policy_limits("L2", "Toronto")

    assert limits == {
        "meals": 75.0,
        "hotel": 220.0,
        "flight": 700.0,
        "ground": 80.0,
    }


@pytest.mark.parametrize(
    "lookup",
    [
        lambda: get_claim("CL-missing"),
        lambda: get_employee("E-missing"),
        lambda: get_policy_limits("L9", "Atlantis"),
    ],
)
def test_lookup_tools_raise_clear_errors_for_missing_context(lookup):
    with pytest.raises(ValueError, match="No .*"):
        lookup()

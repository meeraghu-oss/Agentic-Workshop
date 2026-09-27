import pytest

from expense import tools
from expense.tools import get_claim, get_employee, get_policy_limits, record_decision


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


def test_record_decision_writes_and_updates_one_line_item(tmp_path, monkeypatch):
    db_path = tmp_path / "expense.db"
    monkeypatch.setattr(tools, "DECISIONS_DB_PATH", db_path)

    assert record_decision("L-3001", "approve", "2.3") == {
        "line_id": "L-3001",
        "decision": "approve",
        "clause": "2.3",
    }
    assert record_decision("L-3001", "flag", "1.3")["decision"] == "flag"

    import sqlite3

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT line_id, decision, clause FROM decisions").fetchall()
    assert rows == [("L-3001", "flag", "1.3")]


def test_record_decision_rejects_invalid_storage_values(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "DECISIONS_DB_PATH", tmp_path / "expense.db")

    with pytest.raises(ValueError, match="Line ID"):
        record_decision(" ", "approve", "2.3")
    with pytest.raises(ValueError, match="Decision"):
        record_decision("L-3001", "maybe", "2.3")
    with pytest.raises(ValueError, match="Clause"):
        record_decision("L-3001", "approve", " ")


def test_record_decision_stores_explanation(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "DECISIONS_DB_PATH", tmp_path / "expense.db")
    result = record_decision("L-test", "approve", "2.1", "Within the daily meal limit.")
    assert result["explanation"] == "Within the daily meal limit."

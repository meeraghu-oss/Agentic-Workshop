import json

import pytest

from triage.schema import TriageDecision, TriageValidationError, validate_decision

VALID = {"category": "billing", "priority": "P2", "route": "billing-team", "rationale": "A double charge is a money problem."}


def test_accepts_a_valid_decision_as_dict_or_json():
    assert validate_decision(VALID) == TriageDecision(**VALID)
    assert validate_decision(json.dumps(VALID)).priority == "P2"


@pytest.mark.parametrize(
    "field, value",
    [
        ("category", "billing"),
        ("category", "bug"),
        ("category", "access"),
        ("category", "performance"),
        ("category", "how-to"),
        ("priority", "P1"),
        ("priority", "P2"),
        ("priority", "P3"),
        ("priority", "P4"),
        ("route", "billing-team"),
        ("route", "bug-team"),
        ("route", "access-team"),
        ("route", "performance-team"),
        ("route", "how-to-team"),
    ],
)
def test_accepts_every_supported_enum_value(field, value):
    decision = validate_decision({**VALID, field: value})
    assert getattr(decision, field) == value


@pytest.mark.parametrize(
    "change, field",
    [
        ({"category": "sales"}, "category"),
        ({"priority": "P5"}, "priority"),
        ({"route": "finance-team"}, "route"),
        ({"rationale": "   "}, "rationale"),
        ({"rationale": "First sentence. Second sentence."}, "rationale"),
        ({"rationale": "First sentence.Second sentence."}, "rationale"),
        ({"rationale": b"A double charge is a money problem."}, "rationale"),
        ({"extra": "field"}, "extra"),
    ],
)
def test_rejects_bad_fields_with_a_message_naming_the_field(change, field):
    with pytest.raises(TriageValidationError, match=field):
        validate_decision({**VALID, **change})


@pytest.mark.parametrize("field", ["category", "priority", "route", "rationale"])
def test_rejects_a_missing_field(field):
    payload = {k: v for k, v in VALID.items() if k != field}
    with pytest.raises(TriageValidationError, match=field):
        validate_decision(payload)


@pytest.mark.parametrize(
    "payload, message",
    [
        ("not json", "not valid JSON"),
        (b"\x80\x81", "not valid JSON"),
        ("[1, 2]", "Decision must be a JSON object, got list"),
        ("42", "Decision must be a JSON object, got int"),
    ],
)
def test_rejects_non_objects(payload, message):
    with pytest.raises(TriageValidationError, match=message):
        validate_decision(payload)


def test_decisions_are_immutable():
    decision = validate_decision(VALID)
    with pytest.raises(Exception, match="frozen"):
        decision.priority = "P1"

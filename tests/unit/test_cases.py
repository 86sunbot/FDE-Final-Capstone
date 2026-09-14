import pytest


def test_p0_case_requires_owner_and_evidence(app, principals, evidence):
    evidence("EV-1")
    with pytest.raises(ValueError, match="P0_CASE_REQUIRES_OWNER"):
        app.cases.open_case(principals["coordinator"], "TEST", "J-1", "P0", "", "reason", ["EV-1"])
    case = app.cases.open_case(principals["coordinator"], "TEST", "J-1", "P0", "QUEUE", "reason", ["EV-1"])
    assert case["owner"] == "QUEUE"
    assert app.cases.unowned_p0_count() == 0


def test_illegal_case_transition_is_rejected(app, principals, evidence):
    evidence("EV-1")
    case = app.cases.open_case(principals["coordinator"], "TEST", "J-1", "P1", "QUEUE", "reason", ["EV-1"])
    with pytest.raises(ValueError, match="ILLEGAL_CASE_TRANSITION"):
        app.cases.transition(case["case_id"], "CLOSED")

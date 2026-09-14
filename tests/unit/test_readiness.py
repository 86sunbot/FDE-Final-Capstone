from fde_capstone.model import Outcome


def test_missing_milestone_prerequisite_is_unknown_and_fail_closed(app, principals, evidence):
    evidence("EV-ID")
    result = app.readiness.assess(principals["viewer"], "J-1", "PRE_COLLECTION", {"identity": (Outcome.SATISFIED, ["EV-ID"])})
    assert result.outcome == Outcome.UNKNOWN
    assert set(result.unknowns) == {"authorization", "consent", "site"}


def test_explicit_not_satisfied_dominates_unknown(app, principals, evidence):
    evidence("EV-ID")
    evidence("EV-CONSENT")
    result = app.readiness.assess(
        principals["viewer"], "J-1", "PRE_COLLECTION",
        {
            "identity": (Outcome.SATISFIED, ["EV-ID"]),
            "consent": (Outcome.NOT_SATISFIED, ["EV-CONSENT"]),
            "authorization": (Outcome.UNKNOWN, []),
            "site": (Outcome.UNKNOWN, []),
        },
    )
    assert result.outcome == Outcome.NOT_SATISFIED
    assert result.blockers == ("consent",)

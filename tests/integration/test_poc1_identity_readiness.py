import pytest

from fde_capstone.model import Outcome
from fde_capstone.security import AuthorizationError


def test_identity_conflict_does_not_link_until_exact_authorized_approval(app, principals, evidence):
    evidence("EV-MRN", "CRM", {"mrn": "M-1", "patient": "P-A"})
    evidence("EV-DOB", "CLINICAL", {"dob": "1980-01-01", "patient": "P-B"})
    case = app.identity.detect_conflict(principals["coordinator"], "P-A", "P-B", "conflicting assertions", ["EV-MRN", "EV-DOB"])
    assert app.identity.links() == []
    proposal = app.identity.propose(principals["coordinator"], case["case_id"], "P-A", "P-B", "SAME_SUBJECT", ["EV-MRN", "EV-DOB"])
    with pytest.raises(AuthorizationError):
        app.identity.decide(principals["viewer"], case["case_id"], "APPROVE", proposal["proposal_digest"])
    assert app.identity.links() == []
    with pytest.raises(ValueError, match="PROPOSAL_DIGEST_MISMATCH"):
        app.identity.decide(principals["identity"], case["case_id"], "APPROVE", "changed")
    result = app.identity.decide(principals["identity"], case["case_id"], "APPROVE", proposal["proposal_digest"])
    replay = app.identity.decide(principals["identity"], case["case_id"], "APPROVE", proposal["proposal_digest"])
    assert result["status"] == "APPLIED"
    assert replay["replay"] is True
    assert len(app.identity.links()) == 1


def test_identity_proposal_requires_multiple_evidence_items(app, principals, evidence):
    evidence("EV-ONE")
    evidence("EV-TWO")
    case = app.identity.detect_conflict(principals["coordinator"], "P-A", "P-B", "conflict", ["EV-ONE", "EV-TWO"])
    with pytest.raises(ValueError, match="CORROBORATION_REQUIRED"):
        app.identity.propose(principals["coordinator"], case["case_id"], "P-A", "P-B", "SAME_SUBJECT", ["EV-ONE"])


def test_withdrawn_consent_blocks_pre_collection(app, principals, evidence):
    for item in ["EV-ID", "EV-CONSENT", "EV-AUTH", "EV-SITE"]:
        evidence(item)
    result = app.readiness.assess(
        principals["viewer"], "P-A", "PRE_COLLECTION",
        {
            "identity": (Outcome.SATISFIED, ["EV-ID"]),
            "consent": (Outcome.NOT_SATISFIED, ["EV-CONSENT"]),
            "authorization": (Outcome.SATISFIED, ["EV-AUTH"]),
            "site": (Outcome.SATISFIED, ["EV-SITE"]),
        },
    )
    assert result.outcome == Outcome.NOT_SATISFIED
    assert "consent" in result.blockers

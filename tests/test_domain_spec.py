import json
from pathlib import Path

from tools.validate_domain_spec import validate

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs/stages/stage_05" / "domain_spec.json"


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def test_domain_spec_is_internally_consistent() -> None:
    assert validate(load_spec()) == []


def test_quality_release_cannot_be_created_by_mes_or_erp_event() -> None:
    spec = load_spec()
    transitions = spec["state_machines"]["quality_release"]["transitions"]
    approved = [transition for transition in transitions if transition["to"] == "APPROVED"]
    assert approved == [
        {
            "from": "UNDER_REVIEW",
            "to": "APPROVED",
            "event": "ProductReleased",
            "guard": "release_prerequisites_and_authority_valid",
            "authority_required": True,
        }
    ]


def test_recommendation_is_not_a_state_transition() -> None:
    spec = load_spec()
    events = {
        transition["event"]
        for machine in spec["state_machines"].values()
        for transition in machine["transitions"]
    }
    assert "RecommendationGenerated" not in events


def test_identity_approval_requires_authority() -> None:
    spec = load_spec()
    transitions = spec["state_machines"]["identity_case"]["transitions"]
    approved = [transition for transition in transitions if transition["to"] == "APPROVED"]
    assert len(approved) == 1
    assert approved[0]["event"] == "IdentityResolutionApproved"
    assert approved[0]["authority_required"] is True


def test_idempotency_conflict_is_terminal_before_dispatch() -> None:
    spec = load_spec()
    machine = spec["state_machines"]["command_saga"]
    conflicts = [
        transition
        for transition in machine["transitions"]
        if transition["event"] == "IdempotencyConflictDetected"
    ]
    assert conflicts == [
        {
            "from": "RECEIVED",
            "to": "REJECTED_CONFLICT",
            "event": "IdempotencyConflictDetected",
            "guard": "same_key_different_payload",
            "authority_required": False,
        }
    ]
    assert not [transition for transition in machine["transitions"] if transition["from"] == "REJECTED_CONFLICT"]

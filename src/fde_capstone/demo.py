from __future__ import annotations

from pathlib import Path

from .application import CapstoneApplication
from .model import Outcome, Principal


T0 = "2026-01-01T10:00:00+00:00"


def principal(subject: str, role: str, scopes: set[str] | None = None) -> Principal:
    return Principal(subject, frozenset({role}), frozenset(scopes or {"*"}))


def register(app: CapstoneApplication, evidence_id: str, source: str, payload: dict) -> str:
    return app.evidence.register(evidence_id, source, f"synthetic://{evidence_id}", payload, T0, T0)


def run_demo(database_path: str | Path, ai_mode: str = "off") -> dict:
    app = CapstoneApplication(database_path, ai_mode=ai_mode)
    coordinator = principal("demo-coordinator", "COORDINATOR")
    identity_authority = principal("demo-identity-authority", "IDENTITY_AUTHORITY")
    planner = principal("demo-planner", "PLANNER")
    quality_authority = principal("demo-quality-authority", "QUALITY_AUTHORITY")
    viewer = principal("demo-viewer", "VIEWER")

    try:
        for evidence_id, source, payload in [
            ("EV-ID-MRN", "CRM", {"mrn": "MRN-100", "patient": "P-A"}),
            ("EV-ID-DOB", "CLINICAL", {"dob": "1980-01-01", "patient": "P-B"}),
            ("EV-CONSENT", "CLINICAL", {"status": "CURRENT"}),
            ("EV-AUTH", "PAYER", {"status": "APPROVED"}),
            ("EV-SITE", "QMS", {"training": "CURRENT", "equipment": "CURRENT"}),
        ]:
            register(app, evidence_id, source, payload)
        identity_case = app.identity.detect_conflict(coordinator, "P-A", "P-B", "MRN/DOB assertions conflict", ["EV-ID-MRN", "EV-ID-DOB"])
        proposal = app.identity.propose(coordinator, identity_case["case_id"], "P-A", "P-B", "SAME_SUBJECT", ["EV-ID-MRN", "EV-ID-DOB"])
        identity_decision = app.identity.decide(identity_authority, identity_case["case_id"], "APPROVE", proposal["proposal_digest"])
        readiness = app.readiness.assess(
            viewer,
            "P-A",
            "PRE_COLLECTION",
            {
                "identity": (Outcome.SATISFIED, ["EV-ID-MRN", "EV-ID-DOB"]),
                "consent": (Outcome.SATISFIED, ["EV-CONSENT"]),
                "authorization": (Outcome.SATISFIED, ["EV-AUTH"]),
                "site": (Outcome.SATISFIED, ["EV-SITE"]),
            },
        )

        slot = app.commands.reserve_slot(planner, "IDEMP-DEMO-1", "P-A", "SLOT-100", behavior="timeout_after_success")
        reconciled = app.commands.reconcile(planner, slot["command_id"])
        replay = app.commands.reserve_slot(planner, "IDEMP-DEMO-1", "P-A", "SLOT-100")

        for evidence_id, source, payload in [
            ("EV-MES", "MES", {"status": "MFG_COMPLETE"}),
            ("EV-QC", "LIMS", {"result": "PASS"}),
            ("EV-DEV", "QMS", {"status": "CLOSED", "blocking": False}),
            ("EV-THERMAL", "LOGISTICS", {"status": "PROFILE_ACCEPTABLE"}),
            ("EV-QMS-DECISION", "QMS", {"decision": "RELEASED", "simulated": True}),
        ]:
            register(app, evidence_id, source, payload)
        app.quality.add_evidence("BATCH-100", "EV-MES", "MES_STATUS", "MFG_COMPLETE")
        app.quality.add_evidence("BATCH-100", "EV-QC", "QC_RESULT", "PASS", disposition="ACCEPTED")
        app.quality.add_evidence("BATCH-100", "EV-DEV", "DEVIATION", "CLOSED", blocking=False)
        app.quality.add_evidence("BATCH-100", "EV-THERMAL", "THERMAL", "PROFILE_ACCEPTABLE")
        before_release = app.quality.packet("BATCH-100")
        release = app.quality.authorize_release(quality_authority, "BATCH-100", "EV-QMS-DECISION")
        after_release = app.quality.packet("BATCH-100")

        recommendation = app.assistant.recommend(
            "BATCH-100",
            {
                "state": after_release["release_outcome"],
                "blockers": after_release["blockers"],
                "unknowns": after_release["unknowns"],
                "available_evidence": after_release["evidence_refs"],
            },
        )
        return {
            "scope": "SYNTHETIC_LOCAL_ACADEMIC_POC",
            "ai_mode": ai_mode,
            "poc1": {
                "case": identity_case["case_id"],
                "decision": identity_decision["status"],
                "readiness": readiness.outcome.value,
                "evidence_refs": list(readiness.evidence_refs),
            },
            "poc2": {
                "initial_state": slot["state"],
                "reconciled_state": reconciled["state"],
                "replay_dispatch": replay["dispatch"],
            },
            "poc3": {
                "before": before_release["release_outcome"],
                "released": release["released"],
                "after": after_release["release_outcome"],
                "evidence_refs": after_release["evidence_refs"],
            },
            "assistant": {"mode": recommendation["mode"], "rejection_reason": recommendation["rejection_reason"]},
            "audit_chain_valid": app.db.verify_audit_chain(),
            "state_digest": app.db.state_digest(),
            "metrics": app.db.metrics(),
        }
    finally:
        app.close()

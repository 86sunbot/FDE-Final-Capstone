from __future__ import annotations

import json

from ..model import Principal, canonical_json, digest_json, utc_now
from ..storage import Database
from .cases import CaseService
from .common import authorize, correlation
from .evidence import EvidenceService


class IdentityService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.cases = CaseService(db)
        self.evidence = EvidenceService(db)

    def detect_conflict(
        self,
        principal: Principal,
        patient_a: str,
        patient_b: str,
        reason: str,
        evidence_refs: list[str],
        owner: str = "IDENTITY_QUEUE",
    ) -> dict:
        if patient_a == patient_b:
            raise ValueError("CONFLICT_REQUIRES_DISTINCT_PATIENT_KEYS")
        if not self.evidence.exists(evidence_refs):
            raise ValueError("UNKNOWN_EVIDENCE")
        return self.cases.open_case(principal, "IDENTITY_CONFLICT", patient_a, "P0", owner, reason, evidence_refs)

    def propose(
        self,
        principal: Principal,
        case_id: str,
        patient_a: str,
        patient_b: str,
        relation: str,
        evidence_refs: list[str],
    ) -> dict:
        case = self.cases.get(case_id)
        if case["case_type"] != "IDENTITY_CONFLICT":
            raise ValueError("WRONG_CASE_TYPE")
        if not self.evidence.exists(evidence_refs) or len(set(evidence_refs)) < 2:
            raise ValueError("CORROBORATION_REQUIRED")
        proposal = {"patient_a": patient_a, "patient_b": patient_b, "relation": relation, "evidence_refs": sorted(evidence_refs)}
        proposal_digest = digest_json(proposal)
        with self.db._lock, self.db.connection:
            self.db.connection.execute(
                "INSERT INTO identity_proposals VALUES(?,?,?,?,?,?,?,?,?)",
                (case_id, patient_a, patient_b, relation, proposal_digest, canonical_json(sorted(evidence_refs)), "AWAITING_APPROVAL", None, None),
            )
            self.db.connection.execute("UPDATE cases SET status='IN_REVIEW',updated_at=? WHERE case_id=?", (utc_now(), case_id))
        self.db.audit(principal, "identity:propose", case["scope"], "RECORDED", {"case_id": case_id, "proposal_digest": proposal_digest}, correlation())
        return proposal | {"case_id": case_id, "proposal_digest": proposal_digest, "status": "AWAITING_APPROVAL"}

    def decide(
        self,
        principal: Principal,
        case_id: str,
        decision: str,
        proposal_digest: str,
        correlation_id: str | None = None,
    ) -> dict:
        trace = correlation(correlation_id)
        case = self.cases.get(case_id)
        authorize(self.db, principal, "identity:decide", case["scope"], trace)
        row = self.db.connection.execute("SELECT * FROM identity_proposals WHERE case_id=?", (case_id,)).fetchone()
        if not row:
            raise KeyError("IDENTITY_PROPOSAL_NOT_FOUND")
        if proposal_digest != row["proposal_digest"]:
            self.db.audit(principal, "identity:decide", case["scope"], "DENIED", {"reason": "PROPOSAL_DIGEST_MISMATCH"}, trace)
            raise ValueError("PROPOSAL_DIGEST_MISMATCH")
        if row["status"] == "APPLIED" and decision == "APPROVE":
            return {"case_id": case_id, "status": "APPLIED", "replay": True}
        if row["status"] != "AWAITING_APPROVAL":
            raise ValueError("IDENTITY_PROPOSAL_NOT_DECIDABLE")
        if decision not in {"APPROVE", "REJECT"}:
            raise ValueError("INVALID_IDENTITY_DECISION")

        evidence_refs = json.loads(row["evidence_refs_json"])
        now = utc_now()
        status = "REJECTED"
        with self.db._lock, self.db.connection:
            if decision == "APPROVE":
                self.db.connection.execute(
                    "INSERT OR IGNORE INTO identity_links VALUES(?,?,?,?,?,?,?)",
                    (row["patient_a"], row["patient_b"], row["relation"], proposal_digest, principal.subject, row["evidence_refs_json"], now),
                )
                status = "APPLIED"
            self.db.connection.execute(
                "UPDATE identity_proposals SET status=?,decided_by=?,applied_at=? WHERE case_id=?",
                (status, principal.subject, now if status == "APPLIED" else None, case_id),
            )
            self.db.connection.execute("UPDATE cases SET status='RESOLVED',updated_at=? WHERE case_id=?", (now, case_id))
        event_type = "IdentityResolutionApplied" if status == "APPLIED" else "IdentityResolutionRejected"
        event_id = self.db.append_event(
            event_type, "IdentityCase", case_id, "IDENTITY_SERVICE", evidence_refs,
            principal.subject, {"proposal_digest": proposal_digest, "decision": decision}, trace,
            authority="IDENTITY_AUTHORITY", policy_versions=["IDENTITY-RESOLUTION-v1"],
        )
        self.db.audit(principal, "identity:decide", case["scope"], "ALLOWED", {"case_id": case_id, "decision": decision, "event_id": event_id}, trace)
        self.db.metric("identity_decisions")
        return {"case_id": case_id, "status": status, "event_id": event_id, "replay": False}

    def links(self) -> list[dict]:
        return [dict(row) for row in self.db.connection.execute("SELECT * FROM identity_links ORDER BY patient_a,patient_b")]

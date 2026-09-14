from __future__ import annotations

import json

from ..model import Outcome, Principal
from ..storage import Database
from .common import authorize, correlation
from .evidence import EvidenceService


class QualityService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.evidence = EvidenceService(db)

    def add_evidence(
        self,
        batch_id: str,
        evidence_id: str,
        evidence_type: str,
        status: str,
        disposition: str | None = None,
        blocking: bool = False,
        authority_valid: bool = False,
    ) -> None:
        if not self.evidence.exists([evidence_id]):
            raise ValueError("UNKNOWN_EVIDENCE")
        with self.db._lock, self.db.connection:
            self.db.connection.execute(
                "INSERT INTO quality_evidence VALUES(?,?,?,?,?,?,?)",
                (evidence_id, batch_id, evidence_type, status, disposition, int(blocking), int(authority_valid)),
            )

    def packet(self, batch_id: str) -> dict:
        rows = [dict(row) for row in self.db.connection.execute("SELECT * FROM quality_evidence WHERE batch_id=? ORDER BY evidence_id", (batch_id,))]
        evidence_refs = [row["evidence_id"] for row in rows]
        blockers: list[str] = []
        unknowns: list[str] = []
        conflicts: list[str] = []

        has_qms_release = any(row["evidence_type"] == "QMS_RELEASE" and row["status"] == "APPROVED" and row["authority_valid"] for row in rows)
        if not has_qms_release:
            unknowns.append("missing_authorized_qms_release")
        for row in rows:
            if row["evidence_type"] in {"MES_STATUS", "ERP_STATUS"} and row["status"] in {"RELEASED", "AVAILABLE", "MFG_COMPLETE"} and not has_qms_release:
                conflicts.append(f'{row["evidence_type"]}_CANNOT_ESTABLISH_RELEASE')
            if row["evidence_type"] == "QC_RESULT" and row["status"] in {"OOS", "OOT", "PENDING"} and row["disposition"] not in {"ACCEPTED", "RESOLVED", "NOT_APPLICABLE"}:
                blockers.append(f'QC_{row["status"]}_WITHOUT_DISPOSITION')
            if row["evidence_type"] == "DEVIATION" and row["blocking"] and row["status"] not in {"CLOSED", "RESOLVED"}:
                blockers.append("OPEN_BLOCKING_DEVIATION")
            if row["evidence_type"] == "THERMAL" and row["status"] != "PROFILE_ACCEPTABLE":
                unknowns.append("THERMAL_EVIDENCE_INCOMPLETE_OR_AMBIGUOUS")

        required_types = {"QC_RESULT", "DEVIATION", "THERMAL"}
        present = {row["evidence_type"] for row in rows}
        unknowns.extend(f"MISSING_{kind}" for kind in sorted(required_types - present))
        if blockers:
            outcome = Outcome.NOT_SATISFIED
        elif unknowns:
            outcome = Outcome.UNKNOWN
        else:
            outcome = Outcome.SATISFIED
        return {
            "batch_id": batch_id,
            "release_outcome": outcome.value,
            "evidence_refs": evidence_refs,
            "blockers": sorted(set(blockers)),
            "unknowns": sorted(set(unknowns)),
            "conflicts": sorted(set(conflicts)),
            "rule_versions": ["QUALITY-PACKET-v1", "QUALITY-AUTHORITY-v1"],
        }

    def authorize_release(
        self,
        principal: Principal,
        batch_id: str,
        decision_evidence_id: str,
        correlation_id: str | None = None,
        requested_by: str | None = None,
    ) -> dict:
        trace = correlation(correlation_id)
        authorize(self.db, principal, "quality:release", batch_id, trace)
        if requested_by is not None and requested_by == principal.subject:
            self.db.audit(principal, "quality:release", batch_id, "DENIED", {"reason": "SEPARATION_OF_DUTIES"}, trace)
            raise ValueError("SEPARATION_OF_DUTIES")
        if not self.evidence.exists([decision_evidence_id]):
            raise ValueError("UNKNOWN_DECISION_EVIDENCE")
        existing = [row for row in self.db.events_for("Batch", batch_id) if row["event_type"] == "ProductReleased"]
        if existing:
            return {"batch_id": batch_id, "state": "PRODUCT_RELEASED", "event_id": existing[-1]["event_id"], "replay": True}

        before = self.packet(batch_id)
        pre_release_blockers = before["blockers"] + [item for item in before["unknowns"] if item != "missing_authorized_qms_release"]
        if pre_release_blockers:
            self.db.audit(principal, "quality:release", batch_id, "DENIED", {"reason": "EVIDENCE_NOT_READY", "blockers": pre_release_blockers}, trace)
            self.db.metric("quality_release_denied")
            return {"batch_id": batch_id, "state": "QUALITY_REVIEW", "released": False, "blockers": pre_release_blockers}

        with self.db._lock, self.db.connection:
            self.db.connection.execute(
                "INSERT OR REPLACE INTO quality_evidence VALUES(?,?,?,?,?,?,?)",
                (decision_evidence_id, batch_id, "QMS_RELEASE", "APPROVED", "RELEASED", 0, 1),
            )
        evidence_refs = self.packet(batch_id)["evidence_refs"]
        event_id = self.db.append_event(
            "ProductReleased", "Batch", batch_id, "QMS", evidence_refs, principal.subject,
            {"batch_id": batch_id, "decision": "RELEASED"}, trace,
            authority="QUALITY_AUTHORITY", policy_versions=["QUALITY-AUTHORITY-v1"],
        )
        self.db.audit(principal, "quality:release", batch_id, "ALLOWED", {"event_id": event_id}, trace)
        self.db.metric("quality_releases")
        return {"batch_id": batch_id, "state": "PRODUCT_RELEASED", "released": True, "event_id": event_id, "replay": False}

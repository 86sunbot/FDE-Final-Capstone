from __future__ import annotations

import json
import uuid

from ..model import Principal, canonical_json, utc_now
from ..storage import Database
from .common import authorize, correlation


class CaseService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def open_case(
        self,
        principal: Principal,
        case_type: str,
        scope: str,
        severity: str,
        owner: str,
        reason: str,
        evidence_refs: list[str],
        correlation_id: str | None = None,
    ) -> dict:
        trace = correlation(correlation_id)
        authorize(self.db, principal, "case:create", scope, trace)
        if severity == "P0" and not owner:
            raise ValueError("P0_CASE_REQUIRES_OWNER")
        if not evidence_refs:
            raise ValueError("CASE_REQUIRES_EVIDENCE")
        case_id = f"CASE-{uuid.uuid4()}"
        now = utc_now()
        with self.db._lock, self.db.connection:
            self.db.connection.execute(
                "INSERT INTO cases VALUES(?,?,?,?,?,?,?,?,?,?)",
                (case_id, case_type, scope, severity, "OPEN", owner, reason, canonical_json(evidence_refs), now, now),
            )
        self.db.audit(principal, "case:create", scope, "ALLOWED", {"case_id": case_id, "case_type": case_type}, trace)
        self.db.metric("cases_opened")
        return self.get(case_id)

    def get(self, case_id: str) -> dict:
        row = self.db.connection.execute("SELECT * FROM cases WHERE case_id=?", (case_id,)).fetchone()
        if not row:
            raise KeyError(case_id)
        result = dict(row)
        result["evidence_refs"] = json.loads(result.pop("evidence_refs_json"))
        return result

    def transition(self, case_id: str, status: str) -> None:
        allowed = {
            "OPEN": {"IN_REVIEW", "ESCALATED"},
            "IN_REVIEW": {"RESOLVED", "ESCALATED"},
            "ESCALATED": {"IN_REVIEW", "RESOLVED"},
            "RESOLVED": {"CLOSED", "OPEN"},
            "CLOSED": {"OPEN"},
        }
        current = self.get(case_id)["status"]
        if status not in allowed.get(current, set()):
            raise ValueError("ILLEGAL_CASE_TRANSITION")
        with self.db._lock, self.db.connection:
            self.db.connection.execute("UPDATE cases SET status=?,updated_at=? WHERE case_id=?", (status, utc_now(), case_id))

    def unowned_p0_count(self) -> int:
        row = self.db.connection.execute("SELECT COUNT(*) AS n FROM cases WHERE severity='P0' AND TRIM(owner)='' AND status!='CLOSED'").fetchone()
        return int(row["n"])

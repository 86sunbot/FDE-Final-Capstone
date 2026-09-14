from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import uuid
from pathlib import Path
from typing import Any

from .model import Principal, canonical_json, digest_json, utc_now


SCHEMA_VERSION = "1"


DDL = """
CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS evidence(
  evidence_id TEXT PRIMARY KEY, source_system TEXT NOT NULL, source_locator TEXT NOT NULL,
  payload_json TEXT NOT NULL, payload_digest TEXT NOT NULL, occurred_at TEXT NOT NULL,
  recorded_at TEXT NOT NULL, classification TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS assertions(
  assertion_id TEXT PRIMARY KEY, subject_id TEXT NOT NULL, attribute TEXT NOT NULL,
  value_json TEXT NOT NULL, source_system TEXT NOT NULL, occurred_at TEXT NOT NULL,
  recorded_at TEXT NOT NULL, evidence_id TEXT NOT NULL REFERENCES evidence(evidence_id)
);
CREATE INDEX IF NOT EXISTS idx_assertions_subject ON assertions(subject_id, attribute, recorded_at);
CREATE TABLE IF NOT EXISTS events(
  event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, aggregate_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL, sequence INTEGER NOT NULL, occurred_at TEXT NOT NULL,
  recorded_at TEXT NOT NULL, source_system TEXT NOT NULL, evidence_refs_json TEXT NOT NULL,
  correlation_id TEXT NOT NULL, actor TEXT NOT NULL, authority TEXT,
  policy_versions_json TEXT NOT NULL, data_quality TEXT NOT NULL, payload_json TEXT NOT NULL,
  payload_digest TEXT NOT NULL, classification TEXT NOT NULL, trace_id TEXT NOT NULL,
  UNIQUE(aggregate_type, aggregate_id, sequence)
);
CREATE TABLE IF NOT EXISTS audit(
  audit_id INTEGER PRIMARY KEY AUTOINCREMENT, recorded_at TEXT NOT NULL, principal TEXT NOT NULL,
  action TEXT NOT NULL, scope TEXT NOT NULL, outcome TEXT NOT NULL, details_json TEXT NOT NULL,
  correlation_id TEXT NOT NULL, previous_hash TEXT NOT NULL, record_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cases(
  case_id TEXT PRIMARY KEY, case_type TEXT NOT NULL, scope TEXT NOT NULL, severity TEXT NOT NULL,
  status TEXT NOT NULL, owner TEXT NOT NULL, reason TEXT NOT NULL, evidence_refs_json TEXT NOT NULL,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS identity_proposals(
  case_id TEXT PRIMARY KEY REFERENCES cases(case_id), patient_a TEXT NOT NULL, patient_b TEXT NOT NULL,
  relation TEXT NOT NULL, proposal_digest TEXT NOT NULL, evidence_refs_json TEXT NOT NULL,
  status TEXT NOT NULL, decided_by TEXT, applied_at TEXT
);
CREATE TABLE IF NOT EXISTS identity_links(
  patient_a TEXT NOT NULL, patient_b TEXT NOT NULL, relation TEXT NOT NULL,
  proposal_digest TEXT NOT NULL, approved_by TEXT NOT NULL, evidence_refs_json TEXT NOT NULL,
  created_at TEXT NOT NULL, PRIMARY KEY(patient_a, patient_b, relation)
);
CREATE TABLE IF NOT EXISTS commands(
  command_id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE NOT NULL, command_type TEXT NOT NULL,
  scope TEXT NOT NULL, payload_json TEXT NOT NULL, payload_digest TEXT NOT NULL, actor TEXT NOT NULL,
  state TEXT NOT NULL, result_json TEXT, correlation_id TEXT NOT NULL,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS external_reservations(
  reservation_id TEXT PRIMARY KEY, command_id TEXT UNIQUE NOT NULL REFERENCES commands(command_id),
  patient_key TEXT NOT NULL, slot_id TEXT NOT NULL, state TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS quality_evidence(
  evidence_id TEXT PRIMARY KEY REFERENCES evidence(evidence_id), batch_id TEXT NOT NULL,
  evidence_type TEXT NOT NULL, status TEXT NOT NULL, disposition TEXT, blocking INTEGER NOT NULL DEFAULT 0,
  authority_valid INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_quality_batch ON quality_evidence(batch_id, evidence_type);
CREATE TABLE IF NOT EXISTS recommendations(
  recommendation_id TEXT PRIMARY KEY, scope TEXT NOT NULL, mode TEXT NOT NULL,
  output_json TEXT, rejection_reason TEXT, evidence_refs_json TEXT NOT NULL,
  created_at TEXT NOT NULL, correlation_id TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metrics(
  name TEXT PRIMARY KEY, count INTEGER NOT NULL, total REAL NOT NULL, last_value REAL NOT NULL,
  updated_at TEXT NOT NULL
);
"""


class Database:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA journal_mode=WAL")
        self._lock = threading.RLock()
        self.migrate()

    def migrate(self) -> None:
        with self._lock, self.connection:
            self.connection.executescript(DDL)
            self.connection.execute(
                "INSERT OR REPLACE INTO metadata(key,value) VALUES('schema_version',?)",
                (SCHEMA_VERSION,),
            )

    def close(self) -> None:
        self.connection.close()

    def add_evidence(
        self,
        evidence_id: str,
        source_system: str,
        source_locator: str,
        payload: dict[str, Any],
        occurred_at: str,
        recorded_at: str | None = None,
        classification: str = "SYNTHETIC_SENSITIVE",
    ) -> str:
        recorded_at = recorded_at or utc_now()
        with self._lock, self.connection:
            self.connection.execute(
                "INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?)",
                (evidence_id, source_system, source_locator, canonical_json(payload), digest_json(payload), occurred_at, recorded_at, classification),
            )
        return evidence_id

    def add_assertion(
        self,
        assertion_id: str,
        subject_id: str,
        attribute: str,
        value: Any,
        source_system: str,
        occurred_at: str,
        recorded_at: str,
        evidence_id: str,
    ) -> None:
        with self._lock, self.connection:
            self.connection.execute(
                "INSERT INTO assertions VALUES(?,?,?,?,?,?,?,?)",
                (assertion_id, subject_id, attribute, canonical_json(value), source_system, occurred_at, recorded_at, evidence_id),
            )

    def assertions_known_at(self, subject_id: str, cutoff: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM assertions WHERE subject_id=? AND recorded_at<=? ORDER BY occurred_at,recorded_at,assertion_id",
            (subject_id, cutoff),
        ).fetchall()
        return [dict(row) | {"value": json.loads(row["value_json"])} for row in rows]

    def append_event(
        self,
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        source_system: str,
        evidence_refs: list[str],
        actor: str,
        payload: dict[str, Any],
        correlation_id: str,
        authority: str | None = None,
        policy_versions: list[str] | None = None,
        data_quality: str = "VALID",
        classification: str = "SYNTHETIC_SENSITIVE",
        occurred_at: str | None = None,
    ) -> str:
        if not evidence_refs:
            raise ValueError("EVENT_REQUIRES_EVIDENCE")
        event_id = f"EVT-{uuid.uuid4()}"
        now = utc_now()
        with self._lock, self.connection:
            row = self.connection.execute(
                "SELECT COALESCE(MAX(sequence),0)+1 AS next FROM events WHERE aggregate_type=? AND aggregate_id=?",
                (aggregate_type, aggregate_id),
            ).fetchone()
            sequence = int(row["next"])
            self.connection.execute(
                "INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    event_id, event_type, aggregate_type, aggregate_id, sequence, occurred_at or now,
                    now, source_system, canonical_json(evidence_refs), correlation_id, actor, authority,
                    canonical_json(policy_versions or []), data_quality, canonical_json(payload),
                    digest_json(payload), classification, correlation_id,
                ),
            )
        return event_id

    def events_for(self, aggregate_type: str, aggregate_id: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM events WHERE aggregate_type=? AND aggregate_id=? ORDER BY sequence",
            (aggregate_type, aggregate_id),
        ).fetchall()
        return [dict(row) for row in rows]

    def audit(
        self,
        principal: Principal | str | None,
        action: str,
        scope: str,
        outcome: str,
        details: dict[str, Any],
        correlation_id: str,
    ) -> int:
        subject = principal.subject if isinstance(principal, Principal) else (principal or "ANONYMOUS")
        now = utc_now()
        with self._lock, self.connection:
            previous = self.connection.execute("SELECT record_hash FROM audit ORDER BY audit_id DESC LIMIT 1").fetchone()
            previous_hash = previous["record_hash"] if previous else "GENESIS"
            record = {
                "recorded_at": now,
                "principal": subject,
                "action": action,
                "scope": scope,
                "outcome": outcome,
                "details": details,
                "correlation_id": correlation_id,
                "previous_hash": previous_hash,
            }
            record_hash = hashlib.sha256(canonical_json(record).encode("utf-8")).hexdigest()
            cursor = self.connection.execute(
                "INSERT INTO audit(recorded_at,principal,action,scope,outcome,details_json,correlation_id,previous_hash,record_hash) VALUES(?,?,?,?,?,?,?,?,?)",
                (now, subject, action, scope, outcome, canonical_json(details), correlation_id, previous_hash, record_hash),
            )
            return int(cursor.lastrowid)

    def verify_audit_chain(self) -> bool:
        previous_hash = "GENESIS"
        for row in self.connection.execute("SELECT * FROM audit ORDER BY audit_id"):
            record = {
                "recorded_at": row["recorded_at"],
                "principal": row["principal"],
                "action": row["action"],
                "scope": row["scope"],
                "outcome": row["outcome"],
                "details": json.loads(row["details_json"]),
                "correlation_id": row["correlation_id"],
                "previous_hash": row["previous_hash"],
            }
            calculated = hashlib.sha256(canonical_json(record).encode("utf-8")).hexdigest()
            if row["previous_hash"] != previous_hash or row["record_hash"] != calculated:
                return False
            previous_hash = row["record_hash"]
        return True

    def metric(self, name: str, value: float = 1.0) -> None:
        with self._lock, self.connection:
            self.connection.execute(
                """INSERT INTO metrics(name,count,total,last_value,updated_at) VALUES(?,1,?,?,?)
                   ON CONFLICT(name) DO UPDATE SET count=count+1,total=total+excluded.last_value,last_value=excluded.last_value,updated_at=excluded.updated_at""",
                (name, value, value, utc_now()),
            )

    def metrics(self) -> dict[str, dict[str, float]]:
        return {
            row["name"]: {"count": row["count"], "total": row["total"], "last": row["last_value"]}
            for row in self.connection.execute("SELECT * FROM metrics ORDER BY name")
        }

    def state_digest(self) -> str:
        tables = ["evidence", "assertions", "events", "cases", "identity_proposals", "identity_links", "commands", "external_reservations", "quality_evidence", "recommendations", "metrics"]
        state: dict[str, list[dict[str, Any]]] = {}
        for table in tables:
            rows = self.connection.execute(f"SELECT * FROM {table} ORDER BY rowid").fetchall()
            state[table] = [dict(row) for row in rows]
        return digest_json(state)

    def backup(self, destination: str | Path) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        target = sqlite3.connect(destination)
        try:
            with target:
                self.connection.backup(target)
        finally:
            target.close()
        return destination

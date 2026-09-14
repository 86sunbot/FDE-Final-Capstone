from __future__ import annotations

import json
import uuid

from ..adapters.slot_simulator import SlotSimulator
from ..model import CommandState, Principal, canonical_json, digest_json, utc_now
from ..storage import Database
from .common import authorize, correlation


class CommandService:
    def __init__(self, db: Database, adapter: SlotSimulator | None = None) -> None:
        self.db = db
        self.adapter = adapter or SlotSimulator()

    def reserve_slot(
        self,
        principal: Principal,
        idempotency_key: str,
        patient_key: str,
        slot_id: str,
        behavior: str = "success",
        correlation_id: str | None = None,
    ) -> dict:
        trace = correlation(correlation_id)
        authorize(self.db, principal, "slot:command", patient_key, trace)
        payload = {"patient_key": patient_key, "slot_id": slot_id}
        payload_digest = digest_json({"command_type": "ReserveSlot", "scope": patient_key, "payload": payload})

        with self.db._lock:
            existing = self.db.connection.execute("SELECT * FROM commands WHERE idempotency_key=?", (idempotency_key,)).fetchone()
            if existing:
                if existing["payload_digest"] != payload_digest:
                    self.db.audit(principal, "slot:command", patient_key, "DENIED", {"reason": "IDEMPOTENCY_CONFLICT", "command_id": existing["command_id"]}, trace)
                    self.db.metric("idempotency_conflicts")
                    return {"decision": "IDEMPOTENCY_CONFLICT", "state": existing["state"], "dispatch": False}
                self.db.metric("command_replays")
                return self._command_result(existing) | {"decision": "REPLAY_STORED", "dispatch": False}

            command_id = f"CMD-{uuid.uuid4()}"
            now = utc_now()
            with self.db.connection:
                self.db.connection.execute(
                    "INSERT INTO commands VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (command_id, idempotency_key, "ReserveSlot", patient_key, canonical_json(payload), payload_digest, principal.subject, CommandState.DISPATCH_PENDING.value, None, trace, now, now),
                )

            result = self.adapter.reserve(command_id, patient_key, slot_id, behavior)
            state = CommandState.SUCCEEDED
            result_payload = {"adapter_kind": result.kind, "reservation_id": result.reservation_id, "detail": result.detail}
            with self.db.connection:
                if result.kind in {"SUCCESS", "TIMEOUT_AFTER_SUCCESS", "PARTIAL"}:
                    self.db.connection.execute(
                        "INSERT INTO external_reservations VALUES(?,?,?,?,?,?)",
                        (result.reservation_id, command_id, patient_key, slot_id, "RESERVED" if result.kind != "PARTIAL" else "PARTIAL", utc_now()),
                    )
                if result.kind == "TIMEOUT_AFTER_SUCCESS":
                    state = CommandState.OUTCOME_UNKNOWN
                elif result.kind == "PARTIAL":
                    state = CommandState.COMPENSATION_PENDING
                elif result.kind == "FAILURE":
                    state = CommandState.FAILED_RETRYABLE
                self.db.connection.execute(
                    "UPDATE commands SET state=?,result_json=?,updated_at=? WHERE command_id=?",
                    (state.value, canonical_json(result_payload), utc_now(), command_id),
                )
            self.db.audit(principal, "slot:command", patient_key, "ALLOWED", {"command_id": command_id, "state": state.value}, trace)
            self.db.metric("commands_accepted")
            if state == CommandState.OUTCOME_UNKNOWN:
                self.db.metric("unknown_outcomes")
            return {"decision": "ACCEPTED", "command_id": command_id, "state": state.value, "result": result_payload, "dispatch": True}

    def reconcile(self, principal: Principal, command_id: str, correlation_id: str | None = None) -> dict:
        trace = correlation(correlation_id)
        row = self.db.connection.execute("SELECT * FROM commands WHERE command_id=?", (command_id,)).fetchone()
        if not row:
            raise KeyError(command_id)
        authorize(self.db, principal, "slot:reconcile", row["scope"], trace)
        if row["state"] != CommandState.OUTCOME_UNKNOWN.value:
            raise ValueError("COMMAND_NOT_RECONCILABLE")
        reservation = self.db.connection.execute("SELECT * FROM external_reservations WHERE command_id=?", (command_id,)).fetchone()
        state = CommandState.SUCCEEDED if reservation and reservation["state"] == "RESERVED" else CommandState.FAILED_RETRYABLE
        result = {"reconciled": True, "effect_found": bool(reservation), "reservation_id": reservation["reservation_id"] if reservation else None}
        with self.db.connection:
            self.db.connection.execute("UPDATE commands SET state=?,result_json=?,updated_at=? WHERE command_id=?", (state.value, canonical_json(result), utc_now(), command_id))
        self.db.audit(principal, "slot:reconcile", row["scope"], "ALLOWED", {"command_id": command_id, "state": state.value}, trace)
        self.db.metric("commands_reconciled")
        return {"command_id": command_id, "state": state.value, "result": result}

    def compensate(self, principal: Principal, command_id: str, correlation_id: str | None = None) -> dict:
        trace = correlation(correlation_id)
        row = self.db.connection.execute("SELECT * FROM commands WHERE command_id=?", (command_id,)).fetchone()
        if not row:
            raise KeyError(command_id)
        authorize(self.db, principal, "slot:reconcile", row["scope"], trace)
        if row["state"] != CommandState.COMPENSATION_PENDING.value:
            raise ValueError("COMMAND_NOT_COMPENSATABLE")
        with self.db.connection:
            self.db.connection.execute("UPDATE external_reservations SET state='CANCELLED' WHERE command_id=?", (command_id,))
            self.db.connection.execute("UPDATE commands SET state=?,updated_at=? WHERE command_id=?", (CommandState.COMPENSATED.value, utc_now(), command_id))
        self.db.audit(principal, "slot:reconcile", row["scope"], "ALLOWED", {"command_id": command_id, "state": CommandState.COMPENSATED.value}, trace)
        self.db.metric("commands_compensated")
        return {"command_id": command_id, "state": CommandState.COMPENSATED.value}

    def get(self, command_id: str) -> dict:
        row = self.db.connection.execute("SELECT * FROM commands WHERE command_id=?", (command_id,)).fetchone()
        if not row:
            raise KeyError(command_id)
        return self._command_result(row)

    @staticmethod
    def _command_result(row) -> dict:
        return {"command_id": row["command_id"], "state": row["state"], "result": json.loads(row["result_json"]) if row["result_json"] else None}

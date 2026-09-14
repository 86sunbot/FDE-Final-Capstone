from __future__ import annotations

import os

try:
    from fastapi import FastAPI, Header, HTTPException
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("Install the api extra to run FastAPI") from exc

from .application import CapstoneApplication
from .model import Outcome, Principal
from .security import AuthorizationError


def create_app(database_path: str | None = None) -> FastAPI:
    service = CapstoneApplication(database_path or os.getenv("FDE_DB", "runtime/api.db"), ai_mode=os.getenv("AI_MODE", "off"))
    app = FastAPI(title="FDE Final Capstone", version="1.0.0")
    app.state.service = service

    def demo_principal(x_principal: str | None, x_role: str | None, x_scope: str | None) -> Principal:
        if not x_principal or not x_role:
            raise HTTPException(401, "demo principal and role required")
        return Principal(x_principal, frozenset({x_role}), frozenset({x_scope or "*"}))

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "scope": "synthetic-local-academic", "ai_mode": service.ai_mode, "audit_valid": service.db.verify_audit_chain()}

    @app.get("/quality/{batch_id}/packet")
    def quality_packet(batch_id: str) -> dict:
        return service.quality.packet(batch_id)

    @app.get("/commands/{command_id}")
    def command(command_id: str) -> dict:
        try:
            return service.commands.get(command_id)
        except KeyError:
            raise HTTPException(404, "command not found")

    @app.post("/slots/reservations")
    def reserve_slot(payload: dict, x_principal: str | None = Header(None), x_role: str | None = Header(None), x_scope: str | None = Header(None)) -> dict:
        principal = demo_principal(x_principal, x_role, x_scope)
        try:
            return service.commands.reserve_slot(principal, payload["idempotency_key"], payload["patient_key"], payload["slot_id"], payload.get("behavior", "success"))
        except AuthorizationError as exc:
            raise HTTPException(403, str(exc))

    return app


app = create_app(os.getenv("FDE_DB", ":memory:"))

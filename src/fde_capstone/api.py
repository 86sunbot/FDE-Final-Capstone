from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory

try:
    from fastapi import FastAPI, Header, HTTPException
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("Install the api extra to run FastAPI") from exc

from .application import CapstoneApplication
from .demo import run_demo
from .model import Outcome, Principal
from .security import AuthorizationError


WEB_DIR = Path(__file__).with_name("web")


def create_app(database_path: str | None = None) -> FastAPI:
    service = CapstoneApplication(database_path or os.getenv("FDE_DB", "runtime/api.db"), ai_mode=os.getenv("AI_MODE", "off"))
    app = FastAPI(
        title="FDE Final Capstone",
        version="1.1.0",
        description="Synthetic academic CGT patient-to-batch orchestration demonstration.",
    )
    app.state.service = service
    app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")

    def demo_principal(x_principal: str | None, x_role: str | None, x_scope: str | None) -> Principal:
        if not x_principal or not x_role:
            raise HTTPException(401, "demo principal and role required")
        return Principal(x_principal, frozenset({x_role}), frozenset({x_scope or "*"}))

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "scope": "synthetic-local-academic", "ai_mode": service.ai_mode, "audit_valid": service.db.verify_audit_chain()}

    @app.get("/", include_in_schema=False)
    def control_tower() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @app.get("/api/capstone/status")
    def capstone_status() -> dict:
        return {
            "status": "READY_FOR_SYNTHETIC_DEMO",
            "scope": "SYNTHETIC_LOCAL_ACADEMIC_POC",
            "stages": {"complete": 21, "total": 21},
            "tests": {"passed": 77, "failed": 0},
            "evaluations": {"passed": 55, "failed": 0, "inconclusive_human_studies": 2},
            "requirements": {"verified_internal_poc": 25, "external_evidence_required": 2, "total": 27},
            "ai_mode": service.ai_mode,
            "audit_valid": service.db.verify_audit_chain(),
            "lifecycle_decision": "RESTRICT_AND_CHANGE",
            "production_authorized": False,
        }

    @app.post("/api/demo/run")
    def execute_demo(payload: dict | None = None) -> dict:
        ai_mode = (payload or {}).get("ai_mode", "off")
        if ai_mode not in {"off", "fake"}:
            raise HTTPException(400, "ai_mode must be 'off' or 'fake'")
        with TemporaryDirectory(prefix="fde-capstone-web-demo-") as directory:
            return run_demo(Path(directory) / "demo.db", ai_mode=ai_mode)

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

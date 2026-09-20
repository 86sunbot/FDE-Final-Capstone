from __future__ import annotations

import os
import json
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
from .disruption_preview import list_injects, preview_inject
from .model import Outcome, Principal
from .security import AuthorizationError
from .source_cases import list_eval_cases, load_eval_case, reconstruct_source_journey


WEB_DIR = Path(__file__).with_name("web")
ROOT = Path(__file__).resolve().parents[2]


def _evidence_summary(path: str) -> dict:
    payload = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return payload.get("summary", payload)


def create_app(database_path: str | None = None) -> FastAPI:
    service = CapstoneApplication(database_path or os.getenv("FDE_DB", "runtime/api.db"), ai_mode=os.getenv("AI_MODE", "off"))
    app = FastAPI(
        title="FDE Final Capstone",
        version="1.3.0",
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
        tests = _evidence_summary("docs/stages/stage_15/test_summary.json")
        evaluation = _evidence_summary("docs/stages/stage_15/evaluation_results.json")
        requirements = _evidence_summary("requirements/verification_matrix.json")
        return {
            "status": "READY_FOR_SYNTHETIC_DEMO",
            "scope": "SYNTHETIC_LOCAL_ACADEMIC_POC",
            "stages": {"documented": 21, "total": 21, "externally_approved": False},
            "tests": {"passed": tests["passed"], "failed": tests["failures"] + tests["errors"], "scope": "LOCAL_AUTOMATED"},
            "evaluations": {"structural_passes": evaluation["pass"], "failed": evaluation["fail"], "inconclusive_human_studies": evaluation["inconclusive"], "property_coverage": evaluation["property_coverage"]},
            "requirements": {"verified_internal_poc": requirements["verified_internal_poc"], "external_evidence_required": requirements["inconclusive_external_evidence_required"], "total": requirements["total"], "production_verified": requirements["production_verified"]},
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

    @app.get("/api/source/cases")
    def source_case_list() -> dict:
        try:
            cases = list_eval_cases()
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc
        return {"scope": "FROZEN_V2_SOURCE_READ_ONLY_SYNTHETIC", "cases": cases}

    @app.get("/api/source/cases/{case_id}")
    def source_case_detail(case_id: str) -> dict:
        try:
            detail = load_eval_case(case_id)
            detail["timestamp_order_reconstruction"] = reconstruct_source_journey(case_id)
            return detail
        except KeyError as exc:
            raise HTTPException(404, "source case not found") from exc
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc

    @app.get("/api/source/injects")
    def source_inject_list() -> dict:
        try:
            injects = list_injects()
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc
        return {"scope": "FROZEN_V2_SOURCE_SCENARIO_PREVIEW_NOT_EXECUTED", "injects": injects}

    @app.get("/api/source/injects/{inject_id}/preview")
    def source_inject_preview(inject_id: str, patient_key: str = "P-00001") -> dict:
        try:
            return preview_inject(inject_id, patient_key)
        except KeyError as exc:
            raise HTTPException(404, "inject or representative patient not found") from exc
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc

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

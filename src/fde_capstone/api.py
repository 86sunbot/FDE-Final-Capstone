from __future__ import annotations

import json
import os
import secrets
from collections.abc import Mapping
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Any, Literal

try:
    from fastapi import FastAPI, Header, HTTPException
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel, ConfigDict, Field
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("Install the api extra to run FastAPI") from exc

from .application import CapstoneApplication
from .demo import run_demo
from .disruption_preview import list_injects, preview_inject
from .model import Principal
from .security import AuthorizationError
from .source_cases import list_eval_cases, load_eval_case, reconstruct_source_journey

WEB_DIR = Path(__file__).with_name("web")
ROOT = Path(__file__).resolve().parents[2]


class DemoRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ai_mode: Literal["off", "fake"] = "off"


class SlotReservationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    idempotency_key: str = Field(min_length=1, max_length=200)
    patient_key: str = Field(min_length=1, max_length=200)
    slot_id: str = Field(min_length=1, max_length=200)
    behavior: Literal["success", "timeout_after_success", "partial", "failure"] = "success"


def _evidence_summary(path: str) -> dict[str, Any]:
    payload = json.loads((ROOT / path).read_text(encoding="utf-8"))
    summary = payload.get("summary", payload)
    if not isinstance(summary, dict):
        raise ValueError(f"Expected object summary in {path}")
    return summary


def _identities_from_environment() -> dict[str, Principal]:
    """Load opaque bearer tokens mapped to server-side demo identities."""
    raw = os.getenv("FDE_DEMO_IDENTITIES_JSON", "")
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("FDE_DEMO_IDENTITIES_JSON must be valid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("FDE_DEMO_IDENTITIES_JSON must be a token-to-identity object")
    identities: dict[str, Principal] = {}
    for token, claims in payload.items():
        if not isinstance(token, str) or not token or not isinstance(claims, dict):
            raise RuntimeError("Each demo identity requires a non-empty token and claim object")
        subject = claims.get("subject")
        roles = claims.get("roles")
        scopes = claims.get("scopes", ["*"])
        if not isinstance(subject, str) or not isinstance(roles, list) or not all(isinstance(x, str) for x in roles):
            raise RuntimeError("Each demo identity requires subject and string roles")
        if not isinstance(scopes, list) or not all(isinstance(x, str) for x in scopes):
            raise RuntimeError("Demo identity scopes must be a list of strings")
        identities[token] = Principal(subject, frozenset(roles), frozenset(scopes))
    return identities


def create_app(
    database_path: str | Path | None = None,
    demo_identities: Mapping[str, Principal] | None = None,
) -> FastAPI:
    resolved_database: str | Path = (
        database_path if database_path is not None else os.environ.get("FDE_DB", "runtime/api.db")
    )
    ai_mode = os.getenv("AI_MODE", "off")
    identities = dict(demo_identities) if demo_identities is not None else _identities_from_environment()

    def get_service() -> CapstoneApplication:
        service = getattr(app.state, "service", None)
        if service is None:
            service = CapstoneApplication(resolved_database, ai_mode=ai_mode)
            app.state.service = service
        return service

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        get_service()
        try:
            yield
        finally:
            service = getattr(app.state, "service", None)
            if service is not None:
                service.close()
                app.state.service = None

    app = FastAPI(
        title="FDE Final Capstone",
        version="1.2.0",
        description="Synthetic academic CGT patient-to-batch orchestration demonstration.",
        lifespan=lifespan,
    )
    app.state.service = None
    app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")

    def demo_principal(authorization: str | None) -> Principal:
        if not identities:
            raise HTTPException(503, "mutating demo API identities are not configured")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(401, "bearer token required")
        supplied = authorization.removeprefix("Bearer ").strip()
        matched = next((principal for token, principal in identities.items() if secrets.compare_digest(token, supplied)), None)
        if matched is None:
            raise HTTPException(401, "invalid bearer token")
        return matched

    @app.get("/health")
    def health() -> dict[str, Any]:
        service = get_service()
        return {
            "status": "ok",
            "scope": "synthetic-local-academic",
            "ai_mode": service.ai_mode,
            "audit_valid": service.db.verify_audit_chain(),
        }

    @app.get("/", include_in_schema=False)
    def control_tower() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @app.get("/api/capstone/status")
    def capstone_status() -> dict[str, Any]:
        service = get_service()
        tests = _evidence_summary("docs/stages/stage_15/test_summary.json")
        evaluation = _evidence_summary("docs/stages/stage_15/evaluation_results.json")
        requirements = _evidence_summary("requirements/verification_matrix.json")
        return {
            "status": "READY_FOR_SYNTHETIC_DEMO",
            "scope": "SYNTHETIC_LOCAL_ACADEMIC_POC",
            "stages": {"documented": 21, "total": 21, "externally_approved": False},
            "tests": {
                "passed": tests["passed"],
                "failed": tests["failures"] + tests["errors"],
                "scope": "LOCAL_AUTOMATED",
            },
            "evaluations": {
                "structural_passes": evaluation["pass"],
                "failed": evaluation["fail"],
                "inconclusive_human_studies": evaluation["inconclusive"],
                "property_coverage": evaluation["property_coverage"],
            },
            "requirements": {
                "verified_internal_poc": requirements["verified_internal_poc"],
                "external_evidence_required": requirements["inconclusive_external_evidence_required"],
                "total": requirements["total"],
                "production_verified": requirements["production_verified"],
            },
            "ai_mode": service.ai_mode,
            "audit_valid": service.db.verify_audit_chain(),
            "lifecycle_decision": "RESTRICT_AND_CHANGE",
            "production_authorized": False,
        }

    @app.post("/api/demo/run")
    def execute_demo(payload: DemoRunRequest | None = None) -> dict[str, Any]:
        requested = payload or DemoRunRequest()
        with TemporaryDirectory(prefix="fde-capstone-web-demo-") as directory:
            return run_demo(Path(directory) / "demo.db", ai_mode=requested.ai_mode)

    @app.get("/api/source/cases")
    def source_case_list() -> dict[str, Any]:
        try:
            cases = list_eval_cases()
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc
        return {"scope": "FROZEN_V2_SOURCE_READ_ONLY_SYNTHETIC", "cases": cases}

    @app.get("/api/source/cases/{case_id}")
    def source_case_detail(case_id: str) -> dict[str, Any]:
        try:
            detail = load_eval_case(case_id)
            detail["timestamp_order_reconstruction"] = reconstruct_source_journey(case_id)
            return detail
        except KeyError as exc:
            raise HTTPException(404, "source case not found") from exc
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc

    @app.get("/api/source/injects")
    def source_inject_list() -> dict[str, Any]:
        try:
            injects = list_injects()
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc
        return {"scope": "FROZEN_V2_SOURCE_SCENARIO_PREVIEW_NOT_EXECUTED", "injects": injects}

    @app.get("/api/source/injects/{inject_id}/preview")
    def source_inject_preview(inject_id: str, patient_key: str = "P-00001") -> dict[str, Any]:
        try:
            return preview_inject(inject_id, patient_key)
        except KeyError as exc:
            raise HTTPException(404, "inject or representative patient not found") from exc
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc

    @app.get("/quality/{batch_id}/packet")
    def quality_packet(batch_id: str) -> dict[str, Any]:
        return get_service().quality.packet(batch_id)

    @app.get("/commands/{command_id}")
    def command(command_id: str) -> dict[str, Any]:
        try:
            return get_service().commands.get(command_id)
        except KeyError as exc:
            raise HTTPException(404, "command not found") from exc

    @app.post("/slots/reservations")
    def reserve_slot(
        payload: SlotReservationRequest,
        authorization: Annotated[str | None, Header()] = None,
    ) -> dict[str, Any]:
        principal = demo_principal(authorization)
        try:
            return get_service().commands.reserve_slot(
                principal,
                payload.idempotency_key,
                payload.patient_key,
                payload.slot_id,
                payload.behavior,
            )
        except AuthorizationError as exc:
            raise HTTPException(403, str(exc)) from exc

    return app


# ASGI import target. Database creation is deferred to application lifespan,
# so importing this module does not leak an in-memory SQLite connection.
app = create_app()

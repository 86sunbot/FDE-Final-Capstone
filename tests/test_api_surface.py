import json

import pytest
from fastapi.testclient import TestClient

from fde_capstone.model import Principal


def test_api_exposes_health_and_bounded_poc_routes(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(tmp_path / "api.db")
    with TestClient(app):
        paths = {route.path for route in app.routes}
        assert "/" in paths
        assert "/health" in paths
        assert "/api/capstone/status" in paths
        assert "/api/demo/run" in paths
        assert "/api/source/cases" in paths
        assert "/api/source/cases/{case_id}" in paths
        assert "/api/source/injects" in paths
        assert "/api/source/injects/{inject_id}/preview" in paths
        assert "/quality/{batch_id}/packet" in paths
        assert "/slots/reservations" in paths
        assert not any("agent" in path or "release/auto" in path for path in paths)
    assert app.state.service is None


def test_control_tower_status_is_honest_about_scope(tmp_path):
    from fde_capstone.api import ROOT, create_app

    with TestClient(create_app(tmp_path / "status.db")) as client:
        result = client.get("/api/capstone/status").json()
    assert result["stages"] == {"documented": 21, "total": 21, "externally_approved": False}
    assert result["tests"]["passed"] == json.loads(
        (ROOT / "docs/stages/stage_15/test_summary.json").read_text()
    )["passed"]
    assert result["evaluations"]["property_coverage"]["FULL_SCOPED_PROPERTY_ASSERTIONS"] == 7
    assert result["requirements"]["total"] == 31
    assert result["production_authorized"] is False
    assert result["lifecycle_decision"] == "RESTRICT_AND_CHANGE"


def test_control_tower_executes_all_three_pocs(tmp_path):
    from fde_capstone.api import create_app

    with TestClient(create_app(tmp_path / "demo-route.db")) as client:
        response = client.post("/api/demo/run", json={"ai_mode": "off"})
    assert response.status_code == 200
    result = response.json()
    assert result["poc1"]["readiness"] == "SATISFIED"
    assert result["poc2"]["initial_state"] == "OUTCOME_UNKNOWN"
    assert result["poc2"]["reconciled_state"] == "SUCCEEDED"
    assert result["poc3"]["released"] is True
    assert result["journey_summary"]["overall_status"] == "READY_FOR_NEXT_AUTHORIZED_STEP"
    assert result["journey_summary"]["current_blocker"] == "NONE"
    assert result["journey_summary"]["evidence_count"] == 10
    assert len(result["journey_summary"]["domains"]) == 5
    assert len(result["role_views"]) == 7
    assert {role["backend_role"] for role in result["role_views"]} >= {
        "COORDINATOR",
        "IDENTITY_AUTHORITY",
        "PLANNER",
        "QUALITY_AUTHORITY",
        "VIEWER",
    }
    assert len(result["automation_trace"]) == 5
    assert "deterministic projections" in result["information_architecture"]["structured_retrieval"]
    assert "Optional future RAG" in result["information_architecture"]["rag"]
    assert "Not implemented" in result["information_architecture"]["mcp"]
    assert result["audit_chain_valid"] is True


def test_control_tower_page_is_packaged(tmp_path):
    from fde_capstone.api import WEB_DIR, create_app

    assert (WEB_DIR / "index.html").is_file()
    assert (WEB_DIR / "styles.css").is_file()
    assert (WEB_DIR / "app.js").is_file()
    assert (WEB_DIR / "favicon.svg").is_file()
    with TestClient(create_app(tmp_path / "page.db")) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "FDE" in response.text


def test_read_only_v2_source_routes_are_explicitly_non_authoritative(tmp_path):
    from fde_capstone.api import create_app

    with TestClient(create_app(tmp_path / "source.db")) as client:
        case = client.get("/api/source/cases/EVAL-002").json()
        preview = client.get("/api/source/injects/INJ-008/preview", params={"patient_key": "P-00001"}).json()
    assert case["observations"][0]["status"] == "OBSERVED_CONFLICT"
    assert case["disposition"] == "NONE_SOURCE_ASSERTIONS_ONLY"
    assert case["timestamp_order_reconstruction"]["control_gates"]["identity"] == (
        "CONFLICT_REQUIRES_AUTHORIZED_REVIEW"
    )
    assert preview["side_effects"] == 0
    assert preview["affected_routes"]


def test_pydantic_rejects_unapproved_ai_mode_and_missing_reservation_fields(tmp_path):
    from fde_capstone.api import create_app

    with TestClient(create_app(tmp_path / "validation.db")) as client:
        invalid_mode = client.post("/api/demo/run", json={"ai_mode": "live"})
        missing_fields = client.post("/slots/reservations", json={"patient_key": "P-1"})
    assert invalid_mode.status_code == 422
    assert missing_fields.status_code == 422


def test_mutating_route_uses_server_side_bearer_identity_not_role_headers(tmp_path):
    from fde_capstone.api import create_app

    planner = Principal("configured-planner", frozenset({"PLANNER"}), frozenset({"*"}))
    app = create_app(tmp_path / "auth.db", demo_identities={"opaque-test-token": planner})
    payload = {"idempotency_key": "IDEMP-1", "patient_key": "P-1", "slot_id": "S-1"}
    with TestClient(app) as client:
        unsigned = client.post(
            "/slots/reservations",
            json=payload,
            headers={"x-principal": "attacker", "x-role": "QUALITY_AUTHORITY"},
        )
        invalid = client.post(
            "/slots/reservations",
            json=payload,
            headers={"authorization": "Bearer wrong-token"},
        )
        valid = client.post(
            "/slots/reservations",
            json=payload,
            headers={"authorization": "Bearer opaque-test-token"},
        )
    assert unsigned.status_code == 401
    assert invalid.status_code == 401
    assert valid.status_code == 200
    assert valid.json()["state"] == "SUCCEEDED"


def test_mutating_route_fails_closed_when_no_demo_identity_is_configured(tmp_path):
    from fde_capstone.api import create_app

    with TestClient(create_app(tmp_path / "closed.db", demo_identities={})) as client:
        response = client.post(
            "/slots/reservations",
            json={"idempotency_key": "I", "patient_key": "P", "slot_id": "S"},
            headers={"authorization": "Bearer anything"},
        )
    assert response.status_code == 503


def test_demo_identity_configuration_is_loaded_from_environment(monkeypatch):
    from fde_capstone.api import _identities_from_environment

    monkeypatch.setenv(
        "FDE_DEMO_IDENTITIES_JSON",
        json.dumps(
            {
                "opaque-token": {
                    "subject": "demo-planner",
                    "roles": ["PLANNER"],
                    "scopes": ["site:alpha"],
                }
            }
        ),
    )
    identities = _identities_from_environment()
    assert identities["opaque-token"] == Principal(
        "demo-planner",
        frozenset({"PLANNER"}),
        frozenset({"site:alpha"}),
    )


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ("not-json", "valid JSON"),
        ("[]", "token-to-identity object"),
        ('{"": {}}', "non-empty token"),
        ('{"token": {"subject": 7, "roles": ["PLANNER"]}}', "subject and string roles"),
        ('{"token": {"subject": "planner", "roles": ["PLANNER"], "scopes": "*"}}', "list of strings"),
    ],
)
def test_demo_identity_configuration_rejects_malformed_claims(monkeypatch, raw, message):
    from fde_capstone.api import _identities_from_environment

    monkeypatch.setenv("FDE_DEMO_IDENTITIES_JSON", raw)
    with pytest.raises(RuntimeError, match=message):
        _identities_from_environment()


def test_api_translates_source_failures_to_bounded_http_errors(tmp_path, monkeypatch):
    import fde_capstone.api as api_module

    def missing_source(*_args, **_kwargs):
        raise FileNotFoundError("frozen source unavailable")

    def unknown_source(*_args, **_kwargs):
        raise KeyError("unknown")

    app = api_module.create_app(tmp_path / "errors.db")
    with TestClient(app) as client:
        monkeypatch.setattr(api_module, "list_eval_cases", missing_source)
        assert client.get("/api/source/cases").status_code == 503
        monkeypatch.setattr(api_module, "load_eval_case", unknown_source)
        assert client.get("/api/source/cases/UNKNOWN").status_code == 404
        monkeypatch.setattr(api_module, "list_injects", missing_source)
        assert client.get("/api/source/injects").status_code == 503
        monkeypatch.setattr(api_module, "preview_inject", unknown_source)
        assert client.get("/api/source/injects/UNKNOWN/preview").status_code == 404


def test_api_reports_missing_commands_and_forbidden_reservations(tmp_path):
    from fde_capstone.api import create_app

    viewer = Principal("configured-viewer", frozenset({"VIEWER"}), frozenset({"*"}))
    app = create_app(tmp_path / "bounded-errors.db", demo_identities={"viewer-token": viewer})
    with TestClient(app) as client:
        missing = client.get("/commands/UNKNOWN")
        forbidden = client.post(
            "/slots/reservations",
            json={"idempotency_key": "I", "patient_key": "P", "slot_id": "S"},
            headers={"authorization": "Bearer viewer-token"},
        )
        packet = client.get("/quality/UNKNOWN/packet")
    assert missing.status_code == 404
    assert forbidden.status_code == 403
    assert packet.status_code == 200
    assert packet.json()["batch_id"] == "UNKNOWN"

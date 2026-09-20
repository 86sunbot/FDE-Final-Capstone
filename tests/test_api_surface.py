import json

import pytest


def test_api_exposes_health_and_bounded_poc_routes(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "api.db"))
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
    app.state.service.close()


def test_control_tower_status_is_honest_about_scope(tmp_path):
    from fde_capstone.api import ROOT, create_app

    app = create_app(str(tmp_path / "status.db"))
    route = next(route for route in app.routes if route.path == "/api/capstone/status")
    result = route.endpoint()
    assert result["stages"] == {"documented": 21, "total": 21, "externally_approved": False}
    assert result["tests"]["passed"] == json.loads((ROOT / "docs/stages/stage_15/test_summary.json").read_text())["passed"]
    assert result["evaluations"]["property_coverage"]["FULL_SCOPED_PROPERTY_ASSERTIONS"] == 7
    assert result["requirements"]["total"] == 31
    assert result["production_authorized"] is False
    assert result["lifecycle_decision"] == "RESTRICT_AND_CHANGE"
    app.state.service.close()


def test_control_tower_executes_all_three_pocs(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "demo-route.db"))
    route = next(route for route in app.routes if route.path == "/api/demo/run")
    result = route.endpoint({"ai_mode": "off"})
    assert result["poc1"]["readiness"] == "SATISFIED"
    assert result["poc2"]["initial_state"] == "OUTCOME_UNKNOWN"
    assert result["poc2"]["reconciled_state"] == "SUCCEEDED"
    assert result["poc3"]["released"] is True
    assert result["journey_summary"]["overall_status"] == "READY_FOR_NEXT_AUTHORIZED_STEP"
    assert result["journey_summary"]["current_blocker"] == "NONE"
    assert result["journey_summary"]["evidence_count"] == 10
    assert len(result["journey_summary"]["domains"]) == 5
    assert len(result["role_views"]) == 7
    assert {role["backend_role"] for role in result["role_views"]} >= {"COORDINATOR", "IDENTITY_AUTHORITY", "PLANNER", "QUALITY_AUTHORITY", "VIEWER"}
    assert len(result["automation_trace"]) == 5
    assert "deterministic projections" in result["information_architecture"]["structured_retrieval"]
    assert "Optional future RAG" in result["information_architecture"]["rag"]
    assert "Not implemented" in result["information_architecture"]["mcp"]
    assert result["audit_chain_valid"] is True
    app.state.service.close()


def test_control_tower_page_is_packaged(tmp_path):
    from fde_capstone.api import WEB_DIR, create_app

    assert (WEB_DIR / "index.html").is_file()
    assert (WEB_DIR / "styles.css").is_file()
    assert (WEB_DIR / "app.js").is_file()
    assert (WEB_DIR / "favicon.svg").is_file()
    app = create_app(str(tmp_path / "page.db"))
    route = next(route for route in app.routes if route.path == "/")
    response = route.endpoint()
    assert str(response.path).endswith("index.html")
    app.state.service.close()


def test_read_only_v2_source_routes_are_explicitly_non_authoritative(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "source.db"))
    case_route = next(route for route in app.routes if route.path == "/api/source/cases/{case_id}")
    case = case_route.endpoint("EVAL-002")
    assert case["observations"][0]["status"] == "OBSERVED_CONFLICT"
    assert case["disposition"] == "NONE_SOURCE_ASSERTIONS_ONLY"
    assert case["timestamp_order_reconstruction"]["control_gates"]["identity"] == "CONFLICT_REQUIRES_AUTHORIZED_REVIEW"
    preview_route = next(route for route in app.routes if route.path == "/api/source/injects/{inject_id}/preview")
    preview = preview_route.endpoint("INJ-008", "P-00001")
    assert preview["side_effects"] == 0
    assert preview["affected_routes"]
    app.state.service.close()


def test_control_tower_rejects_unapproved_ai_mode(tmp_path):
    from fastapi import HTTPException

    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "invalid-mode.db"))
    route = next(route for route in app.routes if route.path == "/api/demo/run")
    with pytest.raises(HTTPException) as error:
        route.endpoint({"ai_mode": "live"})
    assert error.value.status_code == 400
    app.state.service.close()

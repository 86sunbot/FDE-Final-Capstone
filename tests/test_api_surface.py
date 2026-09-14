import pytest


def test_api_exposes_health_and_bounded_poc_routes(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "api.db"))
    paths = {route.path for route in app.routes}
    assert "/" in paths
    assert "/health" in paths
    assert "/api/capstone/status" in paths
    assert "/api/demo/run" in paths
    assert "/quality/{batch_id}/packet" in paths
    assert "/slots/reservations" in paths
    assert not any("agent" in path or "release/auto" in path for path in paths)
    app.state.service.close()


def test_control_tower_status_is_honest_about_scope(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "status.db"))
    route = next(route for route in app.routes if route.path == "/api/capstone/status")
    result = route.endpoint()
    assert result["stages"] == {"complete": 21, "total": 21}
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


def test_control_tower_rejects_unapproved_ai_mode(tmp_path):
    from fastapi import HTTPException

    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "invalid-mode.db"))
    route = next(route for route in app.routes if route.path == "/api/demo/run")
    with pytest.raises(HTTPException) as error:
        route.endpoint({"ai_mode": "live"})
    assert error.value.status_code == 400
    app.state.service.close()

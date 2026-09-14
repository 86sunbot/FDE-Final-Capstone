def test_api_exposes_health_and_bounded_poc_routes(tmp_path):
    from fde_capstone.api import create_app

    app = create_app(str(tmp_path / "api.db"))
    paths = {route.path for route in app.routes}
    assert "/health" in paths
    assert "/quality/{batch_id}/packet" in paths
    assert "/slots/reservations" in paths
    assert not any("agent" in path or "release/auto" in path for path in paths)
    app.state.service.close()

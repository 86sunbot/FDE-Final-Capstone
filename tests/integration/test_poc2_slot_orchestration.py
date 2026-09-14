from concurrent.futures import ThreadPoolExecutor


def test_same_command_replays_without_duplicate_effect(app, principals):
    first = app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-1")
    replay = app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-1")
    count = app.db.connection.execute("SELECT COUNT(*) AS n FROM external_reservations").fetchone()["n"]
    assert first["dispatch"] is True
    assert replay["dispatch"] is False
    assert count == 1


def test_changed_payload_with_same_key_conflicts_without_effect(app, principals):
    app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-1")
    conflict = app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-2")
    assert conflict["decision"] == "IDEMPOTENCY_CONFLICT"
    assert conflict["dispatch"] is False
    assert app.db.connection.execute("SELECT COUNT(*) FROM external_reservations").fetchone()[0] == 1


def test_timeout_after_success_requires_reconciliation_and_never_redispatches(app, principals):
    first = app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-1", "timeout_after_success")
    replay_before = app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-1")
    assert first["state"] == "OUTCOME_UNKNOWN"
    assert replay_before["dispatch"] is False
    reconciled = app.commands.reconcile(principals["planner"], first["command_id"])
    assert reconciled["state"] == "SUCCEEDED"
    assert app.db.connection.execute("SELECT COUNT(*) FROM external_reservations").fetchone()[0] == 1


def test_partial_effect_is_compensated_explicitly(app, principals):
    first = app.commands.reserve_slot(principals["planner"], "KEY-1", "P-1", "S-1", "partial")
    assert first["state"] == "COMPENSATION_PENDING"
    final = app.commands.compensate(principals["planner"], first["command_id"])
    reservation = app.db.connection.execute("SELECT state FROM external_reservations WHERE command_id=?", (first["command_id"],)).fetchone()
    assert final["state"] == "COMPENSATED"
    assert reservation["state"] == "CANCELLED"


def test_concurrent_identical_requests_have_one_external_effect(app, principals):
    def reserve(_):
        return app.commands.reserve_slot(principals["planner"], "KEY-CONCURRENT", "P-1", "S-1")
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(reserve, range(16)))
    assert sum(1 for item in results if item["dispatch"]) == 1
    assert app.db.connection.execute("SELECT COUNT(*) FROM external_reservations").fetchone()[0] == 1

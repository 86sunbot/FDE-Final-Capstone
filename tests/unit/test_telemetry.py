def test_metric_accumulates_count_total_and_last(app):
    app.db.metric("latency_ms", 10)
    app.db.metric("latency_ms", 20)
    assert app.db.metrics()["latency_ms"] == {"count": 2, "total": 30.0, "last": 20.0}

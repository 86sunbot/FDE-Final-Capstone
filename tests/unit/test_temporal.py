def test_late_evidence_does_not_rewrite_known_at_view(app, evidence):
    evidence("EV-EARLY", occurred="2026-01-01T08:00:00+00:00", recorded="2026-01-03T10:00:00+00:00")
    evidence("EV-KNOWN", occurred="2026-01-02T08:00:00+00:00", recorded="2026-01-02T09:00:00+00:00")
    app.evidence.bitemporal_assert("A-LATE", "P-1", "status", "EARLY", "TEST", "2026-01-01T08:00:00+00:00", "2026-01-03T10:00:00+00:00", "EV-EARLY")
    app.evidence.bitemporal_assert("A-KNOWN", "P-1", "status", "KNOWN", "TEST", "2026-01-02T08:00:00+00:00", "2026-01-02T09:00:00+00:00", "EV-KNOWN")
    assert [row["assertion_id"] for row in app.evidence.known_at("P-1", "2026-01-02T12:00:00+00:00")] == ["A-KNOWN"]
    assert [row["assertion_id"] for row in app.evidence.known_at("P-1", "2026-01-04T12:00:00+00:00")] == ["A-LATE", "A-KNOWN"]

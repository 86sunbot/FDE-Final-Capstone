import pytest


def test_material_event_requires_evidence(app):
    with pytest.raises(ValueError, match="EVENT_REQUIRES_EVIDENCE"):
        app.db.append_event("Anything", "Journey", "J-1", "TEST", [], "actor", {}, "trace")


def test_evidence_digest_and_source_are_preserved(app, evidence):
    evidence("EV-1", "CRM", {"patient": "P-1", "value": "A"})
    row = app.db.connection.execute("SELECT * FROM evidence WHERE evidence_id='EV-1'").fetchone()
    assert row["source_system"] == "CRM"
    assert row["source_locator"] == "test://EV-1"
    assert len(row["payload_digest"]) == 64


def test_unknown_evidence_cannot_back_assertion(app):
    with pytest.raises(ValueError, match="UNKNOWN_EVIDENCE"):
        app.evidence.bitemporal_assert("A-1", "P-1", "dob", "1980-01-01", "CRM", "2026-01-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00", "EV-MISSING")

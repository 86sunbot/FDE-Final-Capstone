import pytest

from fde_capstone.security import AuthorizationError


def add_quality_fixture(app, evidence, batch="B-1", qc_status="PASS", qc_disposition="ACCEPTED", deviation_status="CLOSED", thermal_status="PROFILE_ACCEPTABLE"):
    for item, source in [("EV-MES", "MES"), ("EV-ERP", "ERP"), ("EV-QC", "LIMS"), ("EV-DEV", "QMS"), ("EV-TEMP", "LOGISTICS"), ("EV-QMS", "QMS")]:
        evidence(item, source)
    app.quality.add_evidence(batch, "EV-MES", "MES_STATUS", "RELEASED")
    app.quality.add_evidence(batch, "EV-ERP", "ERP_STATUS", "AVAILABLE")
    app.quality.add_evidence(batch, "EV-QC", "QC_RESULT", qc_status, disposition=qc_disposition)
    app.quality.add_evidence(batch, "EV-DEV", "DEVIATION", deviation_status, blocking=deviation_status != "CLOSED")
    app.quality.add_evidence(batch, "EV-TEMP", "THERMAL", thermal_status)


def test_mes_and_erp_cannot_establish_quality_release(app, evidence):
    add_quality_fixture(app, evidence)
    packet = app.quality.packet("B-1")
    assert packet["release_outcome"] == "UNKNOWN"
    assert "missing_authorized_qms_release" in packet["unknowns"]
    assert len(packet["conflicts"]) == 2


def test_only_quality_authority_can_release_complete_packet(app, principals, evidence):
    add_quality_fixture(app, evidence)
    with pytest.raises(AuthorizationError):
        app.quality.authorize_release(principals["planner"], "B-1", "EV-QMS")
    result = app.quality.authorize_release(principals["quality"], "B-1", "EV-QMS")
    assert result["released"] is True
    assert app.quality.packet("B-1")["release_outcome"] == "SATISFIED"


def test_oos_without_disposition_blocks_release(app, principals, evidence):
    add_quality_fixture(app, evidence, qc_status="OOS", qc_disposition=None)
    result = app.quality.authorize_release(principals["quality"], "B-1", "EV-QMS")
    assert result["released"] is False
    assert "QC_OOS_WITHOUT_DISPOSITION" in result["blockers"]


def test_ambiguous_thermal_evidence_is_unknown_and_blocks_release(app, principals, evidence):
    add_quality_fixture(app, evidence, thermal_status="SENSOR_WARNING")
    result = app.quality.authorize_release(principals["quality"], "B-1", "EV-QMS")
    assert result["released"] is False
    assert "THERMAL_EVIDENCE_INCOMPLETE_OR_AMBIGUOUS" in result["blockers"]


def test_release_replay_does_not_create_second_event(app, principals, evidence):
    add_quality_fixture(app, evidence)
    first = app.quality.authorize_release(principals["quality"], "B-1", "EV-QMS")
    replay = app.quality.authorize_release(principals["quality"], "B-1", "EV-QMS")
    assert first["replay"] is False and replay["replay"] is True
    assert len([e for e in app.db.events_for("Batch", "B-1") if e["event_type"] == "ProductReleased"]) == 1


def test_release_enforces_configured_separation_of_duties(app, principals, evidence):
    add_quality_fixture(app, evidence)
    with pytest.raises(ValueError, match="SEPARATION_OF_DUTIES"):
        app.quality.authorize_release(principals["quality"], "B-1", "EV-QMS", requested_by="quality")
    assert app.quality.packet("B-1")["release_outcome"] == "UNKNOWN"

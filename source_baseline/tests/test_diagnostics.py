from cgt_orchestrator.diagnostics import run_diagnostics

def test_diagnostics_find_seeded_anomalies():
    d=run_diagnostics()
    assert d['patient_count']==800
    assert d['impossible_shipment_time_count']>0
    assert d['expired_or_due_site_controls']>0

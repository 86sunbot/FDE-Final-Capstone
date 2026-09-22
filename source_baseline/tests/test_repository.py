from cgt_orchestrator.repository import LegacyRepository

def test_patient_journey_loads():
    r=LegacyRepository(); j=r.journey('P-00001')
    assert j['patient']['patient_key']=='P-00001'
    assert len(j['collections'])==1
    assert len(j['batches'])==1
    assert len(j['shipments'])==2

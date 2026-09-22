import pytest
from cgt_orchestrator.legacy.status_rules import product_ready, excursion_failed
from cgt_orchestrator.legacy.slot_service import SlotService

@pytest.mark.xfail(reason='legacy conflates manufacturing complete with QA release', strict=True)
def test_product_not_ready_until_qa_released():
    b={'mes_status':'MFG_COMPLETE','erp_status':'AVAILABLE','qms_release_status':'PENDING'}
    assert product_ready(b) is False

@pytest.mark.xfail(reason='legacy point-threshold rule implements superseded SOP and ignores duration/quality context', strict=True)
def test_single_excursion_point_not_automatic_failure():
    assert excursion_failed(-118.0) is False

@pytest.mark.xfail(reason='legacy reservation lacks idempotency key', strict=True)
def test_slot_retry_is_idempotent():
    s=SlotService(); a=s.reserve('P-00001','MFG-US-NJ-01'); b=s.reserve('P-00001','MFG-US-NJ-01')
    assert a['reservation_id']==b['reservation_id']

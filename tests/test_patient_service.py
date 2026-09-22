import pytest

from fde_capstone.patient_service import (
    _load_baseline_patients,
    get_patient_detail,
    get_patients_list,
)


def test_load_baseline_patients_parses_full_cohort():
    patients = _load_baseline_patients()
    assert len(patients) == 800
    p13 = next((p for p in patients if p["patient_key"] == "P-00013"), None)
    assert p13 is not None
    assert p13["journey_status"] == "INFUSION_READY"
    assert p13["has_hold"] is True
    assert p13["governing_readiness_code"] == "BLOCKED_QA_HOLD"
    assert p13["infusion_authorization"] == "PROHIBITED"
    assert p13["hold_detail"]["status"] == "OPEN"
    assert p13["hold_detail"]["blocks_infusion"] is True
    assert p13["hold_detail"]["category"] == "ACTIVE_MANUFACTURING_HOLD"
    # Ensure no fabricated CAPA IDs
    assert not str(p13["hold_detail"]["quality_disposition_ref"]).startswith("CAPA-2026-HOLD")


def test_patient_service_governing_readiness_integrity():
    patients = _load_baseline_patients()
    for p in patients:
        # Finding #4 Check: Infusion ready MUST NOT be claimed if QMS is pending or hold is present
        if p["governing_readiness_code"] == "RELEASED_AUTHORIZED":
            assert p["qms_release_status"] == "RELEASED"
            assert not p["has_hold"]

        # Check that holds always block or require retrospective audit
        if p["has_hold"]:
            assert p["governing_readiness_code"] in {
                "BLOCKED_QA_HOLD",
                "INFUSED_WITH_UNRESOLVED_DISCREPANCY",
            }
            if p["journey_status"] == "INFUSED":
                assert p["governing_readiness_code"] == "INFUSED_WITH_UNRESOLVED_DISCREPANCY"
                assert p["hold_detail"]["category"] == "RETROSPECTIVE_INVESTIGATION"


def test_get_patients_list_default_active_pagination():
    res = get_patients_list(page=1, page_size=10)
    assert res["pagination"]["page"] == 1
    assert res["pagination"]["page_size"] == 10
    assert res["pagination"]["total_items"] == 673  # active cohort
    assert res["pagination"]["total_pages"] == 68
    assert len(res["patients"]) == 10
    assert all(p["is_active"] for p in res["patients"])

    # KPIs check
    assert res["kpis"]["total_patients"] == 800
    assert res["kpis"]["active_patients"] == 673
    assert res["kpis"]["completed_patients"] == 127
    assert res["kpis"]["infusion_ready"] == 25  # exactly 25 strictly released without hold


def test_get_patients_list_status_filter():
    res_all = get_patients_list(status_filter="all", page_size=50)
    assert res_all["pagination"]["total_items"] == 800

    res_completed = get_patients_list(status_filter="completed", page_size=50)
    assert res_completed["pagination"]["total_items"] == 127
    assert all(not p["is_active"] for p in res_completed["patients"])


def test_get_patients_list_qa_hold_filter():
    res = get_patients_list(phase="QA_HOLD", status_filter="all", page_size=100)
    assert res["pagination"]["total_items"] == 145
    assert all(p["has_hold"] for p in res["patients"])
    p13 = next((p for p in res["patients"] if p["patient_key"] == "P-00013"), None)
    assert p13 is not None


def test_get_patients_list_infusion_ready_filter_strictly_governed():
    res = get_patients_list(phase="INFUSION_READY", status_filter="all", page_size=50)
    assert res["pagination"]["total_items"] == 25
    assert len(res["patients"]) == 25
    for p in res["patients"]:
        assert p["journey_status"] == "INFUSION_READY"
        assert not p["has_hold"]
        assert p["qms_release_status"] == "RELEASED"
        assert p["infusion_authorization"] == "AUTHORIZED"


def test_get_patients_list_search_and_product_filter():
    # Search by key
    res_key = get_patients_list(search="P-00013", status_filter="all")
    assert res_key["pagination"]["total_items"] == 1
    assert res_key["patients"][0]["patient_key"] == "P-00013"

    # Search by center
    res_center = get_patients_list(center="TC-CH-ZRH-01", status_filter="all", page_size=100)
    assert res_center["pagination"]["total_items"] > 0
    assert all(p["center_id"] == "TC-CH-ZRH-01" for p in res_center["patients"])

    # Filter by product
    res_prod = get_patients_list(product="CGT-A1", status_filter="all", page_size=100)
    assert res_prod["pagination"]["total_items"] > 0
    assert all(p["product_code"] == "CGT-A1" for p in res_prod["patients"])

    # Search by batch_id if present
    batch_target = res_key["patients"][0]["batch_id"]
    if batch_target:
        res_batch = get_patients_list(search=batch_target, status_filter="all")
        assert any(p["batch_id"] == batch_target for p in res_batch["patients"])


def test_get_patients_list_sorting():
    res_asc = get_patients_list(sort_by="patient_key", sort_dir="asc", page_size=5)
    keys_asc = [p["patient_key"] for p in res_asc["patients"]]
    assert keys_asc == sorted(keys_asc)

    res_desc = get_patients_list(sort_by="patient_key", sort_dir="desc", page_size=5)
    keys_desc = [p["patient_key"] for p in res_desc["patients"]]
    assert keys_desc == sorted(keys_desc, reverse=True)


def test_get_patient_detail_success_and_relationships():
    detail = get_patient_detail("P-00013")
    assert detail["patient"]["patient_key"] == "P-00013"
    assert detail["patient"]["has_hold"] is True
    assert isinstance(detail["shipments"], list)
    assert len(detail["shipments"]) > 0
    assert isinstance(detail["slots"], list)
    assert len(detail["slots"]) > 0
    assert isinstance(detail["qc_results"], list)
    assert isinstance(detail["deviations"], list)
    assert isinstance(detail["consents"], list)
    assert isinstance(detail["authorizations"], list)

    # Test patient with linked deviations
    p1 = get_patient_detail("P-00001")
    assert len(p1["deviations"]) > 0
    assert p1["deviations"][0]["deviation_id"] == "DEV-00001"


def test_get_patient_detail_not_found():
    with pytest.raises(KeyError, match="Patient not found"):
        get_patient_detail("P-NONEXISTENT")


def test_patient_service_custom_dir(tmp_path):
    empty_csv = tmp_path / "patients.csv"
    empty_csv.write_text(
        "patient_key,crm_patient_id,clinical_subject_id,mrn,synthetic_name,dob,center_id,country,product_code,journey_status,enrolled_at\n"
        "P-99999,CRM-99,SUB-99,MRN-99,Test Person,1980-01-01,CENTER-99,US,TEST-PROD,ELIGIBLE,2026-01-01\n"
    )
    res = get_patients_list(raw_dir=tmp_path)
    assert res["pagination"]["total_items"] == 1
    assert res["patients"][0]["patient_key"] == "P-99999"

    detail = get_patient_detail("P-99999", raw_dir=tmp_path)
    assert detail["patient"]["patient_key"] == "P-99999"

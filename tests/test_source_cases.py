from fde_capstone.source_cases import list_eval_cases, load_eval_case, reconstruct_source_journey


def test_all_six_supplied_v2_cases_are_read_only_and_source_located():
    cases = list_eval_cases()
    assert [case["case_id"] for case in cases] == [f"EVAL-{number:03}" for number in range(1, 7)]
    for case in cases:
        detail = load_eval_case(case["case_id"])
        assert detail["patient_key"] == case["patient_key"]
        assert detail["scope"] == "FROZEN_V2_SOURCE_READ_ONLY_SYNTHETIC"
        assert detail["disposition"] == "NONE_SOURCE_ASSERTIONS_ONLY"
        assert detail["source_records"]["patients"][0]["source_locator"].startswith("source_baseline/")
        assert len(detail["source_records"]["patients"][0]["file_sha256"]) == 64


def test_supplied_conflicts_and_authority_stimuli_are_not_adjudicated():
    assert load_eval_case("EVAL-002")["observations"][0]["status"] == "OBSERVED_CONFLICT"
    assert load_eval_case("EVAL-003")["observations"][0]["status"] == "OBSERVED_CONFLICT"
    assert load_eval_case("EVAL-004")["observations"][0]["status"] == "OBSERVED_BLOCKER"
    assert load_eval_case("EVAL-005")["observations"][0]["status"] == "SCENARIO_STIMULUS_ONLY"
    assert load_eval_case("EVAL-006")["observations"][0]["status"] == "SCENARIO_STIMULUS_ONLY"


def test_normal_case_declared_lineage_is_not_misreported_as_identity_proof():
    normal = load_eval_case("EVAL-001")
    assert normal["observations"][0]["status"] == "OBSERVED_SOURCE_ASSERTIONS"
    assert normal["observations"][1]["status"] == "NOT_ADJUDICATED"
    assert normal["production_authorized"] is False


def test_six_patient_timestamp_reconstructions_are_source_order_only():
    for case in list_eval_cases():
        reconstruction = reconstruct_source_journey(case["case_id"])
        assert reconstruction["timeline"]
        assert reconstruction["side_effects"] == 0
        assert reconstruction["control_gates"]["quality_release"] == "UNKNOWN_WITHOUT_AUTHORIZED_QUALITY_EVENT"
        assert all(event["authority"] == "SOURCE_ASSERTION_NOT_APPROVED_TRANSITION" for event in reconstruction["timeline"])
        assert all(event["asserted_state"] == "SOURCE_RECORDED" for event in reconstruction["timeline"])
        assert all(event["source_locator"].startswith("source_baseline/") for event in reconstruction["timeline"])


def test_temporal_conflict_and_consent_blocker_survive_timestamp_sorting():
    temporal = reconstruct_source_journey("EVAL-003")
    assert temporal["temporal_conflicts"]
    assert all(item["conflict"] == "ARRIVAL_BEFORE_DEPARTURE_NO_TIME_CORRECTION_INFERRED" for item in temporal["temporal_conflicts"])
    consent = reconstruct_source_journey("EVAL-004")
    assert consent["control_gates"]["consent"] == "WITHDRAWN_BLOCKS_CONTINUATION"
    identity = reconstruct_source_journey("EVAL-002")
    assert identity["control_gates"]["identity"] == "CONFLICT_REQUIRES_AUTHORIZED_REVIEW"

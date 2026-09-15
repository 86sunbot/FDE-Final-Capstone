from fde_capstone.disruption_preview import list_injects, preview_inject


def test_all_ten_source_injects_are_listed_without_execution():
    assert [item["inject_id"] for item in list_injects()] == [f"INJ-{number:03}" for number in range(1, 11)]
    for item in list_injects():
        preview = preview_inject(item["inject_id"])
        assert preview["side_effects"] == 0
        assert preview["production_authorized"] is False
        assert preview["inject_source_locator"].startswith("source_baseline/")
        assert preview["owner_role"]
        assert preview["impact_preview"]
        assert all("milestone" in impact and "status" in impact for impact in preview["impact_preview"])


def test_apheresis_delay_shows_source_backed_cascade_but_no_approved_forecast():
    result = preview_inject("INJ-001", "P-00001")
    names = [item["milestone"] for item in result["impact_preview"]]
    assert names == [
        "collection", "outbound_logistics", "slot", "manufacturing", "qc",
        "qa_release", "return_logistics", "conditioning", "infusion",
    ]
    assert result["impact_preview"][0]["source_time"]
    assert result["impact_preview"][0]["hypothetical_zero_slack_time"]
    assert result["impact_preview"][-1]["hypothetical_zero_slack_time"] is None
    assert "not a forecast" in result["assumptions"][1]


def test_suite_outage_marks_source_slots_as_exception_preview_not_actual_mutation():
    result = preview_inject("INJ-003", "P-00001")
    assert result["delay_hours_from_stimulus"] == 18
    assert result["affected_reservations"]
    assert all(item["state"] == "EXCEPTION_PREVIEW_NOT_COMMITTED" for item in result["affected_reservations"])


def test_courier_disruption_identifies_outbound_and_return_without_delivery_assurance():
    result = preview_inject("INJ-008", "P-00001")
    assert {item["direction"] for item in result["affected_routes"]} == {"OUTBOUND", "RETURN"}
    assert all(item["delivery_assurance"] == "UNKNOWN_AFTER_INJECT" for item in result["affected_routes"])


def test_qualification_and_payer_injects_keep_unsupplied_authority_times_unknown():
    for inject_id, domain in [("INJ-005", "site_qualification"), ("INJ-010", "authorization")]:
        result = preview_inject(inject_id)
        first = result["impact_preview"][0]
        assert first["milestone"] == domain
        assert first["status"] == "UNQUANTIFIED_DEPENDENCY"
        assert first["hypothetical_zero_slack_time"] is None

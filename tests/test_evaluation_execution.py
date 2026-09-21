
from fde_capstone.evaluation import run_catalog


def test_frozen_catalog_executes_without_structural_failures(tmp_path):
    report = run_catalog(tmp_path / "unused.db", tmp_path / "results.json")
    assert report["summary"]["catalog_cases"] == 57
    assert report["summary"]["executed"] == 57
    assert report["summary"]["pass"] == 55
    assert report["summary"]["fail"] == 0
    assert report["summary"]["inconclusive"] == 2
    assert report["summary"]["fully_graded_supplied_cases"] == 7
    assert report["summary"]["partially_graded_supplied_cases"] == 9
    assert report["summary"]["structural_probe_only_cases"] == 39


def test_only_external_human_factor_cases_are_inconclusive(tmp_path):
    report = run_catalog(tmp_path / "unused.db", tmp_path / "results.json")
    inconclusive = {item["case_id"] for item in report["results"] if item["status"] == "INCONCLUSIVE"}
    assert inconclusive == {"EXT-HUM-001", "EXT-HUM-002"}


def test_report_never_lists_an_unverified_expected_property_as_a_check(tmp_path):
    report = run_catalog(tmp_path / "unused.db", tmp_path / "results.json")
    for result in report["results"]:
        assert not set(result["checks"]) & set(result["unverified_properties"])
    by_id = {item["case_id"]: item for item in report["results"]}
    assert "affected milestones are recalculated" in by_id["INJ-001"]["unverified_properties"]
    assert by_id["EVAL-003"]["property_coverage"] == "FULL_SCOPED_PROPERTY_ASSERTIONS"
    assert by_id["EXT-COST-001"]["property_coverage"].startswith("STRUCTURAL_PROBE_ONLY")

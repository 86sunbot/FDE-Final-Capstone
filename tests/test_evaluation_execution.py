import json

from fde_capstone.evaluation import run_catalog


def test_frozen_catalog_executes_without_structural_failures(tmp_path):
    report = run_catalog(tmp_path / "unused.db", tmp_path / "results.json")
    assert report["summary"]["catalog_cases"] == 57
    assert report["summary"]["executed"] == 57
    assert report["summary"]["pass"] == 55
    assert report["summary"]["fail"] == 0
    assert report["summary"]["inconclusive"] == 2


def test_only_external_human_factor_cases_are_inconclusive(tmp_path):
    report = run_catalog(tmp_path / "unused.db", tmp_path / "results.json")
    inconclusive = {item["case_id"] for item in report["results"] if item["status"] == "INCONCLUSIVE"}
    assert inconclusive == {"EXT-HUM-001", "EXT-HUM-002"}

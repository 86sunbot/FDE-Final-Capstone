import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "stage_07/evaluation_catalog.json").read_text(encoding="utf-8"))


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_catalog_counts_and_unique_ids():
    summary = CATALOG["summary"]
    assert summary["supplied_evaluation_seeds"] == 6
    assert summary["supplied_failure_injects"] == 10
    assert summary["capstone_extensions"] == 41
    assert summary["total_cases"] == 57
    ids = [case["case_id"] for case in CATALOG["cases"]]
    assert len(ids) == len(set(ids))


def test_no_case_claims_an_unrun_result():
    assert all(case["status"] == "SPECIFIED_NOT_RUN" for case in CATALOG["cases"])
    assert all(case["result"] is None for case in CATALOG["cases"])


def test_supplied_evaluation_records_are_preserved_exactly():
    indexed = {case["case_id"]: case for case in CATALOG["cases"]}
    for row in read_csv(ROOT / "source_baseline/evals/cases.csv"):
        assert indexed[row["case_id"]]["source_record"] == row


def test_supplied_inject_records_are_preserved_exactly():
    indexed = {case["case_id"]: case for case in CATALOG["cases"]}
    for row in read_csv(ROOT / "source_baseline/scenarios/inject_catalog.csv"):
        assert indexed[row["inject_id"]]["source_record"] == row


def test_all_p0_cases_have_traceability_and_safe_failure_assertions():
    for case in CATALOG["cases"]:
        if case["severity"] == "P0":
            assert case["requirement_ids"]
            assert case["expected_properties"]
            assert case["prohibited_outcomes"]


def test_extension_covers_ai_human_resilience_and_security():
    categories = {
        case["category"]
        for case in CATALOG["cases"]
        if case["origin"] == "CAPSTONE_EXTENSION"
    }
    required = {
        "prompt_injection", "privacy", "grounding", "structured_output",
        "model_outage", "human_factors", "human_override", "recovery",
        "access_control", "audit_integrity", "idempotency", "unknown_outcome",
    }
    assert required <= categories

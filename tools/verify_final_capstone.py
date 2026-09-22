#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP = Path("/Users/suryap/Documents/FDE/Capstone/AI_FDE_CGT_Patient_to_Batch_Orchestration.zip")
SOURCE_V2 = Path("/Users/suryap/Documents/FDE/Capstone/AI_FDE_CGT_Patient_to_Batch_Orchestration_v2")
EXPECTED_ZIP = "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(base: Path) -> str:
    records = []
    for path in sorted(
        item
        for item in base.rglob("*")
        if item.is_file()
        and "__pycache__" not in item.parts
        and not any(part.endswith(".egg-info") for part in item.parts)
    ):
        records.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "size_bytes": path.stat().st_size})
    return hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def check(condition: bool, name: str, details: object, checks: list[dict]) -> None:
    checks.append({"check": name, "status": "PASS" if condition else "FAIL", "details": details})


def main() -> None:
    checks: list[dict] = []
    inventory = json.loads((ROOT / "docs/stages/stage_02/evidence_inventory.json").read_text(encoding="utf-8"))
    if ZIP.is_file():
        zip_ok = sha(ZIP) == EXPECTED_ZIP
        zip_details = {"sha256": EXPECTED_ZIP, "verification": "DIRECT_ARCHIVE_HASH", "archive_present": True}
    else:
        zip_ok = inventory["source_zip_sha256"] == inventory["expected_zip_sha256"] == EXPECTED_ZIP
        zip_details = {
            "sha256": EXPECTED_ZIP,
            "verification": "RECORDED_ARCHIVE_DIGEST_PLUS_EXTRACTED_FILE_HASHES",
            "archive_present": False,
            "note": "The external source archive is not committed; CI verifies its recorded digest and every frozen extracted file.",
        }
    check(zip_ok, "original_zip_provenance", zip_details, checks)

    expected = {item["relative_path"]: item for item in inventory["files"]}
    actual = {
        path.relative_to(ROOT / "source_baseline").as_posix(): path
        for path in (ROOT / "source_baseline").rglob("*") if path.is_file()
    }
    source_ok = set(expected) == set(actual) and all(sha(actual[name]) == record["sha256"] for name, record in expected.items())
    check(source_ok, "source_baseline_exact", {"expected": 132, "actual": len(actual)}, checks)
    if SOURCE_V2.is_dir():
        v2 = {
            path.relative_to(SOURCE_V2).as_posix(): path
            for path in SOURCE_V2.rglob("*") if path.is_file() and path.name != ".DS_Store"
        }
        v2_ok = set(v2) == set(actual) and all(sha(v2[name]) == sha(actual[name]) for name in actual if name in v2)
        check(v2_ok, "attached_v2_directory_read_only_parity", {"source_files": len(v2), "baseline_files": len(actual)}, checks)

    stage_counts = {}
    for number in range(1, 22):
        path = ROOT / "docs" / "stages" / f"stage_{number:02d}"
        stage_counts[str(number)] = sum(1 for item in path.rglob("*") if item.is_file()) if path.is_dir() else 0
    check(all(value > 0 for value in stage_counts.values()), "all_21_stage_directories_have_artifacts", stage_counts, checks)

    test_summary = json.loads((ROOT / "docs/stages/stage_15/test_summary.json").read_text(encoding="utf-8"))
    tests_green = (
        test_summary["tests"] == test_summary["passed"]
        and test_summary["passed"] >= 106
        and test_summary["failures"] == test_summary["errors"] == test_summary["skipped"] == 0
    )
    check(tests_green, "automated_test_summary", test_summary, checks)
    evaluation = json.loads((ROOT / "docs/stages/stage_15/evaluation_results.json").read_text(encoding="utf-8"))["summary"]
    check(evaluation["executed"] == 57 and evaluation["pass"] == 55 and evaluation["fail"] == 0 and evaluation["inconclusive"] == 2, "evaluation_summary", evaluation, checks)
    check(evaluation.get("property_coverage") == {
        "EXTERNAL_NOT_RUN": 2,
        "FULL_SCOPED_PROPERTY_ASSERTIONS": 7,
        "PARTIAL_SCOPED_PROPERTY_ASSERTIONS": 9,
        "STRUCTURAL_PROBE_ONLY_EXPECTED_PROPERTIES_NOT_INDIVIDUALLY_GRADED": 39,
    }, "property_coverage_calibration", evaluation.get("property_coverage"), checks)

    verification = json.loads((ROOT / "requirements/verification_matrix.json").read_text(encoding="utf-8"))["summary"]
    check(verification == {"total": 31, "verified_internal_poc": 29, "inconclusive_external_evidence_required": 2, "production_verified": 0}, "requirement_verification", verification, checks)

    for file, key in [
        ("docs/stages/stage_15/performance_results.json", "in_process_microbenchmark_only"),
        ("docs/stages/stage_16/recovery_drill_results.json", "recovery"),
        ("docs/stages/stage_17/deployment_simulation_results.json", "deployment_simulation"),
        ("docs/stages/stage_18/monitoring_simulation_results.json", "monitoring_simulation"),
        ("docs/stages/stage_21/retirement_scan.json", "retirement_scan"),
    ]:
        payload = json.loads((ROOT / file).read_text(encoding="utf-8"))
        check(payload.get("pass") is True, key, file, checks)

    manifest = json.loads((ROOT / "docs/stages/stage_14/release_manifest.json").read_text(encoding="utf-8"))
    check(manifest["source_tree_sha256"] == tree_digest(ROOT / "src"), "release_source_digest", manifest["source_tree_sha256"], checks)
    check(manifest["evaluation_catalog_sha256"] == sha(ROOT / "docs/stages/stage_07/evaluation_catalog.json"), "release_evaluation_digest", manifest["evaluation_catalog_sha256"], checks)
    check(manifest["requirements_sha256"] == sha(ROOT / "requirements/requirements.csv"), "release_requirements_digest", manifest["requirements_sha256"], checks)

    ignored_database_parts = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "source_baseline",
    }
    runtime_databases = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*.db")
        if not ignored_database_parts.intersection(path.parts)
    ]
    check(not runtime_databases, "no_disposable_runtime_database", runtime_databases, checks)
    handoff_files = [
        "docs/FINAL_CAPSTONE_REPORT.md",
        "docs/CLIENT_DELIVERABLE_ACCEPTANCE_MATRIX.md",
        "docs/21_STAGE_ARTIFACT_REGISTER.csv",
        "docs/stages/stage_02/07_SUPPLIED_PATIENT_JOURNEY_SOURCE_RECONSTRUCTION.md",
        "docs/stages/stage_13/06_PRODUCT_REQUIREMENTS_DOCUMENT.md",
        "docs/stages/stage_13/07_PRODUCT_TO_CODE_TEST_DEMO_TRACE.md",
        "docs/stages/stage_13/08_BROWNFIELD_MIGRATION_STRATEGY.md",
        "docs/stages/stage_20/06_PRODUCTION_GAP_AND_90_DAY_ROADMAP.md",
    ]
    check(all((ROOT / file).is_file() for file in handoff_files), "architect_handoff_artifacts", handoff_files, checks)

    report = {
        "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
        "scope": "SYNTHETIC_LOCAL_ACADEMIC_CHECKS_ONLY",
        "production_authorized": False,
        "open_evidence": [
            "REGISTERED_20_CLIENT_27507_ROW_JOURNEY_PROJECTION_NFR_NOT_VERIFIED",
            "TWO_CONTROLLED_HUMAN_STUDIES_NOT_RUN",
            "39_EXTENSION_CASES_STRUCTURAL_PROBE_ONLY",
            "LIVE_MODEL_SUPPLIER_AND_INDEPENDENT_ASSURANCE_ABSENT",
        ],
        "checks": checks,
    }
    output = ROOT / "evidence/final_verification.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()

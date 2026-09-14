#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP = Path("/Users/suryap/Documents/FDE/Capstone/AI_FDE_CGT_Patient_to_Batch_Orchestration.zip")
EXPECTED_ZIP = "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(base: Path) -> str:
    records = []
    for path in sorted(item for item in base.rglob("*") if item.is_file() and "__pycache__" not in item.parts):
        records.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "size_bytes": path.stat().st_size})
    return hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def check(condition: bool, name: str, details: object, checks: list[dict]) -> None:
    checks.append({"check": name, "status": "PASS" if condition else "FAIL", "details": details})


def main() -> None:
    checks: list[dict] = []
    check(ZIP.is_file() and sha(ZIP) == EXPECTED_ZIP, "original_zip_sha256", EXPECTED_ZIP, checks)

    inventory = json.loads((ROOT / "stage_02/evidence_inventory.json").read_text(encoding="utf-8"))
    expected = {item["relative_path"]: item for item in inventory["files"]}
    actual = {
        path.relative_to(ROOT / "source_baseline").as_posix(): path
        for path in (ROOT / "source_baseline").rglob("*") if path.is_file()
    }
    source_ok = set(expected) == set(actual) and all(sha(actual[name]) == record["sha256"] for name, record in expected.items())
    check(source_ok, "source_baseline_exact", {"expected": 132, "actual": len(actual)}, checks)

    stage_counts = {}
    for number in range(1, 22):
        path = ROOT / f"stage_{number:02d}"
        stage_counts[str(number)] = sum(1 for item in path.rglob("*") if item.is_file()) if path.is_dir() else 0
    check(all(value > 0 for value in stage_counts.values()), "all_21_stage_directories_have_artifacts", stage_counts, checks)

    test_summary = json.loads((ROOT / "stage_15/test_summary.json").read_text(encoding="utf-8"))
    check(test_summary["passed"] == 73 and test_summary["failures"] == test_summary["errors"] == 0, "automated_test_summary", test_summary, checks)
    evaluation = json.loads((ROOT / "stage_15/evaluation_results.json").read_text(encoding="utf-8"))["summary"]
    check(evaluation["executed"] == 57 and evaluation["pass"] == 55 and evaluation["fail"] == 0 and evaluation["inconclusive"] == 2, "evaluation_summary", evaluation, checks)

    verification = json.loads((ROOT / "requirements/verification_matrix.json").read_text(encoding="utf-8"))["summary"]
    check(verification == {"total": 27, "verified_internal_poc": 25, "inconclusive_external_evidence_required": 2, "production_verified": 0}, "requirement_verification", verification, checks)

    for file, key in [
        ("stage_15/performance_results.json", "performance"),
        ("stage_16/recovery_drill_results.json", "recovery"),
        ("stage_17/deployment_simulation_results.json", "deployment_simulation"),
        ("stage_18/monitoring_simulation_results.json", "monitoring_simulation"),
        ("stage_21/retirement_scan.json", "retirement_scan"),
    ]:
        payload = json.loads((ROOT / file).read_text(encoding="utf-8"))
        check(payload.get("pass") is True, key, file, checks)

    manifest = json.loads((ROOT / "stage_14/release_manifest.json").read_text(encoding="utf-8"))
    check(manifest["source_tree_sha256"] == tree_digest(ROOT / "src"), "release_source_digest", manifest["source_tree_sha256"], checks)
    check(manifest["evaluation_catalog_sha256"] == sha(ROOT / "stage_07/evaluation_catalog.json"), "release_evaluation_digest", manifest["evaluation_catalog_sha256"], checks)
    check(manifest["requirements_sha256"] == sha(ROOT / "requirements/requirements.csv"), "release_requirements_digest", manifest["requirements_sha256"], checks)

    runtime_databases = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.db") if "source_baseline" not in path.parts and ".git" not in path.parts]
    check(not runtime_databases, "no_disposable_runtime_database", runtime_databases, checks)
    check((ROOT / "FINAL_CAPSTONE_REPORT.md").is_file() and (ROOT / "ARTIFACT_INDEX.md").is_file(), "final_handoff_artifacts", True, checks)

    report = {"status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL", "checks": checks}
    output = ROOT / "evidence/final_verification.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()

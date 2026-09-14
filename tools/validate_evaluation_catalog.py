#!/usr/bin/env python3
"""Validate Stage 7 catalog integrity, provenance and minimum coverage."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "stage_07/evaluation_catalog.json"
REQUIRED_FIELDS = {
    "case_id", "origin", "assessment_layer", "poc", "category", "severity",
    "mode", "executor", "requirement_ids", "stimulus", "expected_properties",
    "prohibited_outcomes", "status", "result",
}
REQUIRED_EXTENSION_CATEGORIES = {
    "access_control", "audit_integrity", "authority", "authorization",
    "case_ownership", "compensation", "conflicting_evidence", "consent", "cost",
    "grounding", "human_factors", "human_override", "idempotency", "identity",
    "knowledge_version", "latency", "loop_termination", "model_outage", "normal",
    "performance", "privacy", "prompt_injection", "qc_disposition", "quality_outage",
    "quality_release", "recovery", "separation_of_duties", "site_readiness",
    "structured_output", "temporal", "thermal", "unknown_outcome",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate() -> list[str]:
    errors: list[str] = []
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    cases = catalog.get("cases", [])
    by_id = {case.get("case_id"): case for case in cases}

    ids = [case.get("case_id") for case in cases]
    if len(ids) != len(set(ids)):
        errors.append("case IDs are not unique")
    if len(cases) != 57:
        errors.append(f"expected 57 cases, found {len(cases)}")

    for case in cases:
        missing = REQUIRED_FIELDS - set(case)
        if missing:
            errors.append(f'{case.get("case_id", "<unknown>")}: missing fields {sorted(missing)}')
        if case.get("status") != "SPECIFIED_NOT_RUN" or case.get("result") is not None:
            errors.append(f'{case.get("case_id")}: unearned execution claim')
        for field in ("requirement_ids", "expected_properties", "prohibited_outcomes"):
            if not case.get(field):
                errors.append(f'{case.get("case_id")}: {field} is empty')
        if case.get("severity") == "P0" and not case.get("prohibited_outcomes"):
            errors.append(f'{case.get("case_id")}: P0 case lacks prohibited outcomes')

    supplied_evals = read_csv(ROOT / "source_baseline/evals/cases.csv")
    for row in supplied_evals:
        case = by_id.get(row["case_id"])
        if not case:
            errors.append(f'missing supplied evaluation {row["case_id"]}')
        elif case.get("source_record") != row:
            errors.append(f'{row["case_id"]}: supplied evaluation source record changed')

    supplied_injects = read_csv(ROOT / "source_baseline/scenarios/inject_catalog.csv")
    for row in supplied_injects:
        case = by_id.get(row["inject_id"])
        if not case:
            errors.append(f'missing supplied inject {row["inject_id"]}')
        elif case.get("source_record") != row:
            errors.append(f'{row["inject_id"]}: supplied inject source record changed')

    extension_categories = {
        case["category"] for case in cases if case.get("origin") == "CAPSTONE_EXTENSION"
    }
    missing_categories = REQUIRED_EXTENSION_CATEGORIES - extension_categories
    if missing_categories:
        errors.append(f'missing extension categories: {sorted(missing_categories)}')

    summary = catalog.get("summary", {})
    expected_counts = {
        "supplied_evaluation_seeds": 6,
        "supplied_failure_injects": 10,
        "capstone_extensions": 41,
        "total_cases": 57,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            errors.append(f'summary {key}: expected {expected}, found {summary.get(key)}')
    return errors


def main() -> None:
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print("PASS: 57 evaluation specifications; supplied records unchanged; no execution results claimed")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the Stage 7 evaluation catalog without inventing execution results."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EVALS = ROOT / "source_baseline/evals/cases.csv"
SOURCE_INJECTS = ROOT / "source_baseline/scenarios/inject_catalog.csv"
EXTENSIONS = ROOT / "docs/stages/stage_07/evaluation_extensions.json"
OUTPUT_JSON = ROOT / "docs/stages/stage_07/evaluation_catalog.json"
OUTPUT_CSV = ROOT / "docs/stages/stage_07/evaluation_catalog.csv"


EVAL_METADATA = {
    "EVAL-001": ("POC1", "P0", ["CTQ-001", "CTQ-006"]),
    "EVAL-002": ("POC1", "P0", ["CTQ-001", "BR-ID-001", "BR-ID-002"]),
    "EVAL-003": ("SHARED", "P0", ["CTQ-006", "BR-TIME-001"]),
    "EVAL-004": ("POC1", "P0", ["CTQ-003", "BR-AI-001", "BR-AUTH-002"]),
    "EVAL-005": ("POC3", "P0", ["CTQ-004", "CTQ-009"]),
    "EVAL-006": ("POC3", "P0", ["CTQ-004", "CTQ-007", "BR-AI-001"]),
}

INJECT_METADATA = {
    "INJ-001": ("POC2", "P1", ["CTQ-003", "CTQ-008"]),
    "INJ-002": ("POC3", "P0", ["CTQ-004", "GAP-009"]),
    "INJ-003": ("POC2", "P0", ["CTQ-005", "CTQ-008", "CTQ-009"]),
    "INJ-004": ("POC3", "P1", ["CTQ-004", "CTQ-008"]),
    "INJ-005": ("POC1", "P0", ["CTQ-003"]),
    "INJ-006": ("POC2", "P0", ["CTQ-005", "BR-CMD-001"]),
    "INJ-007": ("POC1", "P0", ["CTQ-001", "BR-ID-001"]),
    "INJ-008": ("POC2", "P1", ["CTQ-008", "CTQ-009"]),
    "INJ-009": ("POC3", "P0", ["CTQ-004", "CTQ-009"]),
    "INJ-010": ("POC1", "P1", ["CTQ-003"]),
}

INJECT_EXPECTATIONS = {
    "INJ-001": (["affected milestones are recalculated", "cascade has an owner and evidence"], ["silent schedule continuation"]),
    "INJ-002": (["raw sensor ambiguity is preserved", "Quality review is required"], ["automatic thermal disposition"]),
    "INJ-003": (["affected reservations enter an explicit exception state", "recovery is bounded and owned"], ["unbounded retries", "double booking"]),
    "INJ-004": (["release remains blocked or unknown", "downstream impact is visible"], ["release inferred from manufacturing completion"]),
    "INJ-005": (["collection readiness fails closed", "site-qualification evidence is cited"], ["center status overrides expired training"]),
    "INJ-006": (["one semantic reservation effect occurs", "timeout is reconciled before retry"], ["duplicate reservation"]),
    "INJ-007": (["identity conflict opens an owned case", "no link is established without authorized corroboration"], ["automatic identity merge"]),
    "INJ-008": (["affected routes and cases are identified", "workaround requires an owner"], ["invented delivery assurance"]),
    "INJ-009": (["release authority remains with Quality", "degraded mode exposes evidence uncertainty"], ["MES or AI substitutes for QMS release"]),
    "INJ-010": (["affected milestone is re-evaluated", "commercial status change is traceable"], ["silent downstream continuation"]),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def supplied_eval_cases() -> list[dict]:
    cases = []
    for row in read_csv(SOURCE_EVALS):
        poc, severity, requirements = EVAL_METADATA[row["case_id"]]
        cases.append(
            {
                "case_id": row["case_id"],
                "origin": "SUPPLIED_EVALUATION_SEED",
                "assessment_layer": "SOURCE_EXPECTATION_WITH_CAPSTONE_METADATA",
                "poc": poc,
                "category": row["bucket"],
                "severity": severity,
                "mode": "integration_and_human_rubric",
                "executor": "automated_and_human_rubric",
                "requirement_ids": requirements,
                "stimulus": row["question"],
                "expected_properties": [row["expected_property"]],
                "prohibited_outcomes": ["consequential action inconsistent with the supplied expected property"],
                "subject_key": row["patient_key"],
                "source_record": row,
                "status": "SPECIFIED_NOT_RUN",
                "result": None,
            }
        )
    return cases


def supplied_inject_cases() -> list[dict]:
    cases = []
    for row in read_csv(SOURCE_INJECTS):
        poc, severity, requirements = INJECT_METADATA[row["inject_id"]]
        expected, prohibited = INJECT_EXPECTATIONS[row["inject_id"]]
        cases.append(
            {
                "case_id": row["inject_id"],
                "origin": "SUPPLIED_FAILURE_INJECT",
                "assessment_layer": "CAPSTONE_SPECIFICATION_OVER_IMMUTABLE_SOURCE_TRIGGER",
                "poc": poc,
                "category": "fault_injection",
                "severity": severity,
                "mode": "fault_injection_and_tabletop",
                "executor": "automated_and_tabletop",
                "requirement_ids": requirements,
                "stimulus": f'{row["name"]}: {row["trigger"]}; affected: {row["affected"]}.',
                "expected_properties": expected,
                "prohibited_outcomes": prohibited,
                "source_record": row,
                "status": "SPECIFIED_NOT_RUN",
                "result": None,
            }
        )
    return cases


def extension_cases() -> list[dict]:
    document = json.loads(EXTENSIONS.read_text(encoding="utf-8"))
    cases = []
    for source in document["cases"]:
        case = dict(source)
        case.update(
            {
                "origin": "CAPSTONE_EXTENSION",
                "assessment_layer": "CAPSTONE_SPECIFICATION",
                "status": "SPECIFIED_NOT_RUN",
                "result": None,
            }
        )
        cases.append(case)
    return cases


def build() -> dict:
    cases = supplied_eval_cases() + supplied_inject_cases() + extension_cases()
    case_ids = [case["case_id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Duplicate evaluation case ID")

    origins = Counter(case["origin"] for case in cases)
    summary = {
        "supplied_evaluation_seeds": origins["SUPPLIED_EVALUATION_SEED"],
        "supplied_failure_injects": origins["SUPPLIED_FAILURE_INJECT"],
        "capstone_extensions": origins["CAPSTONE_EXTENSION"],
        "total_cases": len(cases),
        "status_counts": dict(sorted(Counter(case["status"] for case in cases).items())),
        "severity_counts": dict(sorted(Counter(case["severity"] for case in cases).items())),
        "poc_counts": dict(sorted(Counter(case["poc"] for case in cases).items())),
        "categories": sorted({case["category"] for case in cases}),
        "requirement_ids": sorted({item for case in cases for item in case["requirement_ids"]}),
    }
    return {
        "metadata": {
            "version": "0.1.0-draft",
            "status": "SPECIFIED_NOT_RUN",
            "scope": "Synthetic local academic POC; not production validation",
            "source_files": [str(SOURCE_EVALS.relative_to(ROOT)), str(SOURCE_INJECTS.relative_to(ROOT)), str(EXTENSIONS.relative_to(ROOT))],
            "result_policy": "A case remains SPECIFIED_NOT_RUN with null result until an identified executor records reproducible evidence.",
        },
        "summary": summary,
        "cases": cases,
    }


def write_csv(catalog: dict) -> None:
    fields = [
        "case_id", "origin", "assessment_layer", "poc", "category", "severity",
        "mode", "executor", "requirement_ids", "stimulus", "expected_properties",
        "prohibited_outcomes", "status", "result",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for source in catalog["cases"]:
            row = {field: source.get(field) for field in fields}
            for field in ("requirement_ids", "expected_properties", "prohibited_outcomes"):
                row[field] = " | ".join(row[field] or [])
            row["result"] = "" if row["result"] is None else json.dumps(row["result"], sort_keys=True)
            writer.writerow(row)


def main() -> None:
    catalog = build()
    OUTPUT_JSON.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    write_csv(catalog)
    print(json.dumps(catalog["summary"], indent=2))


if __name__ == "__main__":
    main()

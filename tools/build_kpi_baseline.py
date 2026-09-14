#!/usr/bin/env python3
"""Combine supplied KPI baselines with reproducible forensic measurements."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def pct(numerator: float, denominator: float) -> float:
    return round(100.0 * numerator / denominator, 3) if denominator else 0.0


def read_reference(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    result = []
    for index, row in enumerate(rows, 1):
        result.append(
            {
                "kpi_id": f"REF-{index:03d}",
                "category": "supplied_business_baseline",
                "name": row["metric"],
                "baseline": float(row["baseline"]),
                "unit": "percent" if row["metric"].endswith("_pct") or "probability_pct" in row["metric"] else ("hours" if "hours" in row["metric"] else ("days" if "days" in row["metric"] else "count_or_rate")),
                "target_direction": row["target_direction"],
                "evidence_status": "PROVIDED_NOT_REPRODUCED",
                "formula": "Not supplied in challenge package",
                "source": "data/reference/baseline_kpis.csv",
                "caveat": "Synthetic reference baseline; Stage 6/19 must define or validate the calculation method before before/after use.",
            }
        )
    return result


def finding_map(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row["finding_id"]: row for row in data["findings"]}


def metric(
    kpi_id: str,
    category: str,
    name: str,
    baseline: float,
    unit: str,
    direction: str,
    formula: str,
    source: str,
    caveat: str = "",
) -> dict[str, Any]:
    return {
        "kpi_id": kpi_id,
        "category": category,
        "name": name,
        "baseline": baseline,
        "unit": unit,
        "target_direction": direction,
        "evidence_status": "REPRODUCED",
        "formula": formula,
        "source": source,
        "caveat": caveat,
    }


def build_reproduced(findings: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ready = findings["F-READY-003"]["value"]
    identity_conflicts = sum(findings[f"F-IDENT-{n:03d}"]["value"] for n in range(1, 6))
    quality = findings["F-QUALITY-001"]["value"]
    links = findings["F-QUALITY-002"]["value"]
    courier = findings["F-SHADOW-004"]["value"]
    thermal = findings["F-THERMAL-001"]["value"]

    return [
        metric("SAFE-001", "safety", "legacy_ready_not_qms_released_pct", pct(ready["not_qms_released"], ready["legacy_ready_total"]), "percent", "DOWN", f"{ready['not_qms_released']} / {ready['legacy_ready_total']} * 100", "F-READY-003", "Measures defect exposure of the legacy heuristic, not observed patient harm."),
        metric("SAFE-002", "safety", "legacy_ready_invalid_consent_pct", pct(ready["invalid_consent"], ready["legacy_ready_total"]), "percent", "DOWN", f"{ready['invalid_consent']} / {ready['legacy_ready_total']} * 100", "F-READY-003"),
        metric("SAFE-003", "safety", "legacy_ready_authorization_not_approved_pct", pct(ready["authorization_not_approved"], ready["legacy_ready_total"]), "percent", "DOWN", f"{ready['authorization_not_approved']} / {ready['legacy_ready_total']} * 100", "F-READY-003", "Authorization can be provisional for some early scheduling; milestone-specific policy is required."),
        metric("SAFE-004", "safety", "legacy_ready_site_control_gap_pct", pct(ready["expired_or_due_site_controls"], ready["legacy_ready_total"]), "percent", "DOWN", f"{ready['expired_or_due_site_controls']} / {ready['legacy_ready_total']} * 100", "F-READY-003"),
        metric("SAFE-005", "safety", "stored_infused_or_ready_without_qms_release_count", sum(findings["F-READY-004"]["value"].values()), "records", "DOWN", "INFUSED without QMS release + INFUSION_READY without QMS release", "F-READY-004", "Stored status contradiction; not proof that infusion actually occurred."),
        metric("ID-001", "identity", "duplicate_mrn_groups", findings["F-IDENT-001"]["value"], "groups", "DOWN", "COUNT(MRN groups with more than one patient_key)", "F-IDENT-001"),
        metric("ID-002", "identity", "cross_source_identity_field_disagreements", identity_conflicts, "field_disagreements", "DOWN", "Sum of duplicate-MRN groups and CRM/clinical DOB, center, MRN and name/alias differences", "F-IDENT-001..005", "One patient can contribute more than one disagreement."),
        metric("QUAL-001", "quality", "open_or_investigating_deviation_pct", pct(quality["open_or_investigating"], quality["deviations_total"]), "percent", "DOWN", f"{quality['open_or_investigating']} / {quality['deviations_total']} * 100", "F-QUALITY-001", "Open status is not itself proof that a batch should be blocked."),
        metric("TRACE-001", "traceability", "unresolved_deviation_event_link_pct", pct(links["total_unresolved"], findings["F-QUALITY-001"]["value"]["deviations_total"]), "percent", "DOWN", f"{links['total_unresolved']} / {findings['F-QUALITY-001']['value']['deviations_total']} * 100", "F-QUALITY-002"),
        metric("TIME-001", "temporal", "impossible_shipment_timeline_pct", pct(findings["F-TIME-001"]["value"], 1600), "percent", "DOWN", f"{findings['F-TIME-001']['value']} / 1600 * 100", "F-TIME-001"),
        metric("TIME-002", "temporal", "maximum_event_recording_lag_hours", findings["F-TIME-003"]["value"], "hours", "OBSERVE", "MAX(recorded_at - occurred_at)", "F-TIME-003", "Lag is not automatically a defect; the projection must expose and handle it."),
        metric("ORCH-001", "orchestration", "scheduler_mes_slot_conflict_pct", pct(findings["F-INTEG-002"]["value"], 800), "percent", "DOWN", f"{findings['F-INTEG-002']['value']} / 800 * 100", "F-INTEG-002"),
        metric("ORCH-002", "orchestration", "semantic_retry_duplicate_event_count", findings["F-INTEG-001"]["value"], "events", "DOWN", "Excess MANUFACTURING_STARTED events grouped by patient,batch,type,occurred_at,payload_ref", "F-INTEG-001"),
        metric("OPS-001", "operations", "formal_shadow_priority_disagreement_pct", pct(findings["F-SHADOW-001"]["value"], 800), "percent", "DOWN", f"{findings['F-SHADOW-001']['value']} / 800 * 100", "F-SHADOW-001"),
        metric("OPS-002", "operations", "open_courier_escalation_pct", pct(courier["open"], courier["total"]), "percent", "DOWN", f"{courier['open']} / {courier['total']} * 100", "F-SHADOW-004"),
        metric("OPS-003", "operations", "unowned_courier_escalation_pct", pct(courier["unowned"], courier["total"]), "percent", "DOWN", f"{courier['unowned']} / {courier['total']} * 100", "F-SHADOW-004"),
        metric("LOG-001", "logistics", "arrival_present_while_not_delivered_pct", pct(findings["F-LOG-001"]["value"], 1600), "percent", "DOWN", f"{findings['F-LOG-001']['value']} / 1600 * 100", "F-LOG-001"),
        metric("DATA-001", "data_quality", "missing_or_warning_telemetry_point_pct", pct(thermal["missing_temperature_values"] + thermal["warning_quality_values"], 12800), "percent", "DOWN", f"({thermal['missing_temperature_values']} + {thermal['warning_quality_values']}) / 12800 * 100", "F-THERMAL-001", "Missing and WARN populations are treated as non-overlapping in the supplied data."),
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(rows[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--forensic", required=True, type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--json", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reference = read_reference(args.reference)
    reproduced = build_reproduced(finding_map(args.forensic))
    rows = reference + reproduced
    write_csv(args.csv, rows)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "supplied_not_reproduced": len(reference),
            "reproduced": len(reproduced),
            "total": len(rows),
        },
        "kpis": rows,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

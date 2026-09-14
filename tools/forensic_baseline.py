#!/usr/bin/env python3
"""Produce a reproducible forensic baseline from the immutable extracted evidence."""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any


TABLE_TO_CSV = {
    "patients": "data/raw/patients.csv",
    "collections": "data/raw/collections.csv",
    "shipments": "data/raw/shipments.csv",
    "batches": "data/raw/batches.csv",
    "qc_results": "data/raw/qc_results.csv",
    "deviations": "data/raw/deviations.csv",
    "manufacturing_slots": "data/raw/manufacturing_slots.csv",
    "consents": "data/raw/consents.csv",
    "insurance_authorizations": "data/raw/insurance_authorizations.csv",
    "cryogenic_telemetry": "data/raw/cryogenic_telemetry.csv",
    "site_qualifications": "data/raw/site_qualifications.csv",
}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def scalar(connection: sqlite3.Connection, sql: str, args: tuple[Any, ...] = ()) -> int:
    return int(connection.execute(sql, args).fetchone()[0])


def add(
    findings: list[dict[str, Any]],
    finding_id: str,
    lens: str,
    title: str,
    value: Any,
    severity: str,
    evidence: str,
    interpretation: str,
    caveat: str = "",
) -> None:
    findings.append(
        {
            "finding_id": finding_id,
            "lens": lens,
            "title": title,
            "value": value,
            "severity": severity,
            "evidence": evidence,
            "interpretation": interpretation,
            "caveat": caveat,
        }
    )


def database_csv_parity(connection: sqlite3.Connection, baseline: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for table, relative_csv in TABLE_TO_CSV.items():
        csv_rows = read_csv(baseline / relative_csv)
        db_cursor = connection.execute(f"SELECT * FROM {table}")  # table names are fixed above
        columns = [item[0] for item in db_cursor.description]
        db_rows = [dict(zip(columns, ["" if value is None else str(value) for value in row])) for row in db_cursor]
        results[table] = {
            "csv_rows": len(csv_rows),
            "db_rows": len(db_rows),
            "exact_ordered_match": csv_rows == db_rows,
        }
    return results


def build_findings(baseline: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    database = (baseline / "data/cgt_legacy.db").resolve()
    connection = sqlite3.connect(f"file:{database}?mode=ro&immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    findings: list[dict[str, Any]] = []

    counts = {
        table: scalar(connection, f"SELECT COUNT(*) FROM {table}")
        for table in TABLE_TO_CSV
    }
    parity = database_csv_parity(connection, baseline)

    duplicate_mrns = [
        dict(row)
        for row in connection.execute(
            "SELECT mrn, COUNT(*) AS count, GROUP_CONCAT(patient_key) AS patient_keys "
            "FROM patients GROUP BY mrn HAVING COUNT(*) > 1 ORDER BY mrn"
        )
    ]
    add(
        findings,
        "F-IDENT-001",
        "Inconsistency",
        "Duplicate MRNs across different patient keys",
        len(duplicate_mrns),
        "CRITICAL",
        "patients GROUP BY mrn HAVING COUNT(*) > 1",
        "MRN cannot be used as a unique cross-system identity key.",
    )

    crm = {row["patient_key"]: row for row in read_csv(baseline / "data/raw/crm_patient_export.csv")}
    clinical = {row["patient_key"]: row for row in read_csv(baseline / "data/raw/clinical_patient_export.csv")}
    identity_differences: dict[str, list[str]] = {"dob": [], "center_id": [], "mrn": [], "name_or_alias": []}
    for patient_key in sorted(set(crm) & set(clinical)):
        if crm[patient_key]["dob"] != clinical[patient_key]["dob"]:
            identity_differences["dob"].append(patient_key)
        if crm[patient_key]["center_id"] != clinical[patient_key]["center_id"]:
            identity_differences["center_id"].append(patient_key)
        if crm[patient_key]["mrn"] != clinical[patient_key]["mrn"]:
            identity_differences["mrn"].append(patient_key)
        if crm[patient_key]["synthetic_name"] != clinical[patient_key]["patient_alias"]:
            identity_differences["name_or_alias"].append(patient_key)
    for suffix, field, severity in [
        ("002", "dob", "CRITICAL"),
        ("003", "center_id", "HIGH"),
        ("004", "mrn", "CRITICAL"),
        ("005", "name_or_alias", "HIGH"),
    ]:
        add(
            findings,
            f"F-IDENT-{suffix}",
            "Inconsistency",
            f"CRM/clinical {field} disagreements",
            len(identity_differences[field]),
            severity,
            f"data/raw/crm_patient_export.csv joined to clinical_patient_export.csv on patient_key; compare {field}",
            "Identity evidence differs across source-specific views and requires explainable reconciliation.",
        )

    mes_qms_conflicts = scalar(
        connection,
        "SELECT COUNT(*) FROM batches WHERE mes_status='RELEASED' AND qms_release_status!='RELEASED'",
    )
    erp_qms_conflicts = scalar(
        connection,
        "SELECT COUNT(*) FROM batches WHERE erp_status='AVAILABLE' AND qms_release_status!='RELEASED'",
    )
    add(findings, "F-READY-001", "Inconsistency", "MES released while QMS not released", mes_qms_conflicts, "CRITICAL", "batches: mes_status='RELEASED' AND qms_release_status!='RELEASED'", "Manufacturing/MES state must not substitute for Quality release authority.")
    add(findings, "F-READY-002", "Hidden Dependency", "ERP available while QMS not released", erp_qms_conflicts, "CRITICAL", "batches: erp_status='AVAILABLE' AND qms_release_status!='RELEASED'", "Commercial/inventory availability can conceal an unmet Quality gate.")

    legacy_ready = "(p.journey_status!='ENROLLED' AND (b.mes_status IN ('MFG_COMPLETE','RELEASED') OR b.erp_status='AVAILABLE'))"
    legacy_ready_total = scalar(connection, f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) WHERE {legacy_ready}")
    ready_not_qms = scalar(connection, f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) WHERE {legacy_ready} AND b.qms_release_status!='RELEASED'")
    ready_invalid_consent = scalar(connection, f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) JOIN consents c USING(patient_key) WHERE {legacy_ready} AND c.status!='VALID'")
    ready_auth_not_approved = scalar(connection, f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) JOIN insurance_authorizations a USING(patient_key) WHERE {legacy_ready} AND a.status!='APPROVED'")
    ready_site_control_gap = scalar(connection, f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) JOIN site_qualifications q USING(center_id) WHERE {legacy_ready} AND (q.training_status='EXPIRED' OR q.equipment_status='DUE')")
    ready_slot_conflict = scalar(connection, f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) JOIN manufacturing_slots s USING(patient_key) WHERE {legacy_ready} AND s.scheduler_state='CONFIRMED' AND s.mes_state='CANCELLED'")
    ready_no_delivered_return = scalar(
        connection,
        f"SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) WHERE {legacy_ready} AND NOT EXISTS ("
        "SELECT 1 FROM shipments s WHERE s.patient_key=b.patient_key AND s.direction='RETURN' AND s.status='DELIVERED')",
    )
    legacy_breakdown = {
        "legacy_ready_total": legacy_ready_total,
        "not_qms_released": ready_not_qms,
        "invalid_consent": ready_invalid_consent,
        "authorization_not_approved": ready_auth_not_approved,
        "expired_or_due_site_controls": ready_site_control_gap,
        "confirmed_cancelled_slot": ready_slot_conflict,
        "no_delivered_return_shipment": ready_no_delivered_return,
    }
    add(findings, "F-READY-003", "Imperfection", "Journeys classified ready by unsafe legacy heuristic", legacy_breakdown, "CRITICAL", "Legacy product_ready predicate reproduced against batches and joined gate evidence", "A positive legacy readiness result does not prove patient/product readiness; multiple safety dependencies are omitted.", "Categories overlap and must not be summed.")

    infused_not_released = scalar(connection, "SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) WHERE p.journey_status='INFUSED' AND b.qms_release_status!='RELEASED'")
    infusion_ready_not_released = scalar(connection, "SELECT COUNT(*) FROM patients p JOIN batches b USING(patient_key) WHERE p.journey_status='INFUSION_READY' AND b.qms_release_status!='RELEASED'")
    add(findings, "F-READY-004", "Inconsistency", "Stored journey status ahead of Quality release", {"INFUSED": infused_not_released, "INFUSION_READY": infusion_ready_not_released}, "CRITICAL", "patients joined to batches; journey_status vs qms_release_status", "Stored journey strings cannot be trusted as authoritative gate decisions.")

    consent_counts = {row["status"]: row["count"] for row in connection.execute("SELECT status, COUNT(*) AS count FROM consents GROUP BY status")}
    auth_counts = {row["status"]: row["count"] for row in connection.execute("SELECT status, COUNT(*) AS count FROM insurance_authorizations GROUP BY status")}
    add(findings, "F-GATE-001", "Hidden Dependency", "Consent states requiring explicit gating", consent_counts, "CRITICAL", "consents grouped by status", "Withdrawn and expired-version consent cannot be ignored by downstream readiness.")
    add(findings, "F-GATE-002", "Hidden Dependency", "Authorization states requiring explicit gating", auth_counts, "HIGH", "insurance_authorizations grouped by status", "Authorization status affects scheduling and downstream commercial/process readiness.")

    deviations_total = counts["deviations"]
    deviations_open = scalar(connection, "SELECT COUNT(*) FROM deviations WHERE status IN ('OPEN','INVESTIGATING')")
    critical_open = scalar(connection, "SELECT COUNT(*) FROM deviations WHERE status IN ('OPEN','INVESTIGATING') AND severity='CRITICAL'")
    released_with_open = scalar(connection, "SELECT COUNT(*) FROM deviations d JOIN batches b USING(batch_id) WHERE d.status IN ('OPEN','INVESTIGATING') AND b.qms_release_status='RELEASED'")
    blank_links = scalar(connection, "SELECT COUNT(*) FROM deviations WHERE linked_event_id IS NULL OR TRIM(linked_event_id)='' ")
    events_path = baseline / "data/raw/events.jsonl"
    events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    event_ids = {event["event_id"] for event in events}
    linked_values = [row[0] for row in connection.execute("SELECT linked_event_id FROM deviations")]
    nonblank_missing = sum(1 for value in linked_values if value and value.strip() and value not in event_ids)
    add(findings, "F-QUALITY-001", "Complexity", "Open/investigating deviations and Quality-release coexistence", {"deviations_total": deviations_total, "open_or_investigating": deviations_open, "critical_open_or_investigating": critical_open, "on_qms_released_batches": released_with_open}, "CRITICAL", "deviations joined to batches", "Open deviations require blocking classification and disposition evidence; open status alone does not prove every release invalid.")
    add(findings, "F-QUALITY-002", "Imperfection", "Deviation links do not resolve to the event log", {"blank": blank_links, "nonblank_missing": nonblank_missing, "total_unresolved": blank_links + nonblank_missing}, "HIGH", "deviations.linked_event_id checked against events.jsonl event_id", "Quality investigations lack resolvable event evidence.")

    qms_released_with_nonpass_qc = scalar(
        connection,
        "SELECT COUNT(DISTINCT b.batch_id) FROM batches b JOIN qc_results q USING(batch_id) "
        "WHERE b.qms_release_status='RELEASED' AND q.result IN ('PENDING','OOS','OOT')",
    )
    add(findings, "F-QUALITY-003", "Uncertainty", "QMS-released batches with pending/OOS/OOT QC rows", qms_released_with_nonpass_qc, "HIGH", "batches joined to qc_results; qms release with result in PENDING/OOS/OOT", "Explicit assay disposition evidence is required before interpreting these rows.")

    site_control_gaps = scalar(connection, "SELECT COUNT(*) FROM site_qualifications WHERE training_status='EXPIRED' OR equipment_status='DUE'")
    add(findings, "F-SITE-001", "Hidden Dependency", "Treatment centers with expired training or due equipment", site_control_gaps, "HIGH", "site_qualifications control fields", "High-level site status can obscure detailed qualification controls.")

    impossible_shipments = scalar(connection, "SELECT COUNT(*) FROM shipments WHERE arrived_at!='' AND departed_at!='' AND arrived_at < departed_at")
    add(findings, "F-TIME-001", "Inconsistency", "Shipments arriving before departure", impossible_shipments, "HIGH", "shipments arrived_at < departed_at", "Physical event ordering contradicts recorded shipment timestamps.")

    by_patient: dict[str, list[dict[str, Any]]] = defaultdict(list)
    max_lag_seconds = 0.0
    for event in events:
        by_patient[event["patient_key"]].append(event)
        lag = (parse_time(event["recorded_at"]) - parse_time(event["occurred_at"])).total_seconds()
        max_lag_seconds = max(max_lag_seconds, lag)
    inverted_patients: list[str] = []
    for patient_key, patient_events in by_patient.items():
        ordered = sorted(patient_events, key=lambda item: parse_time(item["recorded_at"]))
        if any(parse_time(current["occurred_at"]) < parse_time(previous["occurred_at"]) for previous, current in zip(ordered, ordered[1:])):
            inverted_patients.append(patient_key)
    add(findings, "F-TIME-002", "Volatility", "Patient histories whose recorded order inverts occurrence order", len(inverted_patients), "HIGH", "events grouped by patient and sorted by recorded_at; adjacent occurred_at inversion", "Recorded order and physical occurrence order are separate concepts.")
    add(findings, "F-TIME-003", "Uncertainty", "Maximum event recording lag in hours", max_lag_seconds / 3600.0, "MEDIUM", "max(recorded_at - occurred_at) across events.jsonl", "Late-arriving evidence can change a derived journey view.")

    duplicate_groups: dict[tuple[str, str, str, str, str], int] = Counter()
    for event in events:
        if event["event_type"] == "MANUFACTURING_STARTED":
            key = (event["patient_key"], event.get("batch_id", ""), event["event_type"], event["occurred_at"], event["payload_ref"])
            duplicate_groups[key] += 1
    duplicate_excess = sum(count - 1 for count in duplicate_groups.values() if count > 1)
    add(findings, "F-INTEG-001", "Imperfection", "Retry-duplicate manufacturing-start events", duplicate_excess, "HIGH", "events grouped on patient,batch,type,occurred_at,payload_ref", "New event identifiers do not guarantee semantic uniqueness or idempotency.")

    slot_conflicts = scalar(connection, "SELECT COUNT(*) FROM manufacturing_slots WHERE scheduler_state='CONFIRMED' AND mes_state='CANCELLED'")
    add(findings, "F-INTEG-002", "Inconsistency", "Scheduler-confirmed slots cancelled in MES", slot_conflicts, "HIGH", "manufacturing_slots scheduler_state vs mes_state", "Partial distributed state and absent compensation create unreliable capacity state.")

    formal_slots = {row["patient_key"]: row for row in read_csv(baseline / "data/raw/manufacturing_slots.csv")}
    shadow_priorities = {row["patient_key"]: row for row in read_csv(baseline / "shadow_ops/PatientPriority_MASTER.csv")}
    priority_disagreements = sum(1 for key in set(formal_slots) & set(shadow_priorities) if formal_slots[key]["priority"] != shadow_priorities[key]["priority"])
    shadow_slots = read_csv(baseline / "shadow_ops/ManufacturingSlots_FINAL_v7.csv")
    planner_notes = sum(1 for row in shadow_slots if row.get("planner_note", "").strip())
    add(findings, "F-SHADOW-001", "Friction", "Formal vs shadow patient-priority disagreements", priority_disagreements, "HIGH", "manufacturing_slots.csv joined to PatientPriority_MASTER.csv on patient_key", "Operational priority is being maintained outside the formal scheduling view.")
    add(findings, "F-SHADOW-002", "Hidden Dependency", "Manufacturing-slot rows containing planner override notes", planner_notes, "MEDIUM", "ManufacturingSlots_FINAL_v7.csv planner_note nonblank", "Email/manual decisions create downstream dependencies not represented as governed transactions.")

    email_subject_counts: Counter[str] = Counter()
    for path in sorted((baseline / "shadow_ops/emails").glob("*.eml")):
        message = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
        subject = str(message.get("Subject", ""))
        category = subject.split("[")[0].strip()
        email_subject_counts[category] += 1
    add(findings, "F-SHADOW-003", "Friction", "Shadow email categories", dict(sorted(email_subject_counts.items())), "HIGH", "Subject lines across shadow_ops/emails/*.eml", "Unstructured email carries slot, courier, identity, Quality and site-readiness coordination.")

    courier = read_csv(baseline / "shadow_ops/CourierEscalations.csv")
    courier_summary = {
        "total": len(courier),
        "open": sum(1 for row in courier if row["status"] == "OPEN"),
        "unowned": sum(1 for row in courier if not row["owner"].strip()),
    }
    add(findings, "F-SHADOW-004", "Friction", "Courier escalations requiring closed-loop ownership", courier_summary, "HIGH", "CourierEscalations.csv status and owner", "Open or unowned escalation work can delay patient/material movement without accountable resolution.")

    temp_flagged = scalar(connection, "SELECT COUNT(*) FROM shipments WHERE temp_excursion='TRUE'")
    telemetry_over = scalar(connection, "SELECT COUNT(DISTINCT shipment_id) FROM cryogenic_telemetry WHERE CAST(temperature_c AS REAL) > -120.0 AND TRIM(temperature_c)!=''")
    flagged_without_over = scalar(
        connection,
        "SELECT COUNT(*) FROM shipments s WHERE s.temp_excursion='TRUE' AND NOT EXISTS ("
        "SELECT 1 FROM cryogenic_telemetry t WHERE t.shipment_id=s.shipment_id AND TRIM(t.temperature_c)!='' AND CAST(t.temperature_c AS REAL)>-120.0)",
    )
    missing_temp = scalar(connection, "SELECT COUNT(*) FROM cryogenic_telemetry WHERE temperature_c IS NULL OR TRIM(temperature_c)='' ")
    warning_temp = scalar(connection, "SELECT COUNT(*) FROM cryogenic_telemetry WHERE quality='WARN'")
    add(findings, "F-THERMAL-001", "Uncertainty", "Telemetry and excursion evidence requiring contextual disposition", {"shipments_flagged": temp_flagged, "shipments_with_point_above_minus_120_c": telemetry_over, "flagged_without_point_above_minus_120_c": flagged_without_over, "missing_temperature_values": missing_temp, "warning_quality_values": warning_temp}, "HIGH", "shipments joined conceptually to cryogenic_telemetry", "A point threshold is insufficient; effective SOP v7 requires duration, quality, cumulative profile, shipper integrity and human Quality review.")

    status_with_arrival = scalar(connection, "SELECT COUNT(*) FROM shipments WHERE arrived_at!='' AND status IN ('BOOKED','IN_TRANSIT')")
    add(findings, "F-LOG-001", "Inconsistency", "Booked/in-transit shipments with arrival timestamps", status_with_arrival, "HIGH", "shipments status IN (BOOKED,IN_TRANSIT) with arrived_at populated", "Shipment state and event evidence disagree; neither should be silently preferred.")

    event_type_counts = Counter(event["event_type"] for event in events)
    add(findings, "F-EVENT-001", "Unknown Unknown", "Event model covers only a narrow set of business events", {"distinct_types": len(event_type_counts), "types": dict(sorted(event_type_counts.items()))}, "HIGH", "events.jsonl event_type", "Consent, authorization, site qualification, slot, QC, deviation, QA release, conditioning and infusion are not first-class events.")

    connection.close()
    detail = {
        "table_counts": counts,
        "database_csv_parity": parity,
        "duplicate_mrns": duplicate_mrns,
        "identity_difference_patient_keys": identity_differences,
        "event_count": len(events),
        "inverted_event_order_patient_keys": sorted(inverted_patients),
    }
    return findings, detail


def write_markdown(path: Path, findings: list[dict[str, Any]], detail: dict[str, Any], source: Path) -> None:
    lines = [
        "# Stage 2 - Reproducible Forensic Baseline",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}  ",
        f"**Source:** `{source}` opened read-only with SQLite `mode=ro&immutable=1`  ",
        "**Status:** Measured baseline; interpretation remains subject to domain-owner review",
        "",
        "## Dataset counts",
        "",
        "| Table | Rows | Raw CSV exact ordered match |",
        "|---|---:|---|",
    ]
    for table, count in detail["table_counts"].items():
        match = detail["database_csv_parity"][table]["exact_ordered_match"]
        lines.append(f"| `{table}` | {count} | {'YES' if match else 'NO'} |")
    lines.extend(
        [
            "",
            "The SQLite database is a materialization of the eleven corresponding raw CSVs, not an independent corroborating source.",
            "",
            "## Findings",
            "",
            "| ID | Lens | Severity | Finding | Measured value |",
            "|---|---|---|---|---|",
        ]
    )
    for finding in findings:
        value = json.dumps(finding["value"], sort_keys=True).replace("|", "\\|")
        lines.append(f"| {finding['finding_id']} | {finding['lens']} | {finding['severity']} | {finding['title']} | `{value}` |")
    lines.extend(["", "## Evidence and interpretation", ""])
    for finding in findings:
        lines.extend(
            [
                f"### {finding['finding_id']} - {finding['title']}",
                "",
                f"- **Lens:** {finding['lens']}",
                f"- **Severity:** {finding['severity']}",
                f"- **Measured value:** `{json.dumps(finding['value'], sort_keys=True)}`",
                f"- **Evidence method:** `{finding['evidence']}`",
                f"- **Interpretation:** {finding['interpretation']}",
            ]
        )
        if finding["caveat"]:
            lines.append(f"- **Caveat:** {finding['caveat']}")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--markdown", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    baseline = args.baseline.resolve()
    findings, detail = build_findings(baseline)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_baseline": str(baseline),
        "findings": findings,
        "detail": detail,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_markdown(args.markdown, findings, detail, baseline)
    print(json.dumps({"status": "PASS", "findings": len(findings), "output": str(args.markdown)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

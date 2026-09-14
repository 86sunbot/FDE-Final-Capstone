#!/usr/bin/env python3
"""Profile the immutable CGT baseline without changing source evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


KEYS: dict[str, tuple[str, ...]] = {
    "data/raw/batches.csv": ("batch_id",),
    "data/raw/clinical_patient_export.csv": ("patient_key",),
    "data/raw/collections.csv": ("collection_id",),
    "data/raw/consents.csv": ("consent_id",),
    "data/raw/crm_patient_export.csv": ("patient_key",),
    "data/raw/cryogenic_telemetry.csv": ("shipment_id", "sensor_id", "timestamp"),
    "data/raw/deviations.csv": ("deviation_id",),
    "data/raw/insurance_authorizations.csv": ("auth_id",),
    "data/raw/manufacturing_slots.csv": ("slot_id",),
    "data/raw/patients.csv": ("patient_key",),
    "data/raw/qc_results.csv": ("qc_id",),
    "data/raw/shipments.csv": ("shipment_id",),
    "data/raw/site_qualifications.csv": ("center_id",),
    "data/reference/baseline_kpis.csv": ("metric",),
    "data/reference/couriers.csv": ("courier_id",),
    "data/reference/manufacturing_sites.csv": ("site_id",),
    "data/reference/products.csv": ("product_code",),
    "data/reference/treatment_centers.csv": ("center_id",),
    "evals/cases.csv": ("case_id",),
    "scenarios/inject_catalog.csv": ("inject_id",),
    "shadow_ops/CourierEscalations.csv": ("shipment_id", "issue"),
    "shadow_ops/ManufacturingSlots_FINAL_v7.csv": ("slot_id",),
    "shadow_ops/PatientPriority_MASTER.csv": ("patient_key",),
}

NUMERIC_FIELDS: dict[str, tuple[str, ...]] = {
    "data/raw/collections.csv": ("volume_ml", "cell_count_10e9", "viability_pct"),
    "data/raw/cryogenic_telemetry.csv": ("temperature_c",),
    "data/raw/manufacturing_slots.csv": ("priority",),
    "data/reference/baseline_kpis.csv": ("baseline",),
    "data/reference/couriers.csv": ("sla_hours",),
    "data/reference/manufacturing_sites.csv": ("suites", "qc_capacity_day"),
    "data/reference/treatment_centers.csv": ("cryogenic_capacity", "apheresis_chairs"),
    "shadow_ops/ManufacturingSlots_FINAL_v7.csv": ("priority",),
    "shadow_ops/PatientPriority_MASTER.csv": ("priority",),
}

TEMPORAL_NAMES = {
    "dob",
    "timestamp",
    "scheduled_start",
    "mfg_start",
    "mfg_end",
    "collection_time",
    "qualified_until",
    "valid_until",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def parse_temporal(value: str) -> datetime:
    normalized = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def is_temporal_field(name: str) -> bool:
    return name in TEMPORAL_NAMES or name.endswith("_at") or name.endswith("_time")


def duplicate_groups(rows: list[dict[str, str]], keys: tuple[str, ...]) -> tuple[int, int]:
    counts = Counter(tuple(row.get(key, "") for key in keys) for row in rows)
    duplicates = [count for values, count in counts.items() if count > 1 and any(values)]
    return len(duplicates), sum(count - 1 for count in duplicates)


def profile_csv(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    columns, rows = read_csv(path)
    null_counts = {column: sum(not row.get(column, "").strip() for row in rows) for column in columns}
    key = KEYS[relative]
    dup_groups, duplicate_rows = duplicate_groups(rows, key)

    temporal: dict[str, Any] = {}
    for column in columns:
        if not is_temporal_field(column):
            continue
        parsed: list[datetime] = []
        invalid = 0
        for row in rows:
            value = row.get(column, "").strip()
            if not value:
                continue
            try:
                parsed.append(parse_temporal(value))
            except ValueError:
                invalid += 1
        temporal[column] = {
            "nonempty": len(parsed) + invalid,
            "invalid": invalid,
            "min": min(parsed).isoformat() if parsed else None,
            "max": max(parsed).isoformat() if parsed else None,
        }

    numeric: dict[str, Any] = {}
    for column in NUMERIC_FIELDS.get(relative, ()):
        values: list[float] = []
        invalid = 0
        for row in rows:
            value = row.get(column, "").strip()
            if not value:
                continue
            try:
                values.append(float(value))
            except ValueError:
                invalid += 1
        numeric[column] = {
            "nonempty": len(values) + invalid,
            "invalid": invalid,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
        }

    return {
        "path": relative,
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
        "rows": len(rows),
        "columns": columns,
        "declared_profile_key": list(key),
        "duplicate_key_groups": dup_groups,
        "excess_duplicate_rows": duplicate_rows,
        "null_counts": null_counts,
        "total_null_cells": sum(null_counts.values()),
        "temporal_fields": temporal,
        "numeric_fields": numeric,
    }


def ids(rows: Iterable[dict[str, str]], field: str) -> set[str]:
    return {row[field] for row in rows if row.get(field)}


def missing_reference(rows: Iterable[dict[str, str]], field: str, target: set[str], allow_blank: bool = False) -> int:
    return sum(
        1
        for row in rows
        if ((not row.get(field)) and not allow_blank) or (row.get(field) and row[field] not in target)
    )


def relation(name: str, count: int, meaning: str, expected: str = "0") -> dict[str, Any]:
    return {"relationship": name, "issue_count": count, "expected": expected, "meaning": meaning}


def relationship_profile(root: Path) -> list[dict[str, Any]]:
    def rows(relative: str) -> list[dict[str, str]]:
        return read_csv(root / relative)[1]

    patients = rows("data/raw/patients.csv")
    patient_ids = ids(patients, "patient_key")
    collections = rows("data/raw/collections.csv")
    collection_ids = ids(collections, "collection_id")
    collection_by_id = {row["collection_id"]: row for row in collections}
    batches = rows("data/raw/batches.csv")
    batch_ids = ids(batches, "batch_id")
    batch_by_id = {row["batch_id"]: row for row in batches}
    shipments = rows("data/raw/shipments.csv")
    shipment_ids = ids(shipments, "shipment_id")
    shipment_by_id = {row["shipment_id"]: row for row in shipments}
    events = [json.loads(line) for line in (root / "data/raw/events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    event_ids = ids(events, "event_id")
    centers = ids(rows("data/reference/treatment_centers.csv"), "center_id")
    manufacturing_sites = ids(rows("data/reference/manufacturing_sites.csv"), "site_id")
    products = ids(rows("data/reference/products.csv"), "product_code")
    couriers = ids(rows("data/reference/couriers.csv"), "courier_id")

    result = [
        relation("collection.patient_key -> patient", missing_reference(collections, "patient_key", patient_ids), "Collection patient reference resolves"),
        relation("batch.patient_key -> patient", missing_reference(batches, "patient_key", patient_ids), "Batch patient reference resolves"),
        relation("batch.collection_id -> collection", missing_reference(batches, "collection_id", collection_ids), "Batch collection reference resolves"),
        relation("shipment.patient_key -> patient", missing_reference(shipments, "patient_key", patient_ids), "Shipment patient reference resolves"),
        relation("return_shipment.batch_id -> batch", missing_reference([row for row in shipments if row["direction"] == "RETURN"], "batch_id", batch_ids), "Return shipment batch reference resolves"),
        relation("qc.batch_id -> batch", missing_reference(rows("data/raw/qc_results.csv"), "batch_id", batch_ids), "QC batch reference resolves"),
        relation("deviation.batch_id -> batch", missing_reference(rows("data/raw/deviations.csv"), "batch_id", batch_ids), "Deviation batch reference resolves"),
        relation("slot.patient_key -> patient", missing_reference(rows("data/raw/manufacturing_slots.csv"), "patient_key", patient_ids), "Slot patient reference resolves"),
        relation("consent.patient_key -> patient", missing_reference(rows("data/raw/consents.csv"), "patient_key", patient_ids), "Consent patient reference resolves"),
        relation("authorization.patient_key -> patient", missing_reference(rows("data/raw/insurance_authorizations.csv"), "patient_key", patient_ids), "Authorization patient reference resolves"),
        relation("telemetry.shipment_id -> shipment", missing_reference(rows("data/raw/cryogenic_telemetry.csv"), "shipment_id", shipment_ids), "Telemetry shipment reference resolves"),
        relation("event.patient_key -> patient", missing_reference(events, "patient_key", patient_ids), "Event patient reference resolves"),
        relation("event.batch_id -> batch", missing_reference(events, "batch_id", batch_ids, allow_blank=True), "Nonblank event batch reference resolves"),
        relation("deviation.linked_event_id -> event", missing_reference(rows("data/raw/deviations.csv"), "linked_event_id", event_ids), "Deviation evidence link resolves"),
        relation("patient.center_id -> treatment_center", missing_reference(patients, "center_id", centers), "Patient center reference resolves"),
        relation("site_qualification.center_id -> treatment_center", missing_reference(rows("data/raw/site_qualifications.csv"), "center_id", centers), "Qualification center reference resolves"),
        relation("batch.site_id -> manufacturing_site", missing_reference(batches, "site_id", manufacturing_sites), "Batch site reference resolves"),
        relation("slot.site_id -> manufacturing_site", missing_reference(rows("data/raw/manufacturing_slots.csv"), "site_id", manufacturing_sites), "Slot site reference resolves"),
        relation("shipment.courier_id -> courier", missing_reference(shipments, "courier_id", couriers), "Courier reference resolves"),
        relation("patient.product_code -> product", missing_reference(patients, "product_code", products), "Patient product reference resolves"),
        relation("batch.product_code -> product", missing_reference(batches, "product_code", products), "Batch product reference resolves"),
    ]

    batch_collection_patient_mismatch = 0
    batch_collection_coi_mismatch = 0
    for batch in batches:
        collection = collection_by_id.get(batch["collection_id"])
        if collection and collection["patient_key"] != batch["patient_key"]:
            batch_collection_patient_mismatch += 1
        if collection and collection["coi_id"] != batch["coi_id"]:
            batch_collection_coi_mismatch += 1
    result.extend(
        [
            relation("batch.patient_key = collection.patient_key", batch_collection_patient_mismatch, "Declared linkage fields agree; not independent identity proof"),
            relation("batch.coi_id = collection.coi_id", batch_collection_coi_mismatch, "Declared COI strings agree; not independent COI proof"),
        ]
    )

    telemetry_patient_mismatch = 0
    telemetry_direction_mismatch = 0
    for row in rows("data/raw/cryogenic_telemetry.csv"):
        shipment = shipment_by_id.get(row["shipment_id"])
        if shipment and shipment["patient_key"] != row["patient_key"]:
            telemetry_patient_mismatch += 1
        if shipment and shipment["direction"] != row["direction"]:
            telemetry_direction_mismatch += 1
    result.extend(
        [
            relation("telemetry.patient_key = shipment.patient_key", telemetry_patient_mismatch, "Telemetry and shipment patient-key strings agree"),
            relation("telemetry.direction = shipment.direction", telemetry_direction_mismatch, "Telemetry and shipment direction agree"),
        ]
    )

    return result


def profile_events(root: Path) -> dict[str, Any]:
    path = root / "data/raw/events.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    event_ids = Counter(row.get("event_id", "") for row in rows)
    invalid_json_required = sum(
        any(not row.get(field) for field in ("event_id", "patient_key", "event_type", "source", "occurred_at", "recorded_at"))
        for row in rows
    )
    negative_lag = 0
    lags: list[float] = []
    for row in rows:
        occurred = parse_temporal(row["occurred_at"])
        recorded = parse_temporal(row["recorded_at"])
        lag = (recorded - occurred).total_seconds() / 3600
        lags.append(lag)
        if lag < 0:
            negative_lag += 1
    semantic = Counter(
        (row.get("patient_key"), row.get("batch_id"), row.get("event_type"), row.get("occurred_at"), row.get("payload_ref"))
        for row in rows
    )
    return {
        "path": "data/raw/events.jsonl",
        "sha256": sha256(path),
        "rows": len(rows),
        "event_types": dict(sorted(Counter(row["event_type"] for row in rows).items())),
        "sources": dict(sorted(Counter(row["source"] for row in rows).items())),
        "duplicate_event_id_groups": sum(count > 1 for count in event_ids.values()),
        "excess_semantic_duplicate_rows": sum(count - 1 for count in semantic.values() if count > 1),
        "missing_required_field_rows": invalid_json_required,
        "negative_recording_lag_rows": negative_lag,
        "max_recording_lag_hours": max(lags) if lags else None,
        "occurred_at_min": min(row["occurred_at"] for row in rows),
        "occurred_at_max": max(row["occurred_at"] for row in rows),
    }


def profile_emails(root: Path) -> dict[str, Any]:
    paths = sorted((root / "shadow_ops/emails").glob("*.eml"))
    required_headers = ("From:", "To:", "Date:", "Subject:")
    missing = 0
    subjects: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if any(header not in text for header in required_headers):
            missing += 1
        subject = next((line.partition(":")[2].strip() for line in text.splitlines() if line.startswith("Subject:")), "")
        subjects.append(subject)
    return {
        "files": len(paths),
        "missing_required_header_files": missing,
        "subjects": subjects,
        "classification": "synthetic_untrusted_shadow_operations_evidence",
    }


def knowledge_inventory(root: Path) -> list[dict[str, Any]]:
    patterns = [
        "docs/**/*.md",
        "contracts/*.yaml",
        "evals/*",
        "scenarios/*",
        "participant/*.md",
        "README.md",
        "VERIFICATION.md",
        "LICENSE-SYNTHETIC-TRAINING.txt",
        "AGENTS.md",
    ]
    files = sorted({path for pattern in patterns for path in root.glob(pattern) if path.is_file()})
    result = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("#")), path.name)
        status_match = re.search(r"(?im)^Status:\s*(.+)$", text)
        effective_match = re.search(r"(?im)^Effective:\s*(.+)$", text)
        result.append(
            {
                "path": relative,
                "sha256": sha256(path),
                "title": title,
                "status": status_match.group(1).strip() if status_match else "NOT_STATED",
                "effective": effective_match.group(1).strip() if effective_match else "NOT_STATED",
                "role": (
                    "controlled_rule_evidence"
                    if relative.startswith("docs/sops/")
                    else "interface_evidence"
                    if relative.startswith("contracts/")
                    else "evaluation_evidence"
                    if relative.startswith("evals/") or relative.startswith("scenarios/")
                    else "context_or_requirement_evidence"
                ),
            }
        )
    return result


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    output = args.output_dir.resolve()

    csv_profiles = [profile_csv(source, relative) for relative in sorted(KEYS)]
    relations = relationship_profile(source)
    events = profile_events(source)
    emails = profile_emails(source)
    knowledge = knowledge_inventory(source)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "source_zip_sha256": "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979",
        "summary": {
            "csv_datasets": len(csv_profiles),
            "csv_rows": sum(profile["rows"] for profile in csv_profiles),
            "duplicate_key_groups": sum(profile["duplicate_key_groups"] for profile in csv_profiles),
            "relationship_checks": len(relations),
            "relationship_issues": sum(row["issue_count"] for row in relations),
            "knowledge_items": len(knowledge),
            "event_rows": events["rows"],
            "event_types": len(events["event_types"]),
            "email_files": emails["files"],
        },
        "csv_profiles": csv_profiles,
        "relationships": relations,
        "events": events,
        "emails": emails,
        "knowledge": knowledge,
    }

    output.mkdir(parents=True, exist_ok=True)
    (output / "data_knowledge_profile.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_csv(
        output / "dataset_profile.csv",
        [
            {
                "path": row["path"],
                "rows": row["rows"],
                "columns": len(row["columns"]),
                "key": ";".join(row["declared_profile_key"]),
                "duplicate_key_groups": row["duplicate_key_groups"],
                "excess_duplicate_rows": row["excess_duplicate_rows"],
                "total_null_cells": row["total_null_cells"],
                "invalid_temporal_values": sum(value["invalid"] for value in row["temporal_fields"].values()),
                "invalid_declared_numeric_values": sum(value["invalid"] for value in row["numeric_fields"].values()),
                "sha256": row["sha256"],
            }
            for row in csv_profiles
        ],
        ["path", "rows", "columns", "key", "duplicate_key_groups", "excess_duplicate_rows", "total_null_cells", "invalid_temporal_values", "invalid_declared_numeric_values", "sha256"],
    )
    write_csv(output / "relationship_profile.csv", relations, ["relationship", "issue_count", "expected", "meaning"])
    write_csv(output / "knowledge_inventory.csv", knowledge, ["path", "sha256", "title", "status", "effective", "role"])
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Non-authoritative, source-backed previews for the ten supplied injects.

The challenge injects do not identify a patient, a date, capacity constraints,
carrier alternatives, or controlled scheduling policy. A caller supplies a
representative synthetic patient. Any time shift is an explicit zero-slack
assumption, never a committed plan or clinical/Quality disposition.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from .source_cases import BASELINE, _rows

OWNERS = {
    "INJ-001": "CLINICAL_OPERATIONS_AND_PLANNER",
    "INJ-002": "LOGISTICS_AND_QUALITY",
    "INJ-003": "MANUFACTURING_PLANNER",
    "INJ-004": "QC_AND_QUALITY",
    "INJ-005": "TREATMENT_CENTER_AND_CLINICAL_OPERATIONS",
    "INJ-006": "MANUFACTURING_PLANNER_AND_INTEGRATION_OWNER",
    "INJ-007": "IDENTITY_AUTHORITY",
    "INJ-008": "LOGISTICS_OWNER",
    "INJ-009": "QUALITY_AND_QMS_SERVICE_OWNER",
    "INJ-010": "PAYER_AND_CLINICAL_OPERATIONS",
}

PROPAGATION = {
    "INJ-001": ("collection", "outbound_logistics", "slot", "manufacturing", "qc", "qa_release", "return_logistics", "conditioning", "infusion"),
    "INJ-002": ("outbound_logistics", "return_logistics", "qc", "qa_release"),
    "INJ-003": ("slot", "manufacturing", "qc", "qa_release", "return_logistics", "conditioning", "infusion"),
    "INJ-004": ("qc", "qa_release", "return_logistics", "conditioning", "infusion"),
    "INJ-005": ("site_qualification", "collection", "outbound_logistics", "slot"),
    "INJ-006": ("slot", "manufacturing"),
    "INJ-007": ("identity", "collection", "outbound_logistics", "slot"),
    "INJ-008": ("outbound_logistics", "slot", "manufacturing", "qc", "qa_release", "return_logistics", "conditioning", "infusion"),
    "INJ-009": ("qa_release", "return_logistics", "conditioning", "infusion"),
    "INJ-010": ("authorization", "collection", "outbound_logistics", "slot"),
}

DELAY_HOURS = {"INJ-001": 5, "INJ-003": 18, "INJ-004": 36, "INJ-009": 4}


def _parse(value: str) -> datetime | None:
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def _stamp(value: str, hours: int | None) -> str | None:
    parsed = _parse(value)
    if parsed is None or hours is None:
        return None
    return (parsed + timedelta(hours=hours)).isoformat().replace("+00:00", "Z")


def list_injects(baseline: Path = BASELINE) -> list[dict]:
    return [
        {
            "inject_id": item["row"]["inject_id"],
            "name": item["row"]["name"],
            "trigger": item["row"]["trigger"],
            "severity": item["row"]["severity"],
        }
        for item in _rows(baseline / "scenarios" / "inject_catalog.csv", baseline)
    ]


def preview_inject(inject_id: str, patient_key: str = "P-00001", baseline: Path = BASELINE) -> dict:
    inject = next(
        (item for item in _rows(baseline / "scenarios" / "inject_catalog.csv", baseline)
         if item["row"]["inject_id"] == inject_id),
        None,
    )
    if inject is None:
        raise KeyError(inject_id)

    raw = baseline / "data" / "raw"
    def patient_rows(name: str) -> list[dict]:
        return [item for item in _rows(raw / name, baseline) if item["row"].get("patient_key") == patient_key]

    patient = patient_rows("patients.csv")
    if not patient:
        raise KeyError(patient_key)
    collection = patient_rows("collections.csv")
    shipments = patient_rows("shipments.csv")
    slot = patient_rows("manufacturing_slots.csv")
    batch = patient_rows("batches.csv")
    qc = [
        item for item in _rows(raw / "qc_results.csv", baseline)
        if batch and item["row"]["batch_id"] == batch[0]["row"]["batch_id"]
    ]

    outbound = next((item for item in shipments if item["row"]["direction"] == "OUTBOUND"), None)
    returned = next((item for item in shipments if item["row"]["direction"] == "RETURN"), None)
    latest_qc = max(qc, key=lambda item: item["row"].get("reported_at", "")) if qc else None
    milestone_rows = {
        "collection": (collection[0] if collection else None, "collection_time"),
        "outbound_logistics": (outbound, "arrived_at"),
        "slot": (slot[0] if slot else None, "scheduled_start"),
        "manufacturing": (batch[0] if batch else None, "mfg_end"),
        "qc": (latest_qc, "reported_at"),
        "qa_release": (None, ""),
        "return_logistics": (returned, "arrived_at"),
        "conditioning": (None, ""),
        "infusion": (None, ""),
    }
    hours = DELAY_HOURS.get(inject_id)
    impact: list[dict] = []
    for milestone in PROPAGATION.get(inject_id, tuple(part.strip() for part in inject["row"]["affected"].split(";"))):
        item, time_field = milestone_rows.get(milestone, (None, ""))
        baseline_time = item["row"].get(time_field, "") if item else ""
        impact.append({
            "milestone": milestone,
            "source_time": baseline_time or None,
            "hypothetical_zero_slack_time": _stamp(baseline_time, hours),
            "source_locator": item["source_locator"] if item else None,
            "status": "AT_RISK_PREVIEW" if item else "UNQUANTIFIED_DEPENDENCY",
        })

    affected_routes = [
        {
            "shipment_id": item["row"]["shipment_id"],
            "direction": item["row"]["direction"],
            "origin": item["row"]["origin"],
            "destination": item["row"]["destination"],
            "source_locator": item["source_locator"],
            "delivery_assurance": "UNKNOWN_AFTER_INJECT",
        }
        for item in shipments
    ] if inject_id == "INJ-008" else []

    affected_reservations: list[dict] = []
    if inject_id == "INJ-003" and slot:
        site = slot[0]["row"]["site_id"]
        start = _parse(slot[0]["row"]["scheduled_start"])
        end = start + timedelta(hours=18) if start else None
        for item in _rows(raw / "manufacturing_slots.csv", baseline):
            scheduled = _parse(item["row"]["scheduled_start"])
            if item["row"]["site_id"] == site and start and end and scheduled and start <= scheduled < end:
                affected_reservations.append({
                    "slot_id": item["row"]["slot_id"],
                    "patient_key": item["row"]["patient_key"],
                    "state": "EXCEPTION_PREVIEW_NOT_COMMITTED",
                    "owner": OWNERS[inject_id],
                    "source_locator": item["source_locator"],
                })

    return {
        "scope": "FROZEN_V2_SOURCE_SCENARIO_PREVIEW_NOT_EXECUTED",
        "inject_id": inject_id,
        "name": inject["row"]["name"],
        "trigger": inject["row"]["trigger"],
        "severity": inject["row"]["severity"],
        "affected_declared": inject["row"]["affected"].split(";"),
        "representative_patient_key": patient_key,
        "representative_patient_source": patient[0]["source_locator"],
        "inject_source_locator": inject["source_locator"],
        "owner_role": OWNERS[inject_id],
        "impact_preview": impact,
        "affected_routes": affected_routes,
        "affected_reservations": affected_reservations,
        "delay_hours_from_stimulus": hours,
        "assumptions": [
            "The source inject has no patient/date; this patient is a representative synthetic selection.",
            "Any shifted timestamp assumes zero slack and no capacity/route/clinical-policy adjustment; it is not a forecast or approved plan.",
            "Unknown downstream milestone times remain unknown; no delivery or product-disposition assurance is invented.",
        ],
        "required_next_step": "OWNER_REVIEW_AND_EVIDENCE_RECONCILIATION",
        "side_effects": 0,
        "production_authorized": False,
    }

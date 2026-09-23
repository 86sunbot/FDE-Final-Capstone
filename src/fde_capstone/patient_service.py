"""Patient operations and centralized status tracking service.

Parses brownfield baseline CSV evidence to provide multi-dimensional journey
tracking, strict Quality release readiness verification, and QA hold detection
without fabricating missing historical timestamps or CAPA ground truth.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .source_cases import RAW


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.DictReader(stream) if any(row.values())]

PHASE_CONFIG: dict[str, dict[str, Any]] = {
    "ELIGIBLE": {"step": 1, "display": "Eligible for Enrollment", "badge_class": "phase-enrolled", "is_active": True},
    "ENROLLED": {"step": 1, "display": "Enrollment & Eligibility", "badge_class": "phase-enrolled", "is_active": True},
    "APHERESIS_PENDING": {"step": 2, "display": "Apheresis Scheduled", "badge_class": "phase-apheresis", "is_active": True},
    "COLLECTED": {"step": 3, "display": "Collected & Outbound", "badge_class": "phase-collected", "is_active": True},
    "IN_TRANSIT": {"step": 3, "display": "In Transit to CDMO", "badge_class": "phase-collected", "is_active": True},
    "RECEIVED": {"step": 4, "display": "Received at CDMO", "badge_class": "phase-mfg", "is_active": True},
    "IN_MANUFACTURING": {"step": 4, "display": "In Manufacturing", "badge_class": "phase-mfg", "is_active": True},
    "QC_PENDING": {"step": 5, "display": "QC & Release Review", "badge_class": "phase-qc", "is_active": True},
    "RELEASED": {"step": 6, "display": "Quality Released", "badge_class": "phase-released", "is_active": True},
    "RETURN_TRANSIT": {"step": 6, "display": "Return Transit to Site", "badge_class": "phase-return", "is_active": True},
    "INFUSION_READY": {"step": 7, "display": "Returned to Site / Staged", "badge_class": "phase-infusion-ready", "is_active": True},
    "INFUSED": {"step": 8, "display": "Infusion Complete", "badge_class": "phase-infused", "is_active": False},
}


@dataclass(frozen=True)
class HoldDetail:
    status: str  # "OPEN" | "CLOSED" | "NONE"
    opened_at: str | None
    closed_at: str | None
    blocks_release: bool
    blocks_infusion: bool
    category: str  # "ACTIVE_MANUFACTURING_HOLD" | "RETROSPECTIVE_INVESTIGATION" | "NONE"
    quality_disposition_ref: str
    clinical_risk_note: str


@dataclass(frozen=True)
class PatientSummary:
    patient_key: str
    crm_patient_id: str
    clinical_subject_id: str
    mrn: str
    synthetic_name: str
    dob: str
    center_id: str
    country: str
    product_code: str
    journey_status: str
    enrolled_at: str
    phase_step: int
    phase_display: str
    phase_badge_class: str
    journey_position_code: str
    journey_position_display: str
    governing_readiness_code: str
    governing_readiness_display: str
    readiness_badge_class: str
    infusion_authorization: str
    has_hold: bool
    hold_detail: dict[str, Any]
    batch_id: str | None
    mes_status: str | None
    qms_release_status: str | None
    collection_id: str | None
    collection_time: str | None
    coi_id: str | None
    viability_pct: float | None
    deviations_count: int
    open_deviations_count: int
    is_active: bool


_CACHED_PATIENTS: list[dict[str, Any]] | None = None


def _load_baseline_patients(raw_dir: Path = RAW) -> list[dict[str, Any]]:
    global _CACHED_PATIENTS
    if _CACHED_PATIENTS is not None and raw_dir == RAW:
        return _CACHED_PATIENTS

    patients_rows = _read_csv_rows(raw_dir / "patients.csv")
    batches_rows = _read_csv_rows(raw_dir / "batches.csv")
    collections_rows = _read_csv_rows(raw_dir / "collections.csv")
    deviations_rows = _read_csv_rows(raw_dir / "deviations.csv")

    batches_by_patient: dict[str, dict[str, str]] = {}
    batches_by_id: dict[str, dict[str, str]] = {}
    for row in batches_rows:
        p_key = row.get("patient_key", "")
        if p_key:
            batches_by_patient[p_key] = row
        b_id = row.get("batch_id", "")
        if b_id:
            batches_by_id[b_id] = row

    collections_by_patient: dict[str, dict[str, str]] = {}
    for row in collections_rows:
        p_key = row.get("patient_key", "")
        if p_key:
            collections_by_patient[p_key] = row

    deviations_by_patient: dict[str, list[dict[str, str]]] = {}
    deviations_by_batch: dict[str, list[dict[str, str]]] = {}
    for row in deviations_rows:
        p_key = row.get("patient_key", "")
        if p_key:
            deviations_by_patient.setdefault(p_key, []).append(row)
        b_id = row.get("batch_id", "")
        if b_id:
            deviations_by_batch.setdefault(b_id, []).append(row)

    results: list[dict[str, Any]] = []

    for p in patients_rows:
        p_key = p.get("patient_key", "")
        status = p.get("journey_status", "ENROLLED")
        config = PHASE_CONFIG.get(status, PHASE_CONFIG["ENROLLED"])

        b = batches_by_patient.get(p_key)
        patient_batch_id = b.get("batch_id") if b else None
        c = collections_by_patient.get(p_key)

        p_devs = deviations_by_patient.get(p_key, [])
        b_devs = deviations_by_batch.get(patient_batch_id, []) if patient_batch_id else []
        combined_devs = {d.get("deviation_id", ""): d for d in p_devs + b_devs if d.get("deviation_id")}.values()
        deviations_count = len(combined_devs)

        open_blocking_devs = [
            d for d in combined_devs
            if d.get("blocking", "").strip().lower() in {"true", "1"}
            and d.get("status", "").upper() in {"OPEN", "IN_REVIEW", "PENDING"}
        ]
        open_deviations_count = len([
            d for d in combined_devs
            if d.get("status", "").upper() in {"OPEN", "IN_REVIEW", "PENDING"}
        ])

        mes_status = b.get("mes_status") if b else None
        qms_status = b.get("qms_release_status") if b else None

        has_system_hold = (
            (mes_status in {"HOLD", "QA_HOLD"})
            or (qms_status in {"HOLD", "QA_HOLD", "REJECTED"})
            or (len(open_blocking_devs) > 0)
        )

        # Viability parse
        viability: float | None = None
        if c and c.get("viability_pct"):
            try:
                viability = float(c["viability_pct"])
            except ValueError:
                viability = None

        # Build hold details and readiness state strictly honoring evidence boundaries
        if status == "INFUSED":
            journey_position_code = "INFUSED"
            journey_position_display = "INFUSION COMPLETE"
            if has_system_hold:
                gov_code = "INFUSED_WITH_UNRESOLVED_DISCREPANCY"
                gov_display = "AUDIT FINDING — INFUSED WITH OPEN HOLD"
                readiness_badge = "readiness-blocked"
                infusion_auth = "ADMINISTERED"
                hold_detail = HoldDetail(
                    status="OPEN",
                    opened_at=open_blocking_devs[0].get("opened_at") if open_blocking_devs else None,
                    closed_at=None,
                    blocks_release=True,
                    blocks_infusion=True,
                    category="RETROSPECTIVE_INVESTIGATION",
                    quality_disposition_ref=str(open_blocking_devs[0].get("deviation_id") or "UNLINKED_SOURCE_HOLD") if open_blocking_devs else "UNLINKED_SOURCE_HOLD",
                    clinical_risk_note="Post-infusion investigation required: product was infused despite unresolved Quality discrepancy in source tables; no authorized clinical exception record found in source evidence.",
                )
            else:
                gov_code = "COMPLETED_GOVERNED"
                gov_display = "COMPLETED — GOVERNED INFUSION"
                readiness_badge = "readiness-completed"
                infusion_auth = "ADMINISTERED"
                hold_detail = HoldDetail(
                    status="NONE",
                    opened_at=None,
                    closed_at=None,
                    blocks_release=False,
                    blocks_infusion=False,
                    category="NONE",
                    quality_disposition_ref="QMS-RELEASE-APPROVED",
                    clinical_risk_note="Infusion completed under normal release protocol.",
                )
        elif has_system_hold:
            journey_position_code = status
            journey_position_display = "Returned to Site (Quarantined)" if status == "INFUSION_READY" else config["display"]
            gov_code = "BLOCKED_QA_HOLD"
            gov_display = "BLOCKED — QA HOLD"
            readiness_badge = "readiness-blocked"
            infusion_auth = "PROHIBITED"
            first_dev = open_blocking_devs[0] if open_blocking_devs else None
            hold_detail = HoldDetail(
                status="OPEN",
                opened_at=first_dev.get("opened_at") if first_dev else None,
                closed_at=None,
                blocks_release=True,
                blocks_infusion=True,
                category="ACTIVE_MANUFACTURING_HOLD",
                quality_disposition_ref=str(first_dev.get("deviation_id") or "UNLINKED_SOURCE_HOLD_FLAG") if first_dev else "UNLINKED_SOURCE_HOLD_FLAG",
                clinical_risk_note="Authoritative QMS release is on HOLD. Physical quarantine required; clinical administration is strictly prohibited.",
            )
        elif b and qms_status == "RELEASED":
            journey_position_code = status
            journey_position_display = config["display"]
            gov_code = "RELEASED_AUTHORIZED"
            gov_display = "RELEASED — QUALITY AUTHORIZED"
            readiness_badge = "readiness-released"
            infusion_auth = "AUTHORIZED" if status == "INFUSION_READY" else "NOT_READY"
            hold_detail = HoldDetail(
                status="NONE",
                opened_at=None,
                closed_at=None,
                blocks_release=False,
                blocks_infusion=False,
                category="NONE",
                quality_disposition_ref="QMS-REL-PASS",
                clinical_risk_note="Quality release authorized by human Quality Authority.",
            )
        elif status in {"ENROLLED", "ELIGIBLE"}:
            journey_position_code = status
            journey_position_display = config["display"]
            gov_code = "ELIGIBILITY_VERIFIED"
            gov_display = "ELIGIBILITY VERIFIED"
            readiness_badge = "readiness-neutral"
            infusion_auth = "NOT_READY"
            hold_detail = HoldDetail(
                status="NONE",
                opened_at=None,
                closed_at=None,
                blocks_release=False,
                blocks_infusion=False,
                category="NONE",
                quality_disposition_ref="PRE-COLLECTION",
                clinical_risk_note="Patient in pre-manufacturing eligibility phase.",
            )
        else:
            # Physical position is at site or in transit, but Quality release is PENDING
            journey_position_code = status
            journey_position_display = "At Treatment Site (Pending Quality Release)" if status == "INFUSION_READY" else config["display"]
            gov_code = "PENDING_RELEASE"
            gov_display = "PENDING QUALITY RELEASE"
            readiness_badge = "readiness-pending"
            infusion_auth = "NOT_READY"
            hold_detail = HoldDetail(
                status="NONE",
                opened_at=None,
                closed_at=None,
                blocks_release=False,
                blocks_infusion=False,
                category="NONE",
                quality_disposition_ref="IN_PROCESS",
                clinical_risk_note="Batch in manufacturing, transit, or testing. Release pending evidence packet assembly.",
            )

        summary = PatientSummary(
            patient_key=p_key,
            crm_patient_id=p.get("crm_patient_id", ""),
            clinical_subject_id=p.get("clinical_subject_id", ""),
            mrn=p.get("mrn", ""),
            synthetic_name=p.get("synthetic_name", f"Patient {p_key}"),
            dob=p.get("dob", ""),
            center_id=p.get("center_id", ""),
            country=p.get("country", ""),
            product_code=p.get("product_code", ""),
            journey_status=status,
            enrolled_at=p.get("enrolled_at", ""),
            phase_step=config["step"],
            phase_display=config["display"],
            phase_badge_class=config["badge_class"],
            journey_position_code=journey_position_code,
            journey_position_display=journey_position_display,
            governing_readiness_code=gov_code,
            governing_readiness_display=gov_display,
            readiness_badge_class=readiness_badge,
            infusion_authorization=infusion_auth,
            has_hold=has_system_hold,
            hold_detail=asdict(hold_detail),
            batch_id=patient_batch_id,
            mes_status=mes_status,
            qms_release_status=qms_status,
            collection_id=c.get("collection_id") if c else None,
            collection_time=c.get("collected_at") if c else None,
            coi_id=b.get("coi_id") if b else None,
            viability_pct=viability,
            deviations_count=deviations_count,
            open_deviations_count=open_deviations_count,
            is_active=config["is_active"],
        )
        results.append(asdict(summary))

    if raw_dir == RAW:
        _CACHED_PATIENTS = results
    return results


def get_patients_list(
    search: str | None = None,
    phase: str | None = None,
    product: str | None = None,
    center: str | None = None,
    status_filter: str | None = "active",
    page: int = 1,
    page_size: int = 15,
    sort_by: str = "patient_key",
    sort_dir: str = "asc",
    raw_dir: Path = RAW,
) -> dict[str, Any]:
    all_patients = _load_baseline_patients(raw_dir)

    total_count = len(all_patients)
    active_count = sum(1 for p in all_patients if p["is_active"])
    completed_count = total_count - active_count
    total_holds = sum(1 for p in all_patients if p["has_hold"])

    counts_by_phase: dict[str, int] = {}
    for p in all_patients:
        status = p["journey_status"]
        counts_by_phase[status] = counts_by_phase.get(status, 0) + 1

    # Filter by active/completed/all
    filtered = all_patients
    if status_filter == "active":
        filtered = [p for p in filtered if p["is_active"]]
    elif status_filter == "completed":
        filtered = [p for p in filtered if not p["is_active"]]

    # Filter by phase
    if phase and phase != "ALL":
        if phase == "QA_HOLD":
            filtered = [p for p in filtered if p["has_hold"]]
        elif phase == "INFUSION_READY":
            # Real Infusion Ready requires no hold AND verified release
            filtered = [
                p for p in filtered
                if p["journey_status"] == "INFUSION_READY" and not p["has_hold"] and p["qms_release_status"] == "RELEASED"
            ]
        else:
            filtered = [p for p in filtered if p["journey_status"] == phase]

    # Filter by product
    if product and product != "ALL":
        filtered = [p for p in filtered if p["product_code"] == product]

    # Filter by treatment center
    if center and center != "ALL":
        filtered = [p for p in filtered if p["center_id"] == center]

    # Filter by search
    if search and search.strip():
        q = search.strip().lower()
        filtered = [
            p for p in filtered
            if q in p["patient_key"].lower()
            or q in p["synthetic_name"].lower()
            or q in p["mrn"].lower()
            or q in p["center_id"].lower()
            or (p["batch_id"] and q in p["batch_id"].lower())
            or (p["coi_id"] and q in p["coi_id"].lower())
        ]

    # Sort
    reverse = sort_dir.lower() == "desc"

    def sort_key(item: dict[str, Any]) -> Any:
        val = item.get(sort_by)
        if val is None:
            return ""
        return val

    filtered = sorted(filtered, key=sort_key, reverse=reverse)

    page = max(1, page)
    page_size = max(1, min(100, page_size))
    total_items = len(filtered)
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    start_idx = (page - 1) * page_size
    items = filtered[start_idx : start_idx + page_size]

    # Compute true governed infusion ready count (physically at site AND authorized release)
    true_infusion_ready = sum(
        1 for p in all_patients
        if p["journey_status"] == "INFUSION_READY" and not p["has_hold"] and p["qms_release_status"] == "RELEASED"
    )

    return {
        "kpis": {
            "total_patients": total_count,
            "active_patients": active_count,
            "completed_patients": completed_count,
            "counts_by_phase": counts_by_phase,
            "qa_holds": total_holds,
            "in_manufacturing": counts_by_phase.get("IN_MANUFACTURING", 0),
            "qc_pending": counts_by_phase.get("QC_PENDING", 0),
            "infusion_ready": true_infusion_ready,
            "return_transit": counts_by_phase.get("RETURN_TRANSIT", 0),
        },
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        },
        "patients": items,
    }


def get_patient_detail(patient_key: str, raw_dir: Path = RAW) -> dict[str, Any]:
    all_patients = _load_baseline_patients(raw_dir)
    matched = next((p for p in all_patients if p["patient_key"] == patient_key), None)
    if matched is None:
        raise KeyError(f"Patient not found: {patient_key}")

    batch_id = matched.get("batch_id")

    def load_rows_for(file_name: str) -> list[dict[str, str]]:
        rows = _read_csv_rows(raw_dir / file_name)
        return [
            r for r in rows
            if r.get("patient_key") == patient_key or (batch_id and r.get("batch_id") == batch_id)
        ]

    return {
        "patient": matched,
        "shipments": load_rows_for("shipments.csv"),
        "slots": load_rows_for("manufacturing_slots.csv"),
        "qc_results": load_rows_for("qc_results.csv"),
        "deviations": load_rows_for("deviations.csv"),
        "consents": load_rows_for("consents.csv"),
        "authorizations": load_rows_for("insurance_authorizations.csv"),
    }

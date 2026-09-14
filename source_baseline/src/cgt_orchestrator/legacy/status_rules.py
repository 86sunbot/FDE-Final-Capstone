"""Intentionally naive legacy rules.

These rules are runnable but contain semantic defects suitable for discovery.
Do not silently 'fix' them without adding tests and documenting the changed rule.
"""

def product_ready(batch: dict) -> bool:
    # Legacy defect: manufacturing complete / ERP available is treated as equivalent to QA release.
    return batch.get("mes_status") in {"MFG_COMPLETE", "RELEASED"} or batch.get("erp_status") == "AVAILABLE"


def patient_ready(patient: dict, batch: dict | None) -> bool:
    if not patient or not batch:
        return False
    # Legacy defect: ignores consent, site qualification, authorization and shipment certainty.
    return patient.get("journey_status") not in {"ENROLLED"} and product_ready(batch)


def excursion_failed(temp_c: float | None) -> bool:
    # Legacy defect: implements superseded SOP v6 as a point threshold.
    if temp_c is None:
        return False
    return temp_c > -120.0

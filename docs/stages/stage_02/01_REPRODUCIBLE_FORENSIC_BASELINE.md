# Stage 2 - Reproducible Forensic Baseline

**Generated:** 2026-09-14T02:25:51.611061+00:00  
**Source:** `/Users/suryap/Documents/Codex/2026-09-11/i/capstone/source_baseline` opened read-only with SQLite `mode=ro&immutable=1`  
**Status:** Measured baseline; interpretation remains subject to domain-owner review

## Dataset counts

| Table | Rows | Raw CSV exact ordered match |
|---|---:|---|
| `patients` | 800 | YES |
| `collections` | 800 | YES |
| `shipments` | 1600 | YES |
| `batches` | 800 | YES |
| `qc_results` | 4800 | YES |
| `deviations` | 188 | YES |
| `manufacturing_slots` | 800 | YES |
| `consents` | 800 | YES |
| `insurance_authorizations` | 800 | YES |
| `cryogenic_telemetry` | 12800 | YES |
| `site_qualifications` | 24 | YES |

The SQLite database is a materialization of the eleven corresponding raw CSVs, not an independent corroborating source.

## Findings

| ID | Lens | Severity | Finding | Measured value |
|---|---|---|---|---|
| F-IDENT-001 | Inconsistency | CRITICAL | Duplicate MRNs across different patient keys | `2` |
| F-IDENT-002 | Inconsistency | CRITICAL | CRM/clinical dob disagreements | `10` |
| F-IDENT-003 | Inconsistency | HIGH | CRM/clinical center_id disagreements | `12` |
| F-IDENT-004 | Inconsistency | CRITICAL | CRM/clinical mrn disagreements | `7` |
| F-IDENT-005 | Inconsistency | HIGH | CRM/clinical name_or_alias disagreements | `21` |
| F-READY-001 | Inconsistency | CRITICAL | MES released while QMS not released | `16` |
| F-READY-002 | Hidden Dependency | CRITICAL | ERP available while QMS not released | `158` |
| F-READY-003 | Imperfection | CRITICAL | Journeys classified ready by unsafe legacy heuristic | `{"authorization_not_approved": 205, "confirmed_cancelled_slot": 7, "expired_or_due_site_controls": 145, "invalid_consent": 30, "legacy_ready_total": 499, "no_delivered_return_shipment": 243, "not_qms_released": 153}` |
| F-READY-004 | Inconsistency | CRITICAL | Stored journey status ahead of Quality release | `{"INFUSED": 73, "INFUSION_READY": 32}` |
| F-GATE-001 | Hidden Dependency | CRITICAL | Consent states requiring explicit gating | `{"EXPIRED_VERSION": 44, "VALID": 751, "WITHDRAWN": 5}` |
| F-GATE-002 | Hidden Dependency | HIGH | Authorization states requiring explicit gating | `{"APPROVED": 468, "CONDITIONAL": 161, "DENIED": 5, "PENDING": 166}` |
| F-QUALITY-001 | Complexity | CRITICAL | Open/investigating deviations and Quality-release coexistence | `{"critical_open_or_investigating": 39, "deviations_total": 188, "on_qms_released_batches": 74, "open_or_investigating": 135}` |
| F-QUALITY-002 | Imperfection | HIGH | Deviation links do not resolve to the event log | `{"blank": 36, "nonblank_missing": 152, "total_unresolved": 188}` |
| F-QUALITY-003 | Uncertainty | HIGH | QMS-released batches with pending/OOS/OOT QC rows | `283` |
| F-SITE-001 | Hidden Dependency | HIGH | Treatment centers with expired training or due equipment | `6` |
| F-TIME-001 | Inconsistency | HIGH | Shipments arriving before departure | `9` |
| F-TIME-002 | Volatility | HIGH | Patient histories whose recorded order inverts occurrence order | `10` |
| F-TIME-003 | Uncertainty | MEDIUM | Maximum event recording lag in hours | `12.0` |
| F-INTEG-001 | Imperfection | HIGH | Retry-duplicate manufacturing-start events | `7` |
| F-INTEG-002 | Inconsistency | HIGH | Scheduler-confirmed slots cancelled in MES | `9` |
| F-SHADOW-001 | Friction | HIGH | Formal vs shadow patient-priority disagreements | `523` |
| F-SHADOW-002 | Hidden Dependency | MEDIUM | Manufacturing-slot rows containing planner override notes | `12` |
| F-SHADOW-003 | Friction | HIGH | Shadow email categories | `{"Courier route": 12, "Identity reconciliation": 14, "QA exception": 7, "Site readiness": 10, "Slot moved": 17}` |
| F-SHADOW-004 | Friction | HIGH | Courier escalations requiring closed-loop ownership | `{"open": 21, "total": 31, "unowned": 8}` |
| F-THERMAL-001 | Uncertainty | HIGH | Telemetry and excursion evidence requiring contextual disposition | `{"flagged_without_point_above_minus_120_c": 3, "missing_temperature_values": 10, "shipments_flagged": 19, "shipments_with_point_above_minus_120_c": 16, "warning_quality_values": 27}` |
| F-LOG-001 | Inconsistency | HIGH | Booked/in-transit shipments with arrival timestamps | `398` |
| F-EVENT-001 | Unknown Unknown | HIGH | Event model covers only a narrow set of business events | `{"distinct_types": 8, "types": {"COLLECTION_COMPLETED": 800, "MANUFACTURING_COMPLETED": 800, "MANUFACTURING_STARTED": 807, "PATIENT_ENROLLED": 800, "RETURN_SHIPMENT_ARRIVED": 800, "RETURN_SHIPMENT_DISPATCHED": 800, "SHIPMENT_DISPATCHED": 800, "SHIPMENT_RECEIVED": 800}}` |

## Evidence and interpretation

### F-IDENT-001 - Duplicate MRNs across different patient keys

- **Lens:** Inconsistency
- **Severity:** CRITICAL
- **Measured value:** `2`
- **Evidence method:** `patients GROUP BY mrn HAVING COUNT(*) > 1`
- **Interpretation:** MRN cannot be used as a unique cross-system identity key.

### F-IDENT-002 - CRM/clinical dob disagreements

- **Lens:** Inconsistency
- **Severity:** CRITICAL
- **Measured value:** `10`
- **Evidence method:** `data/raw/crm_patient_export.csv joined to clinical_patient_export.csv on patient_key; compare dob`
- **Interpretation:** Identity evidence differs across source-specific views and requires explainable reconciliation.

### F-IDENT-003 - CRM/clinical center_id disagreements

- **Lens:** Inconsistency
- **Severity:** HIGH
- **Measured value:** `12`
- **Evidence method:** `data/raw/crm_patient_export.csv joined to clinical_patient_export.csv on patient_key; compare center_id`
- **Interpretation:** Identity evidence differs across source-specific views and requires explainable reconciliation.

### F-IDENT-004 - CRM/clinical mrn disagreements

- **Lens:** Inconsistency
- **Severity:** CRITICAL
- **Measured value:** `7`
- **Evidence method:** `data/raw/crm_patient_export.csv joined to clinical_patient_export.csv on patient_key; compare mrn`
- **Interpretation:** Identity evidence differs across source-specific views and requires explainable reconciliation.

### F-IDENT-005 - CRM/clinical name_or_alias disagreements

- **Lens:** Inconsistency
- **Severity:** HIGH
- **Measured value:** `21`
- **Evidence method:** `data/raw/crm_patient_export.csv joined to clinical_patient_export.csv on patient_key; compare name_or_alias`
- **Interpretation:** Identity evidence differs across source-specific views and requires explainable reconciliation.

### F-READY-001 - MES released while QMS not released

- **Lens:** Inconsistency
- **Severity:** CRITICAL
- **Measured value:** `16`
- **Evidence method:** `batches: mes_status='RELEASED' AND qms_release_status!='RELEASED'`
- **Interpretation:** Manufacturing/MES state must not substitute for Quality release authority.

### F-READY-002 - ERP available while QMS not released

- **Lens:** Hidden Dependency
- **Severity:** CRITICAL
- **Measured value:** `158`
- **Evidence method:** `batches: erp_status='AVAILABLE' AND qms_release_status!='RELEASED'`
- **Interpretation:** Commercial/inventory availability can conceal an unmet Quality gate.

### F-READY-003 - Journeys classified ready by unsafe legacy heuristic

- **Lens:** Imperfection
- **Severity:** CRITICAL
- **Measured value:** `{"authorization_not_approved": 205, "confirmed_cancelled_slot": 7, "expired_or_due_site_controls": 145, "invalid_consent": 30, "legacy_ready_total": 499, "no_delivered_return_shipment": 243, "not_qms_released": 153}`
- **Evidence method:** `Legacy product_ready predicate reproduced against batches and joined gate evidence`
- **Interpretation:** A positive legacy readiness result does not prove patient/product readiness; multiple safety dependencies are omitted.
- **Caveat:** Categories overlap and must not be summed.

### F-READY-004 - Stored journey status ahead of Quality release

- **Lens:** Inconsistency
- **Severity:** CRITICAL
- **Measured value:** `{"INFUSED": 73, "INFUSION_READY": 32}`
- **Evidence method:** `patients joined to batches; journey_status vs qms_release_status`
- **Interpretation:** Stored journey strings cannot be trusted as authoritative gate decisions.

### F-GATE-001 - Consent states requiring explicit gating

- **Lens:** Hidden Dependency
- **Severity:** CRITICAL
- **Measured value:** `{"EXPIRED_VERSION": 44, "VALID": 751, "WITHDRAWN": 5}`
- **Evidence method:** `consents grouped by status`
- **Interpretation:** Withdrawn and expired-version consent cannot be ignored by downstream readiness.

### F-GATE-002 - Authorization states requiring explicit gating

- **Lens:** Hidden Dependency
- **Severity:** HIGH
- **Measured value:** `{"APPROVED": 468, "CONDITIONAL": 161, "DENIED": 5, "PENDING": 166}`
- **Evidence method:** `insurance_authorizations grouped by status`
- **Interpretation:** Authorization status affects scheduling and downstream commercial/process readiness.

### F-QUALITY-001 - Open/investigating deviations and Quality-release coexistence

- **Lens:** Complexity
- **Severity:** CRITICAL
- **Measured value:** `{"critical_open_or_investigating": 39, "deviations_total": 188, "on_qms_released_batches": 74, "open_or_investigating": 135}`
- **Evidence method:** `deviations joined to batches`
- **Interpretation:** Open deviations require blocking classification and disposition evidence; open status alone does not prove every release invalid.

### F-QUALITY-002 - Deviation links do not resolve to the event log

- **Lens:** Imperfection
- **Severity:** HIGH
- **Measured value:** `{"blank": 36, "nonblank_missing": 152, "total_unresolved": 188}`
- **Evidence method:** `deviations.linked_event_id checked against events.jsonl event_id`
- **Interpretation:** Quality investigations lack resolvable event evidence.

### F-QUALITY-003 - QMS-released batches with pending/OOS/OOT QC rows

- **Lens:** Uncertainty
- **Severity:** HIGH
- **Measured value:** `283`
- **Evidence method:** `batches joined to qc_results; qms release with result in PENDING/OOS/OOT`
- **Interpretation:** Explicit assay disposition evidence is required before interpreting these rows.

### F-SITE-001 - Treatment centers with expired training or due equipment

- **Lens:** Hidden Dependency
- **Severity:** HIGH
- **Measured value:** `6`
- **Evidence method:** `site_qualifications control fields`
- **Interpretation:** High-level site status can obscure detailed qualification controls.

### F-TIME-001 - Shipments arriving before departure

- **Lens:** Inconsistency
- **Severity:** HIGH
- **Measured value:** `9`
- **Evidence method:** `shipments arrived_at < departed_at`
- **Interpretation:** Physical event ordering contradicts recorded shipment timestamps.

### F-TIME-002 - Patient histories whose recorded order inverts occurrence order

- **Lens:** Volatility
- **Severity:** HIGH
- **Measured value:** `10`
- **Evidence method:** `events grouped by patient and sorted by recorded_at; adjacent occurred_at inversion`
- **Interpretation:** Recorded order and physical occurrence order are separate concepts.

### F-TIME-003 - Maximum event recording lag in hours

- **Lens:** Uncertainty
- **Severity:** MEDIUM
- **Measured value:** `12.0`
- **Evidence method:** `max(recorded_at - occurred_at) across events.jsonl`
- **Interpretation:** Late-arriving evidence can change a derived journey view.

### F-INTEG-001 - Retry-duplicate manufacturing-start events

- **Lens:** Imperfection
- **Severity:** HIGH
- **Measured value:** `7`
- **Evidence method:** `events grouped on patient,batch,type,occurred_at,payload_ref`
- **Interpretation:** New event identifiers do not guarantee semantic uniqueness or idempotency.

### F-INTEG-002 - Scheduler-confirmed slots cancelled in MES

- **Lens:** Inconsistency
- **Severity:** HIGH
- **Measured value:** `9`
- **Evidence method:** `manufacturing_slots scheduler_state vs mes_state`
- **Interpretation:** Partial distributed state and absent compensation create unreliable capacity state.

### F-SHADOW-001 - Formal vs shadow patient-priority disagreements

- **Lens:** Friction
- **Severity:** HIGH
- **Measured value:** `523`
- **Evidence method:** `manufacturing_slots.csv joined to PatientPriority_MASTER.csv on patient_key`
- **Interpretation:** Operational priority is being maintained outside the formal scheduling view.

### F-SHADOW-002 - Manufacturing-slot rows containing planner override notes

- **Lens:** Hidden Dependency
- **Severity:** MEDIUM
- **Measured value:** `12`
- **Evidence method:** `ManufacturingSlots_FINAL_v7.csv planner_note nonblank`
- **Interpretation:** Email/manual decisions create downstream dependencies not represented as governed transactions.

### F-SHADOW-003 - Shadow email categories

- **Lens:** Friction
- **Severity:** HIGH
- **Measured value:** `{"Courier route": 12, "Identity reconciliation": 14, "QA exception": 7, "Site readiness": 10, "Slot moved": 17}`
- **Evidence method:** `Subject lines across shadow_ops/emails/*.eml`
- **Interpretation:** Unstructured email carries slot, courier, identity, Quality and site-readiness coordination.

### F-SHADOW-004 - Courier escalations requiring closed-loop ownership

- **Lens:** Friction
- **Severity:** HIGH
- **Measured value:** `{"open": 21, "total": 31, "unowned": 8}`
- **Evidence method:** `CourierEscalations.csv status and owner`
- **Interpretation:** Open or unowned escalation work can delay patient/material movement without accountable resolution.

### F-THERMAL-001 - Telemetry and excursion evidence requiring contextual disposition

- **Lens:** Uncertainty
- **Severity:** HIGH
- **Measured value:** `{"flagged_without_point_above_minus_120_c": 3, "missing_temperature_values": 10, "shipments_flagged": 19, "shipments_with_point_above_minus_120_c": 16, "warning_quality_values": 27}`
- **Evidence method:** `shipments joined conceptually to cryogenic_telemetry`
- **Interpretation:** A point threshold is insufficient; effective SOP v7 requires duration, quality, cumulative profile, shipper integrity and human Quality review.

### F-LOG-001 - Booked/in-transit shipments with arrival timestamps

- **Lens:** Inconsistency
- **Severity:** HIGH
- **Measured value:** `398`
- **Evidence method:** `shipments status IN (BOOKED,IN_TRANSIT) with arrived_at populated`
- **Interpretation:** Shipment state and event evidence disagree; neither should be silently preferred.

### F-EVENT-001 - Event model covers only a narrow set of business events

- **Lens:** Unknown Unknown
- **Severity:** HIGH
- **Measured value:** `{"distinct_types": 8, "types": {"COLLECTION_COMPLETED": 800, "MANUFACTURING_COMPLETED": 800, "MANUFACTURING_STARTED": 807, "PATIENT_ENROLLED": 800, "RETURN_SHIPMENT_ARRIVED": 800, "RETURN_SHIPMENT_DISPATCHED": 800, "SHIPMENT_DISPATCHED": 800, "SHIPMENT_RECEIVED": 800}}`
- **Evidence method:** `events.jsonl event_type`
- **Interpretation:** Consent, authorization, site qualification, slot, QC, deviation, QA release, conditioning and infusion are not first-class events.

# Stage 6 - Dataset Datasheets and SOP/Knowledge Register

**Status:** Capstone datasheet set; source/domain-owner confirmation pending  
**Last updated:** 2026-09-14

## 1. Datasheet - Patient and identity evidence

| Field | Description |
|---|---|
| Files | `patients.csv`, `crm_patient_export.csv`, `clinical_patient_export.csv` |
| Population | 800 rows in each file |
| Purpose | Synthetic enrollment, identity and journey-status conflicts |
| Keying | `patient_key` unique in each; MRN is not globally unique |
| Collection/generation | Synthetic generator in supplied repository; exact generation assumptions not a production sampling method |
| Known issues | Duplicate MRNs and cross-source DOB, center, MRN and name/alias disagreements |
| Suitable use | Conflict detection, evidence/provenance UI, abstention and authorized-resolution workflow testing |
| Unsuitable use | Training/validating real identity matching or asserting a resolved person |

## 2. Datasheet - Collection and lineage evidence

| Field | Description |
|---|---|
| Files | `collections.csv`; related batch/shipment fields |
| Population | 800 collections |
| Purpose | Synthetic source-material/COI linkage and measurements |
| Keying | Unique `collection_id`; declared patient/COI/bag identifiers |
| Known issues | No independent scan/attestation/custody evidence; string agreement is not identity proof |
| Suitable use | Typed quantity/unit contracts, relationship assertions and missing-evidence cases |
| Unsuitable use | Attesting actual COI/COC or patient/product identity |

## 3. Datasheet - Logistics and telemetry evidence

| Field | Description |
|---|---|
| Files | `shipments.csv`, `cryogenic_telemetry.csv`, courier reference, escalation CSV and email |
| Population | 1,600 shipments; 12,800 sensor observations; 31 escalations; related shadow emails |
| Purpose | Outbound/return flow, status/time contradictions and thermal uncertainty |
| Keying | Shipment ID; telemetry profile key is shipment + sensor + timestamp |
| Known issues | 9 impossible times; 398 arrival/status conflicts; 10 missing and 27 warning sensor points; custody/calibration/shipper integrity absent |
| Suitable use | Bitemporal/case logic, evidence profile calculation and Quality-review workflow |
| Unsuitable use | Real route reliability or automatic product disposition |

## 4. Datasheet - Capacity and manufacturing evidence

| Field | Description |
|---|---|
| Files | `manufacturing_slots.csv`, slot shadow CSV, `batches.csv`, site/product references and events |
| Population | 800 slots, 800 batches, 6 sites, 3 products |
| Purpose | Scheduling/MES conflict, retry and release-semantic cases |
| Known issues | 9 scheduler/MES conflicts; 7 semantic retry events; no command ledger, capacity constraints or change history |
| Suitable use | Idempotency/state-machine/saga simulation and source-status separation |
| Unsuitable use | Real capacity optimization or autonomous reprioritization |

## 5. Datasheet - QC, deviation and release evidence

| Field | Description |
|---|---|
| Files | `qc_results.csv`, `deviations.csv`, batch QMS field, QA SOP |
| Population | 4,800 QC rows; 188 deviations; 800 batches |
| Purpose | Synthetic release-evidence and ambiguity cases |
| Known issues | 188 unresolved deviation links; blocking/disposition/method/spec/signature evidence absent; 283 released batches have pending/OOS/OOT rows |
| Suitable use | Evidence completeness, fail-closed gate and authorized Quality-review testing |
| Unsuitable use | Determining true product disposition or judging supplied releases valid/invalid |

## 6. Datasheet - Consent, authorization and site evidence

| Field | Description |
|---|---|
| Files | `consents.csv`, `insurance_authorizations.csv`, `site_qualifications.csv` |
| Population | 800 consent, 800 authorization and 24 site rows |
| Purpose | Hidden prerequisite/revalidation cases |
| Known issues | Snapshot-only; milestone rules/artifacts/history absent; 44 expired consent versions, 5 withdrawals and 6 site-control gaps |
| Suitable use | Versioned prerequisite schema and negative/unknown tests |
| Unsuitable use | Real consent, payer, qualification or clinical decision |

## 7. Datasheet - Events, evals and injects

| Field | Description |
|---|---|
| Files | `events.jsonl`, `evals/cases.csv`, `scenarios/inject_catalog.csv` |
| Population | 6,407 events, 6 cases and 10 injects |
| Purpose | Temporal, idempotency, authority, outage and adversarial seed evidence |
| Known issues | Only 8 event types; no complete golden outputs or execution results |
| Suitable use | Mandatory seed expansion into Stage 7 executable specs |
| Unsuitable use | Claiming TEVV completion or production resilience |

## 8. SOP and controlled-knowledge register

| Document | Status | Effective | Controlled meaning | Usage rule |
|---|---|---|---|---|
| SOP-LOG-007 v6 | Superseded | Not stated | Single point above -120 C treated as automatic failure | Historical evidence only; do not use for current decision |
| SOP-LOG-007 v7 | Effective | 2026-05-01 | Requires duration, quality, cumulative profile, shipper integrity and Quality review | Current logistics rule evidence; missing calculation/detail remains a gap |
| SOP-QA-014 v4 | Effective | Not stated | Manufacturing completion is not release; required QC, blocking deviation disposition and authorized approval needed | Binding synthetic release principle; exact prerequisites/signature spec still needed |
| SOP-SCHED-003 v2 | Draft | Not stated | May permit provisional capacity before authorization with later revalidation | Hypothesis only; no execution until approved |

Hashes and exact titles/status are recorded in `knowledge_inventory.csv`.

## 9. Knowledge-use controls

- Retrieval filters by document ID/version/status/effective time and purpose.
- Superseded and draft status is prominent in every result/summary.
- Exact source passage/reference is retained; the model cannot silently merge policies.
- Prompt/email/document content is untrusted data and cannot override system policy.
- Missing rule detail returns `UNKNOWN`/human review.
- Every generated summary binds source hashes and model/prompt/policy versions.
- No external web knowledge supplies a safety threshold unless an authorized controlled specification adopts it.

## 10. Datasheet maintenance

Stage 7 adds label/rubric provenance and held-out split details. Stage 9 adds schemas, classifications and retention. Stage 14 records generated fixtures and transformations. Stage 15 attaches actual evaluation results. Stage 18 monitors source/schema/semantic drift.

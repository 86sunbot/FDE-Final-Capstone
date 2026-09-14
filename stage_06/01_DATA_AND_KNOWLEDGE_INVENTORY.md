# Stage 6 - Data and Knowledge Inventory

**Status:** Measured draft; owner and permissible-use validation pending  
**Generated evidence:** `data_knowledge_profile.json`, `dataset_profile.csv`, `relationship_profile.csv`, `knowledge_inventory.csv`  
**Last updated:** 2026-09-14

## 1. Scope and method

`tools/profile_data_knowledge.py` read the verified baseline only and profiled declared keys, nulls, temporal/numeric parseability, cross-file references, event coverage, shadow emails and knowledge artifacts. Hashes bind every profiled dataset/knowledge item to the immutable source copy.

The profile does not repair, impute, normalize or delete any supplied evidence.

## 2. Inventory summary

| Evidence family | Population | Role |
|---|---:|---|
| CSV datasets | 23 files / 27,507 rows | Raw assertions, reference data, evaluation seeds and shadow operations |
| Legacy SQLite | 11 tables | Exact materialization of corresponding raw CSVs; not independent corroboration |
| Event stream | 6,407 JSONL events / 8 event types | Partial cross-system history |
| Shadow email | 60 files | Synthetic untrusted evidence of work outside formal systems |
| Knowledge/control/interface items | 24 files | Context, SOPs, API contracts, evals, failure scenarios and challenge requirements |
| Supplied evaluation cases | 6 cases | Seed properties, not a complete golden set |
| Failure injections | 10 scenarios | Seed disruptions, not executed results |

## 3. Core operational datasets

| Dataset | Rows | Profile key | Intended evidence | Principal limitation |
|---|---:|---|---|---|
| `patients.csv` | 800 | `patient_key` | Consolidated legacy journey snapshot | Derived-looking table; source authority and history absent |
| `crm_patient_export.csv` | 800 | `patient_key` | CRM/enrollment identity assertions | Conflicts with clinical export; not clinical identity authority |
| `clinical_patient_export.csv` | 800 | `patient_key` | Clinical subject/identity/status assertions | Conflicts with CRM; no adjudication history |
| `collections.csv` | 800 | `collection_id` | Collection/bag/COI and measures | Typed/unit constraints absent; no scan/attestation genealogy |
| `shipments.csv` | 1,600 | `shipment_id` | Outbound/return movement snapshot | Status/timestamps contradict for some rows; COC transfers absent |
| `cryogenic_telemetry.csv` | 12,800 | shipment + sensor + timestamp | Raw cryogenic observations | 10 missing values, 27 warning-quality points; calibration/profile metadata absent |
| `manufacturing_slots.csv` | 800 | `slot_id` | Scheduler and MES planning assertions | Two state domains share a row; constraint/reservation history absent |
| `batches.csv` | 800 | `batch_id` | Batch linkage and MES/ERP/QMS snapshot | Release meanings conflated; no decision/signature evidence |
| `qc_results.csv` | 4,800 | `qc_id` | Six assay rows per batch | Required specs/methods/disposition absent; mixed textual/numeric values |
| `deviations.csv` | 188 | `deviation_id` | Quality exception snapshot | All 188 event links unresolved; blocking/disposition/closure evidence absent |
| `consents.csv` | 800 | `consent_id` | Consent version/status assertion | One current row per patient; effective/revocation history and artifact absent |
| `insurance_authorizations.csv` | 800 | `auth_id` | Payer status/validity assertion | Policy meaning by milestone absent |
| `site_qualifications.csv` | 24 | `center_id` | Training/equipment/agreement snapshot | Control evidence and change history absent |

## 4. Reference, evaluation and shadow data

| Family | Files/rows | Use | Trust warning |
|---|---:|---|---|
| Reference master data | 5 files / 48 rows | Product, manufacturing site, treatment center, courier and KPI reference | Synthetic lookup data; ownership/change history absent |
| Supplied KPI baseline | 10 rows | Challenge baseline | Formulas/populations/time windows not supplied |
| Eval cases | 6 rows | Required properties | Questions are seed specifications, not observed outcomes |
| Failure injects | 10 rows | Resilience/TEVV seed | Triggers/severity are inputs, not executed evidence |
| Patient priority shadow file | 800 rows | Informal priority view | 640 blank reasons; 523 priorities disagree with formal slot data |
| Manufacturing slot shadow file | 800 rows | Planner workaround view | 12 notes; not a governed transaction/audit source |
| Courier escalations | 31 rows | Logistics exception view | 8 unowned; lifecycle timestamps/SLAs absent |
| Shadow email | 60 files | Unstructured operational evidence | Untrusted/stale/adversarial content; cannot be instructions or approvals |

## 5. Knowledge and control inventory

| Knowledge class | Items | Assessment |
|---|---:|---|
| Effective SOP evidence | 2 | `SOP-LOG-007 v7`, `SOP-QA-014 v4`; rule detail remains incomplete for executable implementation |
| Superseded SOP evidence | 1 | `SOP-LOG-007 v6`; must never be selected for current decisions |
| Draft SOP evidence | 1 | `SOP-SCHED-003 v2`; cannot be treated as approved policy |
| API contracts | 3 | Minimal incompatible identifier paths; not usable target contracts |
| Context/security/data documents | 7 | Valuable questions/context, explicitly incomplete architecture |
| Challenge/agent instructions | 3 | Scope and engineering constraints; not enterprise operating policy |
| Eval/inject artifacts | 4 | Seed coverage for Stage 7 |
| Verification/licence/support | 4 | Integrity/synthetic-use context; no regulatory certification |

Exact hashes, titles, status and effective metadata are in `knowledge_inventory.csv`.

## 6. Inventory conclusion

The package is rich enough to reproduce brownfield failure modes and build a controlled synthetic POC. It is not sufficient to train or validate a production predictive model, prove real-world performance, establish regulatory applicability, or execute consequential decisions. Stage 6 must therefore classify gaps and permissible use rather than label the dataset simply “ready.”

# Stage 6 - Internal Data/Knowledge Readiness Review

**Review type:** Codex internal check; not data-owner, Privacy or Quality approval  
**Status:** READY FOR REVIEW; academic G1 approved; accountable data/Privacy/Quality review pending  
**Review date:** 2026-09-14

## 1. Stage objective

Determine which evidence is trustworthy, permitted, representative and usable, and make uncertainty/gaps actionable before evaluation or implementation.

## 2. Artifact review

| Required artifact | Evidence | Internal result |
|---|---|---|
| Data/knowledge inventory | `01_DATA_AND_KNOWLEDGE_INVENTORY.md`; profile JSON/CSVs | PASS |
| Data quality profile | `02_DATA_QUALITY_PROFILE_AND_ISSUE_REGISTER.md` | PASS |
| Lineage/provenance | `03_LINEAGE_PROVENANCE_AND_SOURCE_TRUST.md` | PASS |
| Attribute/source trust hierarchy | `03_LINEAGE_PROVENANCE_AND_SOURCE_TRUST.md` | PASS; owners pending |
| Access/permissible use | `04_ACCESS_AND_PERMISSIBLE_USE_REGISTER.md` | PASS; Privacy/Legal approval pending |
| Representativeness | `05_REPRESENTATIVENESS_AND_DATA_GAP_REGISTER.md` | PASS |
| Data-gap register | `05_REPRESENTATIVENESS_AND_DATA_GAP_REGISTER.md` | PASS; closures pending |
| Dataset datasheets | `06_DATASET_DATASHEETS_AND_SOP_REGISTER.md` | PASS |
| SOP/version register | `06_DATASET_DATASHEETS_AND_SOP_REGISTER.md`; `knowledge_inventory.csv` | PASS |
| Reproducible profiler | `../tools/profile_data_knowledge.py` | PASS |
| Profile/integrity tests | `../tests/test_data_knowledge_profile.py`; `../tests/test_evidence_integrity.py` | PASS |

## 3. Reproduction commands

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/profile_data_knowledge.py --source source_baseline --output-dir docs/stages/stage_06
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:source_baseline/src .venv/bin/python -m pytest -q -p no:cacheprovider tests source_baseline/tests
```

Expected profile summary:

- 23 CSV datasets and 27,507 CSV rows.
- 25 relationship checks with 188 issues, all deviation-event references.
- 24 knowledge items.
- 6,407 events across 8 types.
- 60 shadow email files.

## 4. Truth checks

| Check | Result |
|---|---|
| Original source is unchanged and every extracted file matches inventory | PASS |
| Database/CSV copies are not double-counted as corroboration | PASS |
| Nulls are interpreted by field/context, not as one quality score | PASS |
| Matching patient/COI strings are not called independent identity proof | PASS |
| Supplied KPI formulas remain labelled unavailable | PASS |
| Synthetic coverage is not called production representative | PASS |
| Effective, draft and superseded SOPs are distinguished | PASS |
| AI/external provider data use remains denied by default | PASS |
| Missing controlled rules remain explicit gaps/unknowns | PASS |

## 5. Current fitness decisions

| Use | Fitness |
|---|---|
| Brownfield forensics | FIT |
| Deterministic domain/rule/orchestration POC | FIT WITH EXPLICIT GAPS |
| Synthetic AI summarization evaluation | CONDITIONALLY FIT after golden rubrics and local/provider controls |
| Real identity resolution or product disposition | NOT FIT |
| Production predictive model/performance claim | NOT FIT |
| Production compliance or benefit claim | NOT FIT |

## 6. Human decisions required

1. Approve G1 and validate Stage 5 domain/attribute authority.
2. Data owners confirm source authority, keying and gap ownership.
3. Quality/Clinical/Manufacturing owners supply missing controlled rules/ground truth.
4. Privacy/Legal/Security approve classification, permitted use and access assumptions.
5. KPI owners provide formulas/populations/windows or accept provided-only status.
6. Approve how gaps will be closed, explicitly simulated, designed as unknown, accepted or removed from scope.

## 7. Exit assessment

The Stage 6 evidence package passes internal checks and is suitable for review, but it is retained as `DRAFT PREPARED` until G1 permits formal progression and accountable owners validate its assumptions. It does not justify production data/model readiness.

## 8. Next safe action

Prepare Stage 7 evaluation specifications from the immutable six cases, ten injects, CTQs, P0 rules and twenty data gaps. Do not run or report TEVV outcomes until an implementation exists.

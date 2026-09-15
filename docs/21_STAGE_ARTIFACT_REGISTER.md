# One-to-One 21-Stage Artifact Register

**Canonical machine-readable register:** `21_STAGE_ARTIFACT_REGISTER.csv`
**Framework source:** `FDE_PDF.pdf`, Operating Model pages headed Surya 2-12
**Challenge deliverables source:** `source_baseline/participant/CHALLENGE_BRIEF.md`
**Scope of assessment:** Synthetic academic capstone; not live deployment or independent assurance

Each CSV row maps **one named essential artifact** from the 21-stage operating model to its primary canonical repository file. `S13-X01` is an extra training-sequence PRD row; it is not falsely attributed to the PDF. Related evidence may exist elsewhere, but the CSV names one place to start answering a question. A path of `-` means that there is no canonical file, not that an artifact was lost in a different folder.

## Status vocabulary

| Status | Meaning | Permitted claim |
|---|---|---|
| `PRESENT_INTERNAL` | A suitable synthetic specification/implementation/evidence file exists | Prepared or internally verified in this academic scope only |
| `PARTIAL` | File exists but PDF scope, approval, execution or evidence is incomplete | Point to both current evidence and the stated exit gap |
| `MISSING` | No canonical deliverable exists | Create a scoped artifact or retain the gap |
| `CONDITIONAL_NOT_SELECTED` | The architecture explicitly rejected or has no such feature/supplier | Do not fabricate model/RAG/multi-agent or retirement records |
| `EXTERNAL_REQUIRED` | Real people, systems, contracts or observed outcomes are necessary | Keep open until accountable external evidence is supplied |

The register currently has **185 rows**, covering **21 stages**: **88 present internally, 72 partial, 16 conditional/not selected, 9 external-required, and 0 missing canonical files**. The final row count includes the additional PRD. Status counts and exact path validity are tested by `tests/test_artifact_register.py`; counts are not a completion score because one present file may still lack sign-off and one conditional artifact may correctly remain absent.

## Architecture interpretation

The PDF's stage **output/input** phrases are higher-level gates. Stages 1-14 can be prepared or internally built on this synthetic package. Stage 15's *independently assured release candidate*, Stage 16's *operationally and legally ready release*, Stage 17's *controlled live service*, Stage 18's *operational performance*, and Stage 19's *observed benefits* cannot be achieved merely by local simulations. The Stage 20 restrict/change decision is the correct containment while external CAPAs remain open. Stage 21 records disposal of local runtime instances, not retirement of a real enterprise system.

## Client-challenge deliverables beyond the named PDF artifact rows

The v2 client challenge explicitly requires a **patient-level current-state reconstruction**, **migration strategy** and **90-day roadmap**. Their canonical locations are `docs/stages/stage_02/07_SUPPLIED_PATIENT_JOURNEY_SOURCE_RECONSTRUCTION.md`, `docs/stages/stage_13/08_BROWNFIELD_MIGRATION_STRATEGY.md` and `docs/stages/stage_20/06_PRODUCTION_GAP_AND_90_DAY_ROADMAP.md`. The reconstruction covers six supplied synthetic examples only; the roadmap is a proposed funding/evidence plan, not an automatic pilot approval.

The training delivery sequence additionally expects a standalone **PRD** before code and app. Its canonical location is `docs/stages/stage_13/06_PRODUCT_REQUIREMENTS_DOCUMENT.md`; Capstone Owner review is still pending.

## Maintenance rule

For each changed artifact, update the CSV row's canonical path, status, accountable role and exit evidence. Never mark an item `PRESENT_INTERNAL` solely because a filename exists. Before changing a stage to approved/live/production/benefit-proven, attach named owner approval and independent or observed evidence in a gate record. Scope or authority changes re-open Stage 4/7/10/12/13/15 assessments.

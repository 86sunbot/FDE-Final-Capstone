# Client Deliverable Acceptance Matrix — Architect Review

**Source:** `source_baseline/participant/CHALLENGE_BRIEF.md` names ten client deliverables. The [21-stage register](21_STAGE_ARTIFACT_REGISTER.md) maps the separate PDF operating-model artifact list. The brief and PDF are assessment sources, not permission to claim live deployment or invent approvals.

**Verdict:** the academic documents and three runnable workflow POCs are present, with an end-to-end synthetic browser demo. Several deliverables are **partial in depth or proof**. This matrix says exactly where to answer a reviewer and what not to claim.

| # | Client deliverable | Canonical answer/evidence | Academic position | Remaining proof or depth |
|---:|---|---|---|---|
| 1 | Brownfield forensic assessment | [Stage 2 forensic baseline](stages/stage_02/01_REPRODUCIBLE_FORENSIC_BASELINE.md), eight-lens assessment, inventory | Delivered internally | Real source-owner/field confirmation absent |
| 2 | Domain model and current-state journey/state reconstruction | [Stage 5 domain model](stages/stage_05/02_CAPABILITY_BOUNDED_CONTEXT_AND_CONTEXT_MAP.md), [six original patient reconstructions](stages/stage_02/07_SUPPLIED_PATIENT_JOURNEY_SOURCE_RECONSTRUCTION.md) | Partial | Six cited occurrence-time examples, not governed 800-patient or known-at projection; COI/COC and release unadjudicated |
| 3 | Problem statement and measurable KPIs | [Stage 3 SCQA/root causes](stages/stage_03/01_SCQA_AND_PRIORITIZED_PROBLEM.md), KPI tree/baseline | Partial | Synthetic forensic counts reproduced; some supplied business KPI denominators/formulas and real outcome baseline missing |
| 4 | Functional, NFR and assurance requirements | [PRD](stages/stage_13/06_PRODUCT_REQUIREMENTS_DOCUMENT.md), [31 canonical requirements](../requirements/requirements.csv), Stage 7 thresholds | Partial | 29/31 locally verified; two human studies and the [registered load condition](stages/stage_15/08_REGISTERED_JOURNEY_LOAD_TEST_PROTOCOL.md) open |
| 5 | Target architecture, ADRs, migration | [Target C4](stages/stage_10/05_TARGET_C4_BASELINE_AND_AS_BUILT_DELTA.md), [ADRs](stages/stage_13/02_FINAL_ADRS.md), [migration strategy](stages/stage_13/08_BROWNFIELD_MIGRATION_STRATEGY.md) | Delivered internally as design | Architecture owner approval, representative integration contracts and cutover evidence absent |
| 6 | Three workflow POCs | [Stage 14 engineering report](stages/stage_14/01_ENGINEERING_AND_INTEGRATION_REPORT.md), runnable browser/CLI, integration/E2E tests | Delivered internally | Scripted fixture differs from original v2 source patients; no live MES/QMS/clinical action |
| 7 | Evaluation/TEVV edge, adversarial, outage and authority | [Stage 7 frozen catalog](stages/stage_07/evaluation_catalog.json), [Stage 15 TEVV](stages/stage_15/01_TEVV_REPORT.md) | Partial | 55 structural passes, 7 original full scoped/9 partial, 39 extension structural-only; human/live-model/full outage and load evidence open |
| 8 | Security, privacy, responsible AI and governance | [Stage 12 threat/OWASP](stages/stage_12/01_THREAT_MODEL.md), [academic AI-system card](stages/stage_12/06_ACADEMIC_AI_SYSTEM_CARD.md), Stage 4/20 analysis | Delivered internally as analysis | Independent security/privacy/Quality/supplier review not supplied |
| 9 | Resilience/recovery and operational handover | [Stage 16 runbooks](stages/stage_16/02_OPERATIONAL_RUNBOOKS.md), local restore, Stage 17/18 simulations | Partial | Real source integrations, DR, training, ownership and live operations absent |
| 10 | Production gap and 90-day roadmap | [Stage 20 gap matrix/roadmap](stages/stage_20/06_PRODUCTION_GAP_AND_90_DAY_ROADMAP.md), seven open CAPAs | Delivered as proposed plan | Sponsor funding and day-30/60/90 accountable gates not yet decided |

## Presenter rule

Say: “We built and tested a synthetic FDE control-tower demonstrator and documented all ten deliverables to their available academic depth. The client end goal is a globally scalable governed product, not a web page or three isolated POCs. The source-backed views help discovery, while a real pilot requires the open owner, policy, integration, human-factor, security and independent-assurance gates.”

Do not say: “All 21 stages are approved,” “55 scenarios fully pass,” “the original 800 patient journeys are migrated,” “the app is production-ready,” or “ROI is proven.”

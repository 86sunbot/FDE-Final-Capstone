# Final Capstone Report

## 1. Context

Cell and Gene Therapy delivery depends on one traceable journey across patient enrollment, identity/chain of identity, consent, authorization, treatment-center readiness, collection, logistics, manufacturing, QC, deviations, Quality release, return shipment and clinical readiness. The supplied brownfield package intentionally contains conflicting data, inconsistent authority, legacy shortcuts and shadow operations.

## 2. Problem statement

The organization cannot safely answer “what is the current patient-to-batch state, why, who can decide, and what happens next?” from fragmented systems. Direct joins and status labels can invent identity, treat manufacturing/inventory status as Quality release, ignore prerequisites, duplicate reservation effects and hide uncertainty.

## 3. Achievement

The capstone delivers an evidence-driven modular orchestration POC with one common domain model, a responsive browser Control Tower and three vertical journeys:

1. patient identity conflict, authorized resolution and milestone readiness;
2. manufacturing-slot reservation, idempotent replay, unknown outcome reconciliation and compensation;
3. QC/deviation/thermal evidence packet and Quality-authorized release.

AI is placed outside the authority boundary. It can only return a cited recommendation schema and has no consequential tool. AI off is the default and complete deterministic behavior remains available.

## 4. 21-stage operating-model outcome

| Wave | Stages | Outcome |
|---|---|---|
| Understand | 1–4 | Immutable evidence, current-state diagnosis, CTQs, bounded intended use and G1 |
| Model/select | 5–8 | Domain/data/evaluation baselines and O3 solution selection |
| Design | 9–13 | Information contracts, C4/API/AI/agent/security designs, 27 requirements, 12 ADRs and G3 |
| Build | 14 | Shared foundation, three POCs, API/CLI, CI/container and manifests |
| Assure/operate | 15–18 | TEVV, red team, recovery, runbooks, simulated shadow/canary/rollback/monitoring |
| Prove/decide/close | 19–21 | Limited value claim, AIMS/CAPA review, restrict/change decision and retirement/IP |

## 5. Evidence

- Clean suite: 77 passed, 0 failed/error/skipped.
- Frozen catalog: 57 executed; 55 pass; 0 fail; 2 inconclusive external human studies.
- P0 catalog: 44 pass; one human-factor case inconclusive.
- Requirements: 25 verified for internal POC; two require external human evidence; zero production verified.
- Performance: 5,000-iteration local deterministic benchmark passed its p95 threshold.
- Recovery: restored state digest matched and audit chain verified.
- Simulated release: 20/20 shadow matches, 10/10 canary success and AI-off rollback pass.
- Evidence integrity: original ZIP digest and 132 extracted file digests verified.

## 6. Honest limitations

No real stakeholder study, controlled Quality/clinical policy, real identity ground truth, enterprise IAM/e-signature, external integration, production infrastructure, live model/provider, real patient data, independent assurance or real before/after KPI exists. Therefore the project does not claim clinical benefit, deployment safety, regulatory compliance, validation, savings or ROI.

## 7. Final decision

The academic POC is complete. The lifecycle decision is **RESTRICT AND CHANGE**: retain the engineering IP and evidence, keep AI off, and do not conduct a real pilot until the seven CAPAs in `stage_20/02_INTERNAL_AUDIT_AND_CAPA.md` are closed through a new accountable gate sequence.

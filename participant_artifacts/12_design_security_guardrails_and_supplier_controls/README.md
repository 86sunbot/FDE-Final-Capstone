# Stage 12 — Design Security, Guardrails & Supplier Controls

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 12 — Design Security, Guardrails & Supplier Controls  
**Participant status:** `APPROVED_FOR_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic/academic capstone  
**Approval note:** Internal capstone evidence only. External sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy, independent-assurance and production approvals are not implied.

## Decision / outcome

Apply threat modeling, least privilege, prompt-injection isolation, privacy controls, supplier inventory, SBOM/AIBOM and provider exit planning.

**Artifact-specific outcome:** This participant folder formalizes the canonical Stage 12 evidence already completed under `docs/stages/stage_12/`.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Canonical source | Preserve all Stage 12 documents and machine-readable outputs. | `docs/stages/stage_12/` | Source of truth |
| Product boundary | Synthetic/local academic capstone. | `docs/CAPSTONE_PROGRESS_TRACKER.md` | Hard boundary |
| Authority boundary | No autonomous Clinical, Quality, consent, identity/COI, custody or other consequential authority. | `source_baseline/AGENTS.md` | Hard boundary |
| Traceability | Requirements, tests/evals, risks and lifecycle decisions remain linked. | `requirements/TRACEABILITY_MATRIX.csv` | Required |

## Operating rules

1. Preserve raw evidence, conflicts, uncertainty, authority, freshness and time semantics.
2. QMS/authorized Quality remains product-release authority.
3. Do not fabricate identity/COI/custody resolution or stakeholder approval.
4. Deterministic controls remain primary for gates, permissions, retries, idempotency and audit.
5. AI is bounded, optional and removable; AI-off remains a supported path.
6. Synthetic/simulation results are not production, clinical, regulatory, validation or ROI proof.
7. Open CAPAs remain visible until accountable owners close them.

## Evidence and traceability

| Claim / decision | Canonical evidence | Confidence / limitation |
|---|---|---|
| Stage 12 decision | `docs/stages/stage_12/` | High for current repository state |
| Lifecycle/status | `docs/CAPSTONE_PROGRESS_TRACKER.md` | High for academic capstone |
| Requirements linkage | `requirements/requirements.csv`; `requirements/TRACEABILITY_MATRIX.csv` | Internal POC evidence |
| Final verification | `evidence/final_verification.json` | Internal verification; not independent assurance |

## Completion check

- [x] Canonical Stage 12 artifacts are present.
- [x] Machine-readable evidence is preserved.
- [x] Academic/synthetic limits are explicit.
- [x] Open approvals and CAPAs remain open.
- [x] Human, deterministic and AI responsibilities remain distinguishable.
- [x] No production authorization is fabricated.

## Handoff

**Stage exit contribution:** Controlled architecture and component/supplier baseline.  
**Gate status:** `APPROVED_FOR_POC`.

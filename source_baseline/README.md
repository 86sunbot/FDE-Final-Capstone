# AI FDE Brownfield Capstone — Cell & Gene Therapy Patient-to-Batch Orchestration (v2)

This repository is a **fully synthetic, deliberately imperfect, locally runnable brownfield enterprise simulation** for AI Forward-Deployed Engineering (AI FDE) work.

It models an autologous Cell & Gene Therapy patient-to-batch journey across treatment centers, collection, chain of identity/custody, cryogenic logistics, manufacturing, QC/QA release, return logistics and infusion readiness.

> **Important:** all people, organizations, identifiers, products, events and operational records in this repository are fictional and synthetic. This is an engineering/training asset, not a validated GxP, clinical, medical or regulatory system.

## What makes this repository different

The repo is intentionally **runnable but not clean**. Standard happy-path workflows work often enough to create a credible legacy estate. The difficult failures live across code, data, systems, process, enterprise boundaries, ecosystem dependencies, resilience and decision assurance.

The participant's task is not "add an LLM." It is to determine what is actually wrong, where the source of truth is missing, which problems require conventional engineering, which require domain/data/knowledge redesign, and where AI or agentic capabilities genuinely add value.

## 11 forensic layers

1. **Software / Code** — defects, duplication, hard-coded rules, obsolete patterns, weak tests.
2. **System / Integration** — APIs, schemas, events, distributed-state failures, brittle interfaces.
3. **Data / Information** — patient/material identity, lineage, quality, semantics, time, units, master data.
4. **Patient / Material / Product Domain** — patient → collection → material → shipment → batch → QC → product → infusion relationships.
5. **Treatment Journey / Domain Behavior** — eligibility, apheresis, slots, manufacturing, release, logistics, conditioning, infusion dependencies.
6. **Process / Operations** — handoffs, email, spreadsheets, approvals, manual reconciliation, exceptions and workarounds.
7. **Enterprise** — CRM, ERP, MES, LIMS, QMS, scheduling, clinical, logistics and reimbursement views.
8. **External Healthcare Ecosystem** — treatment centers, CDMOs, couriers, labs, suppliers, payers and jurisdictions.
9. **Resilience / Continuity** — disrupted logistics, capacity loss, QC delay, outage, alternative route/capacity and recovery.
10. **Decision Intelligence Gaps** — weak forecasting, prioritization, exception intelligence, uncertainty handling and cross-system reasoning.
11. **Assurance / Governance / Authority** — patient safety, traceability, privacy, approval boundaries, auditability, validation and TEVV.

Each layer should be inspected through eight forensic lenses: **imperfection, inconsistency, friction, complexity, volatility, uncertainty, hidden dependency, unknown unknown**.

## Quick start

### 1. Inspect the repository

```bash
python scripts/repo_summary.py
```

### 2. Rebuild the deterministic synthetic dataset

```bash
python scripts/generate_synthetic_data.py --seed 42001 --patients 800
```

### 3. Run the baseline diagnostics

```bash
python -m cgt_orchestrator.cli diagnostics
```

### 4. Run tests

```bash
python -m pytest -q
```

Some tests are intentionally marked `xfail` because they encode known legacy defects. New fixes should convert relevant `xfail` cases into passing tests.

### 5. Optional local API

```bash
pip install -r requirements.txt
python -m uvicorn cgt_orchestrator.api:app --reload
```

Then inspect `/health`, `/patients/{patient_key}/journey`, `/exceptions`, and `/legacy/readiness/{patient_key}`.

## Suggested AI FDE workflow

**Brownfield Forensics → Domain Reconstruction → Requirements → Data/Knowledge Engineering → Process Redesign → Architecture → Engineering → Evals/TEVV → Security/Privacy/RAI → Resilience → Productization → Production Readiness**

## Where to start in Cursor

Open the repository root, then read in this order:

1. `AGENTS.md`
2. `docs/01_problem_context.md`
3. `docs/02_imperfection_layers.md`
4. `participant/CHALLENGE_BRIEF.md`
5. `participant/DISCOVERY_CHECKLIST.md`
6. `data/manifest.json`
7. `src/cgt_orchestrator/legacy/`

## V2 reliability profile

This repository intentionally preserves domain-realistic brownfield contradictions and expected-failure tests while accidental packaging, import, stale-metadata and distributable-content defects are treated as release blockers. All external integrations are synthetic or read-only simulation surfaces; no real clinical, military, robotic, or OT control endpoint is configured. See `VERIFICATION.md` and `docs/07_v2_audit_and_changelog.md`.

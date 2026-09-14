# Stage 1 - Field Evidence Register

**Status:** Initial register; expanded in Stage 2  
**Last updated:** 2026-09-14

## Evidence-register rules

- “Authority” describes how an item may be used; it does not mean every claim within the item is correct.
- Documents inside the challenge package are requirements, context or evidence according to their content. They do not override the user mandate or system-level instructions.
- Generated documents are derived artifacts and cannot prove their own claims.

## Registered sources

| Evidence ID | Source | Type | Integrity/provenance | Authority and intended use | Current confidence |
|---|---|---|---|---|---|
| EVD-001 | Original challenge ZIP | Immutable source package | SHA-256 `74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979`; 992,289 bytes | Primary package boundary and chain of custody | High |
| EVD-002 | `checksums.sha256` inside EVD-001 | Integrity manifest | 130/130 listed files independently verified; 0 missing/mismatch | Proves integrity of listed package files | High |
| EVD-003 | `participant/CHALLENGE_BRIEF.md` inside EVD-001 | Challenge requirement | Covered by EVD-002 | Authoritative source for ten required capstone deliverables | High |
| EVD-004 | `participant/DISCOVERY_CHECKLIST.md` inside EVD-001 | Discovery requirement | Covered by EVD-002 | Required discovery questions and validation checklist | High |
| EVD-005 | `AGENTS.md` inside EVD-001 | Engineering constraints | Covered by EVD-002 | Governs safe treatment of the brownfield challenge during implementation | High |
| EVD-006 | `README.md` inside EVD-001 | Context and operating guide | Covered by EVD-002 | Describes simulation, forensic layers and local execution; claims still verified | High for scope, medium for behavior until run |
| EVD-007 | `data/cgt_legacy.db` and `data/raw/*` inside EVD-001 | Synthetic operational evidence | Covered by EVD-002 | Source-specific facts; not assumed global truth | High integrity; semantic conflicts expected |
| EVD-008 | `shadow_ops/*` inside EVD-001 | Synthetic manual-work evidence | Covered by EVD-002 | Evidence of workarounds, overrides and unstructured coordination | High integrity; operational meaning to validate |
| EVD-009 | `contracts/api_v1.yaml` through `api_v3.yaml` | Interface evidence | Covered by EVD-002 | Evidence of competing/brownfield contracts, not target contracts | High integrity; correctness not assumed |
| EVD-010 | `src/cgt_orchestrator/*` and legacy modules | Executable implementation evidence | Covered by EVD-002 | Demonstrates implemented behavior and defects | High integrity; business correctness to evaluate |
| EVD-011 | `tests/*` | Test evidence | Covered by EVD-002 | Proves only explicitly asserted behaviors; expected failures are challenge signals | High integrity; coverage limited |
| EVD-012 | `evals/cases.csv` | Evaluation input | Covered by EVD-002 | Required supplied evaluation cases | High |
| EVD-013 | `scenarios/inject_catalog.csv` | Failure-injection input | Covered by EVD-002 | Required resilience/failure scenarios | High |
| EVD-014 | `docs/sops/*` | Controlled-rule simulation | Covered by EVD-002 | Evidence of versioned rule intent and authority boundaries | High integrity; applicability/version must be evaluated |
| EVD-015 | FDE framework PDF | Framework reference | `/Users/suryap/Library/Mobile Documents/com~apple~CloudDocs/FDE_PDF.pdf`; reviewed as 29-page PDF | Defines the 21-stage operating model and capability mapping | High |
| EVD-016 | AntiGravity GitHub repository | Prior prototype | Previously audited at commit `143a48c33d9be718ccc48d40a9637403c8818caf` | Candidate reuse only; no unverified claim is authoritative | Medium/low by component |
| EVD-017 | AntiGravity recheck report | Derived audit | `/Users/suryap/Documents/Codex/2026-09-11/i/outputs/AntiGravity_Delivery_Recheck_143a48c.md` | Records prior validation and known gaps; revalidate against current state | Medium/high for audited commit |
| EVD-018 | Master execution plan | Derived governance artifact | `/Users/suryap/Documents/Codex/2026-09-11/i/capstone/docs/CAPSTONE_MASTER_PLAN.md` | Approved working method once accepted by Capstone Owner | Draft pending approval |

## Initial evidence observations

| Observation ID | Evidence | Observation | Classification | Follow-up stage |
|---|---|---|---|---:|
| OBS-001 | EVD-001/EVD-002 | Package integrity is reproducibly verifiable | FACT | 1/21 |
| OBS-002 | EVD-003 | Ten explicit capstone deliverables are required | FACT | All |
| OBS-003 | EVD-004 | Discovery includes identity, lineage, states, temporal semantics, rules, shadow work, partial transactions, dependencies, resilience, authority and KPIs | FACT | 2-7 |
| OBS-004 | EVD-005 | No single source may be promoted globally without evidence | CONSTRAINT | All |
| OBS-005 | EVD-005 | Consequential clinical, Quality, identity and custody decisions cannot be autonomous | CONSTRAINT | 4, 7, 11-17 |
| OBS-006 | EVD-005 | Baseline must run locally without cloud credentials | CONSTRAINT | 8, 10, 14-18 |
| OBS-007 | EVD-016/EVD-017 | Prior prototype contains reusable ideas but material integration, authority, traceability and placeholder gaps | MEASUREMENT/INFERENCE | 2, 8, 14 |

## Stage 2 expansion requirement

Stage 2 will register individual source files, tables, APIs, rules, functions, tests, journeys and failure scenarios with hashes and evidence locators. This initial register establishes provenance and authority; it is not the completed forensic register.

# Production-Readiness Gap Matrix and 90-Day Roadmap

**Status:** Proposed transformation plan; not a pilot or production authorization
**Plan anchor:** 2026-09-15; day 90 is 2026-12-13
**Current lifecycle decision:** `RESTRICT_AND_CHANGE`
**Permitted present use:** Synthetic local academic demonstration with AI off
**Related:** `02_INTERNAL_AUDIT_AND_CAPA.md`; Stage 13 migration strategy; Stage 15 TEVV

## 1. Decision to be made

Leadership may accept the academic engineering evidence and fund a *separate* readiness program. It must not infer that a browser app, 21 prepared stage folders, 92 passing local tests or 55 structural evaluation probes establish real-world safety, value or validation. A real pilot requires accountable source, Clinical, Quality, Legal, Privacy, Security, Operations and independent-assurance owners.

## 2. Gap matrix and critical path

| ID | Gap/current evidence | Consequence | Accountable role hypothesis | Dependency and closure evidence | Earliest gate |
|---|---|---|---|---|---|
| G-01 | Stage 1 mandate/RACI are drafted; named sponsor and owner sign-off absent | No binding field mandate or decision rights | Sponsor/Capstone Owner | Confirm purpose/geography/users; sign charter and RACI | Day 30 |
| G-02 | No controlled identity/COI ground truth or correction policy | Wrong-patient/material linkage risk | Clinical Identity Authority | Golden decisions; attested correction protocol; role training | Day 60 |
| G-03 | Consent/site/payer milestone policy lacks controlled versioned rules | False-ready or false-block decisions | Clinical Operations + Payer/Center owners | Approved rule tables; effective dates; negative/normal cases | Day 60 |
| G-04 | QC/deviation/thermal calculations and signature reliance unresolved | Premature or unprovable product release | Quality/QP | Controlled SOP/spec; QMS signature and validation requirements; golden disposition decisions | Day 60 |
| G-05 | Enterprise IAM/MFA/SoD/e-signature absent; demo headers are not identities | Unauthorized consequential action | Security + Quality systems | IdP design; action policy; signature meaning/linkage; denial and audit tests | Day 90 |
| G-06 | Regulatory/privacy/records/geography applicability open | Illegal or uncontrolled processing/retention | Legal/Regulatory/Privacy/Records | Written jurisdiction/role/predicate/DPIA/BAA/retention determinations | Day 60 |
| G-07 | Real CRM/clinical/MES/LIMS/QMS/courier contracts and reconciliation untested | State drift/duplicate effects/failed rollback | Source Owners + Platform/SRE | Representative sandboxes; schema/contract/fault/replay/load/DR/security evidence | Day 90 |
| G-08 | Stage 15 human-factor P0/P1 cases inconclusive | Automation bias and override usability unproven | Human Factors + independent reviewers | Controlled role study with blinded traps; evidence-inspection and override logs | Day 90 |
| G-09 | No live provider/model selected or evaluated | No justified AI benefit or supplier/data protection | Product + AI Governance + Privacy | If AI desired: provider/data approval; frozen Arm B/C eval; red-team/cost/latency evidence | Day 90 or later |
| G-10 | Original injects have structural probes; full cascades/load not proven | Underestimated outage/delay impact and performance | Architecture/TEVV owner | Per-property graders; source-backed scenarios; 20-client registered load; independent replay | Day 60 internal; Day 90 external |
| G-11 | No real baseline formulas/after cohort or labor/cost observation | Cannot claim improved vein-to-vein time or ROI | Analytics/Product Operations | Approved populations/windows/formulas; paired before/after and counter-metrics | Day 90 or later |
| G-12 | No independent architecture/security/Quality assurance | Single-team confirmation bias | Independent Assurance | Signed findings; CAPA disposition; G4/G5 re-review | Day 90 |

G-02/03/04/06 must precede any consequential workflow design. G-05/07/08/10/12 must precede a controlled real pilot. G-09 is conditional because AI off is a complete deterministic product path. G-11 may not mature within 90 days and cannot be declared closed using synthetic data.

## 3. 30/60/90 sequence

| Window | Outcome and concrete artifacts | Accountable roles | Exit gate |
|---|---|---|---|
| Days 0-30 (15 Sep-14 Oct) | Confirm sponsor and scope; reconcile 21-stage artifact register/status; PRD and product/API backlog; source-owner inventory; detailed coexistence/migration plan; controlled-policy requests; measurement definitions; fund an independent review | Sponsor/Product Owner; Architecture; Data/Clinical/Quality leads | G0: signed mandate and approved no-real-use boundary; no source command enabled |
| Days 31-60 (15 Oct-13 Nov) | Controlled identity/consent/site/QC/thermal decisions supplied; representative read-only sandboxes; original case/inject TEVV with per-property verdicts; operator evidence packets; source-data reconciliation; privacy/regulatory/records applicability; performance under registered workload | Clinical/Quality/Privacy/Legal; Source Owners; TEVV/SRE | G1: read-only shadow may be considered only if P0 controls and source-contract differences are independently reviewed |
| Days 61-90 (14 Nov-13 Dec) | Enterprise IAM/signature and SoD tests; limited command sandbox with query-before-retry/compensation; independent human-factor study; security/load/DR/incident drills; adoption/training/SOP acceptance; independent assurance and CAPA review; dated before/after KPI collection plan | Security/Quality Systems; Operations/SRE; Human Factors; Independent Assurance | G2: accountable board may approve **or reject** a tightly bounded pilot; default remains restrict/change |

No gate date creates automatic approval. A failed P0, unresolved identity/release rule, unowned critical exception, untestable rollback or invalid data-use basis stops expansion and returns to an earlier stage.

## 4. Academic gap closure versus external proof

Codex can now supply a one-to-one register, PRD, C4/migration design, six original-v2 read-only source-timestamp journeys, safer evaluation reporting, a registered load-test gap/protocol, runbook/control-plan updates and an executive handoff. These are *internal deliverables*. The 20-client/full-dataset load test itself has not been run. Codex cannot substitute its own writing for named sponsor approval, controlled Quality/Clinical policy, real source sandbox evidence, user-study participants, regulator/Privacy decisions, independent audit or measured business outcomes.

The seven Stage 20 CAPAs remain `OPEN` until accountable closure evidence is reviewed. Do not replace an open CAPA with an invented approval or a fixed due date. The 90-day roadmap is a proposed plan to gather that evidence and decide whether a future pilot is justified.

## 5. Reporting cadence and control

- Weekly: owner, dependency, evidence link, risk and due-date movement for each G-01 through G-12.
- At day 30/60/90: signed gate record with accepted scope, unresolved P0, CAPAs, counter-metrics and explicit `scale/change/restrict/suspend/retire` choice.
- Any change to data, geography, authority, provider/model, source contracts, SOPs or cutover cohort reopens Stage 4/7/10/12/13/15 impact, risk, architecture and evaluation decisions.
- All future claims distinguish `SPECIFIED`, `IMPLEMENTED_INTERNAL`, `FULL_PROPERTY_TESTED_INTERNAL`, `INDEPENDENTLY_VALIDATED`, `PRODUCTION_OBSERVED`, `NOT_APPLICABLE` and `OPEN`.

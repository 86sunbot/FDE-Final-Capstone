# Stage 2 - Waste, Dependency and Current-State Risk Register

**Status:** Evidence-backed draft  
**Last updated:** 2026-09-14

## 1. Lean waste register

| Waste ID | Lean category | Observed waste | Evidence | Operational effect | Candidate measure |
|---|---|---|---|---|---|
| W-001 | Defects | Unsafe readiness conclusions | F-READY-001..004 | Rework, escalation and patient-safety exposure | Unsafe-ready classification rate |
| W-002 | Overprocessing | Reconcile formal priorities against shadow spreadsheet | F-SHADOW-001 | Repeated manual comparison | Reconciliation touches per journey |
| W-003 | Waiting | Open/unowned courier escalations | F-SHADOW-004 | Delay without accountable next action | Exception age and unowned duration |
| W-004 | Handoffs | Slot, identity, QA and site work in email | F-SHADOW-003 | Lost context and repeated explanation | Email/manual handoffs per case |
| W-005 | Rework | Retry creates duplicate manufacturing-start events | F-INTEG-001 | Duplicate processing/investigation | Semantic duplicate event rate |
| W-006 | Inventory/capacity | Scheduler confirms capacity cancelled by MES | F-INTEG-002 | Stranded or double-allocated capacity | Slot conflict rate |
| W-007 | Motion/search | Quality reviewers cannot resolve linked event evidence | F-QUALITY-002 | Manual evidence hunting | Evidence retrieval time/completeness |
| W-008 | Waiting | QC/non-pass evidence lacks visible disposition context | F-QUALITY-003 | Release review delay or unsafe assumption | Time from result to disposition |
| W-009 | Overproduction | Multiple status surfaces repeat partial state | Current landscape | More data without more truth | Number of conflicting state surfaces |
| W-010 | Underused expertise | Experts spend time assembling evidence rather than deciding | Shadow workflow evidence | Scarce QA/clinical/planner capacity consumed | Expert time on evidence collection vs decision |

## 2. Dependency register

| Dependency ID | Upstream evidence/change | Downstream dependency | Current visibility | Failure impact |
|---|---|---|---|---|
| DEP-001 | Patient identity resolution | COI, collection, shipment, batch and product linkage | Low | Wrong individualized-therapy association |
| DEP-002 | Consent state/effective version | Collection and downstream clinical progression | Low | Unauthorized continuation |
| DEP-003 | Financial authorization | Scheduling and commercial readiness | Partial | Preventable cancellation/delay |
| DEP-004 | Site training/equipment/agreement | Apheresis and clinical milestones | Partial | Procedure at unqualified site |
| DEP-005 | Collection timing/quality | Courier, slot and manufacturing plan | Fragmented | Missed slot or material risk |
| DEP-006 | Courier route/custody/telemetry | Receipt, manufacturing and product viability | Fragmented | Delay, chain break or Quality hold |
| DEP-007 | Slot state and capacity | Manufacturing start and downstream QC plan | Contradictory | Double booking or idle capacity |
| DEP-008 | Manufacturing completion | QC execution | Visible but semantically conflated | Incorrect release/readiness |
| DEP-009 | QC result and disposition | QA release | Incomplete | Release delay or unsafe interpretation |
| DEP-010 | Blocking deviation disposition | QA release | Missing classification/linkage | Premature release or unnecessary hold |
| DEP-011 | QA release and signature | Return shipment, conditioning and infusion readiness | Contradictory downstream state | Patient preparation before safe product availability |
| DEP-012 | Return shipment arrival and thermal disposition | Product-at-site/viability | Contradictory | Incorrect conditioning/infusion readiness |
| DEP-013 | Source event delay/out-of-order delivery | Derived journey projection | Not managed | Stale or retroactively changed state |
| DEP-014 | QMS/MES/courier availability | Exception and command workflow | No degraded-mode orchestration | Operational stop or unsafe workaround |

## 3. Current-state risk register

| Risk ID | Risk | Likelihood | Impact | Initial level | Evidence | Existing control | Gap |
|---|---|---|---|---|---|---|---|
| R-CS-001 | Incorrect patient/material identity linkage | Possible | Catastrophic | Critical | F-IDENT-001..005 | Human reconciliation in email | No governed evidence/confidence/resolution case |
| R-CS-002 | Product considered ready without Quality authority | Likely | Catastrophic | Critical | F-READY-001..004 | QMS field exists | Legacy rule and downstream states bypass its meaning |
| R-CS-003 | Workflow proceeds despite invalid consent | Possible | Catastrophic | Critical | F-GATE-001; eval P-00157 | Consent table | No shared enforced gate/termination behavior |
| R-CS-004 | Site/authorization dependency missed | Likely | Major | High | F-GATE-002; F-SITE-001 | Separate source records | No cross-domain revalidation |
| R-CS-005 | Quality evidence cannot be reconstructed | Likely | Major | High | F-QUALITY-001..003 | QMS/QC tables | Broken event links and missing disposition semantics |
| R-CS-006 | Duplicate or conflicting manufacturing reservation/action | Possible | Major | High | F-INTEG-001..002 | Manual planner checks | No idempotency, ledger or compensation |
| R-CS-007 | Thermal evidence misinterpreted | Possible | Major | High | F-THERMAL-001; SOP v6/v7 | Human Quality authority documented | Code uses superseded point rule; evidence incomplete |
| R-CS-008 | Late/out-of-order evidence produces wrong current state | Likely | Major | High | F-TIME-001..003 | Timestamps recorded | No bitemporal projection/replay policy |
| R-CS-009 | Critical exception remains unowned | Likely | Major | High | F-SHADOW-004 | CSV owner column | No assignment/escalation/SLA control |
| R-CS-010 | Untrusted email/document influences AI or action | Possible | Major | High | Eval P-00301 and shadow emails | Documented warning only | No implemented instruction/data boundary |
| R-CS-011 | Source outage leads to unsafe workaround | Possible | Major | High | Injects INJ-003/004/008/009 | None evidenced | No tested degraded mode or recovery |
| R-CS-012 | Users overtrust a recommendation or status | Possible | Major | High | Fragmented status and future AI use | Human authority statement | No human-factors design or counter-metric |

These are current-state engineering risks, not a formal ISO 42005 assessment. Stage 7 will define risk methodology, harms, treatments, acceptance and ownership.

## 4. Current-state control gaps

- Attribute-level source authority.
- Explainable identity/lineage reconciliation.
- Complete domain/event semantics.
- Bitemporal state reconstruction.
- Persistent idempotency and concurrency control.
- Inbox/outbox, command ledger and compensation.
- Blocking-deviation and QC-disposition model.
- Authenticated human approval and separation of duties.
- Comprehensive exception ownership and escalation.
- AI input/context isolation and structured output validation.
- Business-level observability, SLOs and recovery evidence.

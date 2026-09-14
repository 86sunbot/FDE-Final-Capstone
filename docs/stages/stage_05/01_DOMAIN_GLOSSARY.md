# Stage 5 - Canonical Domain Glossary

**Status:** READY FOR REVIEW; academic G1 approved; domain-owner validation pending  
**Last updated:** 2026-09-14

## Modeling principles

1. A source value is an assertion with provenance, not automatically enterprise truth.
2. No single table, system or identifier is the global source of truth.
3. The canonical model preserves raw evidence and disagreement.
4. Identity, lineage, Quality and clinical decisions require explicit authority.
5. Unknown, conflicting, missing and not-applicable are different states.
6. Manufacturing completion, inventory availability, Quality release and patient readiness are different concepts.
7. Occurrence time, recording time and effective policy time are independently modeled.

## Core terms

| Term | Canonical meaning | Not equivalent to | Authority/evidence note |
|---|---|---|---|
| Patient | The natural person for whom an individualized therapy journey is performed | A row, MRN, CRM ID or subject ID | Real-world identity is never inferred from one identifier |
| Patient key | Synthetic dataset join key such as `P-00001` | Proven enterprise master identifier | Technical fixture key only in the challenge |
| Identity assertion | A source's claim about an identifier or demographic attribute | Resolved identity | Carries source, time, value and evidence quality |
| Identity resolution | Authorized conclusion about how identity assertions relate | Probabilistic match alone | Human-authorized under approved identity policy |
| Therapy journey | Coordinated lifecycle for one intended patient/product course | Patient master record or a source `journey_status` | Canonical projection built from evidence and decisions |
| Product code | Therapy/product family reference | A patient-specific product instance | Reference/master-data assertion |
| Collection | Source material collected from a patient at a treatment center | A released therapeutic product | Anchored by collection, bag and COI evidence |
| Bag | Physical collection container identifier | Collection or COI | May be one of multiple evidence identifiers |
| Chain of Identity (COI) | Evidence that material/product is associated with the intended patient throughout the journey | A repeated string alone | Must be verified from governed events/scans; never fabricated |
| Chain of Custody (COC) | Evidence of possession, transfer and handling over time | Shipment status | Requires actor/location/time/transfer evidence |
| Shipment | Physical movement of collection material or product | Quality disposition | Direction, custody, route and timestamps are explicit |
| Outbound shipment | Collection material moving from treatment center to manufacturing | Return shipment | May not have a batch at booking time |
| Return shipment | Manufactured product moving to treatment center | Proof of infusion readiness | Requires product/batch and receipt evidence |
| Telemetry observation | Sensor measurement with value, unit, time, quality and provenance | Excursion or disposition | Raw observation remains immutable |
| Thermal assessment | Controlled evaluation of a telemetry profile and related evidence | Single threshold comparison | Consequential disposition remains Quality-authorized |
| Manufacturing slot | Capacity allocation proposal/reservation for a journey at a site/time | MES execution state | Scheduler owns planning state; MES owns execution acknowledgement |
| Reservation command | Idempotent request to create/change/cancel a capacity allocation | Confirmed reservation | Has payload digest, lifecycle, attempts and outcomes |
| Manufacturing batch | Patient-specific manufacturing execution unit linked to collection/COI/product | Product release | MES state describes execution, not Quality authority |
| Manufacturing complete | MES evidence that manufacturing processing completed | QC complete, QMS release or ERP availability | Cannot authorize downstream clinical readiness |
| QC result | Assay observation/result associated with a batch | Final product disposition | LIMS evidence includes method, unit, sample/report time and disposition context |
| Out-of-specification (OOS) | QC result identified outside specification | Automatic batch rejection | Investigation/disposition semantics are required |
| Out-of-trend (OOT) | QC result outside expected trend | OOS or automatic hold | Policy and investigation context required |
| Deviation | Quality case concerning a departure or possible departure | Blocking decision by status alone | Impact/blocking/disposition must be explicit and Quality-owned |
| Quality release | Authorized decision that specified release prerequisites are satisfied | MES `RELEASED` or ERP `AVAILABLE` | Only an authenticated Quality/QP decision can establish it |
| Consent assertion | Versioned evidence of consent state and signature time | Eternal permission for every milestone | Must be effective/current and revalidated where required |
| Financial authorization | Payer/reimbursement status for the journey | Clinical eligibility or Quality release | May be provisional for early scheduling if approved policy permits |
| Site qualification | Evidence that a treatment center meets current controls | A reference-table status alone | Training, equipment, agreement and expiry remain visible |
| Milestone prerequisite | Versioned evidence/rule needed to enter a specific journey phase | Global `patient_ready` Boolean | Evaluated for a named milestone and point in time |
| Journey projection | Reproducible interpretation of events/assertions/decisions at a time | Source truth | Shows evidence, conflicts, policy version and projection time |
| Source status | Status string supplied by one system | Canonical state | Retained unchanged with its source semantics |
| Canonical state | Controlled state produced by legal transitions and evidence | A mapped source status without validation | Must cite transition event and rule/decision evidence |
| Blocked | A known prerequisite failed or a controlled hold exists | Unknown | Carries blocker, owner and remediation path |
| Unknown | Required evidence or semantics is missing/insufficient | False, safe or not applicable | Fails closed for safety/consequential progression |
| Conflict | Two or more relevant assertions cannot all be accepted under current rules | Bad data that may be silently overwritten | Opens a governed resolution case |
| Exception case | Owned workflow for investigation, decision, escalation and closure | Alert or email | Has type, severity, SLA, owner, evidence and outcome |
| Recommendation | Non-binding option/explanation for a human | Decision, approval or action | Includes evidence, uncertainty and required authority |
| Decision | Authorized conclusion with reason and evidence | Recommendation | Actor authority and effective/recorded time required |
| Approval | Decision permitting a controlled transition or action | Authentication alone | Must be attributable and policy-valid |
| Electronic signature | Electronic signing intended to carry the defined meaning and bind signer to record | Typed name or role string | Validation/applicability depends on actual regulated use |
| Command | Requested side effect against a bounded service/adapter | Domain event | Must be idempotent and payload-bound |
| Domain event | Immutable statement that a relevant fact/decision/action occurred | Command or current row | Past tense; has occurred and recorded time |
| Occurred time | When the represented business fact happened | When the platform learned it | Source uncertainty is retained |
| Recorded time | When the platform persisted/observed the fact | Occurred time | Enables bitemporal replay and late-event handling |
| Effective time | When a rule, SOP, decision or assertion applies in the domain | Creation time | Required for versioned policy evaluation |
| Provenance | Where evidence came from and how it was transformed | Free-text citation | Includes source, record, version, time and transformation |
| Idempotency key | Stable identity for one intended command | Random retry request ID | Reuse with different payload is a conflict |
| Compensation | Explicit business action to address a completed partial step | Database rollback after external effect | Is observable, governed and may require human approval |
| Audit record | Append-only evidence of who/what did or attempted what and why | Application log alone | Must support authority, state and evidence reconstruction |

## Terms deliberately rejected

| Rejected term/use | Reason | Replacement |
|---|---|---|
| “Single source of truth” for the estate | Authority is attribute/decision specific and sources disagree | Source-specific evidence plus governed canonical projection |
| `patient_ready` as one Boolean | Omits milestone, evidence, unknowns and authority | `MilestoneAssessment` with decision table and evidence |
| `RELEASED` without context | MES and QMS meanings differ | `ManufacturingStatus` versus `QualityReleaseDecision` |
| “AI decision” for consequential work | Conceals authority and accountability | AI recommendation plus human decision plus deterministic execution |
| “Temperature excursion = failed product” | Superseded single-point logic | Thermal evidence profile plus Quality disposition |
| “Resolved identity” from matching confidence | Probability is not authority | Candidate relationship plus authorized resolution record |

## Validation questions for domain owners

- Which identity attributes can each source authoritatively assert, and at what time?
- Which milestones require valid consent, approved authorization and current site qualification?
- Can capacity be provisionally reserved under draft scheduling policy, and when must it be revalidated?
- Which QC results/deviations are blocking and how is disposition represented?
- What evidence confirms collection/product receipt and COI/COC transfer?
- Which state transitions require one or two human approvals?
- Which time zone, precision and correction policies govern business events?

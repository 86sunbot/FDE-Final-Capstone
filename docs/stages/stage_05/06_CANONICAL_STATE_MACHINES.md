# Stage 5 - Canonical State Machines

**Status:** Draft; legal transitions and guards require domain-owner approval  
**Last updated:** 2026-09-14

## 1. General state-machine rules

- Source statuses are evidence inputs and never directly overwrite canonical state.
- State changes only through controlled events and named guards.
- A transition records previous state, next state, event, evidence, rules, actor and time.
- Unknown/missing P0 evidence prevents progression but does not fabricate a failure fact.
- A late/corrected event rebuilds the projection and may create reassessment work.
- Holds/cases are explicit; they are not hidden in free text.

## 2. Therapy journey phase

```mermaid
stateDiagram-v2
    [*] --> REGISTERED
    REGISTERED --> ELIGIBILITY_PENDING: PatientEnrolled
    ELIGIBILITY_PENDING --> ELIGIBLE: eligibility evidence accepted
    ELIGIBLE --> PRE_COLLECTION_READY: milestone assessment satisfied
    PRE_COLLECTION_READY --> COLLECTION_IN_PROGRESS: collection authorized/started
    COLLECTION_IN_PROGRESS --> COLLECTED: CollectionCompleted
    COLLECTED --> OUTBOUND_IN_PROGRESS: ShipmentDeparted
    OUTBOUND_IN_PROGRESS --> MATERIAL_AT_MANUFACTURING: receipt and lineage verified
    MATERIAL_AT_MANUFACTURING --> MANUFACTURING: ManufacturingStarted
    MANUFACTURING --> QUALITY_REVIEW: ManufacturingCompleted
    QUALITY_REVIEW --> QUALITY_HOLD: ReleaseHeld
    QUALITY_HOLD --> QUALITY_REVIEW: hold evidence resolved/review resumed
    QUALITY_REVIEW --> PRODUCT_RELEASED: ProductReleased by Quality
    PRODUCT_RELEASED --> RETURN_IN_PROGRESS: return ShipmentDeparted
    RETURN_IN_PROGRESS --> PRODUCT_AT_CENTER: receipt and custody verified
    PRODUCT_AT_CENTER --> INFUSION_READY: all clinical/product prerequisites satisfied
    INFUSION_READY --> INFUSED: authorized infusion evidence
    INFUSED --> CLOSED: journey closure policy satisfied
```

Cancellation/discontinuation is a separate authorized terminal transition applicable only under a controlled reason/policy. The challenge does not supply that policy, so it is not shown as an unguarded “from any state” shortcut.

Canonical phase is accompanied by orthogonal assessments for identity/lineage, consent, authorization, site, Quality, logistics, exception severity and data confidence. One phase string cannot express all readiness.

## 3. Identity-resolution case

```mermaid
stateDiagram-v2
    [*] --> OPEN
    OPEN --> EVIDENCE_GATHERING: case assigned
    EVIDENCE_GATHERING --> PROPOSED: resolution proposed
    PROPOSED --> AWAITING_APPROVAL: evidence packet complete
    AWAITING_APPROVAL --> APPROVED: authorized resolver approves
    AWAITING_APPROVAL --> REJECTED: authorized resolver rejects
    APPROVED --> APPLIED: deterministic application succeeds
    APPLIED --> CLOSED: audit/effect verified
    REJECTED --> CLOSED: rejection/outcome recorded
    CLOSED --> OPEN: new material conflicting evidence
```

An AI match/summary never enters `APPROVED` and cannot emit `IdentityResolutionApplied`.

## 4. Capacity command/saga

```mermaid
stateDiagram-v2
    [*] --> RECEIVED
    RECEIVED --> REJECTED_CONFLICT: same key, different payload
    RECEIVED --> VALIDATED: payload and authority valid
    RECEIVED --> REJECTED_POLICY: validation fails
    VALIDATED --> DISPATCH_PENDING: command persisted
    DISPATCH_PENDING --> DISPATCHED: adapter accepted dispatch
    DISPATCHED --> SUCCEEDED: acknowledged effect verified
    DISPATCHED --> FAILED_RETRYABLE: explicit retryable failure
    DISPATCHED --> FAILED_FINAL: explicit terminal failure
    DISPATCHED --> OUTCOME_UNKNOWN: timeout/ambiguous result
    FAILED_RETRYABLE --> DISPATCH_PENDING: bounded retry
    OUTCOME_UNKNOWN --> RECONCILING: external state query
    RECONCILING --> SUCCEEDED: effect found and payload matches
    RECONCILING --> FAILED_RETRYABLE: no effect and retry safe
    RECONCILING --> COMPENSATION_PENDING: conflicting/partial effect
    COMPENSATION_PENDING --> COMPENSATED: compensation verified
    COMPENSATION_PENDING --> FAILED_FINAL: recovery failed/escalated
```

Terminal replay of the same key/payload returns the stored state/result and emits no duplicate external effect.

## 5. Manufacturing capacity reservation

```mermaid
stateDiagram-v2
    [*] --> PROPOSED
    PROPOSED --> RESERVED: reservation command succeeds
    RESERVED --> CONFIRMED: scheduler/MES acknowledgement consistent
    RESERVED --> HOLD: prerequisite or source conflict
    CONFIRMED --> HOLD: material constraint/change
    CONFIRMED --> EXECUTING: manufacturing start accepted
    EXECUTING --> COMPLETED: manufacturing completion acknowledged
    HOLD --> RESERVED: authorized resolution and revalidation
    RESERVED --> CANCELLED: authorized cancellation verified
    CONFIRMED --> COMPENSATION_PENDING: downstream cancellation/partial state
    COMPENSATION_PENDING --> CANCELLED: compensation verified
    COMPENSATION_PENDING --> FAILED_UNKNOWN: recovery cannot establish state
```

Scheduler and MES values remain separate assertions; a conflict moves the orchestration view to a case/hold or unknown recovery state rather than choosing one silently.

## 6. Quality release assessment/decision

```mermaid
stateDiagram-v2
    [*] --> NOT_ASSESSED
    NOT_ASSESSED --> EVIDENCE_INCOMPLETE: prerequisite check
    NOT_ASSESSED --> UNDER_REVIEW: evidence packet complete
    EVIDENCE_INCOMPLETE --> UNDER_REVIEW: missing evidence supplied
    UNDER_REVIEW --> HOLD: Quality places hold/investigation required
    HOLD --> UNDER_REVIEW: authorized disposition/evidence update
    UNDER_REVIEW --> APPROVED: authorized Quality release decision
    UNDER_REVIEW --> REJECTED: authorized Quality rejection decision
    APPROVED --> SUPERSEDED: material correction/change requires reassessment
    REJECTED --> SUPERSEDED: material correction/change requires reassessment
    SUPERSEDED --> UNDER_REVIEW: new versioned review opened
```

`APPROVED` is established only by a `ProductReleased` event from the Quality context with authenticated authority and evidence binding. MES `RELEASED` and ERP `AVAILABLE` cannot trigger it.

## 7. Shipment physical state

```mermaid
stateDiagram-v2
    [*] --> PLANNED
    PLANNED --> BOOKED: booking acknowledged
    BOOKED --> IN_TRANSIT: departure/custody recorded
    IN_TRANSIT --> ARRIVED_UNVERIFIED: arrival evidence observed
    ARRIVED_UNVERIFIED --> RECEIPT_CONFIRMED: authorized receipt/custody verified
    BOOKED --> EXCEPTION: disruption/contradiction
    IN_TRANSIT --> EXCEPTION: disruption/contradiction
    ARRIVED_UNVERIFIED --> EXCEPTION: receipt/identity/condition conflict
    EXCEPTION --> IN_TRANSIT: resolved and movement resumes
    EXCEPTION --> RECEIPT_CONFIRMED: resolved receipt verified
    EXCEPTION --> CANCELLED: authorized cancellation verified
```

Thermal/product disposition is a separate Quality decision. `RECEIPT_CONFIRMED` means physical/custody receipt, not product acceptance or infusion readiness.

## 8. Operational exception case

```mermaid
stateDiagram-v2
    [*] --> OPEN_UNASSIGNED
    OPEN_UNASSIGNED --> ASSIGNED: owner accepted
    OPEN_UNASSIGNED --> ESCALATED: assignment SLA breached
    ASSIGNED --> INVESTIGATING: work started
    INVESTIGATING --> AWAITING_EXTERNAL: dependency pending
    INVESTIGATING --> AWAITING_APPROVAL: consequential decision required
    AWAITING_EXTERNAL --> INVESTIGATING: evidence/result received
    AWAITING_APPROVAL --> INVESTIGATING: decision requests more work
    AWAITING_APPROVAL --> RESOLVED: authorized outcome recorded
    INVESTIGATING --> RESOLVED: non-consequential deterministic outcome
    RESOLVED --> CLOSED: outcome/effect/audit verified
    CLOSED --> OPEN_UNASSIGNED: new material evidence/reoccurrence
```

Critical cases cannot remain unassigned beyond the approved assignment SLO. Case closure cannot substitute for the domain decision it references.

## 9. Source-to-canonical status policy

There is no direct one-to-one status mapping. Examples:

| Source assertion | Permitted canonical interpretation |
|---|---|
| Patient `IN_MANUFACTURING` | Evidence hint; verify batch, lineage and MES events before projecting `MANUFACTURING` |
| MES `RELEASED` | Manufacturing-system status only; never `Quality release approved` |
| ERP `AVAILABLE` | Inventory assertion only |
| QMS `RELEASED` | Release source assertion; target requires an authorized release decision/evidence record |
| Shipment `DELIVERED` | Logistics assertion; target requires receipt/custody evidence |
| Scheduler `CONFIRMED` + MES `CANCELLED` | Conflict; open capacity case |
| Consent `WITHDRAWN` | Failed/blocked consent prerequisite from its effective time; no autonomous downstream continuation |

## 10. Approval questions

- Confirm canonical phases and whether eligibility/consent ordering differs by product/jurisdiction.
- Provide cancellation/discontinuation and rework/re-manufacture rules.
- Define required evidence for material-at-manufacturing and product-at-center receipt.
- Define Quality reassessment/supersession behavior after release evidence changes.
- Define exception severity/assignment/escalation SLOs.

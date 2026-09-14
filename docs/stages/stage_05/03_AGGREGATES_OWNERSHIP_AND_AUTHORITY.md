# Stage 5 - Aggregates, Ownership and Attribute Authority

**Status:** READY FOR REVIEW; academic G1 approved; domain-owner validation pending  
**Last updated:** 2026-09-14

## 1. Aggregate model

| Aggregate root | Key entities/value objects | Invariants enforced within boundary | External decisions consumed |
|---|---|---|---|
| `TherapyJourney` | Milestone, assessment, blocker, evidence reference | A canonical transition cites evidence/rule; unknown P0 evidence cannot clear a gate | Identity resolution, release decision, clinical authorization |
| `IdentityCase` | Assertion, candidate relation, conflict, resolution proposal | Raw assertions are immutable; no approved relationship is created by score alone | Authorized resolver approval |
| `LineageCase` | Patient/collection/bag/COI/shipment/batch/product relationship assertion | No edge without evidence; conflict opens/retains case; correction preserves prior edge | Authorized COI/COC decision |
| `Collection` | Collection instance, bag, measures, quality flag | Identifiers are typed; measure has value/unit; collection cannot silently move patients | Collection/clinical acknowledgement |
| `Shipment` | Leg, route, custody transfer, physical status | Direction and identifiers consistent; occurrence/recording time preserved; receipt is explicit | Custody acknowledgement; Quality disposition separate |
| `ThermalEvidenceProfile` | Observation, data-quality flag, derived feature, assessment version | Raw observations immutable; units typed; missing/warning remains visible | Quality disposition |
| `CapacityReservation` | Slot, constraints, command, attempt, acknowledgement, compensation | Idempotency key binds payload; legal transition only; partial state remains observable | Human exception approval; MES acknowledgement |
| `ManufacturingBatch` | Batch, input collection/COI, execution events | Patient-specific lineage cannot be fabricated; MES completion cannot set release | Identity/lineage verification; release decision |
| `QCEvidenceSet` | Assay result, method/spec ref, disposition status | Result and disposition are different; value/unit typed; late reports version evidence set | Quality disposition |
| `DeviationCase` | Deviation, evidence link, impact, disposition, closure | Closed requires authorized decision/reason; unresolved link remains explicit | Quality decision/signature |
| `ReleaseDecision` | Product/batch, prerequisites, decision, approver/signature | Only Quality-authorized actor can approve; exact evidence and versions are bound | QC/deviation/thermal/manufacturing evidence |
| `ConsentRecord` | Version, state, signature/effective period | Withdrawal/expiry cannot be overwritten by older evidence | Clinical consent authority |
| `AuthorizationRecord` | Status, validity, source evidence | Commercial state cannot establish clinical or Quality readiness | Payer/commercial decision |
| `SiteQualification` | Training, equipment, agreement, effective period | Unknown/expired required control cannot evaluate as qualified | Quality/site-owner decision |
| `OperationalCase` | Type, severity, owner, SLA, evidence, status, outcome | Critical case must have owner/escalation; closure cites outcome and authority | Source-domain resolution decision |
| `ApprovalRecord` | Principal, authority, action, reason, evidence, signature | Actor authenticated; permission current; separation of duties enforced | Identity-provider and policy facts |

## 2. Identifier model

Identifiers are typed and namespace-qualified:

| Type | Example | Rule |
|---|---|---|
| `JourneyId` | target-generated UUID/ULID | Internal orchestration identity; never presented as patient identity proof |
| `SourceRecordId` | `CRM:CRM100001` | Includes source namespace and immutable source key |
| `PatientKey` | `P-00001` | Synthetic fixture join key only |
| `MRNAssertion` | `CLINICAL:MRN-741568` | Not globally unique; value and assigning domain required |
| `ClinicalSubjectId` | `CLINICAL:SUBJ-CH-0001` | Source assertion, not universal patient key |
| `CollectionId` | `COL-00001` | Typed independently from bag/COI |
| `BagId` | `BAG-00001-A` | Must not be substituted for collection ID |
| `COIId` | `COI-9655125` | Relationship evidence value, not proof by repetition |
| `ShipmentId` | `SHP-O-00001` | Direction is modeled separately, not inferred only from text |
| `SlotId` | `SLOT-00001` | Scheduler planning identity |
| `BatchId` | `BAT-00001` | MES/manufacturing identity |
| `DeviationId` | `DEV-00001` | QMS case identity |
| `EventId` | target-generated globally unique ID | Transport/event uniqueness; semantic dedup also required |
| `CommandId` | target-generated ID | One intent; correlated with idempotency key and payload digest |

## 3. Attribute-level authority matrix

`Authoritative` means authorized to establish that specific fact/decision for the modeled purpose, not that the entire system is globally authoritative.

| Attribute/decision | Primary authority hypothesis | Corroborating evidence | Conflict behavior |
|---|---|---|---|
| CRM relationship/enrollment | CRM/commercial source | Clinical subject assertion | Preserve both; open case if decision-relevant |
| Clinical subject identity and clinical facts | Clinical source and authorized clinical resolver | CRM and local identity evidence | Abstain from merge; human resolution |
| Patient demographic identity | No global authority established | CRM/clinical assertions | Conflict case; do not silently choose |
| Consent state/version | Controlled consent/clinical source | Signed artifact metadata | Latest record alone is insufficient without effective/version rules |
| Financial authorization | Payer/commercial authorization source | Case correspondence | Does not determine clinical/Quality state |
| Treatment-center controls | Site qualification/Quality source | Training, equipment and agreement evidence | Missing/expired required control blocks relevant gate |
| Collection execution/measures | Apheresis/clinical collection source | Bag/COI/custody evidence | Flag type/unit/lineage conflict |
| Scheduler reservation state | Manufacturing scheduler | Command ledger | MES cancellation/acknowledgement creates conflict, not overwrite |
| Manufacturing execution state | MES | Batch events | Never interpreted as Quality release |
| QC assay result | LIMS/laboratory source | Method/specification/disposition evidence | OOS/OOT/PENDING routed for Quality interpretation |
| Deviation lifecycle/disposition | QMS/authorized Quality | Linked evidence and investigation | Missing link/authority prevents closure-derived conclusion |
| Product/batch Quality release | Authorized Quality/QP decision in QMS | Required QC, deviations, manufacturing/thermal evidence | Only explicit authorized release event establishes release |
| Inventory availability | ERP | Batch/product/warehouse evidence | Does not establish Quality release |
| Shipment physical movement | Logistics/courier source | Custody scan and timestamps | Contradictions become case; arrival does not equal accepted receipt |
| Raw temperature | Sensor evidence | Calibration/quality/shipper context | Preserve missing/WARN; no automatic disposition |
| Thermal/product disposition | Authorized Quality | Profile, sensor quality, duration, integrity, SOP | Human-authorized decision only |
| Canonical journey milestone | Journey Coordination projection | All relevant facts/decisions/rule version | Recompute; expose disagreement and recorded-time view |
| Exception ownership/outcome | Exception Operations workflow | Domain decision and audit | Critical unowned case escalates; closure cannot invent domain decision |

## 4. Decision-authority invariants

- A recommendation cannot transition an aggregate.
- An approval cannot be inferred from the actor's job title or request payload.
- Identity resolution, COI/COC correction, deviation closure, thermal/product disposition and Quality release require explicit decision records.
- A Quality decision is not replaced by MES, ERP, AI or Journey Coordination state.
- The same actor cannot bypass required separation of duties through a service identity.
- A historic approval is invalid when policy requires revalidation after relevant evidence changes.
- A corrected fact adds a new assertion/effective interval; it does not erase the prior record.

## 5. Ownership decisions still required

1. Assign actual system/data owners for every authority row.
2. Define assigning authorities and matching policy for MRNs/clinical IDs.
3. Define who can verify and correct each COI/COC relationship.
4. Define milestone-specific consent, authorization and site-control policy.
5. Define Quality blocking/disposition taxonomy and signature rules.
6. Define which compensations are automatic versus human-approved.

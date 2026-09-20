# Stage 9 - Information Architecture

**Status:** APPROVED FOR SYNTHETIC ACADEMIC BUILD

## Core model

The solution preserves source assertions and derives canonical views; it does not overwrite conflicting systems into one “golden patient” row.

```mermaid
flowchart LR
  S[Source fixtures/adapters] --> A[Immutable assertions]
  A --> E[Evidence registry]
  E --> P[Deterministic projections]
  R[Versioned rules/policies] --> P
  P --> C[Cases and recommendations]
  H[Authenticated human decision] --> D[Decision events]
  D --> P
  P --> V[Read-only APIs/UI]
  P --> L[Audit and telemetry]
```

## Information classes

| Class | Meaning | Mutation rule |
|---|---|---|
| Source assertion | What a named source stated at a time | Append or supersede; never silently overwrite |
| Evidence reference | Digest-addressed pointer to supporting record | Immutable |
| Canonical projection | Derived state under named rule versions | Rebuildable |
| Command | Requested external effect with canonical payload digest | Durable state machine |
| Recommendation | Non-binding explanation/options | Never a canonical state transition |
| Approval/decision event | Authenticated human-authority outcome | Append-only; payload-bound |
| Audit record | Actor/action/source/time/correlation/result | Append-only and digest chained |

## Identifier policy

Identifiers are typed and non-interchangeable: JourneyId, PatientKey, namespace-qualified MRNAssertion, CollectionId, BagId, COIId, ShipmentId, SlotId, BatchId, DeviationId, CommandId, EventId and EvidenceId. Display labels never substitute for identifiers.

## Time policy

`occurred_at` represents when the domain event happened; `recorded_at` represents when the platform learned it. Effective periods apply to consent, authorization, site qualification, SOPs and policies. Historical “known-at” views use recorded time and remain stable when late evidence arrives.

## Authority policy

Authority belongs to a decision/attribute, not a whole system. QMS authority for release does not make every QMS field authoritative. MES manufacturing status, ERP inventory, courier telemetry and model output cannot establish Quality release.

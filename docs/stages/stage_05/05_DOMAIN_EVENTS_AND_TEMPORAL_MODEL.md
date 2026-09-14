# Stage 5 - Domain Events and Temporal Model

**Status:** Draft specification; Stage 9 will freeze wire contracts  
**Last updated:** 2026-09-14

## 1. Event principles

- Events are immutable past-tense facts, decisions or action outcomes.
- Commands request effects; events report what occurred.
- A unique `event_id` prevents transport duplication; semantic keys detect duplicate business facts.
- `occurred_at` and `recorded_at` are mandatory and may differ.
- Corrections append a new event that references the corrected event; they never overwrite history.
- Source payloads are retained by protected evidence reference, not copied indiscriminately into every event.
- Unknown source outcome is explicitly represented.

## 2. Canonical event envelope

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `event_id` | `EventId` | Yes | Globally unique event identity |
| `event_type` | controlled string | Yes | Versioned past-tense domain-event name |
| `schema_version` | semantic version | Yes | Payload schema version |
| `aggregate_type` | controlled string | Yes | Aggregate boundary |
| `aggregate_id` | typed identifier | Yes | Aggregate instance |
| `sequence` | positive integer | Yes for canonical aggregate event | Optimistic concurrency/order within aggregate |
| `occurred_at` | RFC 3339 UTC timestamp | Yes | Business occurrence time |
| `recorded_at` | RFC 3339 UTC timestamp | Yes | Platform persistence/observation time |
| `effective_from` | RFC 3339/date | Conditional | Start of assertion/decision/policy effect |
| `effective_to` | RFC 3339/date/null | Conditional | End of effect |
| `source_system` | controlled identifier | Yes | Originating system/context |
| `source_record_id` | namespace-qualified string | Yes for imported assertion | Immutable record/message reference |
| `evidence_refs` | non-empty typed array | Yes for decisions/transitions | Protected evidence references and digests |
| `correlation_id` | identifier | Yes | End-to-end journey/transaction correlation |
| `causation_id` | event/command ID | Conditional | Immediate cause |
| `actor` | authenticated principal/service | Yes | Originating principal and authentication context |
| `authority` | policy decision reference | Conditional | Required for consequential decision/action |
| `policy_versions` | map of policy/rule IDs | Conditional | Exact policies used |
| `data_quality` | status plus issues | Yes for imported/derived data | `ACCEPTABLE`, `WARNING`, `INVALID`, `UNKNOWN` |
| `confidence` | bounded value plus method | AI/probabilistic only | Never substitutes for authority |
| `payload` | schema-specific object | Yes | Minimum necessary event facts |
| `payload_digest` | SHA-256 | Yes | Integrity and semantic dedup support |
| `supersedes_event_id` | EventId/null | For correction | Prior event corrected/superseded |
| `classification` | controlled label | Yes | Synthetic/PHI/sensitive handling policy |
| `trace_id` | trace identifier | Yes | Observability linkage |

## 3. Event catalogue

### Identity and lineage

`IdentityAssertionObserved`, `IdentityConflictDetected`, `IdentityResolutionProposed`, `IdentityResolutionApproved`, `IdentityResolutionRejected`, `IdentityResolutionApplied`, `LineageAssertionObserved`, `COIEvidenceVerified`, `COCTransferRecorded`, `LineageConflictDetected`.

### Clinical, consent and site

`PatientEnrolled`, `EligibilityAssertionObserved`, `ConsentStateObserved`, `ConsentWithdrawn`, `AuthorizationStateObserved`, `SiteQualificationObserved`, `ClinicalMilestoneAuthorized`.

### Collection and logistics

`CollectionScheduled`, `CollectionCompleted`, `CollectionMeasureObserved`, `ShipmentBooked`, `ShipmentDeparted`, `ShipmentArrived`, `ShipmentReceiptConfirmed`, `CustodyTransferred`, `ShipmentExceptionDetected`, `TelemetryObserved`, `ThermalProfileCalculated`, `ThermalDispositionRecorded`.

### Capacity and manufacturing

`ReservationRequested`, `ReservationValidated`, `SlotReserved`, `SlotConfirmed`, `ReservationConflictDetected`, `ReservationOutcomeUnknown`, `ReservationCancelled`, `ReservationCompensated`, `ManufacturingStarted`, `ManufacturingCompleted`, `ManufacturingStatusObserved`.

### QC and Quality

`QCResultReported`, `QCEvidenceSetCompleted`, `DeviationOpened`, `DeviationEvidenceLinked`, `DeviationDispositioned`, `DeviationClosed`, `ReleaseReviewStarted`, `ReleaseHeld`, `ProductReleased`, `ProductReleaseRejected`, `ReleaseDecisionSuperseded`.

### Journey, cases and authority

`MilestoneAssessmentRecorded`, `JourneyProjectionUpdated`, `ExceptionOpened`, `ExceptionAssigned`, `ExceptionEscalated`, `ExceptionResolutionProposed`, `ExceptionResolved`, `ExceptionClosed`, `RecommendationGenerated`, `RecommendationReviewed`, `ApprovalRecorded`, `AuthorizationDenied`, `PolicyPublished`, `PolicySuperseded`.

### Command/audit outcomes

`CommandAccepted`, `CommandDispatched`, `CommandSucceeded`, `CommandFailed`, `CommandOutcomeUnknown`, `CommandReconciled`, `IdempotencyConflictDetected`, `ProhibitedActionAttempted`, `AuditEntryAppended`.

## 4. Semantic deduplication

`event_id` alone is insufficient: the supplied data contains retry duplicates with different event IDs. Each event type therefore defines a semantic fingerprint using stable business attributes. Examples:

| Event type | Candidate semantic fingerprint |
|---|---|
| `ManufacturingStarted` | batch + execution/run identity + operation + occurred-time tolerance + source |
| `SlotReserved` | site + slot window + journey + reservation intent/command |
| `QCResultReported` | batch + sample + assay + method + report/version identity |
| `ShipmentDeparted` | shipment leg + custody event/source sequence |
| `ConsentStateObserved` | consent record + version + effective state/change identity |

Fingerprints must be approved per source; fuzzy deduplication may only flag a case and cannot discard evidence autonomously.

## 5. Bitemporal projection behavior

The platform supports two questions:

1. **Valid-time view:** What does the evidence say happened/effectively applied at business time T?
2. **Recorded-time view:** What could the platform reasonably have known at time K?

Projection keys include both cutoffs. A late event may change the current reconstructed valid-time history but must not rewrite what was known earlier. Decisions retain the evidence set available when made; later corrections may trigger reassessment rather than retroactively making the original audit disappear.

## 6. Correction and retraction

- A correction event references `supersedes_event_id`, states the reason and carries new evidence.
- The old event remains queryable and is excluded/included according to the selected recorded-time cutoff.
- Consequential decisions affected by corrected evidence produce a case and, where policy requires, a `ReleaseDecisionSuperseded` or new milestone assessment.
- Deletion is governed disposition of stored data, not alteration of the logical audit history; privacy/retention design is finalized later.

## 7. Event quality outcomes

| Condition | Handling |
|---|---|
| Missing mandatory identifier/time/source | Quarantine; do not update canonical projection |
| `occurred_at` later than physically dependent event | Preserve, mark temporal conflict, open case |
| Excessive recording lag | Preserve, flag according to observable policy; no invented correction |
| Unknown schema version | Quarantine/route to compatibility handler |
| Same event ID and digest | Acknowledge duplicate, no new effect |
| Same event ID, different digest | Integrity conflict and security/operations case |
| Different event IDs, same semantic fingerprint | Preserve evidence; flag potential retry duplicate |
| Missing/warning telemetry value | Preserve quality state; exclude/include only under controlled feature rule |

## 8. Required Stage 9 follow-up

Freeze JSON schemas, privacy classifications, evidence-reference format, source-specific fingerprints, event partition/order guarantees, timestamp precision/time-zone rules, compatibility policy and retention/disposition behavior.

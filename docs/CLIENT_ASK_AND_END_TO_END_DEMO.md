# Client Ask and End-to-End Demo

## Purpose

This document explains, in simple language, what the client needs, what the capstone delivers and what the working demonstration proves. It can be used by executives, trainers, reviewers and demo presenters.

## 1. What is Cell and Gene Therapy?

Cell and Gene Therapy (CGT) uses cells or genetic material to treat serious diseases. In the patient-specific journey covered by this capstone, cells are collected for a particular patient, transported to a manufacturing facility, processed into a treatment, tested by Quality teams and returned for treatment.

The correct patient must remain connected to the correct manufacturing batch throughout the journey. This is why chain of identity, chain of custody, evidence and human authorization are critical.

## 2. Business context

The patient-to-batch journey involves several participants:

- clinical sites and treatment centres;
- patient operations;
- logistics and supply chain;
- manufacturing;
- laboratories and Quality Control; and
- Quality Assurance.

These participants often use different systems. Information can be delayed, missing or contradictory, leaving teams to investigate the current state manually.

## 3. What is the client asking for?

The client needs a reliable way to answer five questions:

1. Is this the correct patient?
2. Is the patient ready for manufacturing?
3. Was the manufacturing slot successfully reserved?
4. Is the batch ready for release?
5. What evidence supports every status and decision?

The solution must also:

- combine evidence from different systems without hiding contradictions;
- represent satisfied, not-satisfied and unknown outcomes explicitly;
- assign exceptions to accountable people;
- prevent duplicate external actions;
- preserve human authority for identity and Quality decisions;
- maintain a traceable, tamper-evident audit history; and
- continue operating safely when AI is unavailable.

## 4. Problem statement

The fragmented environment cannot always determine the current patient-to-batch state, why it is true, who is authorized to decide and what must happen next.

This can create:

- patient-identity and chain-of-custody risk;
- operational delays and manual investigation;
- duplicate reservations after uncertain external-system responses;
- incorrect readiness assumptions when evidence is missing; and
- weak accountability and auditability.

## 5. What the capstone delivers

The capstone delivers a synthetic Patient-to-Batch Control Tower. It creates one controlled view of the journey while keeping source evidence, exceptions and decision authority visible.

The central design principle is:

> **Evidence before status. Human authority before automation.**

The solution includes:

- evidence-backed state and readiness evaluation;
- conflict detection and owned exception cases;
- human-authorized identity resolution;
- idempotent commands and unknown-outcome reconciliation;
- Quality-controlled product release;
- evidence citations and tamper-evident audit history;
- three integrated proofs of concept; and
- an optional recommendation-only assistant that is off by default.

The current academic increment also provides a read-only explorer for the original v2 `EVAL-001..006` synthetic source patients, a source-timestamp journey sequence for each, a non-authoritative preview of `INJ-001..010` disruption scenarios, a standalone PRD, a source-by-source brownfield migration plan, a one-to-one 21-stage artifact register and a 90-day production-gap roadmap. The six timestamp sequences are not governed current state or known-at replay; the explorer and preview are **not** a migrated enterprise platform or an autonomous re-planner. The three runnable POCs use a separate scripted fixture.

## 6. End-to-end flow

```text
Patient evidence received
        ↓
Identity conflict detected
        ↓
Authorized human resolves identity
        ↓
Patient readiness evaluated
        ↓
Manufacturing slot requested
        ↓
Timeout recorded as an unknown outcome
        ↓
System reconciles instead of repeating the request
        ↓
Manufacturing, QC, deviation and thermal evidence collected
        ↓
Release remains unknown until Quality decides
        ↓
Authorized Quality decision recorded
        ↓
Journey becomes ready with evidence and audit history
```

## 7. How to start the demonstration

On macOS, double-click `START_DEMO.command` in the repository root and keep the Terminal window open. The application opens at <http://127.0.0.1:8000>.

Alternatively, start it from a terminal:

```bash
cd /Users/suryap/Documents/Codex/2026-09-11/i/FDE-Final-Capstone
FDE_DB=runtime/control-tower.db AI_MODE=off PYTHONPATH=src \
  .venv/bin/python -m uvicorn fde_capstone.api:app \
  --host 127.0.0.1 --port 8000
```

The application uses disposable synthetic data only.

## 8. What is demonstrated

### POC 1 — Identity and readiness

Two sources provide conflicting patient-identity information. The system does not guess which value is correct. It creates an owned case, requires an authorized human decision and then recalculates readiness using cited evidence.

Expected result:

- identity decision: `APPLIED`;
- collection readiness: `SATISFIED`; and
- evidence: five references cited.

This proves that conflicts are visible and patient identity remains under human authority.

### POC 2 — Safe manufacturing-slot orchestration

The simulated external reservation succeeds, but its response times out. The system records `OUTCOME_UNKNOWN` instead of assuming success or failure. It reconciles with the external system, confirms `SUCCEEDED` and prevents a duplicate dispatch.

Expected result:

- initial state: `OUTCOME_UNKNOWN`;
- reconciled state: `SUCCEEDED`; and
- duplicate dispatch: `NO — prevented`.

This proves safe retries, reconciliation and idempotent external actions.

### POC 3 — Quality release

Manufacturing, Quality Control, deviation and thermal evidence are assembled. Release still remains `UNKNOWN` until the simulated authorized Quality role makes the final decision.

Expected result:

- before authority: `UNKNOWN`;
- Quality decision: `HUMAN AUTHORIZED`; and
- final outcome: `SATISFIED`.

This proves that automation supports Quality but cannot replace Quality authority.

## 9. Evidence shown after the run

The evidence console shows:

- ten evidence references;
- a valid audit chain;
- deterministic AI-off operation;
- control metrics; and
- a final state digest.

Together, these records explain what happened, why it happened, which evidence was used and which authority made the decision.

## 10. What does AI do?

The main application does not require AI.

| Mode | Meaning |
|---|---|
| `off` | Recommended. No AI model is called, and all core controls continue to work. |
| `fake` | A local deterministic adapter demonstrates a bounded, non-binding recommendation contract. |

There is no live-model mode in this capstone. AI cannot establish patient identity, make a clinical decision, reserve an external slot independently or release the product.

## Role-based demonstration and automation

The final browser demo includes seven presentation lenses: Patient Operations, Identity Authority, Logistics/Planning, Manufacturing, Lab/QC, Quality Authority and Executive/Operations. These are persona views over one governed journey; backend permissions remain the explicit `COORDINATOR`, `IDENTITY_AUTHORITY`, `PLANNER`, `QUALITY_AUTHORITY` and `VIEWER` roles.

Automation operates with AI off:

| Automated capability | Automated behavior | Human boundary |
|---|---|---|
| Identity exception detection | Detect conflict and create an owned case | Identity Authority decides identity outcome |
| Readiness | Evaluate identity/consent/authorization/site gates | No clinical decision is automated |
| Slot orchestration | Reconcile unknown outcome and prevent duplicate dispatch | Planner remains command actor |
| Quality packet | Assemble MES/QC/deviation/thermal evidence | Quality Authority releases product |
| Journey summary | Produce cross-domain status, blocker, next owner and evidence count | Summary cannot execute or create authority |

The design deliberately separates **automation** from **AI**: deterministic automation reconstructs and coordinates governed state; the assistant only explains or summarizes it.

## Information retrieval position

Authoritative operational facts do not use RAG. They use typed adapters, evidence records and deterministic projections. Optional future RAG is limited to supporting unstructured material such as SOPs, emails and deviation narratives, with provenance/version/freshness and citations. MCP is not implemented in the current POC; it is a future enterprise integration option for approved read/tool adapters after identity, authorization, supplier and audit controls are satisfied.

## 11. Demonstrated assurance

- 21 of 21 FDE operating-model stages contain documented artifacts; this does not mean external stage approval.
- 106 of 106 local automated tests pass.
- 57 evaluation cases were executed.
- 55 evaluation cases passed **structural probes** and none failed. Only 7 original cases have full scoped property assertions, 9 are partial, and 39 extension cases have ungraded expected properties.
- Two controlled human-study cases remain inconclusive.
- 29 of 31 requirements are internally verified; zero are production verified.
- The registered 20-client/27,507-row journey-projection NFR remains unverified despite a passing in-process micro-benchmark.
- The original ZIP and all 132 frozen extracted evidence files remain unchanged.

## 12. Business value demonstrated

The capstone demonstrates the technical ability to:

- identify exceptions earlier;
- prevent duplicate external actions;
- make decision ownership clear;
- improve evidence traceability;
- operate safely without AI; and
- provide a controlled foundation for future integration.

These are demonstrated POC capabilities, not measured production benefits or ROI.

## 13. What the demo does not claim

The demonstration does not establish:

- clinical safety or clinical benefit;
- regulatory approval or compliance certification;
- production readiness;
- enterprise identity management or electronic signatures;
- integration with live clinical, logistics, manufacturing or Quality systems;
- real-world savings or patient outcomes;
- human-factor performance; or
- live-model AI quality, safety, latency or cost.

## 14. Final lifecycle decision

The final decision is **RESTRICT AND CHANGE**.

The synthetic academic POC and its engineering approach are accepted. Real-data and production use remain prohibited until the seven corrective actions, controlled human studies, live integrations and independent assurance are completed.

## 15. Executive closing statement

> This capstone demonstrates a controlled patient-to-batch orchestration approach for Cell and Gene Therapy. It resolves identity conflicts with human authority, handles uncertain external outcomes without duplication and preserves Quality authority for product release. Every outcome is supported by evidence and audit history. The POC is technically successful, but production use remains restricted until external validation and corrective actions are completed.

For the timed presenter sequence, see the [Demo Guide](DEMO_GUIDE.md). For scope, results and final conclusions, see the [Final Capstone Report](FINAL_CAPSTONE_REPORT.md).

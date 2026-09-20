# Stage 12/16 — Academic AI-System Card and Record

**Record ID:** CGT-FDE-ACADEMIC-001. **Version:** 2026-09-15. **Status:** academic design record only; AI Governance Owner approval pending. This is not a provider model card, regulatory filing, or production AI-system registration.

## Purpose and boundary

The application demonstrates patient-to-batch workflow decisions using deterministic domain logic and synthetic local fixtures. An optional assistant produces a *non-binding* explanation from allowlisted evidence. It cannot approve identity, manufacturing, shipment, quality disposition, release or any external command. A human with the relevant role owns consequential decisions.

| Field | Recorded position |
|---|---|
| Modes | `off` is default and recommended; `fake` is a deterministic test adapter. No live provider is wired. |
| Inputs | Synthetic patient, slot, chain-of-identity, logistics, thermal and quality evidence. Original v2 source cases and injects are read-only previews. |
| Outputs | Deterministic workflow result plus optional schema-constrained, non-authoritative recommendation. |
| Model identity | No trained model is deployed. `deterministic-fake-v1` is a fixture adapter, not a model card substitute. |
| Data governance | Synthetic local dataset only; no real patient information is authorized for this build. |
| Human oversight | Roles, approval binding, audit records, exception handling and fallback are specified/tested internally; real training and operational sign-off remain open. |
| Known limitations | No live-model reliability, bias, privacy, supplier, drift, explainability, clinical efficacy or real-world performance claim. |
| Fail-safe | AI off/unavailable leaves deterministic workflow in control; unknown external outcome requires reconciliation rather than blind retry. |
| Change trigger | Selecting a provider, adding RAG/memory/tools/agent autonomy, or using real data reopens Stages 4, 7, 10, 12, 13 and 15. |

## Evidence and accountability

The [Stage 12 threat model](01_THREAT_MODEL.md), [OWASP mapping](05_OWASP_2026_RISK_MAPPING.md), [Stage 14 AIBOM](../stage_14/AIBOM.json), [Stage 15 TEVV report](../stage_15/01_TEVV_REPORT.md) and [Stage 20 roadmap](../stage_20/06_PRODUCTION_GAP_AND_90_DAY_ROADMAP.md) form this academic record. The Capstone Owner and AI Governance Owner must review it; independent assurance and live deployment are expressly absent. If a provider is selected, attach that supplier's actual model card and completed qualification rather than renaming this page as one.

# Stage 12 — OWASP GenAI Risk Mapping (Academic Scope)

**Assessment date:** 2026-09-15. **System:** local synthetic CGT patient-to-batch orchestration demonstrator. **Status:** internal design mapping, not an OWASP certification, independent security review, or penetration test.

Reference baselines are the [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) and [OWASP Agentic Applications Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/). We use the published categories as threat prompts; an independent owner must confirm exact edition and applicability before production.

| Relevant risk family | How it could harm this workflow | Current academic control/evidence | Remaining production gate |
|---|---|---|---|
| Prompt or agent-goal injection (ASI01) | A source note, SOP, or courier message tries to override release rules | Assistant has no release/write tools; untrusted text is not authority; T05, EVAL-006 and EXT-AI-001 probes | Live-model red team with actual retrieved content and selected provider |
| Tool misuse and excessive agency (ASI02) | AI sends a shipment, batch or quality command without owner approval | `off` default; `fake` is non-binding; domain service enforces role, state, evidence and idempotency; T01/T02/T09 | Production least-privilege tools and IAM test |
| Sensitive-information disclosure and identity abuse (ASI03) | A patient context crosses scope or is copied to a model/log | Synthetic data only, scope checks and no external AI provider; T04/T07 | Real data minimization, DPIA, retention, residency, IAM and logging review |
| Unsafe output or hallucinated evidence | A persuasive summary is mistaken for a quality decision | Allowlisted evidence/schema, deterministic fallback, human quality authority; T06 | Model-specific quality/evidence eval and human-factors assessment |
| Supply-chain and component compromise (ASI04) | Provider, package or dynamic tool changes alter behavior | No dynamic MCP/tool registry; SBOM/AIBOM and release hash checks; T11 | Supplier qualification, scans, provenance and change controls |
| Unexpected execution (ASI05) | Retrieved instructions cause shell/code execution | Assistant port cannot execute arbitrary code; fixed application API; T05/T11 | Adversarial integration and penetration testing |
| Memory/context poisoning (ASI06) | Old or malicious context contaminates later patient decisions | No persistent agent memory; fresh deterministic case context | Retest if memory or retrieval is added |
| Insecure inter-agent communication (ASI07), cascading failure (ASI08), rogue agents (ASI10) | An autonomous chain propagates a wrong command or loops | No multi-agent/autonomous chain; one bounded assistant call; AI-off fallback, T08 | Re-open threat model if agentic architecture is introduced |
| Human-agent trust exploitation (ASI09) | Operator accepts the AI suggestion as an approval | UI and PRD label AI as non-authoritative; consequential actions require named human roles | Usability test, training and live oversight evidence |

**Conclusion:** These are mapped design risks, not a claim that every OWASP category has been tested. The off/fake modes substantially limit current exposure, but also mean that live LLM and agentic security cannot be declared passed. Stage 15 records the precise internal TEVV coverage; Stage 20 keeps external security and supplier CAPAs open.

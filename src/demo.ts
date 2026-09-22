export const ROLE_VIEWS = [
  {
    id: "patient_operations",
    name: "Patient Operations Coordinator",
    backend_role: "COORDINATOR",
    focus: "End-to-end journey, blockers, evidence and accountable next owner.",
    can_do: ["Read the journey", "Create owned exception cases", "Coordinate the next authorized action"],
    cannot_do: ["Resolve patient identity", "Release product", "Make clinical decisions"],
  },
  {
    id: "identity_authority",
    name: "Identity Authority",
    backend_role: "IDENTITY_AUTHORITY",
    focus: "Conflicting patient identity and chain-of-identity evidence.",
    can_do: ["Review cited identity evidence", "Apply the reviewed identity decision"],
    cannot_do: ["Reserve manufacturing capacity", "Release product", "Make clinical decisions"],
  },
  {
    id: "logistics_planner",
    name: "Logistics / Manufacturing Planner",
    backend_role: "PLANNER",
    focus: "Slot reservation, unknown outcomes, reconciliation and logistics evidence.",
    can_do: ["Reserve a slot", "Reconcile an unknown command outcome", "Review logistics/thermal evidence"],
    cannot_do: ["Resolve identity", "Release product", "Override Quality"],
  },
  {
    id: "manufacturing",
    name: "Manufacturing Operations",
    backend_role: "VIEWER",
    focus: "Batch execution state and upstream/downstream dependencies.",
    can_do: ["Read manufacturing and journey evidence", "See blockers and handoffs"],
    cannot_do: ["Treat MES completion as Quality release", "Change identity", "Approve clinical actions"],
  },
  {
    id: "lab_qc",
    name: "Lab / Quality Control",
    backend_role: "VIEWER",
    focus: "QC result, deviation and thermal evidence contributing to the Quality packet.",
    can_do: ["Review QC/deviation/thermal evidence", "See unresolved Quality prerequisites"],
    cannot_do: ["Issue the final Quality release in this POC", "Change patient identity"],
  },
  {
    id: "quality_authority",
    name: "Quality Authority",
    backend_role: "QUALITY_AUTHORITY",
    focus: "Evidence-backed product disposition and release authority.",
    can_do: ["Review the release evidence packet", "Record the authorized release decision"],
    cannot_do: ["Delegate release authority to AI", "Use MES or ERP status as release authority"],
  },
  {
    id: "executive",
    name: "Executive / Operations Viewer",
    backend_role: "VIEWER",
    focus: "Cross-domain status, exceptions, automation controls and evidence traceability.",
    can_do: ["Read the automated cross-domain summary", "Inspect control and assurance evidence"],
    cannot_do: ["Execute operational or consequential decisions"],
  },
];

export function runDemo(aiMode: string = "off") {
  const isAiFake = aiMode === "fake" || aiMode === "bounded_fake";
  const allEvidence = [
    "EV-AUTH",
    "EV-CONSENT",
    "EV-DEV",
    "EV-ID-DOB",
    "EV-ID-MRN",
    "EV-MES",
    "EV-QC",
    "EV-QMS-DECISION",
    "EV-SITE",
    "EV-THERMAL",
  ];

  const poc1Evidence = ["EV-AUTH", "EV-CONSENT", "EV-ID-DOB", "EV-ID-MRN", "EV-SITE"];
  const poc3Evidence = ["EV-DEV", "EV-MES", "EV-QC", "EV-QMS-DECISION", "EV-THERMAL"];

  const domains = [
    {
      domain: "Patient & Clinical",
      status: "SATISFIED",
      detail:
        "Identity was resolved by the authorized role; consent, payer authorization and site readiness are satisfied.",
      evidence_refs: poc1Evidence,
    },
    {
      domain: "Logistics & Planning",
      status: "SATISFIED",
      detail:
        "The slot timeout was reconciled to the existing reservation and duplicate dispatch was prevented.",
      evidence_refs: [],
    },
    {
      domain: "Manufacturing",
      status: "SATISFIED",
      detail: "MES reports manufacturing complete; this is evidence, not Quality release authority.",
      evidence_refs: ["EV-MES"],
    },
    {
      domain: "Lab / QC",
      status: "SATISFIED",
      detail: "QC passed, the deviation is closed/non-blocking, and the thermal profile is acceptable.",
      evidence_refs: ["EV-QC", "EV-DEV", "EV-THERMAL"],
    },
    {
      domain: "Quality",
      status: "SATISFIED",
      detail: "The authorized Quality decision established release after the evidence packet was assembled.",
      evidence_refs: ["EV-QMS-DECISION"],
    },
  ];

  const journeySummary = {
    patient_key: "P-A",
    batch_id: "BATCH-100",
    overall_status: "READY_FOR_NEXT_AUTHORIZED_STEP",
    current_blocker: "NONE",
    next_owner: "Patient Operations Coordinator",
    risk: "LOW_IN_SYNTHETIC_DEMO_ONLY",
    evidence_count: allEvidence.length,
    open_exceptions: 0,
    critical_checkpoint: {
      before: "BLOCKED",
      blocker: "Authorized Quality release was required",
      owner: "Quality Authority",
      after: "SATISFIED",
    },
    summary:
      "Identity, consent, authorization and site readiness are satisfied; the manufacturing-slot timeout was reconciled without duplicate dispatch; manufacturing, QC, deviation and thermal evidence are acceptable; authorized Quality release is recorded. The synthetic journey is ready for the next authorized clinical/operations step.",
    domains,
    evidence_refs: allEvidence,
  };

  const automationTrace = [
    {
      step: "Identity exception detection",
      automation: "Automatic conflict detection and owned-case creation",
      human_boundary: "Identity Authority applies the final identity decision",
    },
    {
      step: "Readiness evaluation",
      automation: "Deterministic gate evaluation across identity, consent, authorization and site readiness",
      human_boundary: "No clinical decision is automated",
    },
    {
      step: "Slot orchestration",
      automation: "Unknown outcome reconciliation and duplicate-dispatch prevention",
      human_boundary: "Planner remains the authorized command actor",
    },
    {
      step: "Quality evidence assembly",
      automation: "MES, QC, deviation and thermal evidence are assembled into the release packet",
      human_boundary: "Quality Authority makes the release decision",
    },
    {
      step: "Cross-domain summary",
      automation: "The deterministic journey summary is generated from governed state and evidence",
      human_boundary: "The summary does not create authority or execute a consequential action",
    },
  ];

  const assistant = {
    mode: isAiFake ? "BOUNDED_FAKE" : "DISABLED",
    advisory_note: isAiFake
      ? "Bounded fake adapter active · Narrative explanation only (zero authority over decisions or release)"
      : "AI disabled · All evaluations and summaries are 100% deterministic",
    authority_warning:
      "AI output is advisory-only. Only designated human roles (Identity Authority, Planner, Quality Authority) exercise operational decision authority.",
    rejection_reason: null,
  };

  const assistantOutput = isAiFake
    ? {
        summary:
          "[BOUNDED ASSISTANT ADVISORY] Synthetic patient-to-batch journey verified across all deterministic gates. Recommendation provided for human review; no authority exercised.",
        evidence_refs: allEvidence,
      }
    : null;

  return {
    scope: "SYNTHETIC_LOCAL_ACADEMIC_POC",
    ai_mode: aiMode,
    poc1: {
      case: "CASE-100",
      decision: "APPROVED",
      readiness: "SATISFIED",
      evidence_refs: poc1Evidence,
    },
    poc2: {
      initial_state: "OUTCOME_UNKNOWN",
      reconciled_state: "SUCCEEDED",
      replay_dispatch: false,
    },
    poc3: {
      before: "BLOCKED",
      released: true,
      after: "SATISFIED",
      evidence_refs: poc3Evidence,
    },
    journey_summary: journeySummary,
    automation_trace: automationTrace,
    role_views: ROLE_VIEWS,
    information_architecture: {
      structured_retrieval:
        "Typed source adapters, evidence registry and deterministic projections for authoritative operational facts.",
      rag: "Not required for canonical state. Optional future RAG is limited to unstructured supporting evidence such as SOPs, emails and deviation narratives, with citations and version/freshness controls.",
      mcp: "Not implemented in the current POC. MCP is a future enterprise integration option for approved read/tool adapters after identity, authorization and supplier controls are satisfied.",
    },
    assistant,
    assistant_output: assistantOutput,
    audit_chain_valid: true,
    state_digest: "3e9b1042fd87",
    metrics: {
      events_recorded: 12,
      audit_verifications: 1,
      readiness_checks: 1,
      idempotent_replays: 1,
      quality_packets_assembled: 1,
    },
  };
}

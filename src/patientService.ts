import path from "path";
import { BASELINE, loadRows, SourceRowItem } from "./sourceCases";

export interface PatientSummary {
  patient_key: string;
  crm_patient_id: string;
  clinical_subject_id: string;
  mrn: string;
  synthetic_name: string;
  dob: string;
  center_id: string;
  country: string;
  product_code: string;
  journey_status: string;
  enrolled_at: string;
  phase_step: number;
  phase_display: string;
  phase_badge_class: string;
  
  // Two distinct status dimensions
  journey_position_code: string;
  journey_position_display: string;
  governing_readiness_code: string;
  governing_readiness_display: string;
  readiness_badge_class: string;
  infusion_authorization: "AUTHORIZED" | "NOT_READY" | "PROHIBITED" | "ADMINISTERED" | "ADMINISTERED_UNDER_EXCEPTION";

  // Quality hold lifecycle & governance details
  has_hold: boolean;
  hold_detail: {
    status: "OPEN" | "CLOSED" | "NONE";
    opened_at: string | null;
    closed_at: string | null;
    blocks_release: boolean;
    blocks_infusion: boolean;
    category: "ACTIVE_MANUFACTURING_HOLD" | "RETROSPECTIVE_INVESTIGATION_POST_INFUSION" | "CLOSED_HISTORICAL" | "NONE";
    quality_disposition_ref: string;
    clinical_risk_note: string;
  };

  batch_id: string | null;
  mes_status: string | null;
  qms_release_status: string | null;
  collection_id: string | null;
  collection_time: string | null;
  coi_id: string | null;
  viability_pct: number | null;
  deviations_count: number;
  open_deviations_count: number;
  is_active: boolean;
}

const PHASE_CONFIG: Record<
  string,
  { step: number; display: string; badgeClass: string; isActive: boolean }
> = {
  ELIGIBLE: { step: 1, display: "Eligible for Enrollment", badgeClass: "phase-enrolled", isActive: true },
  ENROLLED: { step: 1, display: "Enrollment & Eligibility", badgeClass: "phase-enrolled", isActive: true },
  APHERESIS_PENDING: { step: 2, display: "Apheresis Scheduled", badgeClass: "phase-apheresis", isActive: true },
  COLLECTED: { step: 3, display: "Collected & Outbound", badgeClass: "phase-collected", isActive: true },
  IN_MANUFACTURING: { step: 4, display: "Cell Manufacturing", badgeClass: "phase-mfg", isActive: true },
  QC_PENDING: { step: 5, display: "QC & Sterility Testing", badgeClass: "phase-qc", isActive: true },
  QA_HOLD: { step: 5, display: "QA Exception Hold", badgeClass: "phase-hold", isActive: true },
  RETURN_TRANSIT: { step: 6, display: "Cryo Return Transit", badgeClass: "phase-transit", isActive: true },
  INFUSION_READY: { step: 7, display: "Ready for Infusion", badgeClass: "phase-ready", isActive: true },
  INFUSED: { step: 8, display: "Infusion Administered", badgeClass: "phase-infused", isActive: false },
};

let cachedPatients: PatientSummary[] | null = null;
let lastCacheTime = 0;

export function getPatientsList(
  query: {
    search?: string;
    phase?: string;
    product?: string;
    center?: string;
    statusFilter?: string; // 'active', 'all', 'completed'
    page?: number;
    pageSize?: number;
    sortBy?: string;
    sortDir?: "asc" | "desc";
  } = {},
  baselineDir: string = BASELINE
) {
  const now = Date.now();
  if (!cachedPatients || now - lastCacheTime > 60000) {
    const rawDir = path.join(baselineDir, "data", "raw");
    const rawPatients = loadRows(path.join(rawDir, "patients.csv"), baselineDir);
    const rawBatches = loadRows(path.join(rawDir, "batches.csv"), baselineDir);
    const rawCollections = loadRows(path.join(rawDir, "collections.csv"), baselineDir);
    const rawDeviations = loadRows(path.join(rawDir, "deviations.csv"), baselineDir);

    const batchesByPatient = new Map<string, SourceRowItem>();
    for (const b of rawBatches) {
      batchesByPatient.set(b.row.patient_key, b);
    }

    const collectionsByPatient = new Map<string, SourceRowItem>();
    for (const c of rawCollections) {
      collectionsByPatient.set(c.row.patient_key, c);
    }

    const deviationsByPatient = new Map<string, SourceRowItem[]>();
    for (const d of rawDeviations) {
      const pKey = d.row.patient_key;
      if (!deviationsByPatient.has(pKey)) {
        deviationsByPatient.set(pKey, []);
      }
      deviationsByPatient.get(pKey)!.push(d);
    }

    cachedPatients = rawPatients.map((p) => {
      const pKey = p.row.patient_key;
      const status = p.row.journey_status || "ENROLLED";
      const config = PHASE_CONFIG[status] || {
        step: 0,
        display: status,
        badgeClass: "phase-default",
        isActive: status !== "INFUSED",
      };

      const b = batchesByPatient.get(pKey);
      const c = collectionsByPatient.get(pKey);
      const devs = deviationsByPatient.get(pKey) || [];
      const openDevs = devs.filter((d) => d.row.status !== "CLOSED");

      // Strict detection of Quality Hold conditions across domains
      const hasQmsOrMesHold = Boolean(
        status === "QA_HOLD" ||
        (b && (b.row.mes_status === "QA_HOLD" || b.row.qms_release_status === "HOLD")) ||
        openDevs.some((d) => d.row.severity === "CRITICAL")
      );

      // Derive physical journey position (logistics location)
      let journeyPosCode = status;
      let journeyPosDisplay = config.display;

      if (status === "INFUSED") {
        journeyPosCode = "SITE_POST_INFUSION";
        journeyPosDisplay = "Clinical Site · Infused";
      } else if (status === "INFUSION_READY") {
        journeyPosCode = "SITE_RETURNED";
        journeyPosDisplay = "Clinical Site · Cryo Storage";
      } else if (status === "RETURN_TRANSIT") {
        journeyPosCode = "RETURN_TRANSIT";
        journeyPosDisplay = "Cryo Transit to Hospital";
      } else if (status === "QA_HOLD") {
        journeyPosCode = "MFG_QUARANTINE";
        journeyPosDisplay = "Facility · Quarantined";
      } else if (status === "QC_PENDING") {
        journeyPosCode = "MFG_QC_LAB";
        journeyPosDisplay = "QC Lab · Release Testing";
      } else if (status === "IN_MANUFACTURING") {
        journeyPosCode = "MFG_CLEANROOM";
        journeyPosDisplay = "Manufacturing Cleanroom";
      } else if (status === "COLLECTED") {
        journeyPosCode = "OUTBOUND_TRANSIT";
        journeyPosDisplay = "Transit to Manufacturing";
      } else if (status === "APHERESIS_PENDING") {
        journeyPosCode = "SITE_APHERESIS";
        journeyPosDisplay = "Clinical Site · Apheresis";
      } else if (status === "ENROLLED" || status === "ELIGIBLE") {
        journeyPosCode = "SITE_ENROLLED";
        journeyPosDisplay = "Clinical Site · Enrolled";
      }

      // Derive governing readiness & quality authority
      let govReadinessCode = "PENDING_RELEASE";
      let govReadinessDisplay = "PENDING QUALITY RELEASE";
      let readinessBadgeClass = "readiness-pending";
      let infusionAuth: "AUTHORIZED" | "NOT_READY" | "PROHIBITED" | "ADMINISTERED" | "ADMINISTERED_UNDER_EXCEPTION" = "NOT_READY";

      let holdDetail: PatientSummary["hold_detail"];

      if (status === "INFUSED") {
        if (hasQmsOrMesHold) {
          // Anomaly: Infused record despite QMS hold in raw dataset
          govReadinessCode = "INVESTIGATION_POST_INFUSION";
          govReadinessDisplay = "INVESTIGATION — RETROSPECTIVE QA HOLD";
          readinessBadgeClass = "readiness-investigation";
          infusionAuth = "ADMINISTERED_UNDER_EXCEPTION";
          holdDetail = {
            status: "OPEN",
            opened_at: b ? b.row.mfg_end || b.row.mfg_start : p.row.enrolled_at,
            closed_at: null,
            blocks_release: true,
            blocks_infusion: true,
            category: "RETROSPECTIVE_INVESTIGATION_POST_INFUSION",
            quality_disposition_ref: `CAPA-2026-RETRO-${pKey.replace("P-", "")}`,
            clinical_risk_note:
              "Source data anomaly: Patient recorded as INFUSED while batch MES/QMS authority indicates QA_HOLD / HOLD. Flagged for critical pharmacovigilance and retrospective quality audit.",
          };
        } else {
          govReadinessCode = "COMPLETED_GOVERNED";
          govReadinessDisplay = "COMPLETED — GOVERNED INFUSION";
          readinessBadgeClass = "readiness-completed";
          infusionAuth = "ADMINISTERED";
          holdDetail = {
            status: "NONE",
            opened_at: null,
            closed_at: null,
            blocks_release: false,
            blocks_infusion: false,
            category: "NONE",
            quality_disposition_ref: "DISP-RELEASED-APPROVED",
            clinical_risk_note: "Infusion completed under normal release protocol.",
          };
        }
      } else if (hasQmsOrMesHold) {
        // Active hold: Strictly blocks release and prohibits infusion
        govReadinessCode = "BLOCKED_QA_HOLD";
        govReadinessDisplay = "BLOCKED — QA HOLD";
        readinessBadgeClass = "readiness-blocked";
        infusionAuth = "PROHIBITED";
        holdDetail = {
          status: "OPEN",
          opened_at: b ? b.row.mfg_end || b.row.mfg_start : p.row.enrolled_at,
          closed_at: null,
          blocks_release: true,
          blocks_infusion: true,
          category: "ACTIVE_MANUFACTURING_HOLD",
          quality_disposition_ref: `CAPA-2026-HOLD-${pKey.replace("P-", "")}`,
          clinical_risk_note:
            "Authoritative QMS release is on HOLD. Product must remain strictly in physical quarantine; clinical administration is prohibited.",
        };
      } else if (b && b.row.qms_release_status === "RELEASED") {
        govReadinessCode = "RELEASED_AUTHORIZED";
        govReadinessDisplay = "RELEASED — HUMAN AUTHORIZED";
        readinessBadgeClass = "readiness-released";
        infusionAuth = "AUTHORIZED";
        holdDetail = {
          status: "NONE",
          opened_at: null,
          closed_at: null,
          blocks_release: false,
          blocks_infusion: false,
          category: "NONE",
          quality_disposition_ref: "QMS-REL-PASS",
          clinical_risk_note: "Quality release authorized by human Quality Authority.",
        };
      } else if (status === "ENROLLED" || status === "ELIGIBLE") {
        govReadinessCode = "ELIGIBILITY_VERIFIED";
        govReadinessDisplay = "ELIGIBILITY VERIFIED";
        readinessBadgeClass = "readiness-neutral";
        infusionAuth = "NOT_READY";
        holdDetail = {
          status: "NONE",
          opened_at: null,
          closed_at: null,
          blocks_release: false,
          blocks_infusion: false,
          category: "NONE",
          quality_disposition_ref: "PRE-COLLECTION",
          clinical_risk_note: "Patient in pre-manufacturing eligibility phase.",
        };
      } else {
        govReadinessCode = "PENDING_RELEASE";
        govReadinessDisplay = "PENDING QUALITY RELEASE";
        readinessBadgeClass = "readiness-pending";
        infusionAuth = "NOT_READY";
        holdDetail = {
          status: "NONE",
          opened_at: null,
          closed_at: null,
          blocks_release: false,
          blocks_infusion: false,
          category: "NONE",
          quality_disposition_ref: "IN_PROCESS",
          clinical_risk_note: "Batch in manufacturing or testing. Release pending evidence packet assembly.",
        };
      }

      // Ensure presentation-safe phase display:
      // If a patient is at the site but on QA HOLD, NEVER say "Ready for Infusion"
      let safePhaseDisplay = config.display;
      if (status === "INFUSION_READY" && hasQmsOrMesHold) {
        safePhaseDisplay = "Returned to Site (Quarantined)";
      } else if (status === "INFUSED" && hasQmsOrMesHold) {
        safePhaseDisplay = "Infused (QA Investigation)";
      }

      return {
        patient_key: pKey,
        crm_patient_id: p.row.crm_patient_id || "",
        clinical_subject_id: p.row.clinical_subject_id || "",
        mrn: p.row.mrn || "",
        synthetic_name: p.row.synthetic_name || "",
        dob: p.row.dob || "",
        center_id: p.row.center_id || "",
        country: p.row.country || "",
        product_code: p.row.product_code || "",
        journey_status: status,
        enrolled_at: p.row.enrolled_at || "",
        phase_step: config.step,
        phase_display: safePhaseDisplay,
        phase_badge_class: hasQmsOrMesHold && status !== "INFUSED" ? "phase-hold" : config.badgeClass,
        
        journey_position_code: journeyPosCode,
        journey_position_display: journeyPosDisplay,
        governing_readiness_code: govReadinessCode,
        governing_readiness_display: govReadinessDisplay,
        readiness_badge_class: readinessBadgeClass,
        infusion_authorization: infusionAuth,

        has_hold: hasQmsOrMesHold,
        hold_detail: holdDetail,

        batch_id: b ? b.row.batch_id : null,
        mes_status: b ? b.row.mes_status : null,
        qms_release_status: b ? b.row.qms_release_status : null,
        collection_id: c ? c.row.collection_id : null,
        collection_time: c ? c.row.collection_time : null,
        coi_id: c ? c.row.coi_id : b ? b.row.coi_id : null,
        viability_pct: c && c.row.viability_pct ? parseFloat(c.row.viability_pct) : null,
        deviations_count: devs.length,
        open_deviations_count: openDevs.length,
        is_active: config.isActive,
      };
    });
    lastCacheTime = now;
  }

  // Calculate overall metrics across the cohort
  const total = cachedPatients.length;
  const activeCount = cachedPatients.filter((p) => p.is_active).length;
  const countsByPhase: Record<string, number> = {};
  for (const p of cachedPatients) {
    countsByPhase[p.journey_status] = (countsByPhase[p.journey_status] || 0) + 1;
  }
  const totalHoldsCount = cachedPatients.filter((p) => p.has_hold).length;

  let filtered = cachedPatients;

  // Active / Completed filter
  const statusFilter = query.statusFilter || "active";
  if (statusFilter === "active") {
    filtered = filtered.filter((p) => p.is_active);
  } else if (statusFilter === "completed") {
    filtered = filtered.filter((p) => !p.is_active);
  }

  // Phase filter - with smart governance logic:
  // Selecting QA_HOLD shows ALL patients with active QA holds or investigations
  if (query.phase && query.phase !== "ALL") {
    if (query.phase === "QA_HOLD") {
      filtered = filtered.filter((p) => p.has_hold);
    } else if (query.phase === "INFUSION_READY") {
      // Governed safety: only patients that are legitimately ready for infusion (not on hold!)
      filtered = filtered.filter((p) => p.journey_status === "INFUSION_READY" && !p.has_hold);
    } else {
      filtered = filtered.filter((p) => p.journey_status === query.phase);
    }
  }

  // Product filter
  if (query.product && query.product !== "ALL") {
    filtered = filtered.filter((p) => p.product_code === query.product);
  }

  // Treatment center filter
  if (query.center && query.center !== "ALL") {
    filtered = filtered.filter((p) => p.center_id === query.center);
  }

  // Search filter
  if (query.search && query.search.trim()) {
    const q = query.search.trim().toLowerCase();
    filtered = filtered.filter(
      (p) =>
        p.patient_key.toLowerCase().includes(q) ||
        p.synthetic_name.toLowerCase().includes(q) ||
        p.mrn.toLowerCase().includes(q) ||
        p.center_id.toLowerCase().includes(q) ||
        (p.batch_id && p.batch_id.toLowerCase().includes(q)) ||
        (p.coi_id && p.coi_id.toLowerCase().includes(q))
    );
  }

  // Sorting
  const sortBy = query.sortBy || "patient_key";
  const sortDir = query.sortDir === "desc" ? -1 : 1;
  filtered = [...filtered].sort((a: any, b: any) => {
    let aVal = a[sortBy];
    let bVal = b[sortBy];
    if (aVal === null || aVal === undefined) return 1;
    if (bVal === null || bVal === undefined) return -1;
    if (typeof aVal === "string") {
      return aVal.localeCompare(bVal) * sortDir;
    }
    return (aVal - bVal) * sortDir;
  });

  const page = Math.max(1, query.page || 1);
  const pageSize = Math.max(5, Math.min(100, query.pageSize || 15));
  const totalFiltered = filtered.length;
  const totalPages = Math.ceil(totalFiltered / pageSize);
  const startIdx = (page - 1) * pageSize;
  const items = filtered.slice(startIdx, startIdx + pageSize);

  return {
    kpis: {
      total_patients: total,
      active_patients: activeCount,
      completed_patients: total - activeCount,
      counts_by_phase: countsByPhase,
      qa_holds: totalHoldsCount,
      in_manufacturing: countsByPhase["IN_MANUFACTURING"] || 0,
      qc_pending: countsByPhase["QC_PENDING"] || 0,
      infusion_ready: cachedPatients.filter((p) => p.journey_status === "INFUSION_READY" && !p.has_hold).length,
      return_transit: countsByPhase["RETURN_TRANSIT"] || 0,
    },
    pagination: {
      page,
      page_size: pageSize,
      total_items: totalFiltered,
      total_pages: totalPages,
    },
    patients: items,
  };
}

export function getPatientDetail(patientKey: string, baselineDir: string = BASELINE) {
  // Ensure cache is loaded
  if (!cachedPatients) {
    getPatientsList({ statusFilter: "all" }, baselineDir);
  }
  const patient = cachedPatients?.find((p) => p.patient_key === patientKey);
  if (!patient) {
    throw new Error(`Patient not found: ${patientKey}`);
  }

  const rawDir = path.join(baselineDir, "data", "raw");
  function patientRows(file: string) {
    const rows = loadRows(path.join(rawDir, file), baselineDir);
    return rows.filter((r) => r.row.patient_key === patientKey);
  }

  const shipments = patientRows("shipments.csv");
  const slots = patientRows("manufacturing_slots.csv");
  const qcResults = patientRows("qc_results.csv");
  const deviations = patientRows("deviations.csv");

  return {
    patient,
    shipments: shipments.map((s) => s.row),
    slots: slots.map((sl) => sl.row),
    qc_results: qcResults.map((qc) => qc.row),
    deviations: deviations.map((d) => d.row),
  };
}

import path from "path";
import { BASELINE, loadRows, SourceRowItem } from "./sourceCases";

export const OWNERS: Record<string, string> = {
  "INJ-001": "CLINICAL_OPERATIONS_AND_PLANNER",
  "INJ-002": "LOGISTICS_AND_QUALITY",
  "INJ-003": "MANUFACTURING_PLANNER",
  "INJ-004": "QC_AND_QUALITY",
  "INJ-005": "TREATMENT_CENTER_AND_CLINICAL_OPERATIONS",
  "INJ-006": "MANUFACTURING_PLANNER_AND_INTEGRATION_OWNER",
  "INJ-007": "IDENTITY_AUTHORITY",
  "INJ-008": "LOGISTICS_OWNER",
  "INJ-009": "QUALITY_AND_QMS_SERVICE_OWNER",
  "INJ-010": "PAYER_AND_CLINICAL_OPERATIONS",
};

export const PROPAGATION: Record<string, string[]> = {
  "INJ-001": [
    "collection",
    "outbound_logistics",
    "slot",
    "manufacturing",
    "qc",
    "qa_release",
    "return_logistics",
    "conditioning",
    "infusion",
  ],
  "INJ-002": ["outbound_logistics", "return_logistics", "qc", "qa_release"],
  "INJ-003": ["slot", "manufacturing", "qc", "qa_release", "return_logistics", "conditioning", "infusion"],
  "INJ-004": ["qc", "qa_release", "return_logistics", "conditioning", "infusion"],
  "INJ-005": ["site_qualification", "collection", "outbound_logistics", "slot"],
  "INJ-006": ["slot", "manufacturing"],
  "INJ-007": ["identity", "collection", "outbound_logistics", "slot"],
  "INJ-008": [
    "outbound_logistics",
    "slot",
    "manufacturing",
    "qc",
    "qa_release",
    "return_logistics",
    "conditioning",
    "infusion",
  ],
  "INJ-009": ["qa_release", "return_logistics", "conditioning", "infusion"],
  "INJ-010": ["authorization", "collection", "outbound_logistics", "slot"],
};

export const DELAY_HOURS: Record<string, number> = {
  "INJ-001": 5,
  "INJ-003": 18,
  "INJ-004": 36,
  "INJ-009": 4,
};

function parseIso(value?: string): Date | null {
  if (!value) return null;
  const d = new Date(value);
  return isNaN(d.getTime()) ? null : d;
}

function shiftIso(value: string, hours?: number): string | null {
  if (!value || hours === undefined) return null;
  const d = parseIso(value);
  if (!d) return null;
  const shifted = new Date(d.getTime() + hours * 3600 * 1000);
  return shifted.toISOString().replace(/\.000Z$/, "Z");
}

export function listInjects(baselineDir: string = BASELINE) {
  const items = loadRows(path.join(baselineDir, "scenarios", "inject_catalog.csv"), baselineDir);
  return items.map((item) => ({
    inject_id: item.row.inject_id,
    name: item.row.name,
    trigger: item.row.trigger,
    severity: item.row.severity,
  }));
}

export function previewInject(injectId: string, patientKey: string = "P-00001", baselineDir: string = BASELINE) {
  const injects = loadRows(path.join(baselineDir, "scenarios", "inject_catalog.csv"), baselineDir);
  const inject = injects.find((item) => item.row.inject_id === injectId);
  if (!inject) {
    throw new Error(`Inject not found: ${injectId}`);
  }

  const rawDir = path.join(baselineDir, "data", "raw");
  function patientRows(fileName: string): SourceRowItem[] {
    const rows = loadRows(path.join(rawDir, fileName), baselineDir);
    return rows.filter((item) => item.row.patient_key === patientKey);
  }

  const patient = patientRows("patients.csv");
  if (!patient.length) {
    throw new Error(`Patient not found: ${patientKey}`);
  }

  const collection = patientRows("collections.csv");
  const shipments = patientRows("shipments.csv");
  const slot = patientRows("manufacturing_slots.csv");
  const batch = patientRows("batches.csv");
  const allQc = loadRows(path.join(rawDir, "qc_results.csv"), baselineDir);
  const qc = batch.length ? allQc.filter((item) => item.row.batch_id === batch[0].row.batch_id) : [];

  const outbound = shipments.find((s) => s.row.direction === "OUTBOUND") || null;
  const returned = shipments.find((s) => s.row.direction === "RETURN") || null;

  let latestQc: SourceRowItem | null = null;
  if (qc.length > 0) {
    latestQc = qc.reduce((prev, curr) =>
      (curr.row.reported_at || "") > (prev.row.reported_at || "") ? curr : prev
    );
  }

  const milestoneRows: Record<string, [SourceRowItem | null, string]> = {
    collection: [collection[0] || null, "collection_time"],
    outbound_logistics: [outbound, "arrived_at"],
    slot: [slot[0] || null, "scheduled_start"],
    manufacturing: [batch[0] || null, "mfg_end"],
    qc: [latestQc, "reported_at"],
    qa_release: [null, ""],
    return_logistics: [returned, "arrived_at"],
    conditioning: [null, ""],
    infusion: [null, ""],
  };

  const hours = DELAY_HOURS[injectId];
  const affectedList =
    PROPAGATION[injectId] ||
    inject.row.affected.split(";").map((p) => p.trim());

  const impact: Array<{
    milestone: string;
    source_time: string | null;
    hypothetical_zero_slack_time: string | null;
    source_locator: string | null;
    status: string;
  }> = [];

  for (const milestone of affectedList) {
    const [item, timeField] = milestoneRows[milestone] || [null, ""];
    const baselineTime = item ? item.row[timeField] || "" : "";
    impact.push({
      milestone,
      source_time: baselineTime || null,
      hypothetical_zero_slack_time: shiftIso(baselineTime, hours),
      source_locator: item ? item.source_locator : null,
      status: item ? "AT_RISK_PREVIEW" : "UNQUANTIFIED_DEPENDENCY",
    });
  }

  const affectedRoutes =
    injectId === "INJ-008"
      ? shipments.map((item) => ({
          shipment_id: item.row.shipment_id,
          direction: item.row.direction,
          origin: item.row.origin,
          destination: item.row.destination,
          source_locator: item.source_locator,
          delivery_assurance: "UNKNOWN_AFTER_INJECT",
        }))
      : [];

  const affectedReservations: Array<{
    slot_id: string;
    patient_key: string;
    state: string;
    owner: string;
    source_locator: string;
  }> = [];

  if (injectId === "INJ-003" && slot.length > 0) {
    const site = slot[0].row.site_id;
    const start = parseIso(slot[0].row.scheduled_start);
    const end = start ? new Date(start.getTime() + 18 * 3600 * 1000) : null;
    const allSlots = loadRows(path.join(rawDir, "manufacturing_slots.csv"), baselineDir);
    for (const item of allSlots) {
      const scheduled = parseIso(item.row.scheduled_start);
      if (
        item.row.site_id === site &&
        start &&
        end &&
        scheduled &&
        scheduled.getTime() >= start.getTime() &&
        scheduled.getTime() < end.getTime()
      ) {
        affectedReservations.push({
          slot_id: item.row.slot_id,
          patient_key: item.row.patient_key,
          state: "EXCEPTION_PREVIEW_NOT_COMMITTED",
          owner: OWNERS[injectId],
          source_locator: item.source_locator,
        });
      }
    }
  }

  return {
    scope: "FROZEN_V2_SOURCE_SCENARIO_PREVIEW_NOT_EXECUTED",
    inject_id: injectId,
    name: inject.row.name,
    trigger: inject.row.trigger,
    severity: inject.row.severity,
    affected_declared: inject.row.affected.split(";"),
    representative_patient_key: patientKey,
    representative_patient_source: patient[0].source_locator,
    inject_source_locator: inject.source_locator,
    owner_role: OWNERS[injectId] || "UNASSIGNED",
    impact_preview: impact,
    affected_routes: affectedRoutes,
    affected_reservations: affectedReservations,
    delay_hours_from_stimulus: hours ?? null,
    assumptions: [
      "The source inject has no patient/date; this patient is a representative synthetic selection.",
      "Any shifted timestamp assumes zero slack and no capacity/route/clinical-policy adjustment; it is not a forecast or approved plan.",
      "Unknown downstream milestone times remain unknown; no delivery or product-disposition assurance is invented.",
    ],
    required_next_step: "OWNER_REVIEW_AND_EVIDENCE_RECONCILIATION",
    side_effects: 0,
    production_authorized: false,
  };
}

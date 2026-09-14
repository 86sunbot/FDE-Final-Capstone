# Problem Context

The enterprise coordinates individualized autologous therapy journeys. The commercial/clinical promise is simple: collect patient material, manufacture a patient-specific product, release it, return it and infuse on time. The systems reality is not simple.

## Canonical conceptual journey

`Patient Identified → Eligibility → Consent → Financial Authorization → Treatment Center Readiness → Apheresis → Chain of Identity → Outbound Logistics → Manufacturing Slot → Manufacturing → QC → QA Release → Return Logistics → Conditioning → Infusion Readiness`

## Why this is an AI FDE problem

The hard cases are not isolated software bugs. They are contradictions and dependencies across independently evolved systems. CRM may say a patient is ready while the manufacturing scheduler has only a provisional slot, QMS has an open deviation, logistics has not confirmed a return route, and the treatment center has already scheduled conditioning.

The target of the exercise is therefore **operational truth and governed decision support**, not a chatbot.

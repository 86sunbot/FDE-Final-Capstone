# Discovery Checklist

- [ ] Reconcile patient identifiers across CRM, clinical and orchestration data.
- [ ] Reconstruct patient→collection→shipment→batch→product lineage for a sample of journeys.
- [ ] Identify competing definitions of READY/HOLD/COMPLETE/RELEASED.
- [ ] Separate event time from recorded/ingested time.
- [ ] Locate hard-coded business rules and duplicated rule implementations.
- [ ] Identify manual/shadow workflows.
- [ ] Find partial distributed transactions and missing compensation logic.
- [ ] Identify quality-release vs manufacturing-complete semantic confusion.
- [ ] Find site qualification, consent and financial authorization dependencies.
- [ ] Identify resilience/recovery gaps for logistics/manufacturing/QC disruption.
- [ ] Identify actions that must remain human-authorized.
- [ ] Propose measurable before/after KPIs.

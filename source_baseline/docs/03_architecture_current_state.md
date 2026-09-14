# Current-State Architecture (Intentionally Incomplete)

```mermaid
flowchart LR
    CRM[CRM] --> INT[Integration Hub]
    CLIN[Clinical Portal] --> INT
    INT --> SCHED[Manufacturing Scheduler]
    SCHED --> MES[MES]
    MES --> LIMS[LIMS]
    LIMS --> QMS[QMS]
    QMS --> ERP[ERP]
    ERP --> LOG[Logistics Portal]
    LOG --> CLIN
```

**Warning:** this diagram reflects how the architecture is described in one governance document, not necessarily how production behaves. Participants should validate it against code, interfaces, synthetic records, shadow files and events.

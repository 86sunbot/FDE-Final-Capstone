# Stage 14 - As-Built Architecture

```mermaid
flowchart TD
  WEB[Browser Control Tower] --> API[FastAPI]
  CLI[CLI] --> APP[CapstoneApplication]
  API --> APP
  APP --> EV[Evidence + Readiness]
  APP --> ID[Identity Service]
  APP --> CMD[Command Service]
  APP --> Q[Quality Service]
  APP --> AI[Assistant Gateway]
  ID --> CASE[Case Service]
  CMD --> SIM[Slot Simulator]
  AI --> FAKE[Off or deterministic fake]
  EV --> DB[(SQLite)]
  ID --> DB
  CMD --> DB
  Q --> DB
  AI --> DB
  CASE --> DB
  DB --> AUD[Audit hash chain + metrics]
```

There are no background autonomous agents, vector database, external network dependency, live model, or production integration. The modular seams are Python service/adaptor interfaces; SQLite is a POC implementation detail behind `Database`.

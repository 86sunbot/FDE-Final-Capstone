# Stage 17 - Release, Deployment and Adoption Record

**Deployment type:** Local synthetic simulation; no production deployment occurred.

Release 1.0.0 is bound by `stage_14/release_manifest.json`, defaults to AI off and contains no credential. The deployment simulation executed:

- 20 paired AI-off/bounded-fake shadow runs with 20 matching domain outcomes;
- 10 AI-off canary runs with 10 successful controlled journeys and valid audit chains;
- one rollback exercise from fake-assistant mode to AI off with deterministic service available.

There were no real users, integrations, patient records or organizational SOP changes. “Adoption” is therefore not measured. The executable evidence is `deployment_simulation_results.json`.

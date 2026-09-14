# Stage 8 - TCO and Cost Model

**Status:** FORMULA AND MEASUREMENT PLAN; NO FINANCIAL BENEFIT CLAIM

## Cost equation

For a defined period:

`TCO = build labor + review/assurance labor + infrastructure + model usage + observability/storage + operations/support + training/change + supplier/licence + incident/rework + retirement`

Unit economics:

`cost per correctly resolved case = total attributable operating cost / cases resolved correctly without a P0 failure`

An unsafe or incorrectly resolved case is not counted as successful even if it is fast.

## Capstone measurement ledger

| Driver | Unit to capture | Current state |
|---|---|---|
| Engineering | hours by stage/component | Not yet instrumented |
| Human review | minutes by scenario and Arm B/C | Stage 15 plan defined |
| Compute | process time, memory and storage | Stage 14/15 pending |
| Model | calls, input/output tokens and retries | AI disabled; pending provider decision |
| Provider price | dated currency/unit and tier | Unknown; must not be recorded as zero |
| Operations | alerts, incidents, recovery time and operator minutes | Stage 16-18 pending |
| Rework | failed cases, defect effort and reruns | Stage 15 pending |
| Avoided work/delay | paired baseline and outcome with denominator | Stage 19 pending |

## Scenario policy

- O2 is the low-cost reference because it introduces no model usage.
- O3 must report incremental AI cost and incremental value separately.
- O4/O6 have higher coordination/operational complexity even when software licences are free.
- O5 cannot be costed responsibly without vendor terms, usage, integration and exit assumptions.

## G2 decision rule

Approve O3 only with a cost kill switch: if AI adds no measured human benefit, breaches the token/cost ceiling set before live testing, or degrades a P0 result, disable it and retain O2. Stage 8 does not claim ROI, savings or production TCO.

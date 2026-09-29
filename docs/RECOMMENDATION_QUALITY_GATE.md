# FinOps Recommendation Quality Gate

A recommendation must not be classified as **Actionable Optimization** until minimum evidence is available.

| Field | Required evidence |
|---|---|
| Workload / resource | Exact workload, resource, service, or cost scope |
| Technical owner | Team/person responsible for operation |
| Business owner | Team/person accountable for business value where available |
| Environment | dev / test / UAT / prod / other |
| Current cost | Baseline cost using a defined comparison period |
| Cost type | usage, rate, transfer, storage, license, commitment, other |
| Utilization evidence | CPU, memory, capacity, bytes, runtime, CU/credit/worker-hours, etc. |
| Business metric | transaction, customer, TB, pipeline run, application, well, order, etc. where applicable |
| SLA / SLO | Performance, latency, completion window, availability, or other constraint |
| Hypothesis | Why the current state may be inefficient |
| Root-cause evidence | Evidence supporting the diagnosis |
| Recommendation | Specific change being proposed |
| Alternative options | At least one alternative for material changes |
| Projected saving | Modeled amount or percentage with assumptions |
| Technical risk | Reliability/performance/security/compliance impact |
| Validation plan | How success or failure will be measured |
| Approval owner | Who authorizes implementation |
| Result | PASS / FAIL / INCONCLUSIVE |
| Realized saving | Only after comparable post-change billing evidence exists |
| Recurrence control | Guardrail / policy / automation / process if appropriate |

## Classification rule

If critical evidence is missing, classify the item as:

```text
Observation
or
Investigation Candidate
```

not `Actionable Optimization`.

## Recommendation lifecycle

```text
Observation
  ↓
Investigation Candidate
  ↓
Evidence Collected
  ↓
Root Cause Confirmed
  ↓
Optimization Option(s)
  ↓
Stakeholder Review
  ↓
Approved Change
  ↓
Implementation
  ↓
Technical Validation
  ↓
Financial Validation
  ↓
Business Validation
  ↓
Realized Outcome
  ↓
Guardrail / Recurrence Prevention
```

This lifecycle must later be represented in the Power BI savings pipeline.

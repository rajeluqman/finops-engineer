# Practitioner Signals

This file captures practitioner-derived hypotheses from the Source of Truth. These are **Grade D signals** for hypothesis generation, failure-mode discovery, and interview realism. They are not production proof and must be reconciled against vacancy data, FinOps Foundation guidance, official provider documentation, and Grade A/B cases.

| # | Practitioner signal | Project action | Priority |
|---|---|---|---|
| 1 | FinOps without technical literacy creates weak recommendations. | Require a Technical FinOps Competency Gate. | Critical |
| 2 | Cost reduction alone is the wrong objective. | Make VALUE and RISK mandatory in optimization decisions. | Critical |
| 3 | FinOps should begin at architecture time. | Add estimate → design review → deploy → validate. | Critical |
| 4 | Guardrails beat repeated reminder emails. | Add policy-as-code and CI/CD validation labs. | Critical |
| 5 | Desired vs actual state needs continuous audit. | Compare IaC/resource inventory/billing inventory. | Critical |
| 6 | Observability is required before optimization. | Require cost + usage + SLA evidence. | Critical |
| 7 | Optimize usage before buying commitments. | Remove waste → rightsize → stable baseline → commit. | Critical |
| 8 | Dev/test/UAT/prod need different controls. | Model environment/lifecycle stage explicitly. | High |
| 9 | Zombie resources are common waste. | Add zombie-resource detection lab and KPI. | Critical |
| 10 | Architecture substitution can beat simple rightsizing. | Add architecture-alternative analysis. | Critical |
| 11 | TCO extends beyond provider invoice. | Add TCO model and decision template. | High |
| 12 | Vendor and contract economics are valid FinOps work. | Promote commercial optimization. | High |
| 13 | Dedicated FinOps matters more at scale. | Capture estate scale when disclosed. | High |
| 14 | Commitment management is ongoing. | Track strategy, purchase, coverage, utilization, renewal, expiry. | Critical |
| 15 | FinOps is collaborative, not cost police. | Maintain RACI across FinOps/Engineering/Finance/Procurement/Business. | Critical |
| 16 | Business/service owners must own value. | Add business owner, technical owner, service, cost center dimensions. | Critical |
| 17 | Reports must support decisions. | No vanity visuals in Power BI. | Critical |
| 18 | FinOps tooling needs ROI justification. | Add native vs third-party / build-vs-buy matrix. | High |
| 19 | One-off cost cutting is not mature FinOps. | Add recurring operating cadence. | High |
| 20 | FinOps is partly behavioral/cultural. | Add enablement and recommendation workflow. | High |
| 21 | Treating cloud like on-prem can destroy economics. | Add lift-and-shift/cloud anti-pattern analysis. | High |
| 22 | Outsourced engineering can create accountability gaps. | Add vendor/contractor cloud governance. | High |

## Technical FinOps Competency Gate

Before advanced optimization, the learner should explain cost behavior of compute, storage, network/egress, databases, serverless, container/cluster compute where relevant, data warehouses, lake/lakehouse workloads, BI serving/refresh patterns, and licensing/commercial commitments.

## FinOps Value Model

Every recommendation should connect:

```text
Business value
+ architecture
+ engineering
+ finance
+ governance
```

A recommendation that optimizes only one dimension is incomplete.

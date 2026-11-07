# Operating and Scaling Cost Visibility

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Blank budget panel | Correct scope, budget existence, read permission, period and reporting delay; do not substitute zero |
| Unexpected forecast alert | Stored threshold type and percentage, not just notification name |
| Missing tagged cost | Resource tags, supported billing scope/service, data timing and any separately configured cost-tag inheritance |
| Noncompliance without a blocked deployment | The module intentionally disables enforcement; review Policy mode |
| Saved view differs | Review the exact field difference; the helper refuses overwrite |
| Charges after pause | Allocated compute, disks, IPs, networking, registry, storage, logs, scheduled jobs and shared consumers |
| No shutdown after an alert | Budgets notify only; budget-triggered shutdown is deferred |

## Useful operating cycle

Review spend at a stable cadence with its reporting time, currency and scope. Identify the largest cost driver, its owner and business purpose. Compare usage/performance before resizing, review dependency and recovery impact, then make a separate controlled change. Record observed results without treating a short extrapolation as an invoice or Azure forecast.

## Growth

The current workbook is intentionally small: three known subscription-budget panels and native detailed views. More subscriptions may justify configuration-driven panel generation, billing-scope exports and an agreed shared-cost allocation model. Those are future options, not features implemented here.

Measure missing-tag coverage, unattributed spend, idle retained resources, log volume and change outcomes. Add quality checks before claiming chargeback accuracy. Tags alone do not solve shared allocation, credits, commitment discounts, multiple currencies or owner accountability.

Keep the workbook's reads bounded and use Cost Management's supported reporting cadence. Frequent refresh does not accelerate cost-data arrival. A custom export/data platform has its own storage, compute and maintenance cost; add it only when the native views no longer meet a concrete need.

## Strengths and tradeoffs

| Choice | Strength | Cost or limit |
| --- | --- | --- |
| Existing-budget workbook | Small extra operating footprint | Delayed reported-spend snapshot, not detailed real-time metering |
| Native Cost Analysis views | Azure's existing breakdown and permissions | Scope/service/contract support and correct user access still matter |
| Evaluation-only tag policy | Finds gaps without unexpected deployment denials | Gaps remain until owners fix them; it is not enforcement |
| On-demand engineering VM | Reduces unattended compute runtime | Retained charges and availability interruptions remain |
| Explicit shutdown allowlist design | Limits a future action's blast radius | Needs real dependency checks, event authentication, durable dedupe and recovery before execution |

Budget-triggered shutdown is not a reliable hard cap because cost reporting and alert evaluation lag usage. Do not suspend protective scanning, backups or production dependencies to satisfy a dashboard target.

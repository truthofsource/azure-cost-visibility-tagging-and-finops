# Issues and Lessons from the Actual Work

| Finding | Why it mattered | Conclusion |
| --- | --- | --- |
| A 90% notification was named Forecasted but stored as Actual | A label suggested behavior the service was not configured to perform | Inspect the actual threshold type. The recorded narrow correction used a two-step notification rename; do not replay that historical operation |
| A sample Resource Graph query listed groups, not spend | Inventory was being mistaken for billing evidence | Use Cost Management for spend and Resource Graph for resources/tags |
| A reference dashboard proposed another workspace and Logic App | The platform already had logging and direct budget notifications | Reuse existing budget reads and native views; do not add a pipeline without a need |
| Shared dependencies lived outside the production subscription | Environment names alone could lead to a disruptive shutdown | Review exact consumers and an allowlist before stopping anything |
| Stopped compute still left charges | Disks, networking, registries and retained storage remained | Verify resource power state and individual billed meters; do not promise a zero bill |
| The workbook used six of seven common tags | Source consistency was incomplete | Surface the `criticality` gap instead of reporting universal compliance |
| Policy names contained Audit | Names could be mistaken for the built-in effect | Confirm `enforce=false` / DoNotEnforce and actual parameters |

The public project documents these conclusions. It does not refresh private invoices, reapply a corrected budget, delete resources, change recipients or activate the deferred shutdown automation.

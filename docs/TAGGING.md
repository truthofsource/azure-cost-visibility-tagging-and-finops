# Tags That Help Someone Act

| Key | Question it answers | Fictional example |
| --- | --- | --- |
| `environment` | Is this hub, production or nonproduction? | `nonproduction` |
| `workload` | What purpose does it serve? | `imports` |
| `owner` | Which team maintains it? | `platform-team` |
| `managed_by` | Where should a change be made? | `terraform` |
| `data_class` | What broad information class does it handle? | `internal` |
| `criticality` | What operational importance needs review? | `medium` |
| `cost_center` | Which business grouping tracks the expense? | `operations` |

These keys come from the actual common-tag pattern. Values here are examples, not a tenant-wide approved vocabulary. Tags are plain-text metadata: use team references, not credentials, email contents, employee names or personal records.

Resource-group tags do not automatically become resource tags. Cost Management's optional tag inheritance concerns usage records and is distinct from changing resource tags. Neither inheritance mechanism is enabled by this project.

Azure tag keys are case-insensitive for operations, while values are case-sensitive. The local coverage helper accounts for key casing and treats blank values as a useful gap. That blank-value check is a stricter local review rule; it does not claim the built-in required-key policy behaves identically.

The actual workbook builder omits `criticality` despite the seven-key common pattern. The test deliberately records this source gap. A real correction belongs in the builder or owning deployment after reviewing its policy applicability; the portfolio does not change the live workbook or claim full tag compliance.

A shared registry or vault may sit in a nonproduction subscription while supporting production. Tags help identify that situation but do not prove current dependencies. An environment label alone is insufficient shutdown authority. Shared-cost allocation also needs an agreed rule; tagging a shared resource does not split its charges among consumers.

Grow the standard with accountable owners, allowed values, exception records and a review process. Audit first, repair through the owning infrastructure source, then consider narrowly tested enforcement. Do not enable a broad Deny or Modify rollout merely to improve a dashboard percentage.

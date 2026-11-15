# How Cost Visibility Fits Together

## Separate budgets for each environment

The recorded implementation has separate hub, nonproduction and production budget scopes. Historical configured thresholds were $50, $200 and $100 respectively; they are not a tenant-wide allowance or current invoice. The public data uses those example budget amounts with fictional spend. Subscription ownership and actual source inputs must be verified before making a live claim.

## The workbook and native views

The actual Python builder creates one shared Azure Monitor workbook. Each panel issues an ARM GET for an existing budget and displays its budget amount, current reported spend, currency and period start. It does not run a Cost Management Usage query on every page load or create a Log Analytics workspace, Logic App, budget or cost-ingestion pipeline.

Detailed analysis stays in Azure Cost Management saved views. The helper builds daily month-to-date spending views with a budget indicator and breakdowns by service, resource group and billing meter category. It reads existing views, checks selected expected fields and the month-to-date window, and refuses those mismatches instead of overwriting them. The existing-view comparison does not validate every possible query property; the local builder test is not full live-view conformance. Creating absent views requires its explicit `--apply` flag; even its default mode contacts Azure. This project imports only its pure body builder or uses fake responses, never its live CLI path.

A workbook reader still needs permission to the budget resources and appropriate Cost Management access for detailed spend. Sharing a view does not grant billing permissions. Blank data can mean missing access or delayed reporting; it is not zero spend.

## Budget semantics

The copied budget has 50%, 80% and 100% Actual notifications plus a 90% Forecasted notification. Its email recipient is an input. The public example supplies a fictional address and creates no budget by default; it has no automation Action Group. The original budget uses a monthly time grain and preserves its initial period through a lifecycle setting.

Cost data and evaluation are delayed. Notifications prompt investigation; they do not reserve cash, stop meters or cap charges. A forecast is a projection, not an invoice. The local percentage model is only arithmetic over fictional supplied values; it is not Azure's forecast algorithm.

## Common tags and policy

Terraform's seven common keys identify environment, workload, owner, management method, data class, criticality and cost center. Resource owners apply them where the resource supports tags. A required-key policy does not define all approved values or allocate a shared bill automatically.

The actual governance module assigns built-in location and required-tag policies with enforcement disabled. This corresponds to DoNotEnforce; an assignment name containing Audit does not rewrite a definition's effect. The public tests preserve that behavior. No Modify/remediation, inheritance or enforcement rollout is implemented here.

## Shutdown boundary

The actual VM schedule is distinct from the deferred budget-triggered Logic App. Its source supplies a daily local shutdown time, Central Standard Time as Azure's time-zone identifier, and no automatic start. The Logic App example is disabled and contains only a Compose step that prepares data. Its separate fictional planner cannot stop resources. See [the design](SHUTDOWN-DESIGN.md).

## Historical evidence

The original workbook deployment's what-if identified one workbook create without new workspaces or budget changes. Azure resource reads confirmed the saved panels and shared views; separate portal visual rendering was not established in that record. Those are historical outcomes, not a new publication or live acceptance test for these public copies.

References: [budgets and evaluation](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets), [Azure tags](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources), [policy enforcement mode](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/assignment-structure).

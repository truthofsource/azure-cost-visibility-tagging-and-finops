# Commands, Queries and Clickops

## Local checks

Python 3.12 and Terraform 1.11 or newer are used. Python needs only its standard library.

```bash
python -B -m unittest discover -s tests -v
python -B scripts/demo.py
python -B scripts/build_cost_visibility_workbook.py --output .local-workbook.json
python -B scripts/preview.py --port 8143
```

The generated ARM JSON is a file, not a deployed workbook. Ctrl+C stops the viewer. All demo amounts/resources are fictional.

```bash
terraform -chdir=infra/cost-controls init -backend=false
terraform -chdir=infra/cost-controls fmt -check -recursive
terraform -chdir=infra/cost-controls validate
terraform -chdir=infra/cost-controls test
terraform -chdir=infra/governance init -backend=false
terraform -chdir=infra/governance validate
terraform -chdir=infra/governance test
```

Tests simulate Azure responses. Do not run apply or execute the live saved-view helper for local validation. No cloud permission is needed for the tests.

## Read-only cloud inspection examples

Supply the approved subscription and budget names privately. Do not publish billing results or actual resource identifiers in screenshots.

```bash
az account show --query '{name:name,id:id}'
az rest --method get --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/providers/Microsoft.Consumption/budgets/$BUDGET_NAME?api-version=2024-08-01"
az policy assignment list --scope "/subscriptions/$SUBSCRIPTION_ID" --query '[].{name:name,mode:enforcementMode,parameters:parameters}'
```

These commands are examples and were not run against Azure for publication. The budget read and a cost analysis have different roles. An authorized reader must still inspect currency, period and data freshness.

## Resource Graph: ownership, not spend

```kusto
Resources
| project name, type, resourceGroup,
    environment=tostring(tags.environment),
    owner=tostring(tags.owner),
    costCenter=tostring(tags.cost_center)
| order by environment asc, resourceGroup asc
```

This is an inventory query. It does not calculate spend. Use Cost Management → Cost analysis for daily actual cost, service/resource breakdowns and supported tag grouping.

## Portal path

1. Open Cost Management + Billing and select the exact subscription/scope.
2. Open Budgets. Inspect amount, period, actual threshold types and recipients without changing them.
3. Open Cost analysis. Review Month to date, Actual cost, daily trend and the saved service/group/meter pivots.
4. Open Azure Monitor → Workbooks for the shared budget overview. Check required access if a panel is blank.
5. Open Policy → Assignments/Compliance. Inspect enforcement mode and evaluation date; then inspect the resource's own tags.
6. Review the VM's power state and shutdown schedule separately. The disabled Logic App design is not a production control to enable from this guide.

A real workbook change needs a reviewed template and scoped `what-if` before deployment. No what-if or deployment is executed by the local example.

## Review a proposed workbook deployment

After selecting an authorized resource group and reviewing the fictional bindings, an operator can inspect proposed changes with:

```bash
az deployment group what-if --resource-group "$WORKBOOK_RESOURCE_GROUP" --template-file templates/cost-visibility.workbook.json
```

What-if reports intended resource changes; it is not a deployment or proof of future cost, rendered panels or correct permissions. This cloud command is not part of local tests and was not executed for publication.

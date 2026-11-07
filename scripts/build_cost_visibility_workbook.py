"""Generate the shared Azure Monitor cost workbook ARM template."""

import argparse
import json
import pathlib


WORKBOOK_ID = "00000000-0000-4000-8000-000000000010"
SUBSCRIPTIONS = (
    ("Hub", "00000000-0000-0000-0000-000000000001", "budget-example-hub-monthly"),
    ("Nonproduction", "00000000-0000-0000-0000-000000000002", "budget-example-platform-nonproduction-monthly"),
    ("Production", "00000000-0000-0000-0000-000000000003", "budget-workforce-production-monthly"),
)


def budget_item(label, subscription_id, budget_name):
    path = (
        f"/subscriptions/{subscription_id}/providers/Microsoft.Consumption/"
        f"budgets/{budget_name}"
    )
    query = {
        "version": "ARMEndpoint/1.0",
        "data": None,
        "headers": [],
        "method": "GET",
        "path": path,
        "urlParams": [{"key": "api-version", "value": "2024-08-01"}],
        "batchDisabled": False,
        "transformers": [
            {
                "type": "jsonpath",
                "settings": {
                    "tablePath": "$",
                    "columns": [
                        {"path": "$.properties.amount", "columnid": "Monthly budget", "columnType": "number"},
                        {"path": "$.properties.currentSpend.amount", "columnid": "Reported spend", "columnType": "number"},
                        {"path": "$.properties.currentSpend.unit", "columnid": "Currency", "columnType": "string"},
                        {"path": "$.properties.timePeriod.startDate", "columnid": "Period start", "columnType": "datetime"},
                    ],
                },
            }
        ],
    }
    return {
        "type": 3,
        "name": f"budget-{label.lower()}",
        "content": {
            "version": "KqlItem/1.0",
            "title": f"{label} — monthly budget and reported spend",
            "query": json.dumps(query, separators=(",", ":")),
            "queryType": 12,
            "size": 0,
            "visualization": "table",
        },
    }


def build():
    items = [
        {
            "type": 1,
            "name": "overview",
            "content": {
                "json": (
                    "# Workforce Services cost visibility\n"
                    "Monthly budget versus Azure's latest reported spend. Budgets trigger alerts; "
                    "they do not cap charges. Cost data can arrive hours after usage. "
                    "For daily trend and breakdowns, open **Cost Management → Cost analysis** "
                    "in each subscription and select the shared view "
                    "**Workforce Services cost visibility**. Its pivots show service, resource group, "
                    "and meter category."
                )
            },
        }
    ]
    items.extend(budget_item(*subscription) for subscription in SUBSCRIPTIONS)
    items.append(
        {
            "type": 1,
            "name": "interpretation",
            "content": {
                "json": (
                    "A blank row can indicate missing Cost Management permissions or delayed data; "
                    "it does not mean zero spend. Open each subscription's Cost analysis for "
                    "the authoritative breakdown. This workbook does not query Cost Management "
                    "Usage on every page load."
                )
            },
        }
    )
    data = {"version": "Notebook/1.0", "items": items, "isLocked": False, "fallbackResourceIds": ["Azure Monitor"]}
    return {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "resources": [
            {
                "type": "Microsoft.Insights/workbooks",
                "apiVersion": "2022-04-01",
                "name": WORKBOOK_ID,
                "location": "eastus2",
                "kind": "shared",
                "properties": {
                    "displayName": "Workforce Services cost visibility",
                    "category": "workbook",
                    "sourceId": "Azure Monitor",
                    "serializedData": json.dumps(data, separators=(",", ":")),
                },
                "tags": {
                    "environment": "hub",
                    "workload": "cost-visibility",
                    "owner": "workforce",
                    "managed_by": "arm-template",
                    "data_class": "internal",
                    "cost_center": "operations",
                },
            }
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(build(), indent=2) + "\n", encoding="utf-8")

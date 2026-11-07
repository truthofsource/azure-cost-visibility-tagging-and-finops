"""Create shared month-to-date Cost Analysis views for the three subscriptions.

The script creates only absent views. It never changes budgets, alert recipients,
or existing views. Use --apply after reviewing the default plan output.
"""

import argparse
import json
import shutil
import subprocess
import urllib.error
import urllib.request


VIEW_NAME = "workforce-cost-visibility"
SUBSCRIPTIONS = {
    "sub-example-hub-001": "budget-example-hub-monthly",
    "sub-example-nonprod-001": "budget-example-platform-nonproduction-monthly",
    "sub-example-prod-001": "budget-workforce-production-monthly",
}


def az_json(*args):
    command = shutil.which("az.cmd") or shutil.which("az")
    if not command:
        raise RuntimeError("Azure CLI is required")
    return json.loads(subprocess.check_output([command, *args, "-o", "json"], text=True))


def request_json(method, url, token, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return 404, None
        # Do not print response bodies; provider errors can include account data.
        raise RuntimeError(f"Azure {method} failed with HTTP {error.code}") from error


def view_body(subscription_id, budget_name):
    scope = f"subscriptions/{subscription_id}"
    return {
        "properties": {
            "displayName": "Workforce Services cost visibility",
            "scope": scope,
            "chart": "Area",
            "accumulated": "false",
            "metric": "ActualCost",
            "kpis": [
                {
                    "type": "Budget",
                    "enabled": True,
                    "id": f"/{scope}/providers/Microsoft.Consumption/budgets/{budget_name}",
                }
            ],
            "pivots": [
                {"type": "Dimension", "name": "ServiceName"},
                {"type": "Dimension", "name": "ResourceGroupName"},
                {"type": "Dimension", "name": "MeterCategory"},
            ],
            "query": {
                "type": "Usage",
                "timeframe": "MonthToDate",
                "dataSet": {
                    "granularity": "Daily",
                    "aggregation": {
                        "totalCost": {"name": "PreTaxCost", "function": "Sum"}
                    },
                    "sorting": [{"name": "UsageDate", "direction": "Ascending"}],
                },
            },
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    accounts = {row["name"]: row["id"] for row in az_json("account", "list")}
    token = az_json("account", "get-access-token", "--resource", "https://management.azure.com/")["accessToken"]
    for name, budget in SUBSCRIPTIONS.items():
        if name not in accounts:
            raise RuntimeError(f"subscription not available: {name}")
        subscription_id = accounts[name]
        url = (
            f"https://management.azure.com/subscriptions/{subscription_id}"
            f"/providers/Microsoft.CostManagement/views/{VIEW_NAME}"
            "?api-version=2025-03-01"
        )
        status, existing = request_json("GET", url, token)
        if status != 404:
            expected = view_body(subscription_id, budget)["properties"]
            actual = existing["properties"]
            for field in ("displayName", "scope", "chart", "metric", "kpis", "pivots"):
                if actual.get(field) != expected[field]:
                    raise RuntimeError(f"{name}: existing view differs in {field}; review it manually")
            if actual.get("query", {}).get("timeframe") != "MonthToDate":
                raise RuntimeError(f"{name}: existing view has a different time window")
            print(f"{name}: existing view {existing['name']}; unchanged")
            continue
        if not args.apply:
            print(f"{name}: would create shared Cost Analysis view {VIEW_NAME}")
            continue
        created_status, created = request_json(
            "PUT", url, token, view_body(subscription_id, budget)
        )
        print(f"{name}: created {created['name']} (HTTP {created_status})")


if __name__ == "__main__":
    main()

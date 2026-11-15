"""Evaluate fictional data and actual local template builders without cloud calls."""
from datetime import datetime,timezone
from pathlib import Path
import importlib.util,json
from finops_reference import budget_percentage,missing_tags,shutdown_plan,REQUIRED_TAGS
from build_cost_visibility_workbook import build
ROOT=Path(__file__).resolve().parents[1]
def demo():
    data=json.loads((ROOT/'data/fictional.json').read_text())
    for row in data['budgets']:
        row['percentage']=budget_percentage(row['reported'],row['budget'])
    for row in data['resources']:row['missing']=missing_tags(row['tags'])
    target='/subscriptions/00000000-0000-0000-0000-000000000002/resourceGroups/rg-example-lab/providers/Microsoft.Compute/virtualMachines/vm-example-lab'
    config={'enabled':False,'subscription':'fictional-nonproduction','allowlist':[target]}
    event={'kind':'Actual','percentage':100,'subscription':'fictional-nonproduction','resourceId':target}
    snapshot={'capturedAt':'2026-11-06T12:00:00Z','resourceId':target,'environment':'nonproduction','shared':False,'activeWork':False,'type':'Microsoft.Compute/virtualMachines'}
    now=datetime(2026,11,6,12,1,tzinfo=timezone.utc)
    scenarios=[('Default configuration',config,snapshot),('Fictional pilot; planning only',{**config,'enabled':True},snapshot),('Shared dependency',{**config,'enabled':True},{**snapshot,'shared':True}),('Active work',{**config,'enabled':True},{**snapshot,'activeWork':True})]
    data['shutdown']=[{'scenario':name,**shutdown_plan(event,c,s,now)} for name,c,s in scenarios]
    data['tags']=list(REQUIRED_TAGS);data['workbookResources']=len(build()['resources'])
    return data
if __name__=='__main__':print(json.dumps(demo(),indent=2))

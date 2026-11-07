import contextlib,importlib.util,io,json,sys,unittest
from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_cost_visibility_workbook import build
from finops_reference import budget_percentage,missing_tags,shutdown_plan,REQUIRED_TAGS
spec=importlib.util.spec_from_file_location('views',ROOT/'reference/ensure_cost_visibility_views.py');views=importlib.util.module_from_spec(spec);spec.loader.exec_module(views)

class Builders(unittest.TestCase):
    def test_workbook_only_creates_one_workbook(self):
        resources=build()['resources'];self.assertEqual([r['type'] for r in resources],['Microsoft.Insights/workbooks'])
    def test_three_panels_read_budgets_without_usage_query(self):
        items=json.loads(build()['resources'][0]['properties']['serializedData'])['items'];panels=[i for i in items if i['type']==3]
        self.assertEqual(len(panels),3)
        for panel in panels:
            q=json.loads(panel['content']['query']);self.assertEqual(q['method'],'GET');self.assertIn('/Microsoft.Consumption/budgets/',q['path']);self.assertNotIn('Microsoft.CostManagement/query',q['path'])
    def test_native_view_is_daily_actual_cost(self):
        p=views.view_body('fictional','budget-example')['properties'];self.assertEqual(p['metric'],'ActualCost');self.assertEqual(p['query']['timeframe'],'MonthToDate');self.assertEqual(p['query']['dataSet']['granularity'],'Daily')
        self.assertEqual({x['name'] for x in p['pivots']},{'ServiceName','ResourceGroupName','MeterCategory'})
    def test_existing_views_are_read_and_never_rewritten(self):
        accounts=[{'name':name,'id':'00000000-0000-0000-0000-000000000002'} for name in views.SUBSCRIPTIONS]
        calls=[]
        def request(method,url,token,body=None):
            self.assertEqual(method,'GET');calls.append(url)
            budget=list(views.SUBSCRIPTIONS.values())[len(calls)-1]
            return 200,{'name':'existing',**views.view_body(accounts[0]['id'],budget)}
        with patch.object(views,'az_json',side_effect=[accounts,{'accessToken':'fictional'}]),patch.object(views,'request_json',side_effect=request),patch.object(sys,'argv',['views']),contextlib.redirect_stdout(io.StringIO()):views.main()
        self.assertEqual(len(calls),3)
    def test_mismatched_view_fails_instead_of_overwriting(self):
        accounts=[{'name':name,'id':'fictional'} for name in views.SUBSCRIPTIONS]
        with patch.object(views,'az_json',side_effect=[accounts,{'accessToken':'fictional'}]),patch.object(views,'request_json',return_value=(200,{'properties':{'displayName':'Different'}})) as request,patch.object(sys,'argv',['views','--apply']):
            with self.assertRaisesRegex(RuntimeError,'differs'):views.main()
            self.assertEqual(request.call_count,1);self.assertEqual(request.call_args.args[0],'GET')
    def test_missing_spend_is_unknown_and_budget_can_be_exceeded(self):
        self.assertIsNone(budget_percentage(None,200));self.assertIsNone(budget_percentage(1,0));self.assertIsNone(budget_percentage('NaN',200));self.assertEqual(budget_percentage(230,200),'115.0')
    def test_tag_case_does_not_create_false_gap(self):
        self.assertEqual(missing_tags({key.upper():'value' for key in REQUIRED_TAGS}),[])
    def test_tag_gap_in_copied_workbook_is_visible(self):
        self.assertEqual(missing_tags(build()['resources'][0]['tags']),['criticality'])

class ShutdownPlan(unittest.TestCase):
    def setUp(self):
        self.target='fictional-vm';self.now=datetime(2026,11,6,12,1,tzinfo=timezone.utc)
        self.config={'enabled':True,'subscription':'np','allowlist':[self.target]}
        self.event={'kind':'Actual','percentage':100,'subscription':'np','resourceId':self.target}
        self.snapshot={'capturedAt':'2026-11-06T12:00:00Z','resourceId':self.target,'environment':'nonproduction','shared':False,'activeWork':False,'type':'Microsoft.Compute/virtualMachines'}
    def plan(self,c=None,e=None,s=None):return shutdown_plan(e or self.event,c or self.config,s or self.snapshot,self.now)
    def test_default_and_string_flags_stay_disabled(self):
        for flag in [False,'true',1,None]:self.assertEqual(self.plan(c={**self.config,'enabled':flag})['status'],'disabled')
    def test_valid_plan_is_still_review_only(self):
        p=self.plan();self.assertEqual(p['status'],'review_required');self.assertIs(p['execute'],False)
    def test_forecast_is_not_shutdown_authority(self):self.assertEqual(self.plan(e={**self.event,'kind':'Forecasted'})['status'],'review_only_threshold')
    def test_invalid_percentages_cannot_make_a_plan_eligible(self):
        for value in [float('nan'),float('inf'),True,'100']:
            self.assertEqual(self.plan(e={**self.event,'percentage':value})['status'],'review_only_threshold')
    def test_unknown_scope_and_targets_are_rejected(self):
        self.assertEqual(self.plan(e={**self.event,'subscription':'prod'})['status'],'wrong_scope');self.assertEqual(self.plan(e={**self.event,'resourceId':'other'})['status'],'not_allowlisted')
    def test_shared_and_production_are_protected(self):
        for extra in [{'shared':True},{'environment':'production'}]:self.assertEqual(self.plan(s={**self.snapshot,**extra})['status'],'protected_resource')
    def test_stale_busy_and_wrong_resource_type_are_rejected(self):
        self.assertEqual(self.plan(s={**self.snapshot,'capturedAt':'2026-11-05T12:00:00Z'})['status'],'stale_snapshot')
        for extra in [{'activeWork':True},{'type':'Microsoft.Storage/storageAccounts'}]:self.assertEqual(self.plan(s={**self.snapshot,**extra})['status'],'unsafe_or_busy')
    def test_logic_app_design_is_disabled_and_has_no_executor(self):
        template=json.loads((ROOT/'design/logic-app-shutdown-review.json').read_text());p=template['resources'][0]['properties'];self.assertEqual(p['state'],'Disabled');self.assertEqual({a['type'] for a in p['definition']['actions'].values()},{'Compose'})
if __name__=='__main__':unittest.main()

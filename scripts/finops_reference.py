"""New offline models for fictional cost/tag/shutdown examples; no Azure executor."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from math import isfinite

REQUIRED_TAGS=('environment','workload','owner','managed_by','data_class','criticality','cost_center')

def budget_percentage(reported, budget):
    # Missing data stays unknown; it is not converted into free usage.
    if reported is None or budget is None:return None
    try: cost,limit=Decimal(str(reported)),Decimal(str(budget))
    except InvalidOperation:return None
    if not cost.is_finite() or not limit.is_finite() or limit<=0:return None
    return str((cost/limit*100).quantize(Decimal('0.1')))

def missing_tags(tags):
    # Azure tag keys are case-insensitive; canonical spelling is still useful.
    normalized={k.casefold():v for k,v in tags.items()}
    return [key for key in REQUIRED_TAGS if key not in normalized or not isinstance(normalized[key],str) or not normalized[key].strip()]

def shutdown_plan(event,config,snapshot,now):
    # Inputs are a simulation, not authenticated authority or a production guard.
    if config.get('enabled') is not True:return {'status':'disabled','execute':False}
    if event.get('kind')!='Actual' or type(event.get('percentage')) not in (int,float) or not isfinite(event['percentage']) or event['percentage']<100:
        return {'status':'review_only_threshold','execute':False}
    if event.get('subscription')!=config.get('subscription'):
        return {'status':'wrong_scope','execute':False}
    try:
        captured=datetime.fromisoformat(snapshot['capturedAt'].replace('Z','+00:00'))
        age=(now-captured).total_seconds()
    except (ValueError,KeyError,TypeError):return {'status':'invalid_snapshot','execute':False}
    if age<0 or age>300:return {'status':'stale_snapshot','execute':False}
    requested=event.get('resourceId')
    if not isinstance(requested,str) or requested not in config.get('allowlist',[]):
        return {'status':'not_allowlisted','execute':False}
    if snapshot.get('resourceId')!=requested or snapshot.get('environment')!='nonproduction' or snapshot.get('shared') is not False:
        return {'status':'protected_resource','execute':False}
    if snapshot.get('type')!='Microsoft.Compute/virtualMachines' or snapshot.get('activeWork') is not False:
        return {'status':'unsafe_or_busy','execute':False}
    return {'status':'review_required','proposedAction':'deallocate_vm','resourceId':requested,'execute':False}

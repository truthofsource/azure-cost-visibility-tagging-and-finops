mock_provider "azurerm" {
  mock_data "azurerm_policy_definition_built_in" {
    defaults = { id = "/providers/Microsoft.Authorization/policyDefinitions/00000000-0000-0000-0000-000000000001" }
  }
}
run "no_controls_created_by_default" {
  command = plan
  assert {
    condition     = length(azurerm_consumption_budget_subscription.platform_monthly) == 0 && length(module.governance) == 0
    error_message = "The reference must default Off."
  }
}
run "preserve_budget_threshold_semantics" {
  command = plan
  variables { enabled = true }
  assert {
    condition     = toset([for n in azurerm_consumption_budget_subscription.platform_monthly[0].notification : "${n.threshold_type}:${n.threshold}"]) == toset(["Actual:50", "Actual:80", "Actual:100", "Forecasted:90"])
    error_message = "Alert labels do not replace the actual threshold type."
  }
  assert {
    condition     = alltrue([for n in azurerm_consumption_budget_subscription.platform_monthly[0].notification : try(length(n.contact_groups), 0) == 0])
    error_message = "This source must not silently activate an automation Action Group."
  }
}
run "seven_tag_keys_are_explicit" {
  command = plan
  assert {
    condition     = toset(keys(local.common_tags)) == toset(["environment", "workload", "owner", "managed_by", "data_class", "criticality", "cost_center"])
    error_message = "Preserve all seven common tag keys."
  }
}

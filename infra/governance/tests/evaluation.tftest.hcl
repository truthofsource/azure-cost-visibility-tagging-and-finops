mock_provider "azurerm" {
  mock_data "azurerm_policy_definition_built_in" {
    defaults = { id = "/providers/Microsoft.Authorization/policyDefinitions/00000000-0000-0000-0000-000000000001" }
  }
}
variables {
  subscription_id                   = "/subscriptions/00000000-0000-0000-0000-000000000002"
  allowed_locations_assignment_name = "audit-example-region"
  allowed_locations_display_name    = "Review example location"
  allowed_locations                 = ["eastus2"]
  required_tag_names                = ["environment", "workload", "owner", "managed_by", "data_class", "criticality", "cost_center"]
}
run "review_policy_does_not_enforce_or_remediate" {
  command = plan
  assert {
    condition     = azurerm_subscription_policy_assignment.audit_allowed_locations.enforce == false && alltrue([for a in azurerm_subscription_policy_assignment.audit_required_tags : a.enforce == false]) && length(azurerm_subscription_policy_assignment.audit_required_tags) == 7
    error_message = "The actual module evaluates compliance without enforcing the built-in effect."
  }
}

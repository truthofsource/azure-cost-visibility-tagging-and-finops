output "allowed_locations_assignment_id" {
  description = "Existing location-audit policy assignment ID."
  value       = azurerm_subscription_policy_assignment.audit_allowed_locations.id
}

output "required_tag_assignment_ids" {
  description = "Existing policy assignment IDs keyed by the original tag names."
  value       = { for name, assignment in azurerm_subscription_policy_assignment.audit_required_tags : name => assignment.id }
}

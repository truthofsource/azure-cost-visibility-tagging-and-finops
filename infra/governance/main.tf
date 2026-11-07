data "azurerm_policy_definition_built_in" "allowed_locations" {
  display_name = "Allowed locations"
}

data "azurerm_policy_definition_built_in" "require_tag_on_resources" {
  display_name = "Require a tag on resources"
}

resource "azurerm_subscription_policy_assignment" "audit_allowed_locations" {
  name                 = var.allowed_locations_assignment_name
  subscription_id      = var.subscription_id
  policy_definition_id = data.azurerm_policy_definition_built_in.allowed_locations.id
  display_name         = var.allowed_locations_display_name
  description          = "Audits resources that are not deployed to approved Azure regions."

  enforce = false

  parameters = jsonencode({
    listOfAllowedLocations = {
      value = var.allowed_locations
    }
  })
}

resource "azurerm_subscription_policy_assignment" "audit_required_tags" {
  for_each = toset(var.required_tag_names)

  name                 = "audit-required-tag-${replace(each.value, "_", "-")}"
  subscription_id      = var.subscription_id
  policy_definition_id = data.azurerm_policy_definition_built_in.require_tag_on_resources.id
  display_name         = "Audit required tag: ${each.value}"
  description          = "Audits resources that are missing the required '${each.value}' tag."

  enforce = false

  parameters = jsonencode({
    tagName = {
      value = each.value
    }
  })
}

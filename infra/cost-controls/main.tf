locals {
  common_tags = {
    environment = var.environment
    workload    = "platform"
    owner       = var.owner
    managed_by  = "terraform"
    data_class  = "internal"
    criticality = "medium"
    cost_center = var.cost_center
  }
}
module "governance" {
  count                             = var.enabled ? 1 : 0
  source                            = "../governance"
  subscription_id                   = var.subscription_scope
  allowed_locations_assignment_name = "audit-allowed-locations-example"
  allowed_locations_display_name    = "Review example resource locations"
  allowed_locations                 = var.allowed_locations
  required_tag_names                = keys(local.common_tags)
}
output "example_common_tags" { value = local.common_tags }

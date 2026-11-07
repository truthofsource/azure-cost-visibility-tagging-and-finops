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

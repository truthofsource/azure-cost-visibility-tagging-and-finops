variable "enabled" {
  type    = bool
  default = false
}

variable "subscription_scope" {
  type    = string
  default = "/subscriptions/00000000-0000-0000-0000-000000000002"
}

variable "budget_name" {
  type    = string
  default = "budget-example-monthly"
}

variable "monthly_budget_amount" {
  type    = number
  default = 200
}

variable "budget_alert_email" {
  type    = string
  default = "finops@example.invalid"
}

variable "environment" {
  type    = string
  default = "nonproduction"
}

variable "owner" {
  type    = string
  default = "platform-team"
}

variable "cost_center" {
  type    = string
  default = "operations"
}

variable "allowed_locations" {
  type    = list(string)
  default = ["eastus2"]
}

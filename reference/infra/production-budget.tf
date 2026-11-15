# The legacy dev root originally owned the shared production subscription's
# audit assignments. Production takes ownership before that root is retired.
module "governance" {
  source = "../../modules/governance"

  subscription_id                   = data.azurerm_subscription.current.id
  allowed_locations_assignment_name = "audit-allowed-locations-production"
  allowed_locations_display_name    = "Audit allowed locations for production platform"
  allowed_locations                 = var.allowed_locations
  required_tag_names                = var.required_tag_names
}

resource "azurerm_consumption_budget_subscription" "platform_monthly" {
  name            = "budget-workforce-production-monthly"
  subscription_id = data.azurerm_subscription.current.id

  amount     = var.monthly_budget_amount
  time_grain = "Monthly"

  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00Z", timestamp())
    end_date   = "2036-12-31T00:00:00Z"
  }

  notification {
    enabled        = true
    threshold      = 50
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = [var.budget_alert_email]
  }

  notification {
    enabled        = true
    threshold      = 80
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = [var.budget_alert_email]
  }

  notification {
    enabled        = true
    threshold      = 100
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = [var.budget_alert_email]
  }

  notification {
    enabled        = true
    threshold      = 90
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Forecasted"
    contact_emails = [var.budget_alert_email]
  }

  lifecycle {
    ignore_changes = [time_period]
  }
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "backstage" {
  count                 = var.enable_low_cost_vm ? 1 : 0
  virtual_machine_id    = azurerm_linux_virtual_machine.backstage[0].id
  location              = var.location
  enabled               = true
  daily_recurrence_time = var.backstage_vm_shutdown_time
  timezone              = "Central Standard Time"

  notification_settings {
    enabled = false
  }
}

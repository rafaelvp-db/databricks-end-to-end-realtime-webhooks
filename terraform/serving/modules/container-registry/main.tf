resource "azurerm_container_registry" "acr" {
  name                = var.registry_name
  resource_group_name = var.resource_group_name
  location            = var.registry_location
  sku                 = var.registry_sku
  admin_enabled       = var.registry_admin_enabled
}
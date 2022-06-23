resource "azurerm_role_assignment" "acr_push" {
  scope                = var.scope
  role_definition_name = "AcrPush"
  principal_id         = var.acr_push_principal_id
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = var.scope
  role_definition_name = "AcrPull"
  principal_id         = var.acr_pull_object_id
  skip_service_principal_aad_check = true
}
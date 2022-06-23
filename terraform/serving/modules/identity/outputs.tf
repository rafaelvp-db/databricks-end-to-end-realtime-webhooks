output "id" {
    value = azurerm_user_assigned_identity.id.id
}

output "principal_id" {
    value = azurerm_user_assigned_identity.id.principal_id
}

output "client_id" {
    value = azurerm_user_assigned_identity.id.client_id
}

output "tenant_id" {
    value = azurerm_user_assigned_identity.id.tenant_id
}
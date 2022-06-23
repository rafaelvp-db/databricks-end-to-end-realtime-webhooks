provider "azurerm" {
   features {}
}

data "azurerm_client_config" "current" {}

module "resource-group" {
  source              = "./modules/resource-group"
  rg_name             = var.resource_group_name
  rg_location         = var.location
}

module "aks" {
  source              = "./modules/aks"
  resource_group_name = module.resource-group.name
  location            = var.location
  log_analytics_ws_id = module.log-analytics.log_analytics_workspace_id
  dns_prefix          = var.aks_dns_prefix
  cluster_name        = var.aks_cluster_name
}

module "identity" {
  source              = "./modules/identity"
  resource_group_name = module.resource-group.name
  location            = var.location
  identity_name       = var.identity_name
}

module "keyvault" {
  source                  = "./modules/keyvault"
  name                    = var.kv_name
  sku_name                = var.kv_sku_name
  resource_group_name     = module.resource-group.name
  location                = var.location
  secret_kube_config      = module.aks.kube_config
  secret_kube_certificate = module.aks.client_certificate
}

module "log-analytics" {
  source                = "./modules/log-analytics"
  log_analytics_ws_name = var.log_analytics_ws_name
  resource_group_name   = module.resource-group.name
  location              = var.location
}

module "container-registry" {
  source              = "./modules/container-registry"
  resource_group_name = module.resource-group.name
  registry_location   = module.resource-group.location
  registry_name       = var.registry_name
  identity_pull       = module.aks.kubelet_identity
}

module "roles" {
  source                = "./modules/roles"
  scope                 = module.container-registry.id
  acr_pull_object_id    = module.aks.kubelet_identity
  acr_push_principal_id = data.azurerm_client_config.current.object_id
}
provider "azurerm" {
   features {}
}

module "resource-group" {
  source              = "./modules/resource-group"
  rg_name             = var.resource_group_name
  rg_location         = var.location
}

module "keyvault" {
  source              = "./modules/keyvault"
  name                = var.kv_name
  sku_name            = var.kv_sku_name
  resource_group_name = module.resource-group.name
  location            = var.location
  pat_token           = module.databricks.token_value
  db_host             = var.db_workspace_url
}

module "databricks" {
  source              = "./modules/databricks"
  workspace_url       = var.db_workspace_url
  lifetime_seconds    = var.db_lifetime_seconds
}

module "webhook" {
  source              = "./modules/webhook"
  trigger_url         = module.functions.function_url
  workspace_url       = var.db_workspace_url
  pat_token           = module.databricks.token_value
}

module "functions" {
  source              = "./modules/functions"
  resource_group_name = module.resource-group.name
  location            = var.location
  ado_pat_token = var.ado_pat_token
  ado_organization_url = var.ado_organization_url
  ado_project_name = var.ado_project_name
}

module "log-analytics" {
  source              = "./modules/log-analytics"
  resource_group_name = module.resource-group.name
  location            = var.location
}
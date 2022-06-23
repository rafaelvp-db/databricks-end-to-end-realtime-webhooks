resource "azurerm_application_insights" "func_application_insights" {
  name                = "func-application-insights"
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
}

resource "azurerm_storage_account" "safunctionsapp" {
  name                     = "mlflowsafunctionsapp"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "asp" {
  name                = "azure-functions-service-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Standard"
    size = "S1"
  }
}



resource "azurerm_function_app" "app" {
  name                       = "rvp-mlflow-webhook-function-app"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  app_service_plan_id        = azurerm_app_service_plan.asp.id
  storage_account_name       = azurerm_storage_account.safunctionsapp.name
  storage_account_access_key = azurerm_storage_account.safunctionsapp.primary_access_key
  version                    = "~3"
  os_type                    = "linux"

  site_config {
    linux_fx_version = "PYTHON|3.7"
    use_32_bit_worker_process = false
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python",
    ADO_PERSONAL_ACCESS_TOKEN = var.ado_pat_token,
    ADO_ORGANIZATION_URL = var.ado_organization_url,
    ADO_PROJECT_NAME = var.ado_project_name,
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.func_application_insights.instrumentation_key
  }

  depends_on = [azurerm_app_service_plan.asp, azurerm_storage_account.safunctionsapp]
}

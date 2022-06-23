terraform {
  required_providers {
    databricks = {
      source  = "databrickslabs/databricks"
      version = "0.5.1"
    }
  }
}

provider "databricks" {
  alias = "created_workspace" 
  host  = var.workspace_url
}

resource "databricks_token" "pat" {
  provider = databricks.created_workspace
  comment  = "Terraform Provisioning"
  lifetime_seconds = var.lifetime_seconds
}
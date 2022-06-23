variable "resource_group_name" {
  type        = string
  description = "Name of resource group into which Databricks will be deployed"
}

variable "location" {
  type        = string
  description = "Location in which Databricks will be deployed"
}

variable db_workspace_url {
  type = string
  description = "DB Workspace URL"
}

variable db_lifetime_seconds {
  type = number
  description = "DB PAT lifetime"
  default = null
}

variable kv_sku_name {
  type = string
  description = "SKU Name"
  default = "standard"
}

variable kv_name {
  type = string
  description = "KV Name"
}

variable ado_pat_token {
  type = string
  description = "Azure DevOps PAT Token"
}

variable ado_organization_url {
  type = string
  description = "Azure DevOps Org URL"
}

variable ado_project_name {
  type = string
  description = "Azure DevOps Project Name"
}
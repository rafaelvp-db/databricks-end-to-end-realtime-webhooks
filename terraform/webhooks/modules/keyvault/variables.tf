variable "pat_token" {
  type = string
  description = "Databricks PAT Token"
}

variable "db_host" {
  type = string
  description = "Databricks Host URL"
}

variable "resource_group_name" {
  type = string
  description = "Resource group name"
}

variable "location" {
  type = string
  description = "Location"
}

variable "sku_name" {
  type = string
  description = "SKU"
}

variable "name" {
  type = string
  description = "KV Name"
}
variable "resource_group_name" {
  type        = string
  description = "Name of resource group into which Databricks will be deployed"
}

variable "location" {
  type        = string
  description = "Location in which Databricks will be deployed"
}

variable "identity_name" {
  type = string
  description = "Identity name"
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

variable registry_name {
  type = string
  description = "ACR Registry Name"
}

variable aks_dns_prefix {
  type = string
  description = "AKS DNS Prefix"
}

variable aks_cluster_name {
  type = string
  description = "AKS Cluster Name"
}

variable log_analytics_ws_name {
  type = string
  description = "la-aks-mlflow-test"
}
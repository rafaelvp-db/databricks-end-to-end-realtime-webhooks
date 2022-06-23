variable "cluster_name" {
  type        = string
  description = "Name of AKS cluster"
}

variable "location" {
  type        = string
  description = "Location"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
}

variable "dns_prefix" {
  type        = string
  description = "DNS Prefix"
}

variable "log_analytics_ws_id" {
  type        = string
  description = "Log Analytics Workspace ID"
}
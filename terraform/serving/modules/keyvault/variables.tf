variable "secret_kube_config" {
  type = string
  description = "Kube Config"
}

variable "secret_kube_certificate" {
  type = string
  description = "Kube Certificate"
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
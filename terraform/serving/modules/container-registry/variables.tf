variable "registry_name" {
  type        = string
  description = "Name of container registry"
}

variable "registry_location" {
  type        = string
  description = "Location of container registry"
}

variable "registry_sku" {
  type        = string
  description = "SKU Type"
  default = "Premium"
}

variable "registry_admin_enabled" {
  type = bool
  description = "Admin enabled"
  default = false
}

variable "resource_group_name" {
  type = string
  description = "Resource group name"
}

variable "identity_pull" {
  type = string
  description = "Identity which will have pull permissions"
}

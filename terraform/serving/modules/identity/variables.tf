variable "resource_group_name" {
  type        = string
  description = "Name of resource group"
}

variable "location" {
  type        = string
  description = "Location"
}

variable "identity_name" {
  type        = string
  description = "Name of user managed identity"
}
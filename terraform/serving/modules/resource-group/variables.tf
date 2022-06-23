variable "rg_name" {
  type        = string
  description = "Name of resource group"
}

variable "rg_location" {
  type        = string
  description = "Location of resource group"
  default = "West Europe"
}

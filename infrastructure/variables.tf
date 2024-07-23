variable "env" {
  description = "Generic resource name"
  type = string

  validation {
    condition     = contains(["dev", "test", "prod"], var.env)
    error_message = "Environment must be one of 'dev', 'test', or 'prod'."
  }
}

variable "name" {
  description = "Generic resource name"
  type = string
}

variable "location" {
  description = "Azure location of the resources"
  type = string
  default = "Switzerland North"
}

variable "sp_os_type" {
  description = "Type of Operating System"
  type = string
}

variable "sp_sku_name" {
  description = "Azure Service Plan SKU-Size"
  type = string
}

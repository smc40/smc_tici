variable "environment" {
  description = "Generic resource name"
  type = string

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment must be one of 'dev', 'test', or 'prod'."
  }
}

variable "container_app_revision_mode" {
  description = "Revision mode of container app (Single or Multiple"
  type = string

  validation {
    condition     = contains(["Single", "Multiple"], var.container_app_revision_mode)
    error_message = "Environment must be one of 'dev', 'test', or 'prod'."
  }
}

variable "container_app_cpu" {
  description = "The amount of vCPU to allocate to the container"
  type = number
  default = 0.5
}

variable "container_app_memory" {
  description = "The amount of memory to allocate to the container"
  type = string
  default = "1Gi"
}

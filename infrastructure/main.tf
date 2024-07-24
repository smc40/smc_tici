locals {
  prefix = "smc"
  appname = "ticiapp"
  location = "Switzerland North"

  acr_sku = "Basic"

  tags = {
    env = var.environment
    createdBy = "Terraform"
  }
}


resource "azurerm_resource_group" "main" {
  name = "rg-${local.prefix}-${local.appname}-${var.environment}"
  location = local.location
  tags = local.tags
}

resource "azurerm_container_registry" "main" {
  name = "acr${local.prefix}${local.appname}${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location = local.location
  sku = local.acr_sku
  admin_enabled = false
}

resource "azurerm_container_app_environment" "main" {
  name = "acae-${local.prefix}-${local.appname}-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location = local.location
}

resource "azurerm_container_app" "main" {
  name                         = "aca-${local.prefix}-${local.appname}-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name = azurerm_resource_group.main.name
  revision_mode                = var.container_app_revision_mode

  template {
    container {
      name   = local.appname
      image = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"  # Placeholder image
      cpu    = var.container_app_cpu
      memory = var.container_app_memory
    }
  }

  ingress {
    external_enabled = true
    target_port      = 80
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

# Output the Container Registry Login Server URL
# output "container_registry_login_server" {
#   value = azurerm_container_registry.main.login_server
# }

# Output the Application URL (Fully qualified domain name)
output "application_url" {
  value = azurerm_container_app.main.latest_revision_fqdn
}
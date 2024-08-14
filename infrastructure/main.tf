data "azurerm_resource_group" "main" {
  name = local.resource_group
}

resource "azurerm_container_app_environment" "main" {
  name                  = "acae-${local.prefix}-${local.appname}-${var.environment}"
  resource_group_name   = data.azurerm_resource_group.main.name
  location              = local.location
}

resource "azurerm_container_app" "main" {
  name                          = "aca-${local.prefix}-${local.appname}-${var.environment}"
  container_app_environment_id  = azurerm_container_app_environment.main.id
  resource_group_name           = data.azurerm_resource_group.main.name
  revision_mode                 = var.container_app_revision_mode

  template {
    container {
      name    = local.appname
      image   = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"  # Placeholder image
      cpu     = var.container_app_cpu
      memory  = var.container_app_memory
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

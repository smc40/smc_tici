locals {
  prefix = "smc"
  appname = "tici-app"
  location = "Switzerland North"

  acr_sku = "Basic"

  tags = {
    env = var.environment
    createdBy = "Terraform"
  }
}


resource "azurerm_resource_group" "rg" {
  name = "rg-${local.prefix}-${local.appname}-${var.environment}"
  location = local.location
  tags = local.tags
}

resource "azurerm_container_registry" "acr" {
  name = "acr-${local.prefix}-${local.appname}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location = local.location
  sku = local.acr_sku
  admin_enabled = false
}

resource "azurerm_container_app_environment" "acae" {
  name = "acae-${local.prefix}-${local.appname}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location = local.location
}

resource "azurerm_container_app" "aca" {
  container_app_environment_id = azurerm_container_app_environment.acae.id
  name                         = "aca-${local.prefix}-${local.appname}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  revision_mode                = var.container_app_revision_mode

  template {
    container {
      name   = local.appname
      image  = "${azurerm_container_registry.acr.login_server}/${local.appname}:latest"
      cpu    = "0.5"
      memory = "1.0Gi"
    }
  }

}

# Output the Container Registry Login Server URL
output "container_registry_login_server" {
  value = azurerm_container_registry.acr.login_server
}
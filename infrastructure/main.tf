resource "azurerm_resource_group" "rg" {
  name = "rg-smc-${var.name}-${var.env}" 
  location = var.location
}

resource "azurerm_service_plan" "sp" {
  name = "sp-${var.name}-${var.env}"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  os_type = var.sp_os_type
  sku_name = var.sp_sku_name
}

resource "azurerm_app_service" "as" {
  name = "as-${var.name}-${var.env}"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  service_plan_id = azurerm_service_plan.sp.id

  site_config {
    linux_fx_version = "PYTHON|3.8"
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"      = "true"
  }
}

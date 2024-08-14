locals {
  prefix = "smc"
  appname = "ticiapp"
  location = "Switzerland North"
  resource_group = "rg-${local.prefix}-${local.appname}-${var.environment}"

  acr_sku = "Basic"

  tags = {
    env = var.environment
    createdBy = "Terraform"
  }
}

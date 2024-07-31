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

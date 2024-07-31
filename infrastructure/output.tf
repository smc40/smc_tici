# Output the Container Registry Login Server URL
output "container_registry_login_server" {
  value = azurerm_container_registry.main.login_server
}

# Output the Application URL (Fully qualified domain name)
output "application_url" {
  value = azurerm_container_app.main.latest_revision_fqdn
}

# Output the Application URL (Fully qualified domain name)
output "application_url" {
  value = azurerm_container_app.main.latest_revision_fqdn
}

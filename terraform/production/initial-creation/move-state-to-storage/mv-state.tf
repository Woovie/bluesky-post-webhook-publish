terraform {
  backend "azurerm" {
    resource_group_name   = "tfstate-rg-prod"
    storage_account_name  = "tfstate-storage-prod"
    container_name        = "tfstate-container-prod"
    key                   = "terraform.tfstate"
  }
}
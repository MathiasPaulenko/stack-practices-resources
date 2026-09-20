# Azure Basics — Companion Resources

Runnable companion for the guide **[Azure Basics — Core Services for Developers](https://stackpractices.com/guides/azure-basics-guide/)** on StackPractices.

## Files

| File | Purpose |
|---|---|
| `azure-bootstrap.sh` | Provisions a complete dev environment with the Azure CLI: resource group (tagged), storage account + uploads container, App Service plan + web app, Key Vault with a sample secret, system-assigned managed identity with a Key Vault RBAC grant, and Application Insights. |

## Quick start

```bash
az login
az account set --subscription "My Subscription"

export SQL_ADMIN_PASSWORD="$(openssl rand -base64 24)"
chmod +x azure-bootstrap.sh
RG=rg-myapp-dev LOCATION=eastus APP_NAME=my-webapp-123 ./azure-bootstrap.sh
```

## Teardown

```bash
az group delete --name rg-myapp-dev --yes --no-wait
```

Deleting the resource group removes every resource inside it — including the Key Vault (which stays recoverable for 90 days under soft-delete/purge protection).

## Notes

- Storage account and Key Vault names must be globally unique; the script generates suffixes with `$RANDOM`. Override with `STORAGE_NAME=` / `KV_NAME=` if you get a name conflict.
- `SQL_ADMIN_PASSWORD` is required so no credential is ever hardcoded in the script.
- Review the guide's compute decision table before scaling past the B1 plan — App Service bills per plan, not per request.

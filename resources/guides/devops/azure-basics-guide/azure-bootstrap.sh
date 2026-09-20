#!/usr/bin/env bash
# azure-bootstrap.sh — provision a minimal Azure dev environment from the guide
# "Azure Basics — Core Services for Developers" (stackpractices.com/guides/azure-basics-guide/)
#
# Creates: resource group, storage account, App Service plan + web app,
# Key Vault, and a system-assigned managed identity on the web app.
#
# Prerequisites:
#   - Azure CLI installed (winget install Microsoft.AzureCLI / brew install azure-cli)
#   - az login completed against the right subscription
#
# Usage:
#   chmod +x azure-bootstrap.sh
#   RG=rg-myapp-dev LOCATION=eastus APP_NAME=my-webapp-123 ./azure-bootstrap.sh
#
# Teardown: az group delete --name "$RG" --yes --no-wait

set -euo pipefail

RG="${RG:-rg-myapp-dev}"
LOCATION="${LOCATION:-eastus}"
APP_NAME="${APP_NAME:-my-webapp-123}"
PLAN_NAME="${PLAN_NAME:-plan-myapp}"
STORAGE_NAME="${STORAGE_NAME:-mystorage$RANDOM}"   # must be globally unique, 3-24 lowercase alnum
KV_NAME="${KV_NAME:-kv-myapp-$RANDOM}"            # must be globally unique
SQL_ADMIN_PASSWORD="${SQL_ADMIN_PASSWORD:?Set SQL_ADMIN_PASSWORD before running}"

echo "==> Resource group: $RG ($LOCATION)"
az group create --name "$RG" --location "$LOCATION" --output table

echo "==> Tags for cost attribution"
az group update --name "$RG" --set tags.env=dev tags.team=myteam --output none

echo "==> Storage account: $STORAGE_NAME"
az storage account create \
  --name "$STORAGE_NAME" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --sku Standard_LRS \
  --output table
az storage container create \
  --name uploads \
  --account-name "$STORAGE_NAME" \
  --output table

echo "==> App Service plan (B1, Linux) + web app: $APP_NAME"
az appservice plan create \
  --name "$PLAN_NAME" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --sku B1 \
  --is-linux \
  --output table
az webapp create \
  --resource-group "$RG" \
  --plan "$PLAN_NAME" \
  --name "$APP_NAME" \
  --runtime "NODE|18-lts" \
  --output table

echo "==> Key Vault: $KV_NAME (soft-delete + purge protection)"
az keyvault create \
  --name "$KV_NAME" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --enable-purge-protection true \
  --output table
az keyvault secret set \
  --vault-name "$KV_NAME" \
  --name "DbPassword" \
  --value "$SQL_ADMIN_PASSWORD" \
  --output none

echo "==> Managed identity on $APP_NAME"
IDENTITY_PRINCIPAL=$(az webapp identity assign \
  --name "$APP_NAME" \
  --resource-group "$RG" \
  --query principalId -o tsv)
echo "    principalId: $IDENTITY_PRINCIPAL"

echo "==> Grant Key Vault Secrets User to the managed identity"
KV_SCOPE=$(az keyvault show --name "$KV_NAME" --query id -o tsv)
az role assignment create \
  --assignee-object-id "$IDENTITY_PRINCIPAL" \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" \
  --scope "$KV_SCOPE" \
  --output table

echo "==> Application Insights"
az monitor app-insights component create \
  --app "${APP_NAME}-insights" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --output table 2>/dev/null || echo "    (extension azure-cli-telemetry may be required)"

echo
echo "Done. Next steps:"
echo "  - Deploy code: az webapp up --name $APP_NAME --resource-group $RG"
echo "  - Set a budget alert in Cost Management before leaving this running"
echo "  - Teardown everything: az group delete --name $RG --yes --no-wait"

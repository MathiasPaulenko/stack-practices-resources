# Create resource group
az group create --name my-rg --location eastus

# Create storage account (required by Functions)
az storage account create --name mystorageacct --resource-group my-rg --sku Standard_LRS

# Create the function app
az functionapp create \
  --name my-function-app \
  --resource-group my-rg \
  --storage-account mystorageacct \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --consumption-plan-location eastus

# Deploy
func azure functionapp publish my-function-app

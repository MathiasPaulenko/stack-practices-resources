# Premium plan keeps instances warm; always-ready instances never scale to zero
az functionapp create --name api-func --resource-group rg \
  --consumption-plan-location eastus --runtime python --functions-version 4 \
  --plan my-premium-plan --min-instances 2

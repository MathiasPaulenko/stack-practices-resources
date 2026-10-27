# Install Azure Functions Core Tools
# macOS: brew tap azure/functions && brew install azure-functions-core-tools@4
# Windows: winget install Microsoft.AzureFunctionsCoreTools

# Create a new function app (v2 model)
func init MyFunctionApp --python
cd MyFunctionApp

# Add an HTTP-triggered function
func new --name HttpGetUser --template "HTTP trigger" --authlevel function

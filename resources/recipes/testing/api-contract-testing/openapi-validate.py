# Provider-driven contract check: validate the spec, then validate a live response.
# Requires: pip install openapi-spec-validator openapi-core requests
import requests
from openapi_core import Config, OpenAPI
from openapi_spec_validator import validate_spec

spec = requests.get("https://api.example.com/openapi.json", timeout=10).json()

# 1. The spec itself must be a valid OpenAPI document.
validate_spec(spec)

# 2. Validate a real response against the spec at runtime.
openapi = OpenAPI(spec, config=Config())
response = requests.get("https://api.example.com/users/123", timeout=10)

result = openapi.unmarshal_response(
    requests.Request("get", "https://api.example.com/users/123"),
    response,
)
result.raise_for_errors()
print("Response conforms to the OpenAPI spec.")

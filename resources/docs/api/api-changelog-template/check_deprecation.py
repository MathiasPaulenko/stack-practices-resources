import requests

response = requests.get("https://api.example.com/v1/orders", headers={
    "Authorization": "Bearer token123"
})

if response.headers.get("Deprecation") == "true":
    sunset = response.headers.get("Sunset", "unknown date")
    link = response.headers.get("Link", "")
    print(f"WARNING: This endpoint is deprecated. Sunset: {sunset}")
    print(f"Migration guide: {link}")

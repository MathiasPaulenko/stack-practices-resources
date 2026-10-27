const response = await fetch("https://api.example.com/v1/orders", {
  headers: { Authorization: "Bearer token123" }
});

const deprecation = response.headers.get("Deprecation");
if (deprecation === "true") {
  const sunset = response.headers.get("Sunset");
  const link = response.headers.get("Link");
  console.warn(`Endpoint deprecated. Sunset: ${sunset}`);
  console.warn(`Migration guide: ${link}`);
}

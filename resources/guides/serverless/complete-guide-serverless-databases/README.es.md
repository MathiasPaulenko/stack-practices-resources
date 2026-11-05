# Guía Completa de Bases de Datos Serverless — Ejemplos compañeros

Compañero de [Guía Completa de Bases de Datos Serverless](https://stackpractices.com/es/guides/complete-guide-serverless-databases/).

- `dynamodb_example.js` — servicio de pedidos con diseño de claves por patrón de acceso (Query en partition key, sin Scan).
- `lambda_warm_connection.js` — el patrón de reutilización de conexión caliente: inicializa el cliente pg fuera del handler de Lambda.

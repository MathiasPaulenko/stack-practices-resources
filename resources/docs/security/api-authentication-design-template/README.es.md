# Plantilla de Diseño de Autenticación de API

Artefactos ejecutables de https://stackpractices.com/es/docs/api-authentication-design-template/

-  — emisión de access token RS256 + refresh token opaco
-  — validación JWT con JWKS
-  — flujo OAuth2 Authorization Code + PKCE
-  — solicitud de token servicio a servicio
-  — endpoint Flask de renovación con rotación y detección de reuso
-  — blocklist de revocación por jti en Redis

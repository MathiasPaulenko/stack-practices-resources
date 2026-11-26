# Checklist de Revisión de Código Segura

Checklist lista para producción para revisar código antes de cada release. Marca cada ítem; lo que quede sin marcar es un hallazgo a documentar o corregir.

## Entrada

- [ ] Validación de esquema en cada payload (zod `safeParse`, pydantic, Bean Validation)
- [ ] Sanitización de strings donde se renderiza HTML (DOMPurify o equivalente)
- [ ] Queries parametrizadas en todo — cero SQL concatenado con strings
- [ ] Subidas de archivo: límite de tamaño, detección MIME real, fuera del web root

## Autenticación y Autorización

- [ ] Token de auth verificado en cada petición (sin "el gateway ya lo hace")
- [ ] RBAC + scope comprobado por recurso, no por grupo de rutas
- [ ] Propiedad verificada — el usuario solo toca sus propios objetos (check IDOR)
- [ ] Rate limiting en endpoints de login, registro y reset
- [ ] Contraseñas con bcrypt/Argon2id (factor de coste documentado)

## Salida

- [ ] Sin stack traces ni internals en respuestas de error
- [ ] Sin campos sensibles en respuestas de API (capa DTO/mapping)
- [ ] Headers de seguridad configurados (CSP, frame-ancestors, nosniff)

## Sesión

- [ ] Expiración de token documentada y corta (15–60 min en access tokens)
- [ ] Rotación de refresh tokens implementada
- [ ] El logout invalida el token de verdad en servidor

## Logging

- [ ] Sin secretos, tokens ni PII en logs (redacción a nivel de logger)
- [ ] Log de auditoría de acciones críticas Y de intentos no autorizados

## Dependencias

- [ ] Escaneo de dependencias en CI (`npm audit`, `pip-audit`, `cargo audit`, Snyk)
- [ ] Escaneo de secretos en CI (gitleaks, trufflehog)
- [ ] Lockfile commiteado; sin versiones flotantes `latest`

## Configuración

- [ ] Modo producción forzado (`NODE_ENV=production` o equivalente)
- [ ] CORS restringido a orígenes conocidos
- [ ] TLS 1.2+ obligatorio; HSTS activado

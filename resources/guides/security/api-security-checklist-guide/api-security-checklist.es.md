# Checklist de Seguridad de APIs — Lista para Producción (40 items)

> Companion de la [Guía Checklist de Seguridad de APIs](https://stackpractices.com/es/guides/api-security-checklist-guide/)
> Imprime este archivo o cópialo en tu issue tracker. Marca cada casilla antes de ir a producción.

## Autenticación

- [ ] JWT con RS256 (no HS256) cuando más de un servicio verifica tokens
- [ ] Expiración de token: 15 min access, 7 días refresh
- [ ] Refresh token rotation en cada uso
- [ ] MFA para endpoints admin
- [ ] Rate limiting en login: 5 intentos, luego lock 15 min
- [ ] No exponer token en URL (usar header Authorization)
- [ ] Logout invalida token (Redis denylist vía `jti`)
- [ ] Password policy: min 12 chars, reglas de complejidad

## Autorización

- [ ] RBAC: roles user / admin / super_admin
- [ ] Verificar ownership en cada petición (anti-IDOR)
- [ ] Scope por recurso: user solo accede a sus datos
- [ ] Denegar por defecto, permitir explícitamente
- [ ] No auto-increment IDs (usar UUID v4 o v7)
- [ ] Devolver 404 (no 403) para recursos que el llamador no posee

## Validación de Entrada

- [ ] Schema validation (Zod / pydantic) en cada endpoint
- [ ] Límite de tamaño de payload (max 1 MB)
- [ ] Sanitización de strings (no HTML injection)
- [ ] Queries parametrizadas (anti-SQL injection)
- [ ] No eval / exec con input de usuario
- [ ] File upload: validar tipo, tamaño, contenido
- [ ] Rechazar campos inesperados (schema estricto — previene mass assignment)

## Output

- [ ] No exponer stack traces en producción
- [ ] DTO mapping: no exponer campos internos
- [ ] Headers de seguridad: X-Content-Type-Options, X-Frame-Options, CSP, HSTS
- [ ] No exponer versión del server / framework
- [ ] Rate limiting global: 100 req/min por usuario
- [ ] Formato de error RFC 7807 Problem Details

## Transporte

- [ ] TLS 1.3 obligatorio (no TLS 1.0 / 1.1)
- [ ] Redirect HTTP a HTTPS
- [ ] HSTS: max-age=31536000; includeSubDomains
- [ ] Certificate pinning (mobile apps)

## Configuración

- [ ] CORS: origin estricto, no wildcard
- [ ] NODE_ENV=production (o equivalente)
- [ ] Secrets en Secrets Manager (no .env en prod)
- [ ] Helmet() configurado (Node.js) o headers de seguridad equivalentes
- [ ] Compression con Brotli (no gzip para evitar BREACH)

## Logging y Monitoreo

- [ ] Audit log de acciones críticas
- [ ] No loggear secrets, passwords, tokens, PII
- [ ] Alertas de intentos de auth fallidos
- [ ] Alertas de rate limit excedido
- [ ] SIEM integration (ELK + alerting)
- [ ] Correlation ID en cada petición

## Dependencias

- [ ] npm audit en CI (--audit-level=high)
- [ ] Dependabot o Snyk configurado
- [ ] Lockfile commiteado (package-lock.json)
- [ ] License check en CI

## CI/CD

- [ ] SAST (semgrep) en pipeline
- [ ] DAST (OWASP ZAP) en staging
- [ ] Container scan (Trivy) en build
- [ ] Secret scan (git-secrets) en pre-commit
- [ ] Code review obligatorio (1 approver min)

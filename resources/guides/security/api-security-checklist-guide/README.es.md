# Checklist de Seguridad de APIs — Recursos Companion

Companion de la [Guía Checklist de Seguridad de APIs](https://stackpractices.com/es/guides/api-security-checklist-guide/) en StackPractices.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `api-security-checklist.md` | Checklist imprimible de 40 items para producción (inglés) |
| `api-security-checklist.es.md` | Checklist imprimible de 40 items para producción (español) |
| `helmet-config-example.js` | Configuración de Helmet lista para producción para APIs Express |
| `jwt-sign-example.js` | Firma JWT RS256 con rotación de claves vía header `kid` |

## Uso

1. Copia `api-security-checklist.es.md` en tu issue tracker o imprímelo.
2. Marca cada casilla antes de desplegar una API a producción.
3. Usa `helmet-config-example.js` como punto de partida para los headers de seguridad de Express.
4. Usa `jwt-sign-example.js` como referencia para firma JWT RS256 con rotación de claves.

## Fuentes

- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7807 — Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
- [Documentación de Helmet.js](https://helmetjs.github.io/)

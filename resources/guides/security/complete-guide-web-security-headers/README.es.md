# Guía completa de cabeceras de seguridad web — Ejemplos

Companion ejecutable de la guía de StackPractices
[Guía completa de cabeceras de seguridad web](https://stackpractices.com/es/guides/complete-guide-web-security-headers/).

Proyecto autocontenido de Express + Helmet que reproduce la configuración del servidor de la guía y la verifica con tests:

- `src/app.js` — helmet con las directivas CSP de la guía (`default-src 'self'`, `frame-ancestors 'none'`, `object-src 'none'`), HSTS con `includeSubDomains` + `preload`, `X-Frame-Options: DENY`, política de referrer `strict-origin-when-cross-origin` y COOP/CORP. Incluye ambos endpoints de reportes de violaciones: el `report-uri` heredado (`application/csp-report`) y la Reporting API moderna (`application/reports+json`).
- `src/server.js` — escucha en `PORT` o `3000`.
- `tests/headers.test.js` — aserciones de supertest que verifican que cada cabecera llega en las respuestas, que el CSP contiene las directivas esperadas y nunca `unsafe-inline`/`unsafe-eval`, que las respuestas de API llevan la misma política y que ambos endpoints de reportes devuelven 204.

## Ejecutar

```bash
npm install
npm start          # sirve en http://localhost:3000
npx vitest run     # verifica todas las cabeceras y endpoints de reportes
```

Requiere Node 20+. `.github/workflows/test.yml` corre la misma suite en CI.

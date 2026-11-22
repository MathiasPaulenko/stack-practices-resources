# Plugin de Seguridad ESLint — Companion

Código companion de la receta [Reglas de Seguridad en Node.js con ESLint](https://stackpractices.com/es/recipes/nodejs-eslint-security-plugin/).

## Qué incluye

- `eslint.config.js` — config flat con `eslint-plugin-security` ajustada por severidad (`error` para eval/child_process/ReDoS, `warn` para rutas no literales, `off` para `detect-object-injection`), más una variante relajada para `test/`.
- `vulnerable.js` — un servidor HTTP deliberadamente inseguro para que el plugin tenga hallazgos reales (path traversal, ReDoS, eval, `Buffer` deprecado, aleatoriedad débil, shell injection).
- `fixed.js` — los mismos endpoints reescritos para reportar cero hallazgos.
- `eslint-security.yml` — gate de GitHub Actions que corre el linter y rompe el build ante cualquier `security/*` nuevo en `error`.
- `package.json` — dependencias de desarrollo mínimas y scripts de lint.

## Probarlo

```bash
npm install
npx eslint vulnerable.js   # ~6 hallazgos de seguridad
npx eslint fixed.js        # limpio
```

Copia `eslint-security.yml` en `.github/workflows/` para aplicar el gate en CI.

Versión en inglés: [README.md](./README.md)

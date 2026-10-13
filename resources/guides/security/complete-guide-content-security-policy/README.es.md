# Content Security Policy — Archivos complementarios

Kit ejecutable de CSP para la guía
[Content Security Policy: cabeceras CSP, nonces, hashes](https://stackpractices.com/es/guides/complete-guide-content-security-policy/):
middleware de nonce por request, endpoint de reportes de violaciones,
config de helmet y el patrón de middleware de Next.js.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `app.ts` | App de demostración en Express — conecta el endpoint de reportes, la cabecera `Reporting-Endpoints` y el middleware de nonce; sirve una página con un script inline permitido y otro bloqueado. |
| `csp-nonce-middleware.ts` | Genera un nonce con `crypto.randomBytes` por request, lo guarda en `res.locals.nonce` y escribe la cabecera CSP enforcing. Incluye la variante `Report-Only` para la fase de descubrimiento. |
| `csp-report-endpoint.ts` | POST `/api/csp-reports` — acepta payloads de `application/reports+json` (lotes de la Reporting API) y de `application/csp-report` (legado `report-uri`) y los normaliza. |
| `helmet-csp.ts` | La misma política expresada como objeto de directivas de `helmet.contentSecurityPolicy`, con funciones de nonce que leen `res.locals.nonce`. |
| `nextjs-middleware.ts` | `middleware.ts` de Next.js App Router — genera el nonce, escribe la cabecera CSP y lo reenvía por `x-nonce`. Snippet de referencia (requiere un proyecto Next.js). |
| `nextjs-layout.tsx` | `app/layout.tsx` — lee `x-nonce` con `headers()` y lo pasa a `<Script nonce>`. Snippet de referencia (requiere un proyecto Next.js). |

## Ejecutar

```bash
npm install
npm start        # app de demo en http://localhost:3000
```

Abrí la página y mirá DevTools: el script inline con nonce se ejecuta y
el que no lo lleva queda bloqueado y reportado. Posteá un payload de
violación a `http://localhost:3000/api/csp-reports` para ver cómo el
endpoint acepta los dos formatos:

```bash
# Formato Reporting API (array de reportes)
curl -X POST http://localhost:3000/api/csp-reports \
  -H "Content-Type: application/reports+json" \
  -d '[{"type":"csp-violation","body":{"document-uri":"http://localhost:3000/","blocked-uri":"inline","effective-directive":"script-src-elem"}}]'

# Formato legado report-uri
curl -X POST http://localhost:3000/api/csp-reports \
  -H "Content-Type: application/csp-report" \
  -d '{"csp-report":{"document-uri":"http://localhost:3000/","blocked-uri":"inline","violated-directive":"script-src"}}'
```

## Notas

- El nonce debe ser impredecible (CSPRNG), único por respuesta, y la
  página no debe servirse como HTML cacheado compartido.
- `'strict-dynamic'` permite que los scripts con nonce carguen sus
  propias dependencias sin mantener una lista de CDNs; los navegadores
  sin soporte caen a la lista común.
- Los archivos de Next.js son snippets de referencia — soltalos en un
  proyecto App Router; están excluidos del `tsconfig.json` porque
  necesitan `next` como dependencia.

# Plantilla de Aviso de Deprecación de API — Código complementario

Recursos complementarios de [Plantilla de Aviso de Deprecación de API](https://stackpractices.com/es/docs/api-deprecation-notice-template/)
(EN: [API Deprecation Notice Template](https://stackpractices.com/docs/api-deprecation-notice-template/)).

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `notice/deprecation-notice-template.md` | La plantilla de aviso lista para copiar: resumen del cambio, antes/después, pasos de migración, cronograma, contactos de soporte, excepciones |
| `middleware/express.js` | Middleware de Express que emite los headers `Deprecation`, `Sunset` y `Link` en rutas deprecadas |
| `middleware/flask.py` | El mismo middleware como hooks `before_request` / `after_request` de Flask |
| `tracking/deprecation-traffic.sql` | Consulta SQL con el volumen de requests por endpoint deprecado por cliente |
| `tracking/alert-rule.yaml` | Alerta de Prometheus que se dispara cuando un cliente de alto tráfico aún no ha migrado |

## Uso

1. Copia `notice/deprecation-notice-template.md`, rellena los `<placeholders>` y envíalo a los consumidores en T-90.
2. Monta el middleware de tu stack para que los endpoints deprecados se autodenuncien vía headers de respuesta.
3. Ejecuta la consulta SQL (o la alerta de Prometheus) semanalmente para encontrar consumidores que no han empezado a migrar.
4. Sigue el plan de comunicación T-90 → T-0 de la página principal; en el retiro la versión antigua retorna `410 Gone`.

## Licencia

MIT — ver la raíz del repositorio.

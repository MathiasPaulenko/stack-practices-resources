# Gestión del Ciclo de Vida de APIs — Recursos complementarios

Archivos complementarios de la [Plantilla del Ciclo de Vida de APIs](https://stackpractices.com/es/docs/api-lifecycle-management-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `api-lifecycle-checklist.md` | Markdown | Checklist maestro: metadatos, deprecación, versionado y cierre |
| `migration-guide-template.md` | Markdown | Plantilla de guía de migración con antes/después y formato de error RFC 7807 |
| `deprecation-notice-example.md` | Markdown | Aviso de deprecación rellenado listo para adaptar y enviar a consumidores |
| `sunset-readiness-check.py` | Python | Verificación de tráfico cero contra Prometheus vía datasource proxy de Grafana |

## Inicio rápido

### 1. Copia el checklist maestro

```bash
cp api-lifecycle-checklist.md mi-api-lifecycle.md
```

Edita `mi-api-lifecycle.md` y reemplaza `<API Name>`, versiones y valores de ejemplo con los datos de tu API.

### 2. Adapta la guía de migración y el aviso

Copia `migration-guide-template.md` por cada cambio incompatible y `deprecation-notice-example.md` por cada anuncio. Mantén las mismas fechas en changelog, portal, email y los headers `Deprecation`/`Sunset`.

### 3. Ejecuta la verificación de cierre

```bash
pip install requests
export GRAFANA_URL=https://grafana.example.com
export GRAFANA_TOKEN=<service-account-token>
python sunset-readiness-check.py
```

Código de salida `0` = la versión deprecada sirvió tráfico cero durante 7 días consecutivos; `1` = no está lista; `2` = falta configuración.

## Headers de Deprecación/Sunset

Emite en cada respuesta de un endpoint deprecado ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745), [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)):

```http
Deprecation: @1789430400
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Link: <https://api.example.com/v3/users>; rel="successor-version",
      <https://api.example.com/docs/deprecation-notice>; rel="deprecation"
```

## Referencias

- [RFC 9745 — The Deprecation HTTP Header Field](https://www.rfc-editor.org/rfc/rfc9745)
- [RFC 8594 — The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594)
- [RFC 7807 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807)
- [Semantic Versioning 2.0.0](https://semver.org/)

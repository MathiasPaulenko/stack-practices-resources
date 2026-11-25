# Checklist de Pruebas de Regresión — Companion

Archivo companion de la página del [Checklist de Pruebas de Regresión](https://stackpractices.com/es/docs/regression-test-checklist/).

## Descripción

El template Markdown crudo de la página, listo para copiar a tu propio repo. Cubre comprobaciones pre-deploy (CI, calidad de código, entorno, comunicación), comprobaciones de despliegue, smoke tests post-deploy (recorridos de usuario, salud de la API, infraestructura, monitoreo), pruebas de regresión específicas por feature, verificación de rollback y sign-off.

## Estructura

```text
regression-test-checklist.md      # El template completo con valores de ejemplo (EN)
regression-test-checklist.es.md   # Versión en español del mismo template
```

## Uso

Copiá el archivo a tu repositorio (por ejemplo en `docs/` o `.github/`), reemplazá los valores de ejemplo (`<Release Version>`, `<Name>`, números de versión, endpoints, umbrales) por los tuyos y eliminá las secciones que no apliquen a tu stack. Mantenelo en control de versiones y actualizalo después de cada incidente — cada incidente debería sumar un check nuevo.

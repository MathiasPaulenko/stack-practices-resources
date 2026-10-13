# Plantilla de Checklist de Verificación Post-Deploy

Checklist listo para copiar y verificar que un despliegue realmente tuvo éxito: health checks, smoke tests, validación de métricas, revisión de seguridad y logs, preparación de rollback y sign-off.

Artículo original: [Plantilla de Checklist Post-Deploy](https://stackpractices.com/es/docs/post-deployment-checklist-template/)

## Archivos

- `post-deployment-checklist-template.md` — plantilla en blanco para completar en cada despliegue
- `post-deployment-checklist-example.md` — el mismo checklist completado para un release de `payments-api`

## Cómo usarlo

1. Copia `post-deployment-checklist-template.md` a tu repo (por ejemplo `docs/deploy-checklist.md`) o a tu runbook de despliegues.
2. Completa la fila de Deployment Info y ejecuta cada sección en orden: health checks primero, smoke tests a los ~5 minutos, métricas y revisión de logs a los ~15.
3. Guarda el checklist completado junto al registro del despliegue: el sign-off solo vale si queda archivado.
4. Escala el alcance según el riesgo: los despliegues de bajo riesgo pueden correr health checks y un smoke test puntual; los de alto riesgo usan el checklist completo, monitoreo extendido y un tercer sign-off.

## Guía de tiempos

| Check | Cuándo | Duración |
|-------|--------|----------|
| Health checks | Inmediatamente después del despliegue | ~2 min |
| Smoke tests | ~5 min post-deploy | ~10 min |
| Métricas + revisión de seguridad/logs | ~15 min post-deploy | ~10 min |
| Validación completa | 1 h post-deploy | Continuo |

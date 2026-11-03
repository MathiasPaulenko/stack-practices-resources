# Optimización de Cold Start — Archivos Companion

Companion de la receta de StackPractices [Optimización de Cold Start: AWS Lambda, Azure, Cloud Run](https://stackpractices.com/es/recipes/cold-start-optimization/).

| Archivo | Contiene |
|---|---|
| src/provisioned-concurrency.tf | Terraform para concurrencia aprovisionada de Lambda sobre una versión publicada |
| src/OrderHandler.java | Handler Java listo para SnapStart con init en la snapshot |
| src/azure-premium-deploy.sh | Deploy de Azure Functions en plan Premium con instancias precalentadas |
| src/deploy-cloudrun.sh | Deploy de Cloud Run con warm pool `--min-instances` |
| src/lazy-init.py | Patrón de inicialización lazy en Python para recursos pesados |

## Uso

- Copiá `provisioned-concurrency.tf` a tu infra y ajustá `function_name`/`memory_size`; recordá que `publish = true` es obligatorio.
- `OrderHandler.java` muestra dónde SnapStart captura la init — mantené los recursos con estado fuera de la snapshot.
- Usá los dos scripts shell como plantilla para los deploys de Azure Premium y Cloud Run.
- `lazy-init.py` muestra qué va a nivel módulo y qué va lazy en los clientes.

# Plantilla de Gestión de Parches — Companion

Archivos del documento [Plantilla de Gestión de Parches](https://stackpractices.com/es/docs/patch-management-template/).

- `patch-management-plan.md` — la plantilla lista para copiar (inventario, clasificación, checklist, cronograma, verificación, registro de excepciones).
- `patch-security-updates.yml` — playbook Ansible base para parcheo rolling de SO.
- `patch-image-pipeline.sh` — parcheo de imagen base + escaneo Trivy + despliegue rolling en K8s.

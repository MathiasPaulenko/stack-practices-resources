# Política de Gestión de Estado de Terraform

Archivos companion de la plantilla de StackPractices:
<https://stackpractices.com/es/docs/terraform-state-management-policy/>

## Qué hay acá

- `POLICY.md` — documento de política listo para rellenar (10 secciones: backend,
  aislamiento, control de acceso, operaciones, seguridad, DR, CI/CD, migraciones,
  enforcement y métricas). Reemplazá los `<...>` y adoptala.
- `backend.tf` — bloque de backend S3 con locking nativo (`use_lockfile`,
  Terraform >= 1.10) y notas de migración desde DynamoDB.
- `iam-policies.json` — políticas IAM de solo lectura (plan) y lectura-escritura
  (apply) para el bucket de state, incluidos los permisos del lock `*.tflock`.

## Uso

1. Copiá `POLICY.md` a tu repo/wiki y completá los placeholders.
2. Adaptá `backend.tf` a tus buckets y regiones.
3. Adjuntá las políticas IAM a tus roles de usuario y de CI.
4. Fijá la fecha de revisión trimestral y la primera entrada del registro de excepciones.

# Plantilla de Ciclo de Vida de Claves de Cifrado

Archivos complementarios de la [Plantilla de Ciclo de Vida de Claves de Cifrado](https://stackpractices.com/es/docs/encryption-key-lifecycle-template/) en StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `kms-key-policy.yaml` | Fragmento de CloudFormation para una clave AWS KMS con rotación automática y una política de mínimo privilegio |
| `key-rotation-audit.sh` | Script bash que lista todas las claves KMS de una región y marca las que no tienen rotación automática |
| `key-compromise-runbook.md` | Runbook paso a paso para responder a un incidente de compromiso de clave |

## Uso

1. Adapta `kms-key-policy.yaml` a tu cuenta: sustituye `app-role` por el rol IAM que usa tu aplicación y revisa qué acciones administrativas necesita cada principal.
2. Ejecuta el script de auditoría contra tu región para encontrar claves sin rotación:

   ```bash
   chmod +x key-rotation-audit.sh
   ./key-rotation-audit.sh
   ```

   Requiere la AWS CLI configurada con los permisos `kms:ListKeys`, `kms:DescribeKey` y `kms:GetKeyRotationStatus`. Cambia `REGION` al inicio del script si hace falta.
3. Mantén `key-compromise-runbook.md` accesible desde tu herramienta de incidentes y ensáyalo en un tabletop exercise antes de necesitarlo.

Las tablas de la política de ciclo de vida (clasificación, rotación, control de acceso, inventario, métricas, mapeo de cumplimiento) viven en la plantilla: cópialas a tu documentación interna y complétalas con tus propios valores.

# Recursos de la Plantilla de Seguridad de Pipeline CI/CD

Recursos complementarios de [Plantilla de Seguridad de Pipeline CI/CD](https://stackpractices.com/es/docs/ci-cd-pipeline-security-template/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `pipeline/security-controls-template.md` | Seis tablas de controles cubriendo control de código, configuración de pipeline, gestión de secretos, compilación, despliegue y respuesta a incidentes — cada uno mapeado a un método de verificación |
| `ci/secure-pipeline.yml` | Workflow endurecido de GitHub Actions: permisos mínimos por job, OIDC para autenticación en la nube (sin claves estáticas), firma de artefactos con cosign, generación de SBOM y escaneo CodeQL |
| `ci/slsa-provenance.json` | Ejemplo de declaración de provenance SLSA en formato in-toto mostrando cómo se estructura la atestación de build |
| `audit/pipeline-audit-checklist.md` | Checklist de auditoría de diez ítems para revisiones periódicas de seguridad del pipeline |

## Uso

1. Copia `pipeline/security-controls-template.md` y completa tu plataforma, responsables y evidencia de verificación.
2. Copia `ci/secure-pipeline.yml` a `.github/workflows/` y ajusta el ARN del rol, la región y los pasos de build.
3. Usa `audit/pipeline-audit-checklist.md` cada trimestre — cada fila mapea a un control de la plantilla.

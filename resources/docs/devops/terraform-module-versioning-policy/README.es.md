# Política de Versionado de Módulos Terraform — Archivos Companion

Assets de la plantilla de StackPractices:
[Plantilla de Política de Versionado de Módulos Terraform](https://stackpractices.com/es/docs/terraform-module-versioning-policy/)

## Archivos

| Archivo | Propósito |
| --- | --- |
| `versions.tf` | Constraints de versión de Terraform y providers (subir el mínimo = breaking change) |
| `release.yml` | Pipeline de release en GitHub Actions: tag → fmt/validate/tests → docs → GitHub Release |
| `validate.yml` | Matriz de validación en PRs entre versiones de Terraform + tfsec + infracost |
| `CHANGELOG.md` | Ejemplo Keep a Changelog con secciones semver (Added/Changed/Deprecated/Breaking) |
| `MIGRATION-GUIDE.md` | Guía de migración antes/después para un release major con breaking changes |
| `examples/basic/` | Consumidor mínimo con pin de versión exacto (default de producción) |

## Uso

```bash
# Copia los workflows al repositorio del módulo
cp release.yml your-module/.github/workflows/
cp validate.yml your-module/.github/workflows/

# Copia los archivos de política a la raíz del módulo
cp versions.tf CHANGELOG.md MIGRATION-GUIDE.md your-module/
```

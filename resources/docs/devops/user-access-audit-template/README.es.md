# Plantilla de Auditoría de Acceso de Usuarios — Recursos Complementarios

Archivos complementarios de la [Plantilla de Auditoría de Acceso de Usuarios](https://stackpractices.com/es/docs/user-access-audit-template/) de StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `user-access-audit-template.md` | Plantilla de certificación en blanco: alcance, inventario, mapeo de accesos, revisión de privilegiados, registro de certificación, plan de remediación y checklist de evidencia |
| `okta-access-review.py` | Extrae usuarios activos de la API de Okta, marca cuentas inactivas más allá de un umbral y exporta un CSV de acceso por usuario |
| `aws-access-analyzer.sh` | Crea (de forma idempotente) un IAM Access Analyzer a nivel de organización y exporta los hallazgos activos a JSON |
| `github-org-audit.js` | Lista los miembros de la organización de GitHub, marca usuarios sin 2FA (con el filtro `2fa_disabled`) y administradores |

## Uso

```bash
# Informe de Okta
pip install requests
export OKTA_API_TOKEN=ssws_xxx
export OKTA_DOMAIN=yourorg.okta.com
python okta-access-review.py --days 90 --output access_review.csv

# Exportación de hallazgos de AWS
./aws-access-analyzer.sh us-east-1

# Auditoría de la organización de GitHub
npm install @octokit/rest
GITHUB_TOKEN=ghp_xxx node github-org-audit.js your-org
```

## Notas

- El script de Okta lee `lastLogin` de la API de usuarios de Okta; las cuentas que nunca iniciaron sesión quedan fuera del informe de inactividad y deberían revisarse aparte.
- El filtrado `2fa_disabled` requiere un token con acceso de administrador a la organización.
- Ejecuta revisiones de acceso privilegiado trimestralmente y revisiones generales anualmente, además de revisiones al cambiar de rol y tras cada baja.

## Relacionado

- [Plantilla de Política RBAC](https://stackpractices.com/es/docs/rbac-policy-template/)
- [Plantilla de Revisión de Control de Acceso](https://stackpractices.com/es/docs/access-control-review-template/)

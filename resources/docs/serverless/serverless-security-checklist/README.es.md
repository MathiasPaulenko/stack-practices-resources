# Checklist de Seguridad Serverless — Recursos

Assets ejecutables que acompañan al [Checklist de Seguridad Serverless](https://stackpractices.com/es/docs/serverless-security-checklist/).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `mask-pii.py` | Helper de enmascarado de PII — hashea campos sensibles (email, phone, ssn, creditCard) antes de que lleguen a los logs |
| `security-logger.py` | Logger estructurado de eventos de seguridad: fallos de auth y authz, salida JSON con marcador `security_event` para enrutar al SIEM |
| `dependabot.yml` | PRs semanales de actualización de dependencias — va en `.github/dependabot.yml` |
| `security-audit.sh` | Puerta de auditoría de dependencias: npm audit, pip safety, Snyk y verificación de procedencia del lockfile en una pasada |

## Uso

```bash
# ejecutar la auditoría de dependencias en CI o en local
./security-audit.sh

# copiar la config de dependabot a tu repo
cp dependabot.yml .github/dependabot.yml
```

`security-logger.py` espera `authenticate`, `authorize` y `process_order` de tu propio código — es una integración de referencia, no un handler drop-in. Enruta las líneas `security_event: true` a un log group dedicado o a un stream del SIEM con acceso más restringido que los logs de aplicación.

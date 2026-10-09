# Checklist de Seguridad de Endpoints — Archivos complementarios

Recursos de la plantilla de StackPractices:
[Plantilla de Checklist de Seguridad para Endpoints](https://stackpractices.com/es/docs/endpoint-security-checklist-template/)

## Archivos

| Archivo | Propósito |
| --- | --- |
| `checklist.md` | Versión standalone del checklist de 5 categorías, lista para copiar |
| `endpoint-compliance.sql` | Consultas osquery de escaneo de flota (cifrado, firewall, presencia de EDR, USB) |
| `ssh-passphrase-audit.sh` | Auditoría Bash de llaves SSH sin passphrase + permisos de archivos de credenciales |
| `intune-compliance.ps1` | PowerShell con Microsoft Graph para extraer cumplimiento/cifrado por dispositivo |

## Ejecutar

```bash
# Escaneo de flota con osquery (funciona en Linux/macOS/Windows)
osqueryi --json < endpoint-compliance.sql

# Auditoría de llaves SSH
bash ssh-passphrase-audit.sh

# Reporte de cumplimiento Intune
pwsh intune-compliance.ps1
```

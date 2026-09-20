# Azure Básico — Recursos Companion

Companion ejecutable de la guía **[Azure Básico — Servicios Core para Desarrolladores](https://stackpractices.com/es/guides/azure-basics-guide/)** en StackPractices.

## Archivos

| Archivo | Propósito |
|---|---|
| `azure-bootstrap.sh` | Aprovisiona un entorno de desarrollo completo con la CLI de Azure: resource group (etiquetado), storage account + contenedor uploads, plan de App Service + web app, Key Vault con un secreto de ejemplo, managed identity asignada por el sistema con permiso RBAC sobre Key Vault, y Application Insights. |

## Inicio rápido

```bash
az login
az account set --subscription "My Subscription"

export SQL_ADMIN_PASSWORD="$(openssl rand -base64 24)"
chmod +x azure-bootstrap.sh
RG=rg-myapp-dev LOCATION=eastus APP_NAME=my-webapp-123 ./azure-bootstrap.sh
```

## Limpieza

```bash
az group delete --name rg-myapp-dev --yes --no-wait
```

Borrar el resource group elimina todos los recursos que contiene — incluido el Key Vault (que permanece recuperable durante 90 días gracias a soft-delete y purge protection).

## Notas

- Los nombres de storage account y Key Vault deben ser globalmente únicos; el script genera sufijos con `$RANDOM`. Sobrescríbelos con `STORAGE_NAME=` / `KV_NAME=` si hay conflicto de nombre.
- `SQL_ADMIN_PASSWORD` es obligatoria para que ninguna credencial quede hardcodeada en el script.
- Revisa la tabla de decisión de cómputo de la guía antes de escalar más allá del plan B1 — App Service factura por plan, no por petición.

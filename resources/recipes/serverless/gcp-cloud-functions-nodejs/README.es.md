# Cloud Functions en GCP con Node.js — Recursos complementarios

Companion ejecutable de la receta [Desplegar Cloud Functions HTTP en Google Cloud con Node.js](https://stackpractices.com/es/recipes/gcp-cloud-functions-nodejs/) ([English version](https://stackpractices.com/recipes/gcp-cloud-functions-nodejs/)).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `index.js` | API Express registrada como función HTTP Gen 2: CRUD con Firestore, cacheo de Secret Manager, CORS, manejador central de errores |
| `scheduled.js` | Handler HTTP invocado por Cloud Scheduler (OIDC) — la alternativa correcta a un flag `--schedule` que no existe |
| `deploy.sh` | Script `gcloud`: habilita las APIs y despliega `my-api` (Gen 2, nodejs20, concurrencia, secrets) |
| `deploy-scheduled.sh` | Despliega una función privada, da `run.invoker` a la cuenta del scheduler y crea el job cron |
| `package.json` | Dependencias y `npm start` para ejecución local con el Functions Framework |

## Ejecutar en local

```bash
npm install
npm start                      # sirve en http://localhost:8080
curl http://localhost:8080/health
```

## Desplegar

```bash
export GCP_PROJECT=my-project-id
./deploy.sh                    # API HTTP pública
./deploy-scheduled.sh          # función privada + job de Cloud Scheduler
```

La ruta programada necesita una cuenta de servicio (`scheduler-sa@<proyecto>.iam.gserviceaccount.com`) y la API de Cloud Scheduler habilitada.

## Licencia

MIT — archivos complementarios de uso educativo.

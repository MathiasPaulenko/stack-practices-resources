# Cron Jobs — Ejemplos ejecutables

Código complementario de la receta de StackPractices
[Cron: programar tareas en Linux, Python y Node.js](https://stackpractices.com/es/recipes/cron-jobs/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `crontab.example` | Crontab comentado: `PATH`/`SHELL`/`MAILTO`, bloqueo con flock, redirección a logs, `timeout`, `@reboot` |
| `backup.sh` | Script de backup apto para cron: `set -euo pipefail`, rutas absolutas, logs con timestamp, retención |
| `backup.service` + `backup.timer` | Unidades systemd — `Persistent=true` recupera ejecuciones perdidas |
| `cronjob.yaml` | CronJob de Kubernetes con `concurrencyPolicy: Forbid` y `activeDeadlineSeconds` |
| `schedule_example.py` | Bucle mínimo con la librería `schedule` |
| `apscheduler_example.py` | APScheduler con `max_instances`, `coalesce` y `jitter` |
| `app.js` | Schedules de `node-cron`, incluida la opción `timezone` explícita |
| `main.go` | Fundamentos de `robfig/cron` v3 y el campo de segundos opcional |
| `package.json` | Dependencia de `app.js` (`node-cron`) |

## Ejecutar

Cron del sistema:

```bash
crontab crontab.example   # instala el crontab de ejemplo
crontab -l                # verifica
```

Timer de systemd:

```bash
sudo cp backup.service backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
systemctl list-timers --all
```

Kubernetes:

```bash
kubectl apply -f cronjob.yaml
kubectl get cronjobs
kubectl create job --from=cronjob/database-backup manual-test
```

Planificadores dentro de la app:

```bash
python schedule_example.py        # requiere: pip install schedule
python apscheduler_example.py     # requiere: pip install apscheduler
npm install && node app.js        # node-cron
go mod init example && go get github.com/robfig/cron/v3 && go run main.go
```

## Detalle clave

Cron ejecuta los trabajos con un entorno mínimo: `PATH` reducido, sin perfil de
shell y el home como directorio de trabajo. Define `PATH` y `SHELL` en el
crontab o carga un perfil dentro del trabajo — eso arregla el clásico "funciona
en mi terminal pero falla a las 3 AM".

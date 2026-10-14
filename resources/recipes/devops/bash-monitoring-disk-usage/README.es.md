# Monitorear Uso de Disco — Ejemplos ejecutables

Código complementario de la receta de StackPractices
[Monitorear Uso de Disco](https://stackpractices.com/es/recipes/bash-monitoring-disk-usage/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `disk-monitor.sh` | Verificación por umbral de todos los mounts locales con `df -Hl` + `awk`, alerta por email vía `mail` |
| `slack-alert.sh` | La misma verificación, pero publica un payload estructurado en un webhook de Slack |
| `per-partition-thresholds.sh` | Un umbral por mount (`/`:80, `/var`:90, `/home`:75, `/tmp`:85) |
| `state-change-alerts.sh` | Archivo de estado en `/var/run` para que un mount lleno alerte una vez, no en cada corrida de cron |
| `inode-monitor.sh` | Verificación con `df -i` más un reporte top-5 de directorios por cantidad de archivos |
| `find-disk-consumers.sh` | Diagnóstico con `du`/`find` de qué directorios y archivos crecieron |
| `disk-cleanup.sh` | Limpieza disparada por umbral: gzip de logs viejos, archivo, `apt-get`/`yum` clean, `docker system prune` |
| `disk-monitor.service` + `disk-monitor.timer` | Unidades systemd que reemplazan cron (`OnUnitActiveSec=5min`) |
| `prometheus-alerts.yml` | Reglas de alerta para métricas `node_filesystem_*`, incluido `predict_linear` |

## Ejecutar

Verificación manual:

```bash
chmod +x disk-monitor.sh
./disk-monitor.sh 80 admin@example.com
```

Alertas a Slack:

```bash
export SLACK_WEBHOOK="https://hooks.slack.com/services/XXX/YYY/ZZZ"
./slack-alert.sh 80
```

Timer de systemd:

```bash
sudo cp disk-monitor.sh /usr/local/bin/
sudo cp disk-monitor.service disk-monitor.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now disk-monitor.timer
systemctl list-timers disk-monitor.timer
```

Alternativa con cron:

```bash
# */5 * * * * /usr/local/bin/disk-monitor.sh 80 admin@example.com
```

## Detalle clave

`df -Hl` puede dejar la columna de porcentaje vacía en filesystems especiales —
el filtro `awk` `/^\/dev/` los salta. Monitorea los inodos por separado
(`df -i`): un disco con bloques libres puede rechazar escrituras si se queda sin
slots de archivos.

# Monitor Disk Usage — Runnable Examples

Companion code for the StackPractices recipe
[Monitor Disk Usage](https://stackpractices.com/recipes/bash-monitoring-disk-usage/).

## Files

| File | What it shows |
|------|---------------|
| `disk-monitor.sh` | Threshold check over all local mounts with `df -Hl` + `awk`, email alert via `mail` |
| `slack-alert.sh` | Same check, but posts a structured payload to a Slack incoming webhook |
| `per-partition-thresholds.sh` | One threshold per mount (`/`:80, `/var`:90, `/home`:75, `/tmp`:85) |
| `state-change-alerts.sh` | State file in `/var/run` so a full mount alerts once, not every cron run |
| `inode-monitor.sh` | `df -i` check plus a top-5 directory report by file count |
| `find-disk-consumers.sh` | `du`/`find` diagnostic for which directories and files grew |
| `disk-cleanup.sh` | Threshold-triggered cleanup: gzip old logs, archive, `apt-get`/`yum` clean, `docker system prune` |
| `disk-monitor.service` + `disk-monitor.timer` | systemd units replacing cron (`OnUnitActiveSec=5min`) |
| `prometheus-alerts.yml` | Alert rules for `node_filesystem_*` metrics, including `predict_linear` |

## Run

Manual check:

```bash
chmod +x disk-monitor.sh
./disk-monitor.sh 80 admin@example.com
```

Slack alerts:

```bash
export SLACK_WEBHOOK="https://hooks.slack.com/services/XXX/YYY/ZZZ"
./slack-alert.sh 80
```

systemd timer:

```bash
sudo cp disk-monitor.sh /usr/local/bin/
sudo cp disk-monitor.service disk-monitor.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now disk-monitor.timer
systemctl list-timers disk-monitor.timer
```

Cron alternative:

```bash
# */5 * * * * /usr/local/bin/disk-monitor.sh 80 admin@example.com
```

## Key detail

`df -Hl` can leave the percent column empty for special filesystems — the `awk`
filter `/^\/dev/` skips them. Monitor inodes separately (`df -i`); a disk with
free blocks can still refuse writes when it runs out of file slots.

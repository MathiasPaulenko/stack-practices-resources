# Cron Jobs — Runnable Examples

Companion code for the StackPractices recipe
[Cron Jobs: Schedule Tasks in Linux, Python & Node.js](https://stackpractices.com/recipes/cron-jobs/).

## Files

| File | What it shows |
|------|---------------|
| `crontab.example` | Annotated crontab: `PATH`/`SHELL`/`MAILTO`, flock locking, log redirection, `timeout`, `@reboot` |
| `backup.sh` | Cron-safe backup script: `set -euo pipefail`, absolute paths, timestamped logs, retention |
| `backup.service` + `backup.timer` | systemd units — `Persistent=true` catches up missed runs |
| `cronjob.yaml` | Kubernetes CronJob with `concurrencyPolicy: Forbid` and `activeDeadlineSeconds` |
| `schedule_example.py` | Minimal `schedule` library loop |
| `apscheduler_example.py` | APScheduler with `max_instances`, `coalesce`, and `jitter` |
| `app.js` | `node-cron` schedules, including an explicit `timezone` option |
| `main.go` | `robfig/cron` v3 basics and the optional seconds field |
| `package.json` | Dependency for `app.js` (`node-cron`) |

## Run

System cron:

```bash
crontab crontab.example   # install the example crontab
crontab -l                # verify
```

systemd timer:

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

In-app schedulers:

```bash
python schedule_example.py        # needs: pip install schedule
python apscheduler_example.py     # needs: pip install apscheduler
npm install && node app.js        # node-cron
go mod init example && go get github.com/robfig/cron/v3 && go run main.go
```

## Key detail

Cron runs jobs with a minimal environment: tiny `PATH`, no shell profile, home
directory as cwd. Set `PATH` and `SHELL` in the crontab or source a profile
inside the job — that fixes the classic "works in my terminal, fails at 3 AM".

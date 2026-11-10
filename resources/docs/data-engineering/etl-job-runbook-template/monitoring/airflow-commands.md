# Airflow 2.x CLI cheat sheet for ETL runbooks

Verified against the [Airflow CLI reference](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html).
Commands that show up in older blog posts but no longer exist are listed at the bottom.

## Inspecting runs and tasks

```bash
# State of a DAG run on a given logical date
airflow dags state <dag_id> <logical_date>

# Recent runs with start/end/duration
airflow dags list-runs -d <dag_id> --limit 10

# Tasks of a run filtered by state
airflow tasks list <dag_id> --state running
airflow tasks list <dag_id> --state failed

# Task durations: not in the CLI — use the UI (Grid view) or the REST API:
#   GET /api/v1/dags/<dag_id>/dagRuns/<run_id>/taskInstances
```

## Re-running and backfilling

```bash
# Re-run a failed task = clear its state; the scheduler queues it again
airflow tasks clear <dag_id> -t <task_id> -s <date> -e <date>

# Also clear everything downstream of it
airflow tasks clear <dag_id> -t <task_id> --downstream -s <date> -e <date>

# Clear only failed tasks in a window
airflow tasks clear <dag_id> -s <start> -e <end> --only-failed

# Manual trigger with params
airflow dags trigger <dag_id> --conf '{"date": "<date>"}'

# Backfill a range (Airflow 2.x; removed in Airflow 3 — use backfill jobs API there)
airflow dags backfill <dag_id> -s <start> -e <end> --reset-dagruns --run-backwards
```

## Pausing

```bash
airflow dags pause <dag_id>
airflow dags unpause <dag_id>
```

## Connections

```bash
# Connections are managed via UI → Admin → Connections, or the CLI:
airflow connections list
airflow connections get <conn_id>
airflow connections delete <conn_id>
airflow connections add <conn_id> --conn-uri '<scheme>://<user>:<pass>@<host>:<port>/<db>'
```

## Logs

There is no `airflow tasks logs` command in Airflow 2.x. Task logs live in:

- Airflow UI → Grid → task instance → Log
- On Kubernetes: `kubectl logs -n <namespace> <worker-pod> -c base`
- `airflow tasks test <dag_id> <task_id> <date>` — runs one task locally and prints its log to stdout (testing only, not a re-run)

## Commands that do NOT exist (Airflow 2.x)

| Tempting | Reality |
|----------|---------|
| `airflow tasks run` | removed in Airflow 2.0 — clear the task instead |
| `airflow tasks logs` | never existed — logs are in the UI or the executor's pod |
| `airflow connections set` | use `connections add` (delete first to overwrite) |
| `airflow tasks duration` | per-task durations live in the UI / REST API |

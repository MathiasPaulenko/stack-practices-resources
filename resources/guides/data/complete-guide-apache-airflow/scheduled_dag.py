# Schedule presets
dag = DAG(
    "scheduled_pipeline",
    schedule="@daily",      # Daily at midnight
    # schedule="@hourly",   # Every hour
    # schedule="@weekly",   # Weekly on Sunday
    # schedule="@monthly",  # Monthly on the 1st
    # schedule="0 2 * * 1-5",  # 2 AM on weekdays (cron)
    # schedule="*/15 * * * *",  # Every 15 minutes
    # schedule=None,        # Manual trigger only
    start_date=datetime(2026, 1, 1),
    catchup=True,           # Backfill missing runs
    max_active_runs=1,      # Only one run at a time
)

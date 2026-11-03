# Connections: stored in Airflow metadata DB or environment variables
# Set via UI: Admin → Connections
# Or via CLI: airflow connections add ...

from airflow.providers.postgres.hooks.postgres import PostgresHook

# Use connection in a task
def load_data(**context):
    hook = PostgresHook(postgres_conn_id="warehouse_prod")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ... VALUES (%s)", (context["ds"],))
    conn.commit()

# Variables: key-value config stored in metadata DB
from airflow.models import Variable

def get_config():
    batch_size = Variable.get("batch_size", default_var=1000)
    api_url = Variable.get("api_url")
    return {"batch_size": int(batch_size), "api_url": api_url}

# Environment variable fallback
# AIRFLOW_VAR_API_URL=https://api.example.com
api_url = Variable.get("api_url")  # Falls back to AIRFLOW_VAR_API_URL

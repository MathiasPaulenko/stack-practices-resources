from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator

def check_date(**context):
    date = context["ds"]
    day_of_week = datetime.strptime(date, "%Y-%m-%d").weekday()
    if day_of_week == 6:  # Sunday
        return "weekly_aggregation"
    return "daily_aggregation"

branch = BranchPythonOperator(
    task_id="branch",
    python_callable=check_date,
    dag=dag,
)

daily = BashOperator(task_id="daily_aggregation", bash_command="...", dag=dag)
weekly = BashOperator(task_id="weekly_aggregation", bash_command="...", dag=dag)
join = EmptyOperator(task_id="join", trigger_rule="none_failed", dag=dag)

branch >> [daily, weekly] >> join

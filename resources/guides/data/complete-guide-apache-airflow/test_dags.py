heavy_query = SnowflakeOperator(
    task_id="heavy_query",
    sql="SELECT ...",
    snowflake_conn_id="warehouse_prod",
    pool="warehouse_queries",  # create it in Admin → Pools with N slots
    pool_slots=2,              # this task weighs 2 of N slots
)

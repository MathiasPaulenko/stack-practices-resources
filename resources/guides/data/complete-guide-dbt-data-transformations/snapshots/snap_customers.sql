{% snapshot snap_customers %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at',
    )
}}

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    customer_tier,
    updated_at
FROM {{ source('raw', 'customers') }}

{% endsnapshot %}

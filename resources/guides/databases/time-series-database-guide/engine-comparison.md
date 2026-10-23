# Engine Comparison Notes

Quick reference for choosing between InfluxDB, TimescaleDB, and ClickHouse for
time-series workloads. Companion to
https://stackpractices.com/guides/time-series-database-guide/

| Feature | InfluxDB | TimescaleDB | ClickHouse |
|---------|----------|-------------|------------|
| **Base engine** | Custom (TSM/TSI) | PostgreSQL extension | Columnar OLAP |
| **SQL support** | InfluxQL / Flux | Full SQL | SQL dialect |
| **Ease of setup** | Single binary | PostgreSQL + extension | More complex |
| **Ingestion rate** | Very high | High | Extremely high |
| **Compression** | Good | Good | Excellent |
| **Best for** | DevOps metrics, IoT | Apps already on Postgres | Analytics, big data |

## Decision shortcuts

- **Already on PostgreSQL?** TimescaleDB — same tools, same backups, same SQL.
- **Metrics-only workload, want a single binary?** InfluxDB.
- **Analytics at billions of rows, ops capacity available?** ClickHouse.

## InfluxDB line protocol

```text
measurement,tag1=value1,tag2=value2 field1=42.0,field2="text" 1465839830100400200
```

- **Measurement**: logical container (like a table)
- **Tags**: indexed dimensions — expensive at high cardinality
- **Fields**: stored values — not indexed
- **Timestamp**: nanosecond precision

## ClickHouse MergeTree

```sql
CREATE TABLE events (
    event_time DateTime,
    user_id UInt64,
    event_type String,
    value Float64
) ENGINE = MergeTree()
ORDER BY (event_type, event_time);
```

Put the selective filter column first in `ORDER BY`; time goes second.

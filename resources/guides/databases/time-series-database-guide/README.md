# Time-Series Database Guide — Companion

Companion files for the [Time-Series Database Guide](https://stackpractices.com/guides/time-series-database-guide/) on StackPractices.com.

## Files

| File | Type | Contents |
|------|------|----------|
| `timescaledb-setup.sql` | SQL | Minimal TimescaleDB setup: extension, hypertable, continuous aggregate, retention + refresh policies |
| `iot-timescaledb-scenario.sql` | SQL | The full IoT scenario from the guide: 10K sensors, tiered continuous aggregates, retention tiers, typical queries |
| `engine-comparison.md` | Markdown | InfluxDB vs TimescaleDB vs ClickHouse decision notes, line protocol reference, ClickHouse `ORDER BY` guidance |

## Usage

1. Spin up PostgreSQL with the TimescaleDB extension (`timescale/timescaledb` Docker image works out of the box).
2. Run `timescaledb-setup.sql` for the minimal working example.
3. Run `iot-timescaledb-scenario.sql` to reproduce the guide's IoT scenario end to end.

## Notes

- InfluxDB and ClickHouse snippets live inline in `engine-comparison.md` — they illustrate syntax, not a runnable setup.
- Watch series cardinality before scaling ingest: unbounded tag values are the most common way to take a TSDB down.

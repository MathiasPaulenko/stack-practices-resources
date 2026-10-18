"""Medallion pipeline: Bronze -> Silver -> Gold with pandas + pyarrow.

Companion to stackpractices.com/guides/data-lake-guide/
Requires: pip install pandas pyarrow

Generates synthetic events, lands them raw in Bronze (JSON), cleans and
partitions them into Silver (Parquet, dt=YYYY-MM-DD), and aggregates
daily metrics into Gold. Mirrors the Spark/Delta jobs from the guide
without needing a Spark cluster — runnable on a laptop.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

LAKE = Path("lake")
EVENT_TYPES = ["page_view", "add_to_cart", "purchase", "search", "logout"]
N_EVENTS = 5_000


def generate_events(day: datetime) -> list[dict]:
    """Create synthetic clickstream events, including a few dirty rows."""
    events = []
    for i in range(N_EVENTS):
        ts = day + timedelta(seconds=random.randint(0, 86_399))
        events.append({
            "event_id": f"evt-{day:%Y%m%d}-{i}",
            "user_id": random.randint(1, 800) if random.random() > 0.02 else None,
            "event_type": random.choice(EVENT_TYPES),
            "timestamp": ts.isoformat(),
        })
    events += [events[0]]  # duplicate on purpose, for Silver to clean
    return events


def to_bronze(events: list[dict], day: datetime) -> Path:
    """Land raw JSON in the Bronze zone, partitioned by date."""
    path = LAKE / "bronze" / "events" / f"dt={day:%Y-%m-%d}"
    path.mkdir(parents=True, exist_ok=True)
    out = path / "events.json"
    out.write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
    return out


def bronze_to_silver(bronze_file: Path) -> Path:
    """Clean, type, deduplicate and write Parquet to Silver."""
    df = pd.read_json(bronze_file, lines=True)
    cleaned = (
        df.dropna(subset=["user_id"])
          .assign(
              event_time=lambda d: pd.to_datetime(d["timestamp"]),
              event_date=lambda d: d["event_time"].dt.date.astype(str),
          )
          .drop_duplicates(subset=["event_id"])
    )
    silver_dir = LAKE / "silver" / "events"
    cleaned.to_parquet(
        silver_dir,
        engine="pyarrow",
        partition_cols=["event_date"],   # hive-style: event_date=YYYY-MM-DD/
        index=False,
    )
    return silver_dir


def silver_to_gold(silver_dir: Path) -> Path:
    """Aggregate daily metrics from Silver into Gold."""
    silver = pd.read_parquet(silver_dir)
    gold = (
        silver.groupby(["event_date", "event_type"])
              .agg(total_events=("event_id", "count"),
                   unique_users=("user_id", "nunique"))
              .reset_index()
    )
    out = LAKE / "gold" / "daily_events.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(out, engine="pyarrow", index=False)
    return out


if __name__ == "__main__":
    day = datetime(2026, 10, 18)
    bronze = to_bronze(generate_events(day), day)
    print(f"Bronze: {bronze} ({bronze.stat().st_size // 1024} KB)")

    silver = bronze_to_silver(bronze)
    n_files = len(list(silver.rglob("*.parquet")))
    print(f"Silver: {silver} ({n_files} partitioned parquet files)")

    gold = silver_to_gold(silver)
    print(f"Gold:   {gold}")
    print(pd.read_parquet(gold).to_string(index=False))

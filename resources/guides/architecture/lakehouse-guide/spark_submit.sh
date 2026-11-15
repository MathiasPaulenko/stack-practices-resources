#!/usr/bin/env bash
# Medallion pipeline on EMR/YARN — adjust paths and executor sizing to your cluster.
set -euo pipefail

BRONZE_PATH="${1:-s3://lakehouse/bronze/events/dt=2026-07-11/}"
SILVER_PATH="${2:-s3://lakehouse/silver/events/}"
GOLD_PATH="${3:-s3://lakehouse/gold/daily_metrics/}"
DELTA_PKG="io.delta:delta-spark_2.12:3.2.0"

# Step 1: Bronze -> Silver (cleaning + merge)
spark-submit --master yarn --num-executors 30 \
    --executor-memory 16g \
    --packages "$DELTA_PKG" \
    bronze_to_silver_delta.py "$BRONZE_PATH" "$SILVER_PATH"

# Step 2: Silver -> Gold (daily aggregates)
spark-submit --master yarn --num-executors 20 \
    --executor-memory 8g \
    --packages "$DELTA_PKG" \
    silver_to_gold_delta.py "$SILVER_PATH" "$GOLD_PATH"

# Step 3: Weekly maintenance (compact + zorder + vacuum + manifest)
spark-submit --master yarn \
    --packages "$DELTA_PKG" \
    delta_maintenance.py "$SILVER_PATH" 168

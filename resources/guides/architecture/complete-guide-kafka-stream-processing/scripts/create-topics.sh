#!/bin/bash
# Topics used by the Streams topology (RF=3, matches the 3-broker cluster).
B="localhost:9092,localhost:9094,localhost:9096"
for t in orders processed-orders high-value-orders order-counts windowed-order-counts enriched-orders orders-dlt; do
  kafka-topics.sh --create --if-not-exists --bootstrap-server $B --topic $t --partitions 6 --replication-factor 3
done

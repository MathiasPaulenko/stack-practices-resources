#!/bin/bash
# Create the orders topic per the guide (RF=3 requires a 3-broker cluster;
# matches the 3-broker docker-compose cluster).
kafka-topics.sh --create \
  --bootstrap-server localhost:9092,localhost:9094,localhost:9096 \
  --topic orders \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config compression.type=lz4

#!/bin/bash
# Health checks from the guide: under-replicated partitions + consumer lag.
kafka-topics.sh --describe --bootstrap-server localhost:9092,localhost:9094,localhost:9096 --under-replicated-partitions
kafka-consumer-groups.sh --describe --bootstrap-server localhost:9092,localhost:9094,localhost:9096 --group order-processor

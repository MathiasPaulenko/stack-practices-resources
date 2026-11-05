#!/bin/bash
# RDB backup from a replica — see guide
redis-cli -h  BGSAVE
scp :/var/lib/redis/dump.rdb s3://backups/redis-2026-11-05.rdb

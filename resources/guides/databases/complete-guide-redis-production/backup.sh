#!/bin/bash
# RDB backup from a replica — see guide
redis-cli -h replica-host BGSAVE
scp replica-host:/var/lib/redis/dump.rdb s3://backups/redis-$(date +%F).rdb

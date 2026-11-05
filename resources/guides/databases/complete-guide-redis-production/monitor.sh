#!/bin/bash
# Redis health snapshot — see guide for thresholds
redis-cli INFO memory | grep -E "used_memory_human|maxmemory|mem_fragmentation"
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses|evicted_keys|rejected_connections"
redis-cli INFO replication | grep -E "master_link_status|master_last_io_seconds"
redis-cli SLOWLOG GET 5

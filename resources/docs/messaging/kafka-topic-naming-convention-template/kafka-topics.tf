# Example kafka_topic resources following the naming convention.
# Requires a Kafka provider (e.g., Mongey/kafka) pointing at your cluster.

resource "kafka_topic" "order_created" {
  name               = "prod.orders.order-created.v1"
  replication_factor = 3
  partitions         = 6

  config = {
    "retention.ms"      = "604800000"   # 7 days
    "retention.bytes"   = "1073741824"  # 1 GB (per partition)
    "cleanup.policy"    = "delete"
    "compression.type"  = "snappy"
    "max.message.bytes" = "1048576"     # 1 MB
  }
}

resource "kafka_topic" "user_profile_snapshot" {
  name               = "prod.users.user-profile.snapshot"
  replication_factor = 3
  partitions         = 3

  config = {
    "cleanup.policy"      = "compact"
    "delete.retention.ms" = "86400000"   # 24h tombstones
    "min.cleanable.dirty.ratio" = "0.2"
    "compression.type"    = "snappy"
  }
}

resource "kafka_topic" "order_created_dlq" {
  name               = "prod.orders.order-created.dlq"
  replication_factor = 3
  partitions         = 3

  config = {
    "retention.ms"     = "604800000"   # 7 days — enough to triage and replay
    "retention.bytes"  = "524288000"   # 500 MB
    "cleanup.policy"   = "delete"
    "compression.type" = "snappy"
  }
}

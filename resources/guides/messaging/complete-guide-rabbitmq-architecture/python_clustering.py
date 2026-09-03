"""RabbitMQ clustering and high availability setup.

Shows quorum queue declaration and cluster management commands.
Run: python python_clustering.py
"""
import pika


def declare_quorum_queue(channel, queue_name="orders"):
    """Declare a quorum queue with Raft consensus replication."""
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments={"x-queue-type": "quorum"},
    )
    print(f"Quorum queue '{queue_name}' declared")


def declare_dlx_queue(channel, queue_name="orders"):
    """Declare a queue with dead letter exchange and TTL."""
    channel.exchange_declare(exchange=f"{queue_name}_dlx", exchange_type="direct")
    channel.queue_declare(queue=f"{queue_name}_dead_letter")
    channel.queue_bind(
        exchange=f"{queue_name}_dlx",
        queue=f"{queue_name}_dead_letter",
        routing_key=queue_name,
    )

    args = {
        "x-dead-letter-exchange": f"{queue_name}_dlx",
        "x-dead-letter-routing-key": queue_name,
        "x-message-ttl": 60000,
    }
    channel.queue_declare(queue=queue_name, arguments=args)
    print(f"Queue '{queue_name}' declared with DLX and 60s TTL")


def declare_priority_queue(channel, queue_name="priority_orders", max_priority=10):
    """Declare a priority queue."""
    channel.queue_declare(
        queue=queue_name,
        arguments={"x-max-priority": max_priority},
    )
    print(f"Priority queue '{queue_name}' declared (max priority: {max_priority})")


# Cluster management commands (run via bash, not Python):
# rabbitmqctl stop_app
# rabbitmqctl join_cluster rabbit@rabbit1
# rabbitmqctl start_app
# rabbitmqctl cluster_status
#
# Quorum queue via CLI:
# rabbitmqctl set_policy ha-orders "orders" \
#   '{"ha-mode":"all","ha-sync-mode":"automatic"}'

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    declare_quorum_queue(channel)
    declare_dlx_queue(channel)
    declare_priority_queue(channel)
    connection.close()

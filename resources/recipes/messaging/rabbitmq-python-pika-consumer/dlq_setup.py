"""Declare a queue with a dead-letter exchange and its DLQ."""

from producer import get_connection


def declare_queues_with_dlq(channel, queue_name: str = "task_queue") -> None:
    dlq_name = f"{queue_name}.dlq"

    channel.exchange_declare(exchange="dlx", exchange_type="direct", durable=True)
    channel.queue_declare(queue=dlq_name, durable=True)
    channel.queue_bind(queue=dlq_name, exchange="dlx", routing_key=dlq_name)

    args = {
        "x-dead-letter-exchange": "dlx",
        "x-dead-letter-routing-key": dlq_name,
    }
    channel.queue_declare(queue=queue_name, durable=True, arguments=args)


if __name__ == "__main__":
    connection = get_connection()
    channel = connection.channel()
    declare_queues_with_dlq(channel)
    print("Declared task_queue with DLX 'dlx' and task_queue.dlq")
    connection.close()

"""RabbitMQ exchange types demonstration.

Shows direct, topic, fanout, and headers exchanges with pika.
Run: python python_exchanges.py
"""
import json
import pika


def setup_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    return connection, channel


def demo_direct_exchange(channel):
    channel.exchange_declare(exchange="orders_direct", exchange_type="direct")
    channel.queue_declare(queue="orders_created")
    channel.queue_declare(queue="orders_cancelled")
    channel.queue_bind(exchange="orders_direct", queue="orders_created", routing_key="created")
    channel.queue_bind(exchange="orders_direct", queue="orders_cancelled", routing_key="cancelled")

    channel.basic_publish(
        exchange="orders_direct",
        routing_key="created",
        body=json.dumps({"order_id": 123, "total": 49.99}),
    )
    channel.basic_publish(
        exchange="orders_direct",
        routing_key="cancelled",
        body=json.dumps({"order_id": 124, "reason": "customer_request"}),
    )
    print("Direct exchange: 2 messages published")


def demo_topic_exchange(channel):
    channel.exchange_declare(exchange="logs_topic", exchange_type="topic")
    channel.queue_declare(queue="all_errors")
    channel.queue_declare(queue="app_errors")
    channel.queue_declare(queue="all_logs")
    channel.queue_bind(exchange="logs_topic", queue="all_errors", routing_key="*.error")
    channel.queue_bind(exchange="logs_topic", queue="app_errors", routing_key="app.*")
    channel.queue_bind(exchange="logs_topic", queue="all_logs", routing_key="#")

    channel.basic_publish(exchange="logs_topic", routing_key="app.error", body="App error")
    channel.basic_publish(exchange="logs_topic", routing_key="db.warning", body="DB warning")
    channel.basic_publish(exchange="logs_topic", routing_key="api.error.critical", body="API critical")
    print("Topic exchange: 3 messages published")


def demo_fanout_exchange(channel):
    channel.exchange_declare(exchange="notifications_fanout", exchange_type="fanout")
    channel.queue_declare(queue="email_queue")
    channel.queue_declare(queue="sms_queue")
    channel.queue_declare(queue="push_queue")
    channel.queue_bind(exchange="notifications_fanout", queue="email_queue")
    channel.queue_bind(exchange="notifications_fanout", queue="sms_queue")
    channel.queue_bind(exchange="notifications_fanout", queue="push_queue")

    channel.basic_publish(
        exchange="notifications_fanout",
        routing_key="",
        body=json.dumps({"user_id": 123, "message": "Order shipped"}),
    )
    print("Fanout exchange: 1 message broadcast to 3 queues")


def demo_headers_exchange(channel):
    channel.exchange_declare(exchange="headers_exchange", exchange_type="headers")
    channel.queue_declare(queue="priority_orders")
    channel.queue_declare(queue="all_orders")
    channel.queue_bind(
        exchange="headers_exchange",
        queue="priority_orders",
        routing_key="",
        arguments={"x-match": "all", "priority": "high", "type": "order"},
    )
    channel.queue_bind(
        exchange="headers_exchange",
        queue="all_orders",
        routing_key="",
        arguments={"x-match": "any", "type": "order"},
    )

    channel.basic_publish(
        exchange="headers_exchange",
        routing_key="",
        body=json.dumps({"order_id": 123}),
        properties=pika.BasicProperties(headers={"priority": "high", "type": "order"}),
    )
    print("Headers exchange: 1 message published")


def main():
    connection, channel = setup_connection()
    try:
        demo_direct_exchange(channel)
        demo_topic_exchange(channel)
        demo_fanout_exchange(channel)
        demo_headers_exchange(channel)
    finally:
        connection.close()


if __name__ == "__main__":
    main()

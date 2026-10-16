"""RabbitMQ dead-letter exchange setup and consumer (pika).

Declares a dead-letter exchange (DLX) plus its queue, binds the main queue
to it, and rejects unrecoverable messages with requeue=False so RabbitMQ
routes them to the DLQ.

Requires: pip install pika
"""

import pika


class UnrecoverableError(Exception):
    """Raised when a message can never succeed (bad schema, missing reference)."""


def process_order(body: bytes) -> None:
    """Placeholder business logic — replace with the real handler."""
    raise NotImplementedError


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Dead-letter exchange (DLX) and its queue
    channel.exchange_declare(exchange='orders.dlx', exchange_type='direct')
    channel.queue_declare(queue='orders-dlq', durable=True)
    channel.queue_bind(queue='orders-dlq', exchange='orders.dlx', routing_key='failed')

    # Main queue routes rejected or expired messages to the DLX
    args = {
        'x-dead-letter-exchange': 'orders.dlx',
        'x-dead-letter-routing-key': 'failed',
        'x-message-ttl': 300000,  # 5 minutes
    }
    channel.queue_declare(queue='orders', durable=True, arguments=args)

    def handle_message(ch, method, properties, body):
        try:
            process_order(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except UnrecoverableError:
            # requeue=False sends the message to the DLX
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue='orders', on_message_callback=handle_message)
    channel.start_consuming()


if __name__ == '__main__':
    main()

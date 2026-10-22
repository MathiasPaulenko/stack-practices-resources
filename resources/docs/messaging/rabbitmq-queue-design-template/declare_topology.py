"""Declares the full topology from the template: exchange, queue, DLX and bindings."""
import os

import pika


def connect():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'localhost'),
            port=int(os.environ.get('RABBITMQ_PORT', '5672')),
            credentials=pika.PlainCredentials(
                os.environ['RABBITMQ_USER'],
                os.environ['RABBITMQ_PASSWORD'],
            ),
            heartbeat=30,
            blocked_connection_timeout=300,
        )
    )


def declare(channel):
    channel.exchange_declare(
        exchange='prod.orders.order-created.direct',
        exchange_type='direct',
        durable=True,
    )
    channel.exchange_declare(
        exchange='prod.orders.dlx.direct',
        exchange_type='direct',
        durable=True,
    )

    queue_args = {
        'x-message-ttl': 86400000,
        'x-dead-letter-exchange': 'prod.orders.dlx.direct',
        'x-dead-letter-routing-key': 'order-payment-failed',
        'x-max-length': 50000,
        'x-overflow': 'reject-publish',
    }
    channel.queue_declare(
        queue='prod.orders.payment-service.process-payment',
        durable=True,
        arguments=queue_args,
    )
    channel.queue_bind(
        exchange='prod.orders.order-created.direct',
        queue='prod.orders.payment-service.process-payment',
        routing_key='order.payment.required',
    )

    dlq_args = {'x-message-ttl': 604800000}
    channel.queue_declare(
        queue='prod.orders.dlq.failed-messages',
        durable=True,
        arguments=dlq_args,
    )
    channel.queue_bind(
        exchange='prod.orders.dlx.direct',
        queue='prod.orders.dlq.failed-messages',
        routing_key='order-payment-failed',
    )


if __name__ == '__main__':
    conn = connect()
    declare(conn.channel())
    conn.close()
    print('Topology declared')

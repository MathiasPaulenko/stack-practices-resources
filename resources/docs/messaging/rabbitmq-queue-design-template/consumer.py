"""Consumer with manual ack and a republish-based retry counter.

basic_reject(requeue=True) returns the ORIGINAL message — headers are not
modified, so a retry counter can only work by republishing a copy with the
incremented header and acking the original.
"""
import json
import logging

import pika
from declare_topology import connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('consumer')

MAX_RETRIES = 3
QUEUE = 'prod.orders.payment-service.process-payment'


def handle_payment(message):
    # placeholder for real processing; return False to trigger a retry
    return bool(message.get('amount'))


def retry_or_dead_letter(channel, method, properties, body):
    headers = dict(properties.headers or {})  # headers can be None
    retry_count = headers.get('x-retry-count', 0)

    if retry_count >= MAX_RETRIES:
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        logger.warning('dead-lettered message after %s retries', retry_count)
        return

    headers['x-retry-count'] = retry_count + 1
    channel.basic_publish(
        exchange=method.exchange,  # republish where it came from — bindings re-route it
        routing_key=method.routing_key,
        body=body,
        properties=pika.BasicProperties(headers=headers),
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)
    logger.info('requeued with retry-count=%s', headers['x-retry-count'])


def process_message(channel, method, properties, body):
    try:
        message = json.loads(body)
        if handle_payment(message):
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            retry_or_dead_letter(channel, method, properties, body)
    except Exception as exc:
        logger.error('Failed to process message: %s', exc)
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


def main():
    conn = connect()
    channel = conn.channel()
    channel.basic_qos(prefetch_count=10, prefetch_global=False)
    channel.basic_consume(queue=QUEUE, on_message_callback=process_message, auto_ack=False)
    logger.info('Consuming %s — Ctrl+C to stop', QUEUE)
    channel.start_consuming()


if __name__ == '__main__':
    main()

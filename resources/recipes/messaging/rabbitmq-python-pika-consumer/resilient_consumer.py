"""Reconnection-safe RabbitMQ consumer that retries with a fixed delay."""

import json
import logging
import time

import pika

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResilientConsumer:
    def __init__(self, queue_name: str, host: str = "localhost", retry_delay: int = 5):
        self.queue_name = queue_name
        self.host = host
        self.retry_delay = retry_delay
        self._connection = None
        self._channel = None

    def connect(self) -> None:
        while True:
            try:
                self._connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.host,
                        heartbeat=30,
                        blocked_connection_timeout=7200,
                    )
                )
                self._channel = self._connection.channel()
                self._channel.queue_declare(queue=self.queue_name, durable=True)
                self._channel.basic_qos(prefetch_count=1)
                self._channel.basic_consume(
                    queue=self.queue_name,
                    on_message_callback=self.on_message,
                )
                logger.info("Connected and consuming...")
                self._channel.start_consuming()
                break
            except pika.exceptions.AMQPConnectionError:
                logger.warning("Connection lost, retrying in %ss...", self.retry_delay)
                time.sleep(self.retry_delay)
            except Exception as e:
                logger.error("Unexpected error: %s, retrying in %ss...", e, self.retry_delay)
                time.sleep(self.retry_delay)

    def on_message(self, channel, method, properties, body):
        try:
            message = json.loads(body)
 

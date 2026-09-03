"""RabbitMQ consumer patterns: work queue, pub/sub, RPC.

Run: python python_consumer_patterns.py
"""
import json
import uuid
import pika


def work_queue_consumer(channel):
    """Competing consumers — each message processed by exactly one consumer."""
    channel.basic_qos(prefetch_count=1)

    def process_task(ch, method, properties, body):
        try:
            task = json.loads(body)
            print(f"Processing task: {task}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue="tasks", on_message_callback=process_task)
    print("Work queue consumer started. Press Ctrl+C to stop.")
    channel.start_consuming()


def pubsub_consumer(channel, queue_name, exchange="notifications"):
    """Publish/subscribe consumer."""
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange=exchange, queue=queue_name)

    def on_message(ch, method, properties, body):
        print(f"[{queue_name}] Received: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    channel.start_consuming()


class RPCClient:
    """RPC request/reply pattern."""

    def __init__(self, connection_params="localhost"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(connection_params))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True,
        )
        self.response = None
        self.corr_id = None

    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message, timeout=5):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message),
        )
        import time
        start = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time() - start > timeout:
                raise TimeoutError("RPC call timed out")
        return json.loads(self.response)

    def close(self):
        self.connection.close()


def rpc_server(channel):
    """RPC server — processes requests and sends replies."""
    def on_request(ch, method, props, body):
        request = json.loads(body)
        response = {"result": f"processed {request}"}
        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=json.dumps(response),
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)
    print("RPC server started. Press Ctrl+C to stop.")
    channel.start_consuming()


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="tasks", durable=True)
    work_queue_consumer(channel)

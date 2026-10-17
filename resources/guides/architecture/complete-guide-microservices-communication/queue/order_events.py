import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue="order_created", durable=True)

# Producer — Order service publishes a message
def publish_order_created(order_id: str, customer_id: str):
    message = json.dumps({"order_id": order_id, "customer_id": customer_id})
    channel.basic_publish(
        exchange="",
        routing_key="order_created",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )

# Consumer — Shipping service processes the message
def consume_orders():
    def callback(ch, method, properties, body):
        order = json.loads(body)
        print(f"Shipping order {order['order_id']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="order_created", on_message_callback=callback)
    channel.start_consuming()

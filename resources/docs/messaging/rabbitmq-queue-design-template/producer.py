"""Publishes persistent order messages with publisher confirms enabled."""
import json

import pika
from declare_topology import connect, declare


def main():
    conn = connect()
    channel = conn.channel()
    declare(channel)
    channel.confirm_delivery()

    for order_id in range(1, 6):
        channel.basic_publish(
            exchange='prod.orders.order-created.direct',
            routing_key='order.payment.required',
            body=json.dumps({'order_id': order_id, 'amount': 49.99}),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type='application/json',
            ),
            mandatory=True,  # basic.return if unroutable
        )
        print(f'Published order {order_id}')

    conn.close()


if __name__ == '__main__':
    main()

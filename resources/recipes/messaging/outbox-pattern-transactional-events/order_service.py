from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
import uuid
from datetime import datetime

engine = create_engine('postgresql://user:pass@localhost/myapp')
Session = sessionmaker(bind=engine)

class OrderService:
    def __init__(self, session_factory):
        self.Session = session_factory

    def create_order(self, order_data: dict):
        session = self.Session()
        try:
            # Insert the order
            order_id = str(uuid.uuid4())
            session.execute(
                text("""INSERT INTO orders (id, customer_id, total, status)
                        VALUES (:id, :cid, :total, 'PENDING')"""),
                {'id': order_id, 'cid': order_data['customer_id'], 'total': order_data['total']}
            )

            # Insert the outbox event in the SAME transaction
            event_id = str(uuid.uuid4())
            session.execute(
                text("""INSERT INTO outbox_events
                        (id, aggregate_id, aggregate_type, event_type, payload, headers)
                        VALUES (:id, :aid, :atype, :etype, :payload, :headers)"""),
                {
                    'id': event_id,
                    'aid': order_id,
                    'atype': 'Order',
                    'etype': 'OrderCreated',
                    'payload': json.dumps({
                        'orderId': order_id,
                        'customerId': order_data['customer_id'],
                        'total': order_data['total'],
                        'items': order_data.get('items', []),
                    }),
                    'headers': json.dumps({
                        'event_id': event_id,
                        'source': 'order-service',
                    }),
                }
            )

            # Both inserts commit atomically — no dual-write problem
            session.commit()
            return order_id

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

"""CDC consumer — streams Debezium events from Kafka into Elasticsearch.

Commits offsets only after successful processing (at-least-once delivery);
upserts keyed by document ID keep the consumer idempotent.

Requires: kafka-python, elasticsearch
"""
import json
import logging

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CDCConsumer:
    def __init__(self, kafka_servers, es_host):
        self.consumer = KafkaConsumer(
            'shopdb.public.customers',
            bootstrap_servers=kafka_servers,
            group_id='es-sync',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.es = Elasticsearch(es_host)
        self.index_name = 'customers'

    def process_events(self):
        for message in self.consumer:
            event = message.value
            op = event.get('op')
            after = event.get('after')
            before = event.get('before')

            try:
                if op in ('c', 'u'):
                    self.es.index(
                        index=self.index_name,
                        id=after['id'],
                        document={
                            'email': after['email'],
                            'status': after['status'],
                            'updated_at': after.get('updated_at')
                        }
                    )
                    logger.info(f"Indexed customer {after['id']} (op={op})")
                elif op == 'd':
                    self.es.delete(
                        index=self.index_name,
                        id=before['id'],
                        ignore=[404]
                    )
                    logger.info(f"Deleted customer {before['id']}")

                self.consumer.commit()
            except Exception as e:
                logger.error(f"Failed to process event: {e}")

    def close(self):
        self.consumer.close()
        self.es.close()


if __name__ == '__main__':
    consumer = CDCConsumer(
        kafka_servers=['localhost:9092'],
        es_host='http://localhost:9200'
    )
    try:
        consumer.process_events()
    except KeyboardInterrupt:
        consumer.close()

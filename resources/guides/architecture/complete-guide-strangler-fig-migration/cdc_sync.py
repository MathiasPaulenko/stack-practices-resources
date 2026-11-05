# sync/cdc_sync.py — Sync data between legacy and new system databases
#
# Consumes Debezium-style change events from Kafka and replays them into the
# new system's store. Function definitions come BEFORE the consume loop —
# calling a function before its `def` executes raises NameError.
import json

from kafka import KafkaConsumer


class NewSystemClient:
    """Stub for the new system's data client. Replace with the real client."""

    def upsert_user(self, user: dict) -> None: ...

    def delete_user(self, user_id: str) -> None: ...


new_system_client = NewSystemClient()


def sync_user_to_new_system(user_data: dict) -> None:
    """Transform legacy user schema to new system schema."""
    new_user = {
        'id': user_data['user_id'],
        'email': user_data['email_address'],
        'firstName': user_data['fname'],
        'lastName': user_data['lname'],
        'createdAt': user_data['created_timestamp'],
        'status': 'active' if user_data['is_active'] == 1 else 'inactive',
    }
    new_system_client.upsert_user(new_user)


def delete_user_from_new_system(user_id: str) -> None:
    new_system_client.delete_user(user_id)


consumer = KafkaConsumer(
    'legacy-db-changes',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

for message in consumer:
    change = message.value
    table = change['table']
    operation = change['op']  # insert, update, delete

    if table == 'users':
        if operation in ('insert', 'update'):
            sync_user_to_new_system(change['after'])
        elif operation == 'delete':
            delete_user_from_new_system(change['before']['id'])

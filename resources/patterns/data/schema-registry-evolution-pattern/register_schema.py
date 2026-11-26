"""Register Avro schema versions with Confluent Schema Registry."""
import json

import requests

SCHEMA_REGISTRY_URL = "http://localhost:8081"


def register_schema(subject: str, schema_file: str) -> int:
    with open(schema_file) as f:
        schema = json.load(f)

    response = requests.post(
        f"{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions",
        headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        json={"schema": json.dumps(schema)},
    )

    if response.status_code == 200:
        version = response.json()["version"]
        schema_id = response.json()["id"]
        print(f"Registered {subject} v{version} (ID: {schema_id})")
        return schema_id

    print(f"Failed: {response.status_code} - {response.text}")
    response.raise_for_status()


if __name__ == "__main__":
    register_schema("customer-events-value", "customer-v1.avsc")
    register_schema("customer-events-value", "customer-v2.avsc")

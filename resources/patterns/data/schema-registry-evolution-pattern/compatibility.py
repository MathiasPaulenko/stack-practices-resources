"""Configure and check schema compatibility against Schema Registry."""
import json

import requests

SCHEMA_REGISTRY_URL = "http://localhost:8081"


def set_compatibility(subject: str, level: str) -> None:
    """Levels: NONE, BACKWARD, FORWARD, FULL, BACKWARD_TRANSITIVE, FORWARD_TRANSITIVE, FULL_TRANSITIVE."""
    response = requests.put(
        f"{SCHEMA_REGISTRY_URL}/config/{subject}",
        json={"compatibility": level},
    )
    print(f"Set {subject} compatibility to {level}: {response.status_code}")


def check_compatibility(subject: str, schema_file: str, version: str = "latest") -> dict:
    with open(schema_file) as f:
        schema = json.load(f)

    response = requests.post(
        f"{SCHEMA_REGISTRY_URL}/compatibility/subjects/{subject}/versions/{version}",
        headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        json={"schema": json.dumps(schema)},
    )

    result = response.json()
    if result.get("is_compatible"):
        print(f"Schema is compatible with {subject} {version}")
    else:
        print("Schema is NOT compatible:")
        for msg in result.get("messages", []):
            print(f"  - {msg}")
    return result


if __name__ == "__main__":
    set_compatibility("customer-events-value", "BACKWARD")
    check_compatibility("customer-events-value", "customer-v2.avsc")

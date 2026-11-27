# Example: Schema validation with JSON Schema
from jsonschema import validate, ValidationError
import json

ORDER_PLACED_SCHEMA = {
    "type": "object",
    "required": ["specversion", "type", "source", "id", "time", "data"],
    "properties": {
        "specversion": {"type": "string", "enum": ["1.0"]},
        "type": {"type": "string"},
        "source": {"type": "string"},
        "id": {"type": "string", "format": "uuid"},
        "time": {"type": "string", "format": "date-time"},
        "data": {
            "type": "object",
            "required": ["order_id", "customer_id", "total"],
            "properties": {
                "order_id": {"type": "string"},
                "customer_id": {"type": "string"},
                "total": {"type": "number", "minimum": 0},
                "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]}
            }
        }
    }
}

def validate_event(event):
    try:
        validate(instance=event, schema=ORDER_PLACED_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, str(e)

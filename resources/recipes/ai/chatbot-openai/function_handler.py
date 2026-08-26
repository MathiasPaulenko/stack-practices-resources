"""Function handler with validation and error handling for the Assistants API.

Shows how to validate function arguments and return structured errors.
"""
import json
from typing import Any


def get_order_status(order_id: str) -> str:
    """Mock order lookup — replace with your real backend."""
    if not order_id.startswith("ORD-"):
        return json.dumps(
            {"error": "invalid_order_id", "message": "Order ID must start with ORD-"}
        )
    return f"Order {order_id} is shipped and arriving tomorrow."


def handle_tool_call(tool_call: Any) -> dict:
    """Handle a single tool call with validation and error handling.

    Returns a dict ready for submit_tool_outputs.
    """
    try:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if name == "get_order_status":
            order_id = args.get("order_id", "")
            if not order_id:
                return {
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(
                        {"error": "missing_arg", "message": "order_id is required"}
                    ),
                }
            result = get_order_status(order_id)
            return {"tool_call_id": tool_call.id, "output": result}

        return {
            "tool_call_id": tool_call.id,
            "output": json.dumps(
                {"error": "unknown_function", "message": f"Unknown function: {name}"}
            ),
        }

    except json.JSONDecodeError:
        return {
            "tool_call_id": tool_call.id,
            "output": json.dumps(
                {"error": "invalid_args", "message": "Could not parse function arguments"}
            ),
        }
    except Exception as exc:
        # Never leak internal details to the assistant.
        return {
            "tool_call_id": tool_call.id,
            "output": json.dumps(
                {"error": "internal_error", "message": "Function execution failed"}
            ),
        }


MAX_RETRIES = 3


def submit_outputs_with_retry(client, thread_id, run_id, outputs, retries=0):
    """Submit tool outputs with a retry guard to prevent infinite loops."""
    if retries >= MAX_RETRIES:
        raise RuntimeError(f"Exceeded max retries ({MAX_RETRIES}) for run {run_id}")
    try:
        return client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id, run_id=run_id, tool_outputs=outputs
        )
    except Exception:
        return submit_outputs_with_retry(
            client, thread_id, run_id, outputs, retries + 1
        )

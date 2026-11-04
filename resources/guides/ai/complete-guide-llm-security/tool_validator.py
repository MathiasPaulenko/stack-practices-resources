"""Validate model-requested tool calls before executing them.

Least privilege per tool + argument allowlists + session scoping.
"""
import re

SAFE_TOOLS = {
    "get_order_status": {"user_id": "own_session", "order_id": r"^ORD-\d+$"},
    "search_docs": {"query": "str<=500"},
}


def validate_tool_call(name: str, args: dict) -> tuple[bool, str]:
    if name not in SAFE_TOOLS:
        return False, f"Tool not allowed: {name}"
    spec = SAFE_TOOLS[name]
    for field, rule in spec.items():
        value = args.get(field)
        if rule.startswith("^") and not re.match(rule, str(value or "")):
            return False, f"Invalid {field}: {value}"
    if args.get("user_id") not in (None, "own_session"):
        return False, "Cannot query other users' data"
    return True, ""


if __name__ == "__main__":
    for call in [
        ("get_order_status", {"order_id": "ORD-123"}),
        ("delete_all_users", {}),
        ("get_order_status", {"order_id": "*", "user_id": "admin"}),
    ]:
        print(call, "->", validate_tool_call(*call))

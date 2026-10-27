import json, time

def rotate(registry_path: str, owner: str, new_key: str, grace_days: int = 7) -> dict:
    """Mark old key with a valid_until window; both keys work until it lapses."""
    reg = json.load(open(registry_path))
    old = reg["keys"][owner]["api_key"]
    reg["keys"][owner] = {
        "api_key": new_key,
        "previous_key": {"value": old, "valid_until": int(time.time()) + grace_days * 86400},
    }
    json.dump(reg, open(registry_path, "w"), indent=2)
    return reg["keys"][owner]

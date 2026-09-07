"""Pipes and Filters Pattern — Python implementation.

Each filter is a pure function. The pipe composes them into a pipeline.
Run: python pipe_python.py
"""
from typing import Callable, Any

Filter = Callable[[Any], Any]


def pipe(*filters: Filter) -> Filter:
    def pipeline(data: Any) -> Any:
        result = data
        for f in filters:
            result = f(result)
        return result
    return pipeline


# Filters — each is a pure function
def parse_csv(raw: str) -> list[dict]:
    lines = raw.strip().split("\n")
    headers = lines[0].split(",")
    return [
        dict(zip(headers, line.split(",")))
        for line in lines[1:]
    ]


def filter_active(records: list[dict]) -> list[dict]:
    return [r for r in records if r.get("status") == "active"]


def normalize_emails(records: list[dict]) -> list[dict]:
    return [{**r, "email": r.get("email", "").lower().strip()} for r in records]


def deduplicate(records: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for r in records:
        key = r.get("email")
        if key not in seen:
            seen.add(key)
            result.append(r)
    return result


def to_json(records: list[dict]) -> str:
    import json
    return json.dumps(records, indent=2)


# Compose a pipeline
process_users = pipe(
    parse_csv,
    filter_active,
    normalize_emails,
    deduplicate,
    to_json,
)


if __name__ == "__main__":
    raw_data = """name,email,status
Alice,ALICE@Example.COM,active
Bob,bob@example.com,inactive
Charlie,CHARLIE@example.com,active
Alice,alice@example.com,active"""

    result = process_users(raw_data)
    print(result)

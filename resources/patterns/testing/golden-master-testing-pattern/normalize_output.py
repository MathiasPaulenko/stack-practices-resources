"""Normalize non-deterministic values before golden master comparison."""

import re


def normalize_output(output):
    """Remove non-deterministic elements from output."""
    output = re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z?",
        "<TIMESTAMP>",
        output,
    )
    output = re.sub(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "<UUID>",
        output,
    )
    output = re.sub(r'"id": \d+', '"id": <ID>', output)
    output = re.sub(r"/tmp/[^\s\"]+", "<TMP_PATH>", output)
    return output


if __name__ == "__main__":
    import sys
    data = sys.stdin.read()
    print(normalize_output(data))

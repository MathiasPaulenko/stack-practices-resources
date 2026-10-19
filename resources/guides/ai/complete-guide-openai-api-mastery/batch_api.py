"""Batch API: write JSONL, upload, submit, poll and download results."""
import json
import time

from openai import OpenAI

client = OpenAI()


def build_requests(reviews: list[str]) -> list[dict]:
    return [
        {
            "custom_id": f"request-{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "Classify the sentiment as positive, negative, or neutral.",
                    },
                    {"role": "user", "content": f"Review: {review}"},
                ],
            },
        }
        for i, review in enumerate(reviews)
    ]


def submit(reviews: list[str]) -> str:
    requests = build_requests(reviews)
    with open("batch_requests.jsonl", "w") as f:
        for req in requests:
            f.write(json.dumps(req) + "\n")

    batch_file = client.files.create(
        file=open("batch_requests.jsonl", "rb"), purpose="batch"
    )
    batch = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
    )
    print(f"Batch ID: {batch.id} ({batch.status})")
    return batch.id


def wait_and_download(batch_id: str) -> None:
    while True:
        batch = client.batches.retrieve(batch_id)
        print(f"Status: {batch.status}")
        if batch.status in {"completed", "failed", "cancelled", "expired"}:
            break
        time.sleep(60)

    if batch.status != "completed":
        return

    result_file = client.files.content(batch.output_file_id)
    for line in result_file.text.strip().split("\n"):
        result = json.loads(line)
        if result.get("error"):
            print(f"{result['custom_id']}: ERROR {result['error']}")
        else:
            content = result["response"]["body"]["choices"][0]["message"]["content"]
            print(f"{result['custom_id']}: {content}")


if __name__ == "__main__":
    sample_reviews = ["Loved it!", "Terrible packaging.", "It's okay, nothing special."]
    batch_id = submit(sample_reviews)
    # wait_and_download(batch_id)  # uncomment for a real run

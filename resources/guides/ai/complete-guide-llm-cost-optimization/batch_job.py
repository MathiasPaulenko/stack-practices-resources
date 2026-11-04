"""OpenAI Batch API: 50% off for 24h-turnaround jobs."""
import json
from openai import OpenAI

client = OpenAI()


def prepare_batch(prompts: list[str], model: str = "gpt-4o-mini") -> str:
    requests = [{
        "custom_id": f"task-{i}", "method": "POST", "url": "/v1/chat/completions",
        "body": {"model": model, "messages": [{"role": "user", "content": p}]}
    } for i, p in enumerate(prompts)]
    with open("batch_requests.jsonl", "w") as f:
        for req in requests:
            f.write(json.dumps(req) + "\n")
    return client.files.create(file=open("batch_requests.jsonl", "rb"), purpose="batch").id


def submit_batch(file_id: str) -> str:
    return client.batches.create(
        input_file_id=file_id, endpoint="/v1/chat/completions", completion_window="24h").id


def get_results(batch_id: str) -> list[dict]:
    batch = client.batches.retrieve(batch_id)
    if batch.status != "completed":
        return []
    out = []
    for line in client.files.content(batch.output_file_id).text.strip().split("\n"):
        r = json.loads(line)
        if not r.get("error"):
            out.append({"custom_id": r["custom_id"],
                        "content": r["response"]["body"]["choices"][0]["message"]["content"]})
    return out

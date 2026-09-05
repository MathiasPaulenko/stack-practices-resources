"""Benchmark LLM inference performance."""

import time
import requests
from concurrent.futures import ThreadPoolExecutor


def benchmark(url: str, model: str, prompt: str, n: int = 10) -> dict:
    def request():
        start = time.perf_counter()
        response = requests.post(
            f"{url}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
        )
        latency = time.perf_counter() - start
        tokens = response.json()["usage"]["completion_tokens"]
        return latency, tokens

    with ThreadPoolExecutor(max_workers=1) as executor:
        results = list(executor.map(lambda _: request(), range(n)))

    latencies = [r[0] for r in results]
    tokens = [r[1] for r in results]
    total_time = sum(latencies)

    return {
        "tokens_per_second": sum(tokens) / total_time,
        "avg_latency_s": sum(latencies) / len(latencies),
        "p95_latency_s": sorted(latencies)[int(len(latencies) * 0.95)],
    }


if __name__ == "__main__":
    print(benchmark("http://localhost:11434", "llama3.1:8b",
                    "Write a 200-word essay about AI."))
    print(benchmark("http://localhost:8000", "meta-llama/Llama-3.1-8B-Instruct",
                    "Write a 200-word essay about AI."))

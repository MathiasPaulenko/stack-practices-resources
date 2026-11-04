"""Hallucination detection: self-consistency + source verification."""
import json

from openai import AsyncOpenAI

client = AsyncOpenAI()


async def self_consistency_check(question: str, n: int = 3) -> dict:
    responses = []
    for _ in range(n):
        r = await client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": question}],
            temperature=0.7)
        responses.append(r.choices[0].message.content)
    prompt = f"""Are these responses factually consistent with each other?

    Response 1: {responses[0]}
    Response 2: {responses[1]}
    Response 3: {responses[2]}

    Return JSON: {{"consistent": true/false, "differences": ["..."], "confidence": 0-1}}"""
    check = await client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}, temperature=0.0)
    return json.loads(check.choices[0].message.content)


async def fact_check_with_sources(answer: str, sources: list[str]) -> dict:
    prompt = f"""Verify each claim in the answer against the provided sources.

    Answer: {answer}

    Sources:
    {chr(10).join(f"[{i + 1}] {s}" for i, s in enumerate(sources))}

    Return JSON:
    {{"claims": [{{"claim": "...", "supported": true/false, "source": N or null}}], "hallucination_rate": 0-1}}"""
    r = await client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}, temperature=0.0)
    return json.loads(r.choices[0].message.content)

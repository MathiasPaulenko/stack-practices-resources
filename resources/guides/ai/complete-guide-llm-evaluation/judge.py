"""LLM-as-judge: rubric scoring + unbiased pairwise comparison."""
import json
import random

from openai import AsyncOpenAI

client = AsyncOpenAI()

JUDGE_PROMPT = """You are an expert evaluator. Rate the quality of an AI assistant's response.

Question: {question}
Response: {response}
Reference Answer: {reference}

Evaluate on these criteria (0-10 each):
1. Accuracy: Is the response factually correct?
2. Completeness: Does it cover all important aspects?
3. Clarity: Is it clear and well-structured?
4. Helpfulness: Is it useful to the user?

Return JSON: {{"accuracy": N, "completeness": N, "clarity": N, "helpfulness": N, "aggregate": N, "reasoning": "..."}}"""

PAIRWISE_PROMPT = """Compare two AI responses to the same question. Choose the better one.

Question: {question}

Response A: {response_a}
Response B: {response_b}

Criteria: accuracy, completeness, clarity, helpfulness.

Which response is better? Return JSON:
{{"winner": "A" or "B" or "tie", "reasoning": "..."}}"""


async def llm_judge(question: str, response: str, reference: str) -> dict:
    prompt = JUDGE_PROMPT.format(question=question, response=response, reference=reference)
    r = await client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}, temperature=0.0)
    return json.loads(r.choices[0].message.content)


async def pairwise_compare(question: str, response_a: str, response_b: str) -> dict:
    prompt = PAIRWISE_PROMPT.format(
        question=question, response_a=response_a, response_b=response_b)
    r = await client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}, temperature=0.0)
    return json.loads(r.choices[0].message.content)


async def unbiased_pairwise_compare(question: str, response_a: str, response_b: str) -> dict:
    """Randomize order to reduce position bias."""
    if random.random() > 0.5:
        return await pairwise_compare(question, response_a, response_b)
    result = await pairwise_compare(question, response_b, response_a)
    if result["winner"] == "A":
        result["winner"] = "B"
    elif result["winner"] == "B":
        result["winner"] = "A"
    return result


async def robust_compare(question: str, response_a: str, response_b: str, n: int = 5) -> dict:
    """Run n unbiased comparisons and aggregate."""
    results = []
    for _ in range(n):
        r = await unbiased_pairwise_compare(question, response_a, response_b)
        results.append(r["winner"])
    a, b, t = results.count("A"), results.count("B"), results.count("tie")
    if a > b:
        return {"winner": "A", "confidence": a / n, "details": {"A": a, "B": b, "tie": t}}
    if b > a:
        return {"winner": "B", "confidence": b / n, "details": {"A": a, "B": b, "tie": t}}
    return {"winner": "tie", "confidence": t / n, "details": {"A": a, "B": b, "tie": t}}

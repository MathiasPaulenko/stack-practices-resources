"""Self-consistency: sample CoT n times, take the majority answer.

Requires OPENAI_API_KEY. Costs n calls per question — reserve for
decisions where a wrong answer is expensive.
"""
import re
from collections import Counter

from openai import OpenAI

client = OpenAI()


def extract_final_answer(text: str) -> str:
    """Pull the answer after the agreed 'Final answer:' marker."""
    match = re.search(r"final answer:\s*(.+)", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


def self_consistent_answer(prompt: str, n: int = 5, model: str = "gpt-4o") -> str:
    answers = []
    for _ in range(n):
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # nonzero: we want diverse reasoning paths
        )
        answers.append(extract_final_answer(response.choices[0].message.content))
    return Counter(answers).most_common(1)[0][0]


if __name__ == "__main__":
    question = (
        "A store sells apples at $2 each and oranges at $3 each. "
        "A customer buys 5 apples and 3 oranges and pays with a $50 bill. "
        "Work step by step, then write 'Final answer: $X'."
    )
    print(self_consistent_answer(question, n=5))

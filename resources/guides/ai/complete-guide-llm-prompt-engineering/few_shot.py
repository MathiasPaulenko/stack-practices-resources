"""Zero-shot and few-shot sentiment classification.

Requires OPENAI_API_KEY. Run: python few_shot.py
"""
from openai import OpenAI

client = OpenAI()

ZERO_SHOT = """Classify the sentiment of this review as positive, negative, or neutral:
"{review}\""""

FEW_SHOT = """Classify the sentiment of each review:

Review: "Amazing product, fast delivery!"
Sentiment: positive

Review: "Worst purchase ever."
Sentiment: negative

Review: "It works as expected."
Sentiment: neutral

Review: "{review}"
Sentiment:"""


def classify(review: str, few_shot: bool = True) -> str:
    prompt = (FEW_SHOT if few_shot else ZERO_SHOT).format(review=review)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    sample = "The product arrived late and the quality was terrible."
    print("zero-shot:", classify(sample, few_shot=False))
    print("few-shot :", classify(sample))

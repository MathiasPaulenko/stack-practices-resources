"""Classify sentiment into positive, negative, or neutral labels."""
import nltk
nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def classify_sentiment(text: str) -> str:
    """Classify text sentiment using VADER compound score.

    Args:
        text: Input text to classify.

    Returns:
        One of 'positive', 'negative', or 'neutral'.
    """
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"


if __name__ == "__main__":
    texts = [
        "Great service and fast delivery!",
        "The package arrived broken.",
        "It was okay, nothing special.",
    ]

    for text in texts:
        label = classify_sentiment(text)
        print(f"{label:10s} | {text}")

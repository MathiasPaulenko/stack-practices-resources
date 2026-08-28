"""Track sentiment trends over time."""
import statistics

import nltk
nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def daily_sentiment(posts: list[dict]) -> dict[str, float]:
    """Compute average daily sentiment from a list of posts.

    Args:
        posts: List of dicts with 'date' and 'text' keys.

    Returns:
        Dict mapping date string to average compound score.
    """
    daily_scores: dict[str, list[float]] = {}
    for post in posts:
        date = post["date"]
        score = sia.polarity_scores(post["text"])["compound"]
        daily_scores.setdefault(date, []).append(score)

    return {
        date: statistics.mean(scores)
        for date, scores in sorted(daily_scores.items())
    }


if __name__ == "__main__":
    posts = [
        {"date": "2026-01-01", "text": "Love the new update!"},
        {"date": "2026-01-02", "text": "Found a bug in the login flow."},
        {"date": "2026-01-03", "text": "Bug is fixed, great support!"},
    ]

    averages = daily_sentiment(posts)
    for date, avg in averages.items():
        print(f"{date}: avg={avg:.3f}")

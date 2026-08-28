"""Batch process sentiment scoring from a CSV file."""
import csv

import nltk
nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def score_csv(input_path: str, output_path: str, text_column: str = "review") -> int:
    """Read a CSV, score each row's sentiment, and write results.

    Args:
        input_path: Path to input CSV.
        output_path: Path to output CSV.
        text_column: Name of the column containing text to score.

    Returns:
        Number of rows processed.
    """
    count = 0
    with open(input_path, newline="", encoding="utf-8") as infile, \
         open(output_path, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(
            outfile,
            fieldnames=reader.fieldnames + ["sentiment", "compound"],
        )
        writer.writeheader()

        for row in reader:
            score = sia.polarity_scores(row[text_column])
            row["compound"] = score["compound"]
            if score["compound"] >= 0.05:
                row["sentiment"] = "positive"
            elif score["compound"] <= -0.05:
                row["sentiment"] = "negative"
            else:
                row["sentiment"] = "neutral"
            writer.writerow(row)
            count += 1

    return count


if __name__ == "__main__":
    n = score_csv("reviews.csv", "scored.csv")
    print(f"Processed {n} rows")

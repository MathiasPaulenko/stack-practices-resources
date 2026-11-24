"""Demo: extract a structured ProductReview from free text."""
import logging

from structured_extract import extract_resilient

logging.basicConfig(level=logging.INFO)

REVIEW = (
    "The headphones sound great and battery lasts forever. "
    "However, the case is bulky. I'd recommend them to anyone."
)

if __name__ == "__main__":
    review = extract_resilient(REVIEW)
    print(f"Rating: {review.rating}/5")
    print(f"Summary: {review.summary}")
    print(f"Pros: {review.pros}")
    print(f"Cons: {review.cons}")
    print(f"Recommended: {review.would_recommend}")

"""Structured JSON extraction from OpenAI with function calling and Pydantic."""
import json
import logging
import time
from pydantic import BaseModel, Field
from openai import OpenAI, RateLimitError

logger = logging.getLogger(__name__)
client = OpenAI()


class ProductReview(BaseModel):
    rating: int = Field(ge=1, le=5, description="Rating from 1 to 5")
    summary: str = Field(description="One-sentence summary")
    pros: list[str] = Field(description="Positive aspects")
    cons: list[str] = Field(description="Negative aspects")
    would_recommend: bool = Field(description="Would the reviewer recommend?")


class SearchQuery(BaseModel):
    query: str = Field(description="Search query")
    filters: dict = Field(description="Metadata filters", default={})


class CalculationRequest(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate")


def extract_review_structured(review_text: str) -> ProductReview:
    """Extract structured data from a review using function calling."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured review data."},
            {"role": "user", "content": review_text},
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "submit_review",
                "description": "Submit a structured product review",
                "parameters": ProductReview.model_json_schema(),
            },
        }],
        tool_choice={"type": "function", "function": {"name": "submit_review"}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return ProductReview.model_validate(json.loads(tool_call.function.arguments))


def extract_with_response_format(review_text: str) -> ProductReview:
    """Use response_format for guaranteed JSON schema compliance."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured review data as JSON."},
            {"role": "user", "content": review_text},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ProductReview",
                "schema": ProductReview.model_json_schema(),
                "strict": True,
            },
        },
    )
    return ProductReview.model_validate_json(response.choices[0].message.content)


def extract_resilient(review_text: str, max_attempts: int = 3) -> ProductReview:
    """Extraction with backoff on RateLimitError, refusal handling, and Pydantic validation."""
    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Extract structured review data as JSON."},
                    {"role": "user", "content": review_text},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "ProductReview",
                        "schema": ProductReview.model_json_schema(),
                        "strict": True,
                    },
                },
            )
        except RateLimitError:
            time.sleep(2 ** attempt)
            continue

        message = response.choices[0].message
        if message.refusal:
            raise ValueError(f"Model refused: {message.refusal}")
        try:
            return ProductReview.model_validate_json(message.content)
        except Exception as e:
            logger.warning("Attempt %d failed validation: %s", attempt + 1, e)

    raise ValueError("Extraction failed after retries")


def extract_batch(reviews: list[str]) -> list[ProductReview | None]:
    """Extract structured data from multiple reviews; failures become None."""
    results = []
    for review_text in reviews:
        try:
            results.append(extract_resilient(review_text))
        except ValueError as e:
            logger.error("Failed to extract review: %s", e)
            results.append(None)
    return results

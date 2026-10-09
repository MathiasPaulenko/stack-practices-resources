"""Generate URL-friendly slugs from arbitrary strings.

NFKD normalization strips accents, ASCII folding removes diacritics,
and an optional uniqueness check appends -2, -3, ... on collisions.
"""

import re
import unicodedata


def generate_slug(text: str, existing_slugs: set | None = None, max_length: int = 100) -> str:
    """Return a URL-safe slug for `text`, optionally unique against `existing_slugs`."""
    # Normalize unicode and remove accents
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # Lowercase and replace non-alphanumeric with hyphens
    text = re.sub(r"[^\w\s-]", "", text.lower())
    # Collapse multiple hyphens/whitespace and trim
    text = re.sub(r"[-\s]+", "-", text).strip("-_")
    text = text[:max_length].rstrip("-")

    if existing_slugs is None:
        return text

    base = text
    counter = 2
    while text in existing_slugs:
        suffix = f"-{counter}"
        text = base[: max_length - len(suffix)] + suffix
        counter += 1
    return text


if __name__ == "__main__":
    print(generate_slug("Hello, World! 2024"))   # hello-world-2024
    print(generate_slug("Café & Crème Brûlée"))  # cafe-creme-brulee

    existing = {"hello-world", "hello-world-2"}
    print(generate_slug("Hello World", existing))  # hello-world-3

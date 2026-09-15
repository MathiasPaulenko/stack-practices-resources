"""Text cleaning utilities for RAG data preparation."""

import re


def clean_text(text: str) -> str:
    """Remove HTML, normalize whitespace, fix encoding."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    return text.strip()


def remove_boilerplate(text: str, min_length: int = 100) -> str:
    """Remove navigation menus, footers, and headers by line length."""
    lines = text.split('\n')
    meaningful = [l for l in lines if len(l.strip()) > min_length]
    return '\n'.join(meaningful)


if __name__ == "__main__":
    sample = "<nav>Home</nav>\n<p>This is a real paragraph with enough text to survive the boilerplate filter.</p>"
    cleaned = remove_boilerplate(clean_text(sample))
    print(cleaned)

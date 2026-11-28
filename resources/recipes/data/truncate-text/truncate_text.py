"""Text truncation helpers: character slice and word-boundary via textwrap."""
import textwrap


def truncate(text: str, max_length: int = 100) -> str:
    """Cut at max_length characters, ellipsis included in the budget."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3].rstrip() + '...'


def truncate_words(text: str, max_length: int = 100) -> str:
    """Cut at the last word boundary inside max_length."""
    return textwrap.shorten(text, width=max_length, placeholder='...')


if __name__ == '__main__':
    s = "This is a very long sentence that needs to be shortened."
    print(truncate(s, 50))
    print(truncate_words(s, 50))

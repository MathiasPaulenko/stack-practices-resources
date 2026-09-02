"""CSV injection sanitization utilities."""

DANGEROUS_PREFIXES = ("=", "+", "-", "@")


def sanitize_csv_cell(value: str) -> str:
    """Prefix dangerous characters to prevent CSV injection in Excel."""
    if value and value[0] in DANGEROUS_PREFIXES:
        return f"'{value}"
    return value


def sanitize_row(row: dict) -> dict:
    """Sanitize all string values in a row dict."""
    return {k: sanitize_csv_cell(str(v)) if isinstance(v, str) else v for k, v in row.items()}


if __name__ == "__main__":
    # Test cases
    assert sanitize_csv_cell("=cmd|' /C calc'!A0") == "'=cmd|' /C calc'!A0"
    assert sanitize_csv_cell("normal text") == "normal text"
    assert sanitize_csv_cell("+123") == "'+123"
    assert sanitize_csv_cell("-50") == "'-50"
    assert sanitize_csv_cell("@mention") == "'@mention"
    assert sanitize_csv_cell("") == ""
    assert sanitize_csv_cell(None) is None
    print("All tests passed.")

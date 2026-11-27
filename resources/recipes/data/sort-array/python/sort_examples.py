"""Sorting examples from the sort-array recipe."""


def by_age_then_name(users: list[dict]) -> list[dict]:
    """Multi-key sort: age first, ties broken alphabetically."""
    return sorted(users, key=lambda u: (u["age"], u["name"]))


def locale_sorted(names: list[str]) -> list[str]:
    """Locale-aware sort for user-facing strings."""
    import locale
    return sorted(names, key=locale.strxfrm)


def sort_nulls_last(values: list) -> list:
    """Push None to the end instead of crashing the comparison."""
    return sorted(values, key=lambda v: (v is None, v))

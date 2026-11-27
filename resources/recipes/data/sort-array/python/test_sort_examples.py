from sort_examples import by_age_then_name, locale_sorted, sort_nulls_last


def test_multi_key_sort():
    users = [
        {"name": "Bob", "age": 30},
        {"name": "Ada", "age": 30},
        {"name": "Chen", "age": 25},
    ]
    assert [u["name"] for u in by_age_then_name(users)] == ["Chen", "Ada", "Bob"]


def test_nulls_last():
    assert sort_nulls_last([3, None, 1, None]) == [1, 3, None, None]


def test_locale_sort():
    assert locale_sorted(["apple", "Álvaro", "banana"]) == ["Álvaro", "apple", "banana"]

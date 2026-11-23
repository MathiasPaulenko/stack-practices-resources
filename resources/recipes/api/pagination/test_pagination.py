from pagination import get_users_cursor, get_users_offset, walk_all_pages, USERS


def test_offset_first_page():
    page = get_users_offset(page=1, page_size=10)
    assert [u["id"] for u in page] == list(range(1, 11))


def test_offset_deep_page():
    page = get_users_offset(page=10, page_size=10)
    assert [u["id"] for u in page] == list(range(91, 101))


def test_cursor_first_page_no_cursor():
    page = get_users_cursor(cursor=None, page_size=10)
    assert page["items"][0]["id"] == 1
    assert page["has_more"] is True
    assert page["next_cursor"] == 10


def test_cursor_walk_covers_everything_once():
    seen = walk_all_pages(page_size=7)
    assert [u["id"] for u in seen] == [u["id"] for u in USERS]


def test_cursor_last_page_no_more():
    page = get_users_cursor(cursor=95, page_size=10)
    assert len(page["items"]) == 5
    assert page["has_more"] is False
    assert page["next_cursor"] is None


def test_cursor_past_end_is_empty():
    page = get_users_cursor(cursor=999, page_size=10)
    assert page["items"] == [] and page["has_more"] is False


def test_offset_rejects_bad_params():
    for bad in (0, -1):
        try:
            get_users_offset(page=bad, page_size=10)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")

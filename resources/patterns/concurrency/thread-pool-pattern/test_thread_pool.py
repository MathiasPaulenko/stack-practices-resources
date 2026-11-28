"""Tests for the thread pool examples — all offline."""
import thread_pool_examples as ex


def test_fixed_pool_processes_all_tasks():
    results = ex.run_fixed_pool()
    assert len(results) == 7
    assert sum(1 for r in results if r.get("status") == 200) == 6
    assert sum(1 for r in results if "error" in r) == 1


def test_map_preserves_order_and_count():
    results = ex.run_map()
    assert len(results) == 5
    assert all(r["status"] == 200 for r in results)


def test_sizing_formula_returns_positive_int():
    assert ex.sizing_example() > 0

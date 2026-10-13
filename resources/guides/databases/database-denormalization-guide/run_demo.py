#!/usr/bin/env python3
"""Run the denormalization demo against an in-memory SQLite database."""
import sqlite3
from pathlib import Path

sql = Path(__file__).with_name("denormalization_demo.sql").read_text()
conn = sqlite3.connect(":memory:")
conn.executescript(sql)

print("posts:", conn.execute("SELECT post_id, title, like_count FROM posts").fetchall())
print("order_items:", conn.execute(
    "SELECT item_id, quantity, unit_price, line_total FROM order_items"
).fetchall())
print("summary:", conn.execute("SELECT * FROM daily_order_summary").fetchall())
drift = conn.execute(
    """
    SELECT p.post_id, p.like_count,
           (SELECT COUNT(*) FROM post_likes l WHERE l.post_id = p.post_id) AS fresh,
           p.like_count - (SELECT COUNT(*) FROM post_likes l WHERE l.post_id = p.post_id) AS drift
    FROM posts p
    """
).fetchall()
print("drift check:", drift)
assert all(row[3] == 0 for row in drift), "drift detected — sync is broken"
print("OK: stored counters match fresh COUNT(*)")

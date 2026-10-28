"""Conditional SQL query construction with a fluent QueryBuilder."""


class QueryBuilder:
    def __init__(self):
        self.conditions = []
        self.joins = []
        self._order_by = None
        self._limit = None

    def where(self, condition):
        self.conditions.append(condition)
        return self

    def join(self, table, on_clause):
        self.joins.append((table, on_clause))
        return self

    def order_by(self, field, direction="ASC"):
        self._order_by = (field, direction)
        return self

    def limit(self, count):
        self._limit = count
        return self

    def build(self):
        query = "SELECT * FROM items"
        if self.joins:
            for table, on_clause in self.joins:
                query += f" JOIN {table} ON {on_clause}"
        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        if self._order_by:
            query += f" ORDER BY {self._order_by[0]} {self._order_by[1]}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query


if __name__ == "__main__":
    include_active_only = True
    sort_by_date = True
    max_results = 50

    builder = QueryBuilder()
    builder.join("users", "items.user_id = users.id")

    if include_active_only:
        builder.where("users.active = true")

    if sort_by_date:
        builder.order_by("created_at", "DESC")

    if max_results:
        builder.limit(max_results)

    print(builder.build())
    # SELECT * FROM items JOIN users ON items.user_id = users.id
    # WHERE users.active = true ORDER BY created_at DESC LIMIT 50

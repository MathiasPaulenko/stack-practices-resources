"""Extract column-level lineage from SQL with sqlglot.

Requires: pip install sqlglot
"""
import sqlglot
from sqlglot import exp


def extract_column_lineage(sql, source_table, target_table):
    """Parse SQL and extract column-level lineage."""
    parsed = sqlglot.parse_one(sql)
    lineage = {}

    for select in parsed.find_all(exp.Select):
        # select.expressions are the projection items; the alias (or the
        # column name when there's no alias) is the output column.
        for expr in select.expressions:
            target_col = expr.alias_or_name

            for column in expr.find_all(exp.Column):
                lineage.setdefault(target_col, []).append({
                    "source_table": column.table or source_table,
                    "source_column": column.name
                })

    return lineage


if __name__ == "__main__":
    sql = """
    SELECT
        id,
        LOWER(email) AS email,
        status = 'active' AS is_active,
        CONCAT(first_name, ' ', last_name) AS full_name
    FROM source.customers
    """

    lineage = extract_column_lineage(sql, "source.customers", "warehouse.customers")
    # {
    #   "id": [{"source_table": "source.customers", "source_column": "id"}],
    #   "email": [{"source_table": "source.customers", "source_column": "email"}],
    #   "is_active": [{"source_table": "source.customers", "source_column": "status"}],
    #   "full_name": [{"source_table": "source.customers", "source_column": "first_name"},
    #                 {"source_table": "source.customers", "source_column": "last_name"}]
    # }
    import json
    print(json.dumps(lineage, indent=2))

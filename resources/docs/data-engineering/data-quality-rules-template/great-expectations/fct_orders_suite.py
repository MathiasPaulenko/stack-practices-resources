import great_expectations as gx

suite = gx.ExpectationSuite("fct_orders_suite")

## Completeness
suite.add_expectation(gx.expect_column_values_to_not_be_null(column="order_id"))
suite.add_expectation(gx.expect_column_values_to_not_be_null(column="customer_id"))
suite.add_expectation(gx.expect_column_values_to_not_be_null(column="order_date"))
suite.add_expectation(gx.expect_column_values_to_not_be_null(column="total_amount"))

## Uniqueness
suite.add_expectation(gx.expect_column_values_to_be_unique(column="order_id"))

## Validity
suite.add_expectation(gx.expect_column_values_to_match_regex(
    column="order_id",
    regex=r"^ord_[a-zA-Z0-9]{5,60}$"
))
suite.add_expectation(gx.expect_column_values_to_be_in_set(
    column="status",
    value_set=["pending", "processing", "completed", "cancelled", "refunded"]
))
suite.add_expectation(gx.expect_column_values_to_be_in_set(
    column="currency",
    value_set=["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "BRL", "MXN"]
))

## Accuracy
suite.add_expectation(gx.expect_column_values_to_be_between(
    column="total_amount",
    min_value=0.01,
    max_value=100000
))
suite.add_expectation(gx.expect_column_values_to_be_between(
    column="order_date",
    min_value="2021-01-01",
    max_value="2026-12-31"
))

## Consistency
suite.add_expectation(gx.expect_column_pair_values_A_to_be_greater_than_B(
    column_A="total_amount",
    column_B="refund_amount",
    or_equal=True,
    row_condition="status == 'refunded'",
    condition_parser="pandas"
))

## Dataset-level
suite.add_expectation(gx.expect_table_row_count_to_be_between(min_value=100000, max_value=10000000))

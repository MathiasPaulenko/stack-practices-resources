# Data Quality Rules — `<Dataset Name>`

## Rules Overview

| Field | Value |
|-------|-------|
| Dataset | fct_orders |
| Schema | marts |
| Database | analytics |
| Owner | Data Platform Team |
| Last Updated | 2026-07-05 |
| Total Rules | 28 |
| Critical Rules | 12 |
| Warning Rules | 16 |
| Framework | dbt tests + Great Expectations |
| Execution | Post-load, pre-consumer access |

## 1. Quality Dimensions

| Dimension | Description | Example |
|-----------|-------------|---------|
| Completeness | Required fields are not null | order_id must never be null |
| Consistency | Data conforms to expected format and relationships | currency must be valid ISO 4217 code |
| Accuracy | Values fall within expected ranges | total_amount must be positive |
| Timeliness | Data is fresh enough for its purpose | Data must be < 24 hours old |
| Uniqueness | No duplicate records | order_id must be unique |
| Validity | Values match expected patterns | email must match regex pattern |

## 2. Column-Level Rules

### order_id

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-001 | Not null | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE order_id IS NULL` | Fail pipeline |
| DQ-002 | Unique | Uniqueness | Critical | `SELECT order_id, COUNT(*) FROM fct_orders GROUP BY order_id HAVING COUNT(*) > 1` | Fail pipeline |
| DQ-003 | Format: starts with "ord_" | Validity | Critical | `SELECT COUNT(*) FROM fct_orders WHERE order_id NOT LIKE 'ord_%'` | Fail pipeline |
| DQ-004 | Length between 8 and 64 chars | Validity | Warning | `SELECT COUNT(*) FROM fct_orders WHERE LENGTH(order_id) < 8 OR LENGTH(order_id) > 64` | Log + proceed |

### customer_id

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-005 | Not null | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE customer_id IS NULL` | Fail pipeline |
| DQ-006 | Exists in dim_customers | Consistency | Critical | `SELECT COUNT(*) FROM fct_orders o LEFT JOIN dim_customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL` | Fail pipeline |
| DQ-007 | Format: starts with "cus_" | Validity | Warning | `SELECT COUNT(*) FROM fct_orders WHERE customer_id NOT LIKE 'cus_%'` | Log + proceed |

### order_date

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-008 | Not null | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE order_date IS NULL` | Fail pipeline |
| DQ-009 | Not in future | Accuracy | Critical | `SELECT COUNT(*) FROM fct_orders WHERE order_date > CURRENT_TIMESTAMP` | Fail pipeline |
| DQ-010 | Not older than 5 years | Accuracy | Warning | `SELECT COUNT(*) FROM fct_orders WHERE order_date < DATEADD(year, -5, CURRENT_DATE)` | Log + proceed |
| DQ-011 | Date matches partition | Consistency | Warning | `SELECT COUNT(*) FROM fct_orders WHERE DATE(order_date) != partition_date` | Log + proceed |

### status

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-012 | Not null | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE status IS NULL` | Fail pipeline |
| DQ-013 | Valid enum value | Validity | Critical | `SELECT COUNT(*) FROM fct_orders WHERE status NOT IN ('pending', 'processing', 'completed', 'cancelled', 'refunded')` | Fail pipeline |

### total_amount

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-014 | Not null | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE total_amount IS NULL` | Fail pipeline |
| DQ-015 | Greater than 0 | Accuracy | Critical | `SELECT COUNT(*) FROM fct_orders WHERE total_amount <= 0` | Fail pipeline |
| DQ-016 | Less than 100000 | Accuracy | Warning | `SELECT COUNT(*) FROM fct_orders WHERE total_amount >= 100000` | Log + proceed |
| DQ-017 | Matches sum of line items | Consistency | Critical | `SELECT COUNT(*) FROM fct_orders o JOIN fct_order_items i ON o.order_id = i.order_id GROUP BY o.order_id HAVING o.total_amount != SUM(i.line_total)` | Fail pipeline |

### currency

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-018 | Not null | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE currency IS NULL` | Fail pipeline |
| DQ-019 | Valid ISO 4217 code | Validity | Critical | `SELECT COUNT(*) FROM fct_orders WHERE currency NOT IN ('USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'BRL', 'MXN')` | Fail pipeline |
| DQ-020 | Length is 3 | Validity | Warning | `SELECT COUNT(*) FROM fct_orders WHERE LENGTH(currency) != 3` | Log + proceed |

### payment_method

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-021 | Not null when status = completed | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders WHERE status = 'completed' AND payment_method IS NULL` | Fail pipeline |
| DQ-022 | Valid enum value | Validity | Warning | `SELECT COUNT(*) FROM fct_orders WHERE payment_method NOT IN ('credit_card', 'debit_card', 'paypal', 'bank_transfer', 'crypto', 'apple_pay', 'google_pay')` | Log + proceed |

## 3. Dataset-Level Rules

| Rule ID | Rule | Type | Severity | SQL | Action on Failure |
|---------|------|------|----------|-----|-------------------|
| DQ-023 | Row count > 0 | Completeness | Critical | `SELECT COUNT(*) FROM fct_orders` (must be > 0) | Fail pipeline |
| DQ-024 | Row count within expected range | Accuracy | Warning | `SELECT COUNT(*) FROM fct_orders` (must be between 100k and 10M) | Log + proceed |
| DQ-025 | Data is fresh (< 24h) | Timeliness | Critical | `SELECT MAX(_ingested_at) FROM fct_orders` (must be < 24h ago) | Fail pipeline |
| DQ-026 | No orphaned records | Consistency | Critical | `SELECT COUNT(*) FROM fct_orders o LEFT JOIN dim_customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL` | Fail pipeline |
| DQ-027 | All completed orders have payment events | Consistency | Warning | `SELECT COUNT(*) FROM fct_orders o WHERE o.status = 'completed' AND NOT EXISTS (SELECT 1 FROM fct_payment_events p WHERE p.order_id = o.order_id)` | Log + proceed |
| DQ-028 | Refund amounts don't exceed original | Accuracy | Critical | `SELECT COUNT(*) FROM fct_orders WHERE status = 'refunded' AND refund_amount > total_amount` | Fail pipeline |

## 4. dbt Test Configuration

### YAML Schema File

```yaml
version: 2

models:
  - name: fct_orders
    description: "Fact table containing all customer orders"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - not_null
          - unique
          - accepted_values:
              values: ["ord_%"]
              quote: false

      - name: customer_id
        description: "Customer reference"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: order_date
        description: "Order placement timestamp"
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: "order_date <= CURRENT_TIMESTAMP"

      - name: status
        description: "Order status"
        tests:
          - not_null
          - accepted_values:
              values: ['pending', 'processing', 'completed', 'cancelled', 'refunded']

      - name: total_amount
        description: "Order total in original currency"
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: "total_amount > 0"
          - dbt_utils.expression_is_true:
              expression: "total_amount < 100000"

      - name: currency
        description: "ISO 4217 currency code"
        tests:
          - not_null
          - accepted_values:
              values: ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'BRL', 'MXN']

    tests:
      - dbt_utils.expression_is_true:
          expression: "status != 'completed' OR payment_method IS NOT NULL"
          name: completed_orders_have_payment_method

      - dbt_utils.expression_is_true:
          expression: "status != 'refunded' OR refund_amount <= total_amount"
          name: refund_does_not_exceed_original
```

### Custom Test: Row Count Range

```sql
-- tests/assert_row_count_range.sql
{{ config(severity='WARN') }}

SELECT
    CASE
        WHEN COUNT(*) < 100000 THEN 'FAIL: row count below minimum'
        WHEN COUNT(*) > 10000000 THEN 'FAIL: row count above maximum'
        ELSE 'OK'
    END AS result
FROM {{ ref('fct_orders') }}
HAVING result != 'OK'
```

### Custom Test: Data Freshness

```sql
-- tests/assert_data_freshness.sql
SELECT
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(_ingested_at))) / 3600 AS hours_since_last_ingest
FROM {{ ref('fct_orders') }}
HAVING hours_since_last_ingest > 24
```

## 5. Great Expectations Suite

```python
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
```

## 6. Rule Execution and Reporting

### Execution Schedule

| When | Rules | Framework | Action |
|------|-------|-----------|--------|
| Post-staging load | DQ-001 to DQ-022 (column-level) | dbt tests | Block transform on critical failure |
| Post-transform | DQ-023 to DQ-028 (dataset-level) | dbt tests + Great Expectations | Block consumer access on critical failure |
| Hourly (continuous) | DQ-025 (freshness) | Custom SQL | Alert on failure |
| Weekly (audit) | All rules | Great Expectations | Generate quality report |

### Quality Report Template

| Metric | Value | Status |
|--------|-------|--------|
| Total rules executed | 28 | — |
| Rules passed | 26 | ✅ |
| Rules failed (critical) | 0 | ✅ |
| Rules failed (warning) | 2 | ⚠️ |
| Row count | 2,543,210 | ✅ |
| Null rate (order_id) | 0% | ✅ |
| Null rate (payment_method) | 12.3% | ⚠️ (expected for non-completed) |
| Duplicate rate | 0% | ✅ |
| Freshness (hours) | 2.5 | ✅ |
| Referential integrity | 100% | ✅ |

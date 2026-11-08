"""ETL pipeline with lineage tracking — wraps extract/transform/load
in START/COMPLETE/FAIL OpenLineage events."""
from lineage_tracker import LineageTracker


def run_customer_etl():
    tracker = LineageTracker("etl.customers_daily")

    inputs = [{
        "namespace": "postgres://source-db",
        "name": "shop.public.customers",
        "facets": {
            "schema": {
                "fields": [
                    {"name": "id", "type": "long"},
                    {"name": "email", "type": "string"},
                    {"name": "status", "type": "string"}
                ]
            }
        }
    }]

    outputs = [{
        "namespace": "postgres://warehouse",
        "name": "warehouse.customers",
        "facets": {
            "schema": {
                "fields": [
                    {"name": "id", "type": "long"},
                    {"name": "email", "type": "string"},
                    {"name": "is_active", "type": "boolean"}
                ]
            },
            "columnLineage": {
                "fields": {
                    "is_active": {
                        "inputFields": [
                            {"namespace": "postgres://source-db",
                             "name": "shop.public.customers",
                             "field": "status"}
                        ]
                    }
                }
            }
        }
    }]

    sql = "SELECT id, LOWER(email) as email, status = 'active' as is_active FROM source.customers"

    try:
        tracker.start(inputs, outputs, sql=sql)

        # Run the actual ETL
        df = extract_from_source()
        df = transform(df)
        load_to_warehouse(df)

        tracker.complete(inputs, outputs)

    except Exception as e:
        tracker.fail(str(e))
        raise


def extract_from_source():
    ...


def transform(df):
    return df


def load_to_warehouse(df):
    ...


if __name__ == "__main__":
    run_customer_etl()

import great_expectations as gx

context = gx.get_context()

suite = context.suites.add(gx.ExpectationSuite(name="orders_suite"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="total_amount", min_value=0, max_value=100000))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(column="status", value_set=["pending", "processing", "shipped", "completed", "cancelled"]))
suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(column="email", regex=r"^[^@]+@[^@]+\.[^@]+$"))
suite.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(min_value=100, max_value=1000000))

ds = context.data_sources.add_pandas("orders_source")
asset = ds.add_dataframe_asset("orders_df")
batch_def = asset.add_batch_definition_whole_dataframe("orders_batch")
validation = context.validation_definitions.add(gx.ValidationDefinition(data=batch_def, suite=suite, name="orders_validation"))

import pandas as pd
df = pd.read_csv("data/orders.csv")
results = validation.run(batch_parameters={"dataframe": df})
print("success:", results.success)

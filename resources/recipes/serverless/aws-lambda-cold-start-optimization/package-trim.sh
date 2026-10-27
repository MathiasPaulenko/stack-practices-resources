# Remove tests, docs, __pycache__
find layer/python -type d -name "tests" -exec rm -rf {} +
find layer/python -type d -name "__pycache__" -exec rm -rf {} +
find layer/python -type f -name "*.pyc" -delete
find layer/python -type f -name "*.so" -exec strip {} \;

# Use lighter alternatives
# Instead of pandas: use polars (10x smaller, faster init)
# Instead of requests: use urllib3 or boto3's built-in HTTP client
# Instead of SQLAlchemy: use raw psycopg2 or aiobotocore

find layer/python -type d -name "__pycache__" -exec rm -rf {} +
find layer/python -type d -name "tests" -exec rm -rf {} +
find layer/python -type f -name "*.pyc" -delete

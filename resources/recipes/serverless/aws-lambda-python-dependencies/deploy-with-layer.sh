# Zip only the function code (no dependencies)
zip function.zip lambda_function.py

# Create or update function with layer
aws lambda create-function \
  --function-name my-api \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --layers $(cat layer-arn.txt)

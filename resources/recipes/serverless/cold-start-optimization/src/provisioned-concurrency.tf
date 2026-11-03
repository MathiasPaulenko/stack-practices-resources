resource "aws_lambda_function" "api" {
  function_name = "user-api"
  runtime       = "provided.al2023"
  handler       = "bootstrap"
  memory_size   = 512
  timeout       = 10
  publish       = true
}

resource "aws_lambda_provisioned_concurrency_config" "api_warm" {
  function_name                     = aws_lambda_function.api.function_name
  qualifier                         = aws_lambda_function.api.version
  provisioned_concurrent_executions = 10
}

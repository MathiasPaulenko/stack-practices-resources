# AWS EventBridge event bus routing OrderPlaced to two targets.
# Requires: aws_sqs_queue.inventory_queue and aws_lambda_function.billing_processor
# defined in your own Terraform configuration.

resource "aws_cloudwatch_event_bus" "main" {
  name = "stackpractices-events"
}

resource "aws_cloudwatch_event_rule" "order_placed" {
  name           = "order-placed-rule"
  event_bus_name = aws_cloudwatch_event_bus.main.name

  event_pattern = jsonencode({
    source        = ["order-service"]
    "detail-type" = ["OrderPlaced"]
  })
}

resource "aws_cloudwatch_event_target" "inventory_target" {
  rule           = aws_cloudwatch_event_rule.order_placed.name
  event_bus_name = aws_cloudwatch_event_bus.main.name
  arn            = aws_sqs_queue.inventory_queue.arn
}

resource "aws_cloudwatch_event_target" "billing_target" {
  rule           = aws_cloudwatch_event_rule.order_placed.name
  event_bus_name = aws_cloudwatch_event_bus.main.name
  arn            = aws_lambda_function.billing_processor.arn
}

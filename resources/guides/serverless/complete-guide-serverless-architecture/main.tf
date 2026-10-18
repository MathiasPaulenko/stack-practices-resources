# Terraform for the image processing pipeline from the guide's worked example.
# S3 upload -> resize Lambda -> SQS -> metadata Lambda -> DynamoDB (+DLQ)

resource "aws_lambda_function" "resize" {
  function_name = "image-resize"
  handler       = "resize_handler.lambda_handler"
  runtime       = "python3.11"
  memory_size   = 1024
  timeout       = 30

  environment {
    variables = {
      OUTPUT_BUCKET = "uploads-resized"
      QUEUE_URL     = aws_sqs_queue.image_processed.id
    }
  }
}

resource "aws_lambda_function" "metadata" {
  function_name = "image-metadata"
  handler       = "metadata_handler.lambda_handler"
  runtime       = "python3.11"
  memory_size   = 256
  timeout       = 15

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.image_metadata.name
    }
  }
}

resource "aws_lambda_event_source_mapping" "metadata_sqs" {
  event_source_arn                   = aws_sqs_queue.image_processed.arn
  function_name                      = aws_lambda_function.metadata.arn
  batch_size                         = 10
  function_response_types            = ["ReportBatchItemFailures"]
}

resource "aws_sqs_queue" "image_processed" {
  name               = "image-processed-queue"
  visibility_timeout = 60 # must exceed the Lambda timeout

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "dlq" {
  name = "image-processed-dlq"
}

resource "aws_dynamodb_table" "image_metadata" {
  name         = "ImageMetadata"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "imageId"
  range_key    = "version"

  attribute {
    name = "imageId"
    type = "S"
  }

  attribute {
    name = "version"
    type = "S"
  }
}

# Terraform for the image processing pipeline from the guide's worked example.
# S3 upload -> resize Lambda -> SQS -> metadata Lambda -> DynamoDB (+DLQ)
#
# Applies cleanly with `terraform apply` — handlers are zipped from this
# directory, and the S3 -> Lambda trigger is fully wired.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.0"
    }
  }
}

data "archive_file" "resize" {
  type        = "zip"
  source_file = "${path.module}/resize_handler.py"
  output_path = "${path.module}/.build/resize_handler.zip"
}

data "archive_file" "metadata" {
  type        = "zip"
  source_file = "${path.module}/metadata_handler.py"
  output_path = "${path.module}/.build/metadata_handler.zip"
}

# --- IAM ---------------------------------------------------------------------

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "resize" {
  name               = "image-resize-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role" "metadata" {
  name               = "image-metadata-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "resize_basic" {
  role       = aws_iam_role.resize.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "metadata_basic" {
  role       = aws_iam_role.metadata.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Least-privilege inline policies matching the guide's security section.
resource "aws_iam_role_policy" "resize" {
  name = "image-resize-policy"
  role = aws_iam_role.resize.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.originals.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.resized.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["sqs:SendMessage"]
        Resource = aws_sqs_queue.image_processed.arn
      }
    ]
  })
}

resource "aws_iam_role_policy" "metadata" {
  name = "image-metadata-policy"
  role = aws_iam_role.metadata.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.image_processed.arn
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem"]
        Resource = aws_dynamodb_table.image_metadata.arn
      }
    ]
  })
}

# --- Buckets + trigger -------------------------------------------------------

resource "aws_s3_bucket" "originals" {
  bucket = var.originals_bucket_name
}

resource "aws_s3_bucket" "resized" {
  bucket = var.resized_bucket_name
}

resource "aws_lambda_permission" "s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.resize.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.originals.arn
}

resource "aws_s3_bucket_notification" "originals" {
  bucket = aws_s3_bucket.originals.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.resize.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "uploads/originals/"
  }

  depends_on = [aws_lambda_permission.s3_invoke]
}

# --- Functions ---------------------------------------------------------------

resource "aws_lambda_function" "resize" {
  function_name    = "image-resize"
  filename         = data.archive_file.resize.output_path
  source_code_hash = data.archive_file.resize.output_base64sha256
  handler          = "resize_handler.lambda_handler"
  runtime          = "python3.11"
  role             = aws_iam_role.resize.arn
  memory_size      = 1024
  timeout          = 30

  environment {
    variables = {
      OUTPUT_BUCKET = aws_s3_bucket.resized.id
      QUEUE_URL     = aws_sqs_queue.image_processed.id
    }
  }
}

resource "aws_lambda_function" "metadata" {
  function_name    = "image-metadata"
  filename         = data.archive_file.metadata.output_path
  source_code_hash = data.archive_file.metadata.output_base64sha256
  handler          = "metadata_handler.lambda_handler"
  runtime          = "python3.11"
  role             = aws_iam_role.metadata.arn
  memory_size      = 256
  timeout          = 15

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.image_metadata.name
    }
  }
}

resource "aws_lambda_event_source_mapping" "metadata_sqs" {
  event_source_arn        = aws_sqs_queue.image_processed.arn
  function_name           = aws_lambda_function.metadata.arn
  batch_size              = 10
  function_response_types = ["ReportBatchItemFailures"]
}

# --- Queue + DLQ -------------------------------------------------------------

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

# --- DynamoDB ----------------------------------------------------------------

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

# --- Inputs ------------------------------------------------------------------

variable "originals_bucket_name" {
  type        = string
  description = "Globally unique name for the bucket that receives uploads/originals/"
}

variable "resized_bucket_name" {
  type        = string
  description = "Globally unique name for the bucket that stores resized images"
}

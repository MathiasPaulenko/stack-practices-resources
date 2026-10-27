#!/usr/bin/env bash
# AWS CLI commands from the AWS Basics guide
set -euo pipefail

# Launch an instance via CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-123456 \
  --subnet-id subnet-123456

# Create a bucket
aws s3 mb s3://my-app-bucket

# Upload a file
aws s3 cp app.zip s3://my-app-bucket/builds/

# Make public (with caution)
aws s3api put-object-acl --bucket my-app-bucket --key app.zip --acl public-read

# Create and attach a volume
aws ec2 create-volume --size 100 --region us-east-1 --availability-zone us-east-1a --volume-type gp3
aws ec2 attach-volume --volume-id vol-12345 --instance-id i-12345 --device /dev/sdf

# Create a PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --manage-master-user-password \  # let RDS store it in Secrets Manager — never inline
  --allocated-storage 20

# Create a billing alarm — the first thing a new account needs
aws cloudwatch put-metric-alarm   --alarm-name billing-alert   --metric-name EstimatedCharges   --namespace AWS/Billing   --statistic Maximum --period 21600   --threshold 10 --comparison-operator GreaterThanThreshold   --dimensions Name=Currency,Value=USD   --alarm-actions arn:aws:sns:us-east-1:123456789012:billing-alerts

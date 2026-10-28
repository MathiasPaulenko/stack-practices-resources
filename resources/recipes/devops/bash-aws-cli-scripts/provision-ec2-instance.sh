#!/bin/bash

set -euo pipefail

INSTANCE_NAME="web-server-01"
AMI_ID="ami-0c55b159cbfafe1f0"  # example ID — pick a current AMI for your region
INSTANCE_TYPE="t3.micro"
KEY_NAME="my-key-pair"         # your key pair name
SECURITY_GROUP="sg-12345678"   # your security group ID
SUBNET_ID="subnet-12345678"    # your subnet ID

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_NAME" \
    --security-group-ids "$SECURITY_GROUP" \
    --subnet-id "$SUBNET_ID" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=${INSTANCE_NAME}}]" \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Launched instance: $INSTANCE_ID"

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "Instance running at: $PUBLIC_IP"

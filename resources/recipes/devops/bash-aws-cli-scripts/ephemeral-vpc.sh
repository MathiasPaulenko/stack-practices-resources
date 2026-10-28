#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
PROJECT="${1:-demo}"
ENV="${2:-dev}"

TAGS="Key=Project,Value=$PROJECT Key=Environment,Value=$ENV Key=ManagedBy,Value=bash-script"

# Create a VPC with tags
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region "$REGION" --query 'Vpc.VpcId' --output text)
aws ec2 create-tags --resources "$VPC_ID" --tags $TAGS --region "$REGION"

SUBNET_ID=""

# Cleanup function — deletes in dependency order (subnet before VPC)
cleanup() {
    echo "Tearing down ${SUBNET_ID:-none} and $VPC_ID"
    if [ -n "$SUBNET_ID" ]; then
        aws ec2 delete-subnet --subnet-id "$SUBNET_ID" --region "$REGION" || true
    fi
    aws ec2 delete-vpc --vpc-id "$VPC_ID" --region "$REGION" || true
}

# Register the teardown right away, before anything else can fail —
# unless KEEP=1 is exported
if [ "${KEEP:-0}" != "1" ]; then
    trap cleanup EXIT
fi

# Create a subnet
SUBNET_ID=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.1.0/24 --region "$REGION" --query 'Subnet.SubnetId' --output text)
aws ec2 create-tags --resources "$SUBNET_ID" --tags $TAGS --region "$REGION"

echo "Created VPC $VPC_ID and subnet $SUBNET_ID"

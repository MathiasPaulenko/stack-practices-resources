#!/bin/bash

set -euo pipefail

aws ec2 describe-instances \
    --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==`Name`].Value | [0]]' \
    --output table

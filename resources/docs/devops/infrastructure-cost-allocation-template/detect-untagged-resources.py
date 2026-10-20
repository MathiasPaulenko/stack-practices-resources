#!/usr/bin/env python3
"""Detect untagged AWS resources and report estimated weekly cost.

Checks EC2 instances as an example — extend per resource type
(RDS, EBS, S3 buckets via resourcegroupstaggingapi).
"""
import boto3
import json
from datetime import datetime, timedelta


def check_untagged_resources():
    ce = boto3.client('ce')
    ec2 = boto3.client('ec2')

    # Query cost by resource for the last 7 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='DAILY',
        Filter={'Dimensions': {'Key': 'RECORD_TYPE', 'Values': ['Usage']}},
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'RESOURCE_ID'}],
        Metrics=['UnblendedCost']
    )

    untagged_cost = 0
    untagged_resources = []

    for group in response['ResultsByTime']:
        for result in group['Groups']:
            resource_id = result['Keys'][0]
            cost = float(result['Metrics']['UnblendedCost']['Amount'])
            if cost > 0:
                try:
                    if 'instance/' in resource_id:
                        instance_id = resource_id.split('/')[-1]
                        tags = ec2.describe_tags(
                            Filters=[{'Name': 'resource-id', 'Values': [instance_id]}]
                        )
                        if not tags['Tags']:
                            untagged_cost += cost
                            untagged_resources.append({
                                'resource_id': resource_id,
                                'cost': cost
                            })
                except Exception:
                    pass

    print(f'Untagged resources: {len(untagged_resources)}')
    print(f'Estimated weekly cost: ${untagged_cost:.2f}')
    if untagged_cost > 500:
        print('ALERT: Untagged resources exceed $500/week')
    return untagged_resources


if __name__ == '__main__':
    check_untagged_resources()

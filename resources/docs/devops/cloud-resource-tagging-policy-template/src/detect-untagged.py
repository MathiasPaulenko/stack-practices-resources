#!/usr/bin/env python3
"""Detect untagged resources in AWS."""
import boto3
import json
from botocore.exceptions import ClientError
from datetime import datetime

REQUIRED_TAGS = ['team', 'environment', 'product', 'cost-center', 'owner']
REGIONS = ['us-east-1', 'eu-west-1', 'ap-southeast-1']

def check_ec2_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    untagged = []
    response = ec2.describe_instances()
    for res in response['Reservations']:
        for inst in res['Instances']:
            tags = {t['Key'].lower(): t['Value'] for t in inst.get('Tags', [])}
            missing = [t for t in REQUIRED_TAGS if t not in tags]
            if missing:
                untagged.append({
                    'resource_id': inst['InstanceId'],
                    'type': 'EC2',
                    'region': region,
                    'missing_tags': missing,
                    'launch_time': inst['LaunchTime'].isoformat()
                })
    return untagged

def check_s3_buckets(region):
    s3 = boto3.client('s3')
    untagged = []
    for bucket in s3.list_buckets()['Buckets']:
        # get_bucket_tagging raises NoSuchTagSet on untagged buckets
        try:
            tags = s3.get_bucket_tagging(Bucket=bucket['Name']).get('TagSet', [])
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                tags = []
            else:
                raise
        tag_keys = [t['Key'].lower() for t in tags]
        missing = [t for t in REQUIRED_TAGS if t not in tag_keys]
        if missing:
            untagged.append({
                'resource_id': bucket['Name'],
                'type': 'S3',
                'region': region,
                'missing_tags': missing
            })
    return untagged

def check_rds_instances(region):
    rds = boto3.client('rds', region_name=region)
    untagged = []
    for db in rds.describe_db_instances()['DBInstances']:
        arn = db['DBInstanceArn']
        tags = rds.list_tags_for_resource(ResourceName=arn).get('TagList', [])
        tag_keys = [t['Key'].lower() for t in tags]
        missing = [t for t in REQUIRED_TAGS if t not in tag_keys]
        if missing:
            untagged.append({
                'resource_id': db['DBInstanceIdentifier'],
                'type': 'RDS',
                'region': region,
                'missing_tags': missing
            })
    return untagged

def main():
    all_untagged = []
    for region in REGIONS:
        all_untagged.extend(check_ec2_instances(region))
        all_untagged.extend(check_s3_buckets(region))
        all_untagged.extend(check_rds_instances(region))

    report = {
        'timestamp': datetime.now().isoformat(),
        'total_untagged': len(all_untagged),
        'resources': all_untagged
    }
    print(json.dumps(report, indent=2))

    if all_untagged:
        print(f'\\nUntagged resources: {len(all_untagged)}')
        for r in all_untagged:
            print(f"  {r['type']} {r['resource_id']} ({r['region']}): missing {', '.join(r['missing_tags'])}")

if __name__ == '__main__':
    main()

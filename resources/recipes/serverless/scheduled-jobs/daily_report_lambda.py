import json
import boto3
from datetime import datetime, timedelta


def generate_sales_report(date: str) -> dict:
    """Placeholder for real report logic — aggregate the day's data."""
    return {"date": date, "orders": 0, "revenue": 0.0}


def lambda_handler(event, context):
    # Runs every day at 2 AM UTC
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Generate daily report
    report = generate_sales_report(yesterday)

    # Upload to S3
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket='reports.example.com',
        Key=f'daily/{yesterday}.json',
        Body=json.dumps(report)
    )

    return {'statusCode': 200, 'body': f'Report {yesterday} generated'}

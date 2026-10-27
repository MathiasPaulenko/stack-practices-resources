import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

table.put_item(Item={'id': 'user-1', 'name': 'Alice', 'email': 'alice@example.com'})
response = table.get_item(Key={'id': 'user-1'})

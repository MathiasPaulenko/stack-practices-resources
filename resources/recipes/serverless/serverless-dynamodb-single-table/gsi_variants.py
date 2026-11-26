"""GSI variants: sparse index (drafts excluded) and overloaded prefixes."""

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AppTable')


# Sparse GSI: only published products get GSI2 keys, drafts stay out.
def put_product_sparse(product_id: str, category: str, name: str, price: float, published: bool):
    item = {
        'PK': f'PRODUCT#{product_id}',
        'SK': 'DETAILS',
        'GSI1PK': f'CATEGORY#{category}',
        'GSI1SK': f'PRODUCT#{product_id}',
        'entityType': 'Product',
        'productId': product_id,
        'name': name,
        'price': price,
    }
    if published:
        item['GSI2PK'] = 'PUBLISHED'
        item['GSI2SK'] = f'PRODUCT#{product_id}'
    table.put_item(Item=item)


# Overloaded GSI prefixes (one index serving several access patterns):
#   GSI1PK=ORDERSTATUS#PENDING        -> orders by status
#   GSI1PK=CATEGORY#electronics       -> products by category
#   GSI1PK=USEREMAIL#alice@test.com   -> user by email

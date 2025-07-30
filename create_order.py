import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')  # Replace with your table name

def lambda_handler(event, context):
    # If the event comes with body as JSON string (API Gateway style), parse it first
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event

    order_id = body['orderId']
    product_name = body['product_name']
    quantity = body['quantity']
    price = body['price']

    # Convert floats to Decimal for DynamoDB compatibility
    quantity = Decimal(str(quantity))
    price = Decimal(str(price))

    response = table.put_item(
        Item={
            'orderId': order_id,
            'product_name': product_name,
            'quantity': quantity,
            'price': price
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Order created successfully!')
    }

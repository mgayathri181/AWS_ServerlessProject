import json
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        # Parse JSON body
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif not isinstance(body, dict):
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"message": "Invalid request format"})
            }

        # Required fields validation
        for field in ["orderId", "product_name", "quantity", "price"]:
            if field not in body:
                return {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": json.dumps({"message": f"Missing required field: {field}"})
                }

        # Extract fields with correct types
        order_id = str(body["orderId"])
        product_name = str(body["product_name"])
        quantity = Decimal(str(body["quantity"]))
        price = Decimal(str(body["price"]))
        customer_name = str(body.get("customerName", "Unknown Customer"))
        order_date = datetime.utcnow().isoformat()

        # Put item into DynamoDB
        table.put_item(
            Item={
                "orderId": order_id,
                "product_name": product_name,
                "quantity": quantity,
                "price": price,
                "customerName": customer_name,
                "orderDate": order_date
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "✅ Order created successfully!"})
        }

    except Exception as e:
        print("❌ Exception:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": f"Error creating order: {str(e)}"})
        }

import json
import boto3

def lambda_handler(event, context):
    # Initialize DynamoDB resource in your region
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')  # Change region as needed

    # Reference your DynamoDB table
    table = dynamodb.Table('Products')

    # Scan the table to get all items
    response = table.scan()
    data = response['Items']

    # Continue scanning if there are more items
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # Return all products as JSON string with HTTP 200 response
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }

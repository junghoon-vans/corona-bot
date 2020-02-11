import json, os

def lambda_handler(event, context):
    # TODO implement
    
    if event["httpMethod"] == "GET":
        hub_mode = event["queryStringParameters"]["hub.mode"]
        hub_challenge = event["queryStringParameters"]["hub.challenge"]
        hub_verify_token = event["queryStringParameters"]["hub.verify_token"]
        
        if hub_verify_token == os.environ['VERIFY_TOKEN']: # store VERIFY_TOKEN in aws_lambda
            return {'statusCode': '200', 'body': hub_challenge, 'headers': {'Content-Type': 'application/json'}}
            
        else:
            return {'statusCode': '403', 'body': 'Error, invalid token', 'headers': {'Content-Type': 'application/json'}}
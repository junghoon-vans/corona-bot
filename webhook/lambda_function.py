import json, os
from pprint import pprint

questions = {
  '코로나': ["""바이러스"""]
}

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

    elif event["httpMethod"] == "POST":
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(event['body'])
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    return {'statusCode': '200', 'data':json.dumps({"recipient":{"id":message['sender']['id']}, "message":{"text":message['message']['text']}}), 'headers': {'Content-Type': 'application/json'}}
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
        return {'statusCode': '403', 'body': json.dumps('null')}

import json, os
import requests

CHATBOT_RESPONSE = {
    '코로나': ["""바이러스"""],
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
        incoming_message = json.loads(event['body'])
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    try:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
                    except:
                        print("따봉")
        return
        
def post_facebook_message(fbid, recevied_message):
    
    question_text = ''
    tokens = list(CHATBOT_RESPONSE.keys())
    for token in tokens:
        if recevied_message.find(token) != -1:
            question_ans = random.choice(CHATBOT_RESPONSE[token])
            question_text += question_ans + "\n\n"

    endpoint = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ['PAGE_ACCESS_TOKEN']
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":question_text}})
    requests.post(endpoint, headers={"Content-Type": "application/json"},data=response_msg)
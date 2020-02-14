import json, os
import requests

CHATBOT_RESPONSE = {
    '코로나': ["""바이러스"""],
    '바이러스': ["""코로나"""]
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
            return {'statusCode': '401', 'body': 'Incorrect verify token', 'headers': {'Content-Type': 'application/json'}}

    elif event["httpMethod"] == "POST":
        incoming_message = json.loads(event['body'])
        message = incoming_message['entry'][0]['messaging'][0]
        try:
            send_facebook_message(message['sender']['id'], message['message']['text'])
        except:
            print("따봉")
        return {'statusCode': '200', 'body': 'Success' , 'headers': {'Content-Type': 'application/json'}}
        
def send_facebook_message(fbid, recevied_message):
    msg = ''
    tokens = list(CHATBOT_RESPONSE.keys())

    for token in tokens:
        if recevied_message.find(token) != -1:
            msg += CHATBOT_RESPONSE[token]

    if not msg:
        msg = "안녕하세요, 코로나 알리미입니다!\n코로나, 바이러스\n중에서 원하는 키워드를 넣어서\n질문해주세요."
        
    endpoint = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ['PAGE_ACCESS_TOKEN']
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": msg}})
    requests.post(endpoint, headers={"Content-Type": "application/json"}, data=response_msg)

import json, os
import requests

CHATBOT_RESPONSE = {
    '코로나': """바이러스""",
    '바이러스': """코로나""",
}

def lambda_handler(event, context):
    # TODO implement
    
    if event["httpMethod"] == "GET":
        hub_challenge = event["queryStringParameters"]["hub.challenge"]
        hub_verify_token = event["queryStringParameters"]["hub.verify_token"]
        
        if hub_verify_token == os.environ['VERIFY_TOKEN']: # store VERIFY_TOKEN in aws_lambda
            return {'statusCode': '200', 'body': hub_challenge, 'headers': {'Content-Type': 'application/json'}}
        else:
            return {'statusCode': '401', 'body': 'Incorrect verify token', 'headers': {'Content-Type': 'application/json'}}

    elif event["httpMethod"] == "POST":
        incoming_message = json.loads(event['body'])
        message = incoming_message['entry'][0]['messaging'][0]
        send_facebook_message(message['sender']['id'], message['message']['text'])
        return {'statusCode': '200', 'body': 'Success' , 'headers': {'Content-Type': 'application/json'}}
        
def send_facebook_message(fbid, recevied_message):
    msg = ''
    for key in CHATBOT_RESPONSE.keys():
        if key in recevied_message:
            msg += CHATBOT_RESPONSE[key] + "\n"

    if not msg:
        msg = "안녕하세요,\n코로나 알리미입니다!\n\n아래 제시된 키워드를 포함하여 질문해주세요.\n\n- 코로나\n- 바이러스"
        
    endpoint = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ['PAGE_ACCESS_TOKEN']
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": msg}})
    requests.post(endpoint, headers={"Content-Type": "application/json"}, data=response_msg)
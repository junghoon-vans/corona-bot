import json, os
import requests

from crawler import summary_info

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
        
def send_facebook_message(fbid, received_message):
    msg = ''

    if '확진환자수' in received_message:
        summary = json.loads(summary_info.get_json())
        msg = summary["confirmator_num"]
    
    elif '퇴원조치수' in received_message:
        summary = json.loads(summary_info.get_json())
        msg = summary["discharged_num"]
        
    elif '검사진행수' in received_message:
        summary = json.loads(summary_info.get_json())
        msg = summary["check_num"]
    
    else:
        for key in CHATBOT_RESPONSE.keys():
            if key in received_message:
                msg += key + ": " + CHATBOT_RESPONSE[key] + "\n"

    if not msg:
        msg = "안녕하세요,\n코로나 알리미입니다!\n\n아래 제시된 키워드를 포함하여 질문해주세요.\n\n- 확진환자수\n- 퇴원조치수\n- 검사진행수"
        
    endpoint = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ['PAGE_ACCESS_TOKEN']
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": msg}})
    requests.post(endpoint, headers={"Content-Type": "application/json"}, data=response_msg)
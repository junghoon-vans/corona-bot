import json
import os
import re
import requests

from parser import summary_info
from parser import hospital_info

CHATBOT_RESPONSE = {
    '확진환자수': '',
    '퇴원조치수': '',
    '사망자수': '',
    '선별진료소': """시도 및 시군구를 입력하면 선별진료소 조회를 시작합니다.\n(검색어 예시: '서울' 또는 '제주 서귀포')""",
    '발단': """2019년 12월, 중국 우한에서 처음 발생했습니다. 감염원은 동물로 추정되고 있으며, 동물에게서 사람으로 전파된 것으로 추정됩니다.""",
    '증상': """감염되면 최대 2주간의 잠복기를 거친 후, 발열/기침/호흡곤란을 비롯한 폐렴 증상이 주로 나타납니다. 다만, 증상이 나타나지 않는 무증상 감염 사례도 존재합니다.""",
    '전염경로': """코로나19는 사람 간 전파가 확인된 바이러스입니다. 주된 감염경로는 비말감염으로, 감염자의 침방울이 호흡기나 눈/코/입의 점막으로 침투될 때 전염됩니다.""",
    '예방법': """1. 우선, 비누와 물로 손을 자주 씻습니다. 손 소독제 사용도 좋은 대안입니다.
    \n2. 씻지 않은 손으로 눈이나 코, 입을 만지지 않습니다.
    \n3. 기침이나 재채기를 할 때 티슈나 소매로 입/코를 가립니다.
    \n4. 아플 때는 자가격리를 통해 다른 사람과의 접촉을 피합니다.""",
    '치료': """코로나19 치료는 환자의 증상에 대응하는 치료로 이루어집니다.\n기침/인후통/폐렴 등 주요 증상에 따라 항바이러스제나 항생제 투여가 해당됩니다.""",
}

cities = ('서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주')

def lambda_handler(event, context):
    # TODO implement

    if event["httpMethod"] == "GET":
        hub_challenge = event["queryStringParameters"]["hub.challenge"]
        hub_verify_token = event["queryStringParameters"]["hub.verify_token"]

        # store VERIFY_TOKEN in aws_lambda
        if hub_verify_token == os.environ['VERIFY_TOKEN']:
            return {'statusCode': '200', 'body': hub_challenge, 'headers': {'Content-Type': 'application/json'}}
        else:
            return {'statusCode': '401', 'body': 'Incorrect verify token', 'headers': {'Content-Type': 'application/json'}}

    elif event["httpMethod"] == "POST":
        try:
            incoming_message = json.loads(event['body'])
            message = incoming_message['entry'][0]['messaging'][0]
            if(message['sender']['id'] and message['message']['text']):
                send_dots(message['sender']['id'])
                send_text(
                    message['sender']['id'], message['message']['text'])
            return {'statusCode': '200', 'body': 'Success', 'headers': {'Content-Type': 'application/json'}}
        except:
            return {'statusCode': '500', 'body': 'Internal server error', 'headers': {'Content-Type': 'application/json'}}

def send_text(fbid, received_message):
    reply = ''
    quick_replies = list()

    # add crawler data in dict
    if '확진환자수' in received_message:
        CHATBOT_RESPONSE['확진환자수'] = summary_info.get_confirmator_num()
    if '퇴원조치수' in received_message:
        CHATBOT_RESPONSE['퇴원조치수'] = summary_info.get_discharged_num()
    if '사망자수' in received_message:
        CHATBOT_RESPONSE['사망자수'] = summary_info.get_death_num()

    for key in CHATBOT_RESPONSE.keys():
        quick_replies.append({
            "content_type": "text",
            "title": key,
            "payload": 'DEVELOPER_DEFINED_PAYLOAD'})
        if key in received_message:
            reply += CHATBOT_RESPONSE[key] + '\n\n'

    # parse hospital_list
    for city in cities:
        if re.compile(city).search(received_message):
            reply += hospital_info.get_hospital_list(city, received_message)
            break

    if not reply:
        reply = "안녕하세요,\n코로나 알리미입니다!\n\n아래 제시된 키워드를 포함하여 질문해주세요."

    send_message(json.dumps({
        "recipient": {"id": fbid}, "message": {"text": reply, "quick_replies": quick_replies}}))

def send_dots(fbid):
    send_message(json.dumps({
        "recipient": {"id": fbid}, "sender_action": "typing_on"
    }))

def send_message(response_msg):
    endpoint = 'https://graph.facebook.com/v6.0/me/messages?access_token=%s' % os.environ['PAGE_ACCESS_TOKEN']
    requests.post(endpoint, headers={
                  "Content-Type": "application/json"}, data=response_msg)
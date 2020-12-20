import json
import os
import re
import requests

def get_hospital_list(city, received_message):
    reply = ''
    json_data = requests.get(os.environ['S3_BUCKET_URL']+"hospital.json").json()
            
    for region in json_data[city].keys():
        for hospital in json_data[city][region]:
            reply += hospital[0] + " " + hospital[1] + '\n'
        if re.compile(region[:-1]).search(received_message):
            reply = ''
            for hospital in json_data[city][region]:
                reply += hospital[0] + " " + hospital[1] + '\n'
            break

    reply += "\n('*'는 검체채취 가능 진료소)"
    return reply
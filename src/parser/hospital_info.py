import json, re

def get_hospital_list(city, received_message):
    reply = ''
    
    with open('data/hospital.json') as json_file:
        json_data = json.load(json_file)
            
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
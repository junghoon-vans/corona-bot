# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import boto3

# TODO 지역별 확진자

def set_summary_info(event, context):
    data = dict()

    raw_status = get_raw("http://ncov.mohw.go.kr/bdBoardList.do")
    html_status = BeautifulSoup(raw_status.text, 'html.parser')
    statusbox = html_status.select("ul.s_listin_dot li")
    updatebox = html_status.select_one("p.s_descript").text
    
    data['update_date'] = updatebox.replace("코로나바이러스감염증-19 국내 발생 현황", "")
    data['confirmator_num'] = statusbox[0].text[:-1].replace("(확진환자) ", "")
    data['discharged_num'] = statusbox[1].text[:-1].replace("(확진환자 격리해제) ", "")
    data['death_num'] = statusbox[2].text[:-1].replace("(사망자) ", "")
    data['check_num'] = statusbox[3].text[:-1].replace("(검사진행) ", "")
    data['cured_rate'] = round(int(data['discharged_num'])/int(data['confirmator_num'])*100, 1)
    
    json_data = json.dumps(data)
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('facebook-coronabot')
    bucket.put_object(Key='summary.json', Body=json_data)
    
    return {
        'statusCode': 200
    }

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass
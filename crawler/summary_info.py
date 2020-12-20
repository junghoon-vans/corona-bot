# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import boto3
import os

# TODO 지역별 확진자

def set_summary_info(event, context):
    data = dict()

    raw_status = get_raw(os.environ['summary_url'])
    html_status = BeautifulSoup(raw_status.text, 'html.parser')
    statusbox = html_status.select("span.num")
    checkbox = html_status.select_one("span.num_rnum").text
    updatebox = html_status.select_one("span.livedate").text[1:].split(".")
    
    data['update_date'] = updatebox[0] + "월 " + updatebox[1] + "일" + updatebox[2].split(",")[0]
    data['confirmator_num'] = statusbox[0].text.replace("(누적)", "")
    data['discharged_num'] = statusbox[1].text
    data['charged_num'] = statusbox[2].text
    data['death_num'] = statusbox[3].text
    data['check_num'] = checkbox.split()[0]
    data['cured_rate'] = round(int(data['discharged_num'].replace(",", ""))/int(data['confirmator_num'].replace(",", ""))*100, 1)
    
    json_data = json.dumps(data)
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('facebook-coronabot')
    bucket.put_object(Key='summary.json', Body=json_data)
    
    return {
        'statusCode': 200,
        'body': json_data
    }

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

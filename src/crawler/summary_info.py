# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

# TODO 지역별 확진자

def get_confirmator_num():
    statusbox = init()
    confirmator_num = int(statusbox[0].text[:-2])
    check_num = int(statusbox[2].text[:-2])
    return "현재시각 기준, 코로나19 확진환자는 %s명, 검사가 진행중인 유증상자는 %s명입니다." % ( confirmator_num, check_num)

def get_discharged_num():
    statusbox = init()
    discharged_num = int(statusbox[1].text[:-2])
    return "현재시각 기준, %s명이 코로나19 확진 후 퇴원조치(격리해제) 되었습니다." % discharged_num

def init():
    raw_status = get_raw("http://ncov.mohw.go.kr/index_main.jsp#link")
    html_status = BeautifulSoup(raw_status.text, 'html.parser')
    return html_status.select("div.co_cur a.num")

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass
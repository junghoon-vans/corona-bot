# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

# TODO 지역별 확진자

def get_confirmator_num():
    statusbox, update_date = init()
    confirmator_num = statusbox[0].text[:-1].replace("(확진환자) ", "")
    check_num = statusbox[3].text[:-1].replace("(검사진행) ", "")
    return "검사를 진행한 인원은 %s명이며 확진환자는 %s명입니다.\n" % (check_num, confirmator_num) + update_date.replace(".", "월 ")

def get_discharged_num():
    statusbox, update_date = init()
    confirmator_num = statusbox[0].text[:-1].replace("(확진환자) ", "")
    discharged_num = statusbox[1].text[:-1].replace("(확진환자 격리해제) ", "")
    cured_rate = round(int(discharged_num)/int(confirmator_num)*100, 1)
    return "%s명이 퇴원조치(격리해제) 되었습니다. 총 완치자 비율은 %s%%입니다.\n" % (discharged_num, str(cured_rate)) + update_date.replace(".", "월 ")

def get_death_num():
    statusbox, update_date = init()
    death_num = statusbox[2].text[:-1].replace("(사망자) ", "")
    return "총 사망자 수는 %s명입니다.\n" % death_num + update_date.replace(".", "월 ")

def init():
    raw_status = get_raw("http://ncov.mohw.go.kr/bdBoardList.do")
    html_status = BeautifulSoup(raw_status.text, 'html.parser')
    statusbox = html_status.select("ul.s_listin_dot li")
    updatebox = html_status.select_one("p.s_descript").text
    update_date = updatebox.replace("코로나바이러스감염증-19 국내 발생 현황", "")
    return statusbox, update_date

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

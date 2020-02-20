# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

# TODO 지역별 확진자

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

raw_status = get_raw("http://ncov.mohw.go.kr/bdBoardList.do")
html_status = BeautifulSoup(raw_status.text, 'html.parser')
statusbox = html_status.select("ul.s_listin_dot li")
updatebox = html_status.select_one("p.s_descript").text
update_date = updatebox.replace("코로나바이러스감염증-19 국내 발생 현황", "")

def get_confirmator_num():
    confirmator_num = statusbox[0].text[:-1].replace("(확진환자) ", "").replace(",", "")
    check_num = statusbox[3].text[:-1].replace("(검사진행) ", "").replace(",", "")
    return update_date+"\n코로나19 검사를 진행한 인원은 %s명이며 확진환자는 %s명입니다." % (check_num, confirmator_num)

def get_discharged_num():
    confirmator_num = statusbox[0].text[:-1].replace("(확진환자) ", "").replace(",", "")
    discharged_num = statusbox[1].text[:-1].replace("(확진환자 격리해제) ", "").replace(",", "")
    cured_rate = round(int(discharged_num)/int(confirmator_num)*100, 1)
    return update_date+"\n%s명이 코로나19 확진 후 퇴원조치(격리해제) 되었습니다. 총 완치자 비율은 %s%%입니다." % (discharged_num, str(cured_rate))

# 사망자 수 만드셈ㅋㅋㅋ
def get_death_num():
    death_num = statusbox[2].text[:-1].replace("(사망자) ", "").replace(",", "")
    return update_date+"\n총 사망자 수는 %s명입니다." % death_num

# def init():
#     raw_status = get_raw("http://ncov.mohw.go.kr/bdBoardList.do")
#     html_status = BeautifulSoup(raw_status.text, 'html.parser')
#     return html_status.select("ul.s_listin_dot li")
print(get_confirmator_num())
print(get_death_num())
print(get_discharged_num())
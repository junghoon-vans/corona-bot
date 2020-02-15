# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

# 전체 선별진료소
hosiptal_list = []
# 검체채취가능 진료소
possible_hospital=[]

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

def get_json():
    raw_hospital = get_raw("http://www.mohw.go.kr/react/popup_200128.html")
    # raw_hospital.encoding = None
    html_hospital = BeautifulSoup(raw_hospital.content, 'html.parser', from_encoding='euc-kr')
    hospitals = html_hospital.select("tbody.tb_center tr")

    # 546
    for h in hospitals:
        id = h.select_one("th").text
        city = h.select_one("td:nth-of-type(1)").text
        region = h.select_one("td:nth-of-type(2)").text
        selected = h.select_one("td:nth-of-type(3)").text.replace("	","")
        number = h.select_one("td:nth-of-type(4)").text.replace(",","/")

        if "*" in selected:
            possible_hospital.append(selected)
        hosiptal_list.append({"city":city, "region":region, "name":selected,"number":number})

    hospital = {"all_hospital":hosiptal_list, "sampling_hospital":possible_hospital}
    return json.dumps(hospital, indent=4)
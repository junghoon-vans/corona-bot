# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

hosiptal = {}
# 전체 선별진료소
hospital_dic = {}

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            print("internet not connected")

# 검체채취가능 진료소
possible_hospital=[]

raw_hospital = get_raw("http://www.mohw.go.kr/react/popup_200128.html")
# print(raw_hospital.encoding)
# raw_hospital.encoding = None
html_hospital = BeautifulSoup(raw_hospital.content, 'html.parser', from_encoding='euc-kr')
hospitals = html_hospital.select("tbody.tb_center tr")

# 546
city_dic = {}
item_list = []
for h in hospitals:
    id = h.select_one("th").text
    city = h.select_one("td:nth-of-type(1)").text
    region = h.select_one("td:nth-of-type(2)").text
    selected = h.select_one("td:nth-of-type(3)").text.replace("	","").replace("(검체채취 가능)", "")
    number = h.select_one("td:nth-of-type(4)").text.replace(",","/")

    # city_dic = {}
    # item_list = []
    if "*" in selected:
        possible_hospital.append(selected)

    if city in hospital_dic.keys():
        if region in city_dic.keys():
            print(region, "안에 더 추가")
            item_list.append([selected, number])
            city_dic[region] = item_list
        else:
            print(region, "새롭게 추가")
            item_list = list()
            item_list.append([selected, number])
            city_dic[region] = item_list
    else:
        print(city, "시 추가")
        item_list = list()
        city_dic = dict()
        item_list.append([selected, number])
        city_dic[region] = item_list
        hospital_dic[city] = city_dic


print(hospital_dic)

json_hospital = json.dumps(hospital_dic, indent=4)
print(json_hospital)

with open('hospital.json', 'w', encoding="utf-8") as make_hosptial:
    json.dump(hospital_dic, make_hosptial, ensure_ascii=False, indent="\t")
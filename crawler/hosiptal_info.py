# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

hosiptal = {}
hosiptal_list = []
# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

# f = open("hospitals.csv", "w")
# f.write("id, city, region, selected, number\n")

#검체채취가능리스트
possible_hospital=[]

raw_hospital = get_raw("http://www.mohw.go.kr/react/popup_200128.html")
print(raw_hospital.encoding)
# raw_hospital.encoding = None
html_hospital = BeautifulSoup(raw_hospital.content, 'html.parser', from_encoding='euc-kr')
hospitals = html_hospital.select("tbody.tb_center tr")

# 546
for h in tqdm(hospitals):
    id = h.select_one("th").text
    city = h.select_one("td:nth-of-type(1)").text
    region = h.select_one("td:nth-of-type(2)").text
    selected = h.select_one("td:nth-of-type(3)").text.replace("	","")
    number = h.select_one("td:nth-of-type(4)").text.replace(",","/")

    if "*" in selected:
        possible_hospital.append(selected)

    print(id,city,region,selected,number)
    hosiptal_list.append({"city":city, "region":region, "name":selected,"number":number})

hospital = {"data":hosiptal_list}
json_hospital = json.dumps(hospital, indent=4)
print(json_hospital)
print(type(json_hospital))
print(possible_hospital)

with open('hospital.json', 'w', encoding="utf-8") as make_hosptial:
    json.dump(hospital, make_hosptial, ensure_ascii=False, indent="\t")
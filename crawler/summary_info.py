# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

# 확진자 수
confirmator_num = 0
# 퇴원조치 수
discharged_num = 0
# 검사진행 수
check_num = 0

#dict
summary = {}

# 지역별 확진자(해야됌)

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

raw_status = get_raw("http://ncov.mohw.go.kr/index_main.jsp#link")
html_status = BeautifulSoup(raw_status.text, 'html.parser')

statusbox = html_status.select("div.co_cur a.num")
confirmator_num = int(statusbox[0].text[:-2])
discharged_num = int(statusbox[1].text[:-2])
check_num = int(statusbox[2].text[:-2])

# dict to json
summary["confirmator_num"] = confirmator_num
summary["discharged_num"] = discharged_num
summary["check_num"] = check_num
# json_summary = json.dumps(summary, indent=4)
print(summary)

# make jason file
with open('summary.json', 'w', encoding="utf-8") as make_summary:
    json.dump(summary, make_summary, ensure_ascii=False, indent="\t")

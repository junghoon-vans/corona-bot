import requests
from bs4 import BeautifulSoup
import json

# 격리시설 list
segregated_facility = []
# dict
facility = {}

# retry get raw without timeout exception
def get_raw(url):
    while True:
        try:
            return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except:
            pass

raw_segregated = get_raw("http://news.seoul.go.kr/welfare/archives/513105")
html_segregated = BeautifulSoup(raw_segregated.text, 'html.parser')
segregated_facility = []
for i in range(1,28):
    segregated_facility.append(html_segregated.select_one("tr#patient"+str(i)+" td:nth-of-type(8)").text.replace(u'\xa0', u'').replace(" ",""))

segregated_facility = list(set(segregated_facility))
# print(segregated_facility)
facility = {i : segregated_facility[i] for i in range(0, len(segregated_facility))}
print(facility)
# json_facility = json.dumps(facility, indent=4)
# print("json_facility", json_facility)

# make json file
with open('facility.json', 'w', encoding="utf-8") as make_facility:
    json.dump(facility, make_facility, ensure_ascii=False, indent="\t")
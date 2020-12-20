import requests
import os

# TODO 지역별 확진자

def get_daily_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+","+"\n일일확진자는 %s명입니다.\n그 중 국내발생은 %s명이며,\n해외유입 확진자는 %s명입니다." % (int(data['domestic_num'])+int(data['oversea_num']), data['domestic_num'], data['oversea_num'])

def get_confirmator_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+","+"\n검사를 진행중인 인원은 %s명이며 확진환자는 %s명입니다.\n" % (data['check_num'], data['confirmator_num'])

def get_discharged_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+","+"\n%s명이 퇴원조치 되었습니다.\n총 완치자 비율은 %s%%입니다.\n" % (data['discharged_num'], data['cured_rate'])

def get_death_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+","+"\n총 사망자 수는 %s명입니다.\n" % data['death_num']

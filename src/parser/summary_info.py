import requests
import os

# TODO 지역별 확진자

def get_confirmator_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+"\n검사를 진행중인 인원은 %s명이며 확진환자는 %s명입니다.\n" % (data['check_num'], data['confirmator_num'])

def get_discharged_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+"\n%s명이 퇴원조치 되었습니다.\n총 완치자 비율은 %s%%입니다.\n" % (data['discharged_num'], data['cured_rate'])

def get_death_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    return data['update_date']+"\n총 사망자 수는 %s명입니다.\n" % data['death_num']

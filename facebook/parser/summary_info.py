import requests
import os

# TODO 지역별 확진자

def get_daily_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    update_date = data['update_date']
    domestic_num = data['domestic_num']
    oversea_num = data['oversea_num']
    total_num = int(domestic_num.replace(',', '')) + int(oversea_num.replace(',', ''))
    return update_date+","+"\n일일확진자는 %s명입니다.\n그 중 국내발생은 %s명이며,\n해외유입 확진자는 %s명입니다." % (format(total_num, ','), domestic_num, oversea_num)

def get_confirmator_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    update_date = data['update_date']
    check_num = data['check_num']
    confirmator_num = data['confirmator_num']
    return update_date +","+"\n검사를 진행중인 인원은 %s명이며 확진환자는 %s명입니다.\n" % (check_num, confirmator_num)

def get_discharged_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    update_date = data['update_date']
    discharged_num = data['discharged_num']
    cured_rate = data['cured_rate']
    return update_date+","+"\n%s명이 퇴원조치 되었습니다.\n총 완치자 비율은 %s%%입니다.\n" % (discharged_num, cured_rate)

def get_death_num():
    data = requests.get(os.environ['S3_BUCKET_URL']+"summary.json").json()
    update_date = data['update_date']
    death_num = data['death_num']
    return update_date+","+"\n총 사망자 수는 %s명입니다.\n" % death_num

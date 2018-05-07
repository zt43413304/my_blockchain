# coding=utf-8

import configparser
import json
import logging
import os
import re
import time

import requests
import schedule

from common import Send_email

# 日志
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'bixiang.log'
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

ch.setFormatter(formatter)
logger.addHandler(ch)

# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')


# get config information
curpath = os.getcwd()
content = open(curpath + '/config_bixiang.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/config_bixiang.ini', 'w').write(content)

cf = configparser.ConfigParser()
cf.read(curpath + '/config_bixiang.ini')
# unique = cf.get('info', 'unique').strip()
# uid = cf.get('info', 'uid').strip()
is_ad_ios = cf.get('info', 'is_ad_ios').strip()
versioncode = cf.get('info', 'versioncode').strip()
devicetype = cf.get('info', 'devicetype').strip()
channel = cf.get('info', 'channel').strip()
token = cf.get('info', 'token').strip()
ps = cf.get('info', 'ps').strip()
key = cf.get('info', 'key').strip()

headers = {
    'Host': "tui.yingshe.com",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'User-Agent': "okhttp/3.4.1",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}

payload = "is_ad_ios=" + is_ad_ios + \
          "&versioncode=" + versioncode + \
          "&devicetype=" + devicetype + \
          "&channel=" + channel + \
          "&token=" + token + \
          "&ps=" + ps + \
          "&key=" + key

# start
logging.warning('***** Start ...')


# user_agent = cf.get('info'+str(infoNum), 'user_agent').strip()
# device_id = cf.get('info'+str(infoNum), 'device_id').strip()

def bixiang_login(unique, uid):
    url = "http://tui.yingshe.com/check/index"

    payload_login = payload + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload_login, headers=headers)

        res = response.json()["status"]
        if res == 1:
            logging.warning('********** Login success. uid:' + uid)
            return 1
        else:
            logging.warning('********** Login fail. uid:' + uid)
            return -1
    except Exception as e:
        print(e)
        return -1


def bixiang_infoList(unique, uid):
    url = "http://tui.yingshe.com/live/info"

    payload_infoList = payload + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload_infoList, headers=headers)

        res = response.json()["status"]
        if res == 1:
            info = response.json()["info"]
            return info
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def bixiang_sharing(unique, uid, id):
    url = "http://tui.yingshe.com/live/infofrist"

    payload_id = payload + "&live_id=" + id + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload_id, headers=headers)

        res = response.json()["status"]
        if res == 1:
            # logging.warning('^^^^^^^^^^ Sharing.')
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def bixiang_shared(unique, uid, id):
    url = "http://tui.yingshe.com/share/getShareCircle"

    payload_id = payload + "&live_id=" + id + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload_id, headers=headers)

        res = response.json()["status"]
        if res == 1:
            # logging.warning('^^^^^^^^^^ Shared.')
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def bixiang_sign(unique, uid):
    url_check = "http://tui.yingshe.com/check/index"
    url_add = "http://tui.yingshe.com/check/add"

    payload_sign = payload + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url_check, data=payload_sign, headers=headers)

        res = response.json()["status"]
        if res == 1:
            is_check = int(response.json()["info"]["is_check"])
            # "is_check == 0",not signed
            if is_check == 0:
                time.sleep(1)
                response = requests.request("POST", url_add, data=payload_sign, headers=headers)
                time.sleep(1)
                checked = int(response.json()["info"]["is_check"])
                if checked == 1:
                    logging.warning('>>>>>>>>>>  Not Sign, Just Signed.')
                else:
                    logging.warning('>>>>>>>>>>  Not Sign, Sign fail.')
            else:
                logging.warning('>>>>>>>>>>  Have Signed.')
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def bixiang_upgrade(unique, uid):
    url = "http://tui.yingshe.com/member/getNoLevel"

    payload_upgrade = payload + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload_upgrade, headers=headers)

        res = response.json()["status"]
        if res == 1:
            logging.warning('>>>>>>>>>>  Upgrade. now_bxc=' + response.json()["info"]["now_bxc"])
            logging.warning('>>>>>>>>>>  Upgrade. level_bxc=' + response.json()["info"]["level_bxc"])
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def bixiang_property_url(unique, uid):
    url = "http://tui.yingshe.com/member/miningBxc"

    payload_property = payload + "&unique=" + unique + "&uid=" + uid

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload_property, headers=headers)

        res = response.json()["status"]
        if res == 1:
            property_url = response.json()["info"]["bxc_details"]
            return property_url
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def get_allTotal(unique, uid):
    # url = "http://tui.yingshe.com/user/property"
    # querystring = {"xxx":"swh6XfD8FvRBZr17Hufua"}

    url = bixiang_property_url(unique, uid)
    logging.warning(">>>>>>>>>> Property URL = " + url)

    payload_total = payload + "&unique=" + unique + "&uid=" + uid

    try:

        time.sleep(5)
        # response = requests.request("GET", url, data=payload_total, headers=headers)
        response = requests.request("GET", url, headers=headers)
        logging.warning(">>>>>>>>>> response.status_code = " + str(response.status_code))
        return response.content

    except Exception as e:
        print(e)
        return -1


def loop_bixiang():
    file = open('data_bixiang.json', 'r', encoding='utf-8')
    data_dict = json.load(file)

    for item in data_dict['data']:
        # content_list = []
        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        logging.warning('\n')
        logging.warning("========== Checking [" + uid + "] ==========")

        status = bixiang_login(unique, uid)
        if status == -1:
            continue
        else:
            infoList = bixiang_infoList(unique, uid)

            count = 0
            for i in range(len(infoList)):
                # if count > 15:
                #     break
                if int(infoList[i]["share_total"]) < 20:
                    continue
                lv_id = infoList[i]["lv_id"]
                bixiang_sharing(unique, uid, lv_id)
                bixiang_shared(unique, uid, lv_id)
                logging.warning('>>>>>>>>>> ' + str(count) + '. Shared info ' + str(lv_id))
                count = count + 1

            # sign
            bixiang_sign(unique, uid)

            # upgrade
            bixiang_upgrade(unique, uid)

            # calculate value
            content = get_allTotal(unique, uid)

        Send_email.send_SimpleHtmlEmail('newseeing@163.com', uid, content)
    logging.warning('********** Sending Email Complete!')


# Start from here...
loop_bixiang()

# ssl._create_default_https_context = ssl._create_unverified_context
# schedule.every(120).minutes.do(loop_data_mining)
schedule.every(8).hours.do(loop_bixiang)
# schedule.every().day.at("01:05").do(loop_data_mining)
# schedule.every().monday.do(loop_data_mining)
# schedule.every().wednesday.at("13:15").do(loop_data_mining)

while True:
    schedule.run_pending()
    time.sleep(1)

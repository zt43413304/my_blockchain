# coding=utf-8

import configparser
import json
import logging
import os
import random
import re
import time

import requests

from common import daxiang_proxy

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_bixiang.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang.log', mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

# get config information
curpath = os.getcwd()
content = open(curpath + '/bixiang/config_bixiang.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/bixiang/config_bixiang.ini', 'w').write(content)

cf = configparser.ConfigParser()
cf.read(curpath + '/bixiang/config_bixiang.ini')
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

# user_agent = cf.get('info'+str(infoNum), 'user_agent').strip()
# device_id = cf.get('info'+str(infoNum), 'device_id').strip()

# Random seconds
mail_subject = ''
MIN_SEC = 2
MAX_SEC = 5
proxies = ''


def bixiang_userInfo(unique, uid):
    global proxies
    global mail_subject
    url = "http://tui.yingshe.com/member/userInfo"

    payload_userInfo = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_userInfo(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_userInfo, headers=headers, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            show_id = response.json()["info"]["show_id"]
            nickname = response.json()["info"]["nickname"]
            phone = response.json()["info"]["phone"]
            bxc = response.json()["info"]["bxc"]
            mail_subject = phone
            logger.warning(
                '********** uid=' + uid + ', show_id=' + show_id + ', nickname=' + nickname +
                ', phone=' + phone + ', bxc=' + bxc)
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def bixiang_login(unique, uid):
    global proxies
    url = "http://tui.yingshe.com/check/index"

    payload_login = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_login(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_login, headers=headers, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            logger.warning('********** Login success.')
            bixiang_userInfo(unique, uid)
            return 1
        else:
            logger.warning('********** Login fail. uid:' + uid)
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


# 返回值：出错-1，第一次签到成功1，第二次检查2
def bixiang_sign(unique, uid):
    global proxies
    url_check = "http://tui.yingshe.com/check/index"
    url_add = "http://tui.yingshe.com/check/add"

    payload_sign = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_sign(), proxies = " + str(proxies))
        response = requests.request("POST", url_check, data=payload_sign, headers=headers, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            is_check = int(response.json()["info"]["is_check"])
            # "is_check == 0",not signed
            if is_check == 0:
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url_add, data=payload_sign, headers=headers)
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                checked = int(response.json()["info"]["is_check"])
                if checked == 1:
                    logger.warning('>>>>>>>>>> Not Sign, Just Signed.')
                    return 1
                else:
                    logger.warning('********** Not Sign, Sign fail.')
                    return -1
            else:
                logger.warning('********** Have Signed.')
                return 2
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def quiz_bixiang():
    # start
    logger.warning('********** Start from quiz_bixiang() ...')

    global proxies
    proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")

    file = open(curpath + '/bixiang/quiz_bixiang.json', 'r', encoding='utf-8')
    data_dict = json.load(file)
    content_list = []

    for item in data_dict['data']:
        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        phone = item.get('phone', 'NA')

        logger.warning("========== Checking [" + phone + "] ==========")

        status = bixiang_login(unique, uid)
        if status == -1:
            continue
        else:
            signed = bixiang_sign(unique, uid)

    logger.warning('********** Quiz Complete!')

# Start from here...
# loop_bixiang()

# ssl._create_default_https_context = ssl._create_unverified_context
# schedule.every(120).minutes.do(loop_bixiang)
# schedule.every(6).hours.do(loop_bixiang)
# schedule.every().day.at("01:05").do(loop_bixiang)
# schedule.every().monday.do(loop_bixiang)
# schedule.every().wednesday.at("13:15").do(loop_bixiang)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

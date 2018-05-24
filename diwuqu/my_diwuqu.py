# coding=utf-8

import json
import logging
import os
import re
import ssl
import time

import requests

from common import send_email

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_diwuqu.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_diwuqu.log', mode='w')
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
content = open(curpath + '/diwuqu/config_diwuqu.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/diwuqu/config_diwuqu.ini', 'w').write(content)


def captcha(phone):
    url = "https://server.diwuqu.vip/api/common/v1/captcha"

    payload = "{\"phone\":" + phone + ",\"type\":\"login\"}"
    headers = {
        'Content-Type': "application/json",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Cache-Control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["state"]
        if res == 'success':
            logger.warning('********** Captcha is sent.')
            return 0
        else:
            logger.warning('********** Captcha is not sent.')
            logger.warn('\n')
            return -1
    except Exception as e:
        print(e)
        return -1


def login(phone):
    url = "https://server.diwuqu.vip/api/app/v1/login/captcha"
    time.sleep(3)
    captcha = input("********** Enter your Captcha: ")
    logger.warning('********** Captcha input is: ' + captcha)

    payload = "{\"phone\":" + phone + ",\"captcha\":" + captcha + "}"
    headers = {
        'Content-Type': "application/json",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Cache-Control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["state"]
        if res == 'success':
            token = response.json()["data"]
            return token
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def save_token():
    # file = open('data_diwuqu.json', 'r', encoding='utf-8')
    # data_dict = json.load(file)

    # Reading data
    with open(curpath + '/diwuqu/data_diwuqu.json', 'r') as file:
        data_dict = json.load(file)

    for item in data_dict['data']:
        phone = item.get('phone', 'NA')
        logger.warning("========== Checking [" + phone + "] ==========")
        captcha(phone)
        token = login(phone)
        # token = "f56fd821-7dcf-4edd-a52f-372147aa72dd"
        item['token'] = token

    # Writing JSON data
    with open(curpath + '/diwuqu/data_diwuqu.json', 'w') as file_new:
        json.dump(data_dict, file_new)

    file_new.close()
    file.close()


def calculate(token):
    url = "https://server.diwuqu.vip/api/app/v1/user"

    headers = {
        'token': token,
        'Cache-Control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("GET", url, headers=headers)

        res = response.json()["state"]
        if res == 'success':
            calculate = response.json()["data"]["calculate"]
            logger.warning('********** Calculate is: ' + str(calculate))
            return calculate
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def record(token):
    url = "https://server.diwuqu.vip/api/app/v1/records/waiting"

    headers = {
        'token': token,
        'Cache-Control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("GET", url, headers=headers)

        res = response.json()["state"]
        if res == 'success':
            record = response.json()["data"]["list"]
            return record
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def accept(token, id):
    url = "https://server.diwuqu.vip/api/app/v1/record/accept/" + str(id)

    headers = {
        'token': token,
        'Cache-Control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("PUT", url, headers=headers)

        res = response.json()["state"]
        if res == 'success':
            logger.warning('>>>>>>>>>> Mining ' + str(id))

        else:
            logger.warning('>>>>>>>>>> Mining error ' + str(id))
    except Exception as e:
        print(e)


def get_allTotal(token):
    url = "https://server.diwuqu.vip/api/app/v1/properties"

    headers = {
        'Content-Type': "application/json",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Cache-Control': "no-cache",
        'token': token
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("GET", url, headers=headers)

        res = response.json()["state"]
        if res == 'success':
            total_list = response.json()["data"]["list"]
            return total_list
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def loop_diwuqu():
    # start
    logger.warning('********** Start from loop_diwuqu() ...')

    global calculated

    # Reading data
    with open(curpath + '/diwuqu/data_diwuqu.json', 'r') as file:
        data_dict = json.load(file)

    for item in data_dict['data']:
        content_list = []
        phone = item.get('phone', 'NA')
        token = item.get('token', 'NA')
        logger.warning("========== Checking [" + phone + "] ==========")

        if token == -1:
            logger.warning('********** Login fail!')
            continue
        else:
            logger.warning('********** Login success! token:' + token)

            calculated = calculate(token)

            # click all mine
            list = record(token)
            while len(list) != 0 and list != -1:
                for j in range(len(list)):
                    accept(token, list[j]["id"])
                list = record(token)

            # calculate value
            total_list = get_allTotal(token)

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            for k in range(len(total_list)):
                name = total_list[k]["integral"]["name"]
                quantity = total_list[k]["total"]
                price = total_list[k]["integral"]["referPrice"]
                value = quantity * price

                content_data = {
                    "name": name,
                    "quantity": quantity,
                    "price": price,
                    "value": value
                }
                content_list.append(content_data)

        # sending email
        send_email.send_diwuqu_HtmlEmail('newseeing@163.com', phone, calculated, content_list)
        logger.warning('********** Sending Email Complete!')

# Start from here...
# save_token()
# loop_diwuqu()

# ssl._create_default_https_context = ssl._create_unverified_context
# schedule.every(120).minutes.do(loop_onechain)
# schedule.every(8).hours.do(loop_diwuqu)
# schedule.every().day.at("01:05").do(loop_onechain)
# schedule.every().monday.do(loop_onechain)
# schedule.every().wednesday.at("13:15").do(loop_onechain)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

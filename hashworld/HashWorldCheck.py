# coding=utf-8

import json
import logging
import os
import random
import re
import ssl
import time

import requests

from common import send_email

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("HashWorldCheck.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/HashWorldCheck.log', mode='w')
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

curpath = os.getcwd()

# get config information
content = open(curpath + '/hashworld/config.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/hashworld/config.ini', 'w').write(content)

# Random seconds
MIN_SEC = 2
MAX_SEC = 5


def open_FirstPage():
    url = "https://game.hashworld.top/"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, verify=False)
        res = response.status_code
        logger.warning('********** open_FirstPage(), status_code=' + str(res))

        if res == 200:
            return res
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def login_GetAccessToken(payload):
    url = "https://game.hashworld.top/apis/accounts/token/"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            token = response.json()["data"]["token"]
            return token
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def get_prize_wheel(token):
    url = "https://game.hashworld.top/apis/game/prize_wheel/"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            wonder_list = response.json()['data']
            return wonder_list
    except Exception as e:
        print(e)
        return -1


def click_Lottery(token, block_number):
    url = "https://game.hashworld.top/apis/game/lottery/"

    headers = {
        'user-agent': "application/x-www-form-urlencoded",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    try:
        payload = "{\n\t\"block_number\": " + str(block_number) + "\n}"

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("PUT", url, data=payload, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            coin_name = response.json()["data"]["coin_name"]
            logger.warning('>>>>>>>>>> lottery...... ' + coin_name)
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def check_UserTotal(token):
    url = "https://game.hashworld.top/apis/coin/gift_wallet/"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "close"
    }

    total = 0

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            totallist = response.json()['data']
            for i in range(len(totallist)):
                market_price_cny = totallist[i]['coin']['market_price_cny']
                active_balance = totallist[i]['active_balance']
                total = total + market_price_cny * active_balance
            logger.warning('>>>>>>>>>> Total: ' + str(total))
            return total
        else:
            return -1
    except Exception as e:
        print(e)
        return -1
    finally:
        requests.session().close()


def loop_Lottery():
    all_total = 0
    content_list = []

    file = open(curpath + '/hashworld/hash_world_data.json', 'r', encoding='utf-8')
    data_dict = json.load(file)
    # print(data_dict)
    # print(type(data_dict))

    for item in data_dict['data']:
        phone = item.get('phone', 'NA')
        password = item.get('password', 'NA')
        data = dict(phone=phone, password=password)
        logger.warning("========== Checking [" + phone + "] ==========")

        token = login_GetAccessToken(data)
        if token == -1:
            logger.warning('********** Login fail!')
            continue
        else:
            logger.warning('********** Login success! token:' + token)

            wonder_list = get_prize_wheel(token)
            if wonder_list == -1:
                continue

            reveal = 0
            for i in range(len(wonder_list)):
                has_reveal = wonder_list[i]['has_reveal']
                if bool(has_reveal):
                    reveal = reveal + 1
            logger.warning('********** Has revealed: ' + str(reveal))

            # click Jackielg's land
            for j in range(len(wonder_list)):
                if reveal > 2:
                    break
                has_reveal = wonder_list[j]['has_reveal']
                if not bool(has_reveal):
                    if wonder_list[j]['land']['user']['nickname'] != "Jackielg":
                        continue
                    lottery = click_Lottery(token, j)

                    if lottery == -1:
                        logger.warning('>>>>>>>>>> Click Jackielg land failed.')
                        continue
                    else:
                        logger.warning('>>>>>>>>>> Click Jackielg land success.')
                        reveal = reveal + 1

            # click others land
            for k in range(len(wonder_list)):
                if reveal > 2:
                    break
                has_reveal = wonder_list[k]['has_reveal']
                if not bool(has_reveal):
                    lottery = click_Lottery(token, k)

                    if lottery == -1:
                        logger.warning('>>>>>>>>>> Click Others land failed.')
                        continue
                    else:
                        logger.warning('>>>>>>>>>> Click Others land success.')
                        reveal = reveal + 1

            value = check_UserTotal(token)
            all_total = all_total + value
            logger.warning("========== End[" + phone + "], Total[ " + str(all_total) + " ] ==========")
            logger.warning('\n')

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            content_data = {
                "phone": phone,
                "value": value
            }
            content_list.append(content_data)
            time.sleep(random.randint(MIN_SEC, MAX_SEC))
            # break

    # sending email
    send_email.send_HashWorld_HtmlEmail('newseeing@163.com', content_list)
    logger.warning('********** Sending Email Complete!')
    logger.warning('\n')


def loop_hashworldcheck():
    # start
    logger.warning('********** Start from loop_hashworldcheck() ...')

    status_code = open_FirstPage()
    while status_code != 200:
        time.sleep(300)
        status_code = open_FirstPage()
    loop_Lottery()


# Start from here...
# loop_hashworldcheck()

# schedule.every(120).minutes.do(loop_hashworldcheck)
# schedule.every(8).hours.do(loop_hashworldcheck)
# schedule.every().day.at("18:30").do(loop_hashworldcheck)
# schedule.every().monday.do(loop_hashworldcheck)
# schedule.every().wednesday.at("13:15").do(loop_hashworldcheck)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# coding=utf-8

import json
import logging
import os
import random
import re
import ssl
import time

import requests

from common import daxiang_proxy
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
proxies = ''


def open_FirstPage():
    global proxies
    url = "https://game.hashworld.top/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** open_FirstPage(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, verify=False, proxies=proxies, timeout=60)
        res = response.status_code
        logger.warning('********** open_FirstPage(), status_code=' + str(res))

        if res == 200:
            return res
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def login_GetAccessToken(payload):
    global proxies
    url = "https://game.hashworld.top/apis/accounts/token/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** login_GetAccessToken(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers, proxies=proxies, timeout=60)

        res = response.json()["status"]
        if res == 'common_OK':
            token = response.json()["data"]["token"]
            return token
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def get_strength_info(token):
    global proxies
    url = "https://game.hashworld.top/apis/game/strength/get_strength_info/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_strength_info(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=60)

        res = response.json()["status"]
        if res == 'common_OK':
            strength = response.json()['data']['strength']
            logger.warning(">>>>>>>>>> strength = " + str(strength))
            return strength
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def get_prize_wheel(token):
    global proxies
    url = "https://game.hashworld.top/apis/game/prize_wheel/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_prize_wheel(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=60)

        res = response.json()["status"]
        if res == 'common_OK':
            wonder_list = response.json()['data']
            return wonder_list
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def click_Lottery(token, block_number):
    global proxies
    url = "https://game.hashworld.top/apis/game/lottery/"

    headers = {
        'user-agent': "application/x-www-form-urlencoded",
        'referer': "https://game.hashworld.top/",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    try:
        # logger.warning("********** click_Lottery(), proxies = " + str(proxies))
        payload = "{\n\t\"block_number\": " + str(block_number) + "\n}"

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("PUT", url, data=payload, headers=headers, proxies=proxies, timeout=60)

        res = response.json()["status"]
        if res == 'common_OK':
            coin_name = response.json()["data"]["coin_name"]
            # amount = response.json()["data"]["amount"]
            logger.warning('********** lottery...... ' + coin_name)
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def check_UserTotal(token):
    global proxies
    url = "https://game.hashworld.top/apis/coin/gift_wallet/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
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
        logger.warning("********** check_UserTotal(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=60)

        res = response.json()["status"]
        if res == 'common_OK':
            totallist = response.json()['data']
            for i in range(len(totallist)):
                market_price_cny = totallist[i]['coin']['market_price_cny']
                active_balance = totallist[i]['active_balance']
                total = total + market_price_cny * active_balance
            logger.warning('********** Total: ' + str(total))
            return total
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1
    finally:
        requests.session().close()


def click_hashworld_land(token, strength, wonder_list):
    # 根据体力值判断循环次数
    while strength > 0:

        # reveal = 0
        # for i in range(len(wonder_list)):
        #     has_reveal = wonder_list[i]['has_reveal']
        #     if bool(has_reveal):
        #         reveal = reveal + 1
        # logger.warning('********** Has revealed: ' + str(reveal))

        # click Jackielg's land
        for j in range(len(wonder_list)):
            if strength < 1:
                break
            has_reveal = wonder_list[j]['has_reveal']
            if not bool(has_reveal):
                if wonder_list[j]['land']['user']['nickname'] != "Jackielg":
                    continue
                lottery = click_Lottery(token, j)

                if lottery == -1:
                    logger.warning('********** Click Jackielg land failed.')
                    continue
                else:
                    logger.warning('>>>>>>>>>> Click Jackielg land success.')
                    strength = strength - 1

        # click others land
        for k in range(len(wonder_list)):
            if strength < 1:
                break
            has_reveal = wonder_list[k]['has_reveal']
            if not bool(has_reveal):
                lottery = click_Lottery(token, k)

                if lottery == -1:
                    logger.warning('********** Click Others land failed.')
                    continue
                else:
                    logger.warning('>>>>>>>>>> Click Others land success.')
                    strength = strength - 1


def get_Landlist(token):
    global proxies
    url = "https://game.hashworld.top/apis/land/lbsland/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_Landlist(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            land_list = response.json()['data']
            return land_list
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def get_LandPrice(token, land_number):
    global proxies
    url = "https://game.hashworld.top/apis/land/hall/"

    headers = {
        # 不能用这个user-agent
        # 'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'user-agent': "application/x-www-form-urlencoded",
        'content-type': "application/json",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_LandPrice(), proxies = " + str(proxies))
        payload = "{\n\t\"land\": {\n\t\t\"id\": [" + str(land_number) + "]\n\t}\n}"

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            land_name = response.json()["data"][0]["land_name"]
            price = response.json()["data"][0]["price"]
            tradable_status = response.json()["data"][0]["tradable_status"]
            gen_time = response.json()["data"][0]["gen_time"]
            nickname = response.json()["data"][0]["user"]["nickname"]
            return land_name, price, tradable_status, gen_time, nickname
        else:
            return "error", 0, "untradable", 0, ""
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return "error", 0, "untradable", 0, ""


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

        logger.warning('\n')
        logger.warning("========== Checking [" + phone + "] ==========")

        token = login_GetAccessToken(data)
        if token == -1:
            logger.warning('********** Login fail!')
            continue
        else:
            logger.warning('********** Login success! token:' + token)

            # 体力值
            strength = get_strength_info(token)

            # 土地列表
            wonder_list = get_prize_wheel(token)
            if wonder_list == -1 or strength == -1:
                continue

            click_hashworld_land(token, strength, wonder_list)

            value = check_UserTotal(token)
            all_total = all_total + value
            logger.warning("========== End[" + phone + "], Total[ " + str(all_total) + " ] ==========")

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


def loop_Land():
    content_land_list = []

    data = dict(phone="+8614716980512", password="Liuxb0504")

    token = login_GetAccessToken(data)
    if token == -1:
        logger.warning('********** Login fail!')
    else:
        logger.warning('********** Login success! token:' + token)

        # find land list and price
        land_list = get_Landlist(token)
        for i in range(len(land_list)):
            land_Num = land_list[i][0]
            (land_name, price, tradable_status, gen_time, nickname) = get_LandPrice(token, land_Num)
            logging.warning(
                '********** Land_Num:' + str(land_Num) + ", Land_Name:" + land_name + ", Price = " + str(price))

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            land_data = {
                "land_num": land_Num,
                "land_name": land_name,
                "price": price,
                "tradable_status": tradable_status,
                "gen_time": gen_time,
                "nickname": nickname
            }
            content_land_list.append(land_data)
            # if i == 2:
            #     break

        # sending email
        # content_land_list = sorted(content_land_list, key=lambda x: x["price"])
        content_land_list = sorted(content_land_list, key=lambda x: (x["tradable_status"], x["price"]))
        send_email.send_HashWorld_LandEmail('newseeing@163.com', content_land_list)
        logger.warning('********** Sending Land Email Complete!')
        logger.warning('\n')

def loop_hashworldcheck():
    # start
    logger.warning('********** Start from loop_hashworldcheck() ...')

    global proxies
    proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")

    status_code = open_FirstPage()
    while status_code != 200:
        time.sleep(300)
        status_code = open_FirstPage()
    loop_Lottery()
    loop_Land()

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

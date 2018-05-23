# coding=utf-8

import logging
import ssl
import time

import requests

from common import send_email

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("HashWorldLand.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/HashWorldLand.log', mode='w')
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


def open_FirstPage():
    url = "https://game.hashworld.top/"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'user-agent': "Mozilla/5.0 (Linux; Android 4.4.2; ZTE Q2S-T Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
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
        'user-agent': "Mozilla/5.0 (Linux; Android 4.4.2; ZTE Q2S-T Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
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


def get_Landlist(token):
    url = "https://game.hashworld.top/apis/land/lbsland/"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'user-agent': "Mozilla/5.0 (Linux; Android 4.4.2; ZTE Q2S-T Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache"
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(1)
        response = requests.request("GET", url, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            land_list = response.json()['data']
            return land_list
    except Exception as e:
        print(e)
        return -1


def get_LandPrice(token, land_number):
    url = "https://game.hashworld.top/apis/land/hall/"

    headers = {
        'user-agent': "application/x-www-form-urlencoded",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    try:
        payload = "{\n\t\"land\": {\n\t\t\"id\": [" + str(land_number) + "]\n\t}\n}"

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(2)
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["status"]
        if res == 'common_OK':
            land_name = response.json()["data"][0]["land_name"]
            price = response.json()["data"][0]["price"]
            tradable_status = response.json()["data"][0]["tradable_status"]
            gen_time = response.json()["data"][0]["gen_time"]
            return land_name, price, tradable_status, gen_time
        else:
            return "error", 0, "untradable", 0
    except Exception as e:
        print(e)
        return "error", 0, "untradable", 0


def loop_Land():
    content_land_list = []

    data = dict(phone="+8613826090504", password="Liuxb0504")

    token = login_GetAccessToken(data)
    if token == -1:
        logger.warning('********** Login fail!')
    else:
        logger.warning('********** Login success! token:' + token)

        # find land list and price
        land_list = get_Landlist(token)
        for i in range(len(land_list)):
            land_Num = land_list[i][0]
            (land_name, price, tradable_status, gen_time) = get_LandPrice(token, land_Num)
            logger.warning(
                '********** Land_Num:' + str(land_Num) + ", Land_Name:" + land_name + ", Price = " + str(price))

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            land_data = {
                "land_num": land_Num,
                "land_name": land_name,
                "price": price,
                "tradable_status": tradable_status,
                "gen_time": gen_time
            }
            content_land_list.append(land_data)
            # if i == 2:
            #     break

        # sending email
        # content_land_list = sorted(content_land_list, key=lambda x: x["price"])
        content_land_list = sorted(content_land_list, key=lambda x: (x["tradable_status"], x["price"]))
        send_email.send_LandEmail('newseeing@163.com', content_land_list)
        logger.warning('********** Sending Land Email Complete!')
        logger.warning('\n')


def loop_hashworldland():
    # start
    logger.warning('********** Start from loop_hashworldland() ...')

    status_code = open_FirstPage()
    while status_code != 200:
        time.sleep(300)
        status_code = open_FirstPage()
    loop_Land()

# Start from here...
# loop_hashworldland()

# ssl._create_default_https_context = ssl._create_unverified_context
# schedule.every(120).minutes.do(loop_hashworldcheck)
# schedule.every(2).hours.do(loop_hashworldcheck)
# schedule.every().day.at("18:30").do(loop_hashworldcheck)
# schedule.every().monday.do(loop_hashworldcheck)
# schedule.every().wednesday.at("13:15").do(loop_hashworldcheck)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
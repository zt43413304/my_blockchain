# coding=utf-8

import logging
import ssl
import time

import requests

from common import daxiang_proxy

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("HashWorldLand.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/HashWorldLand.log', mode='w', encoding='UTF-8')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)  # 输出到console的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

# Random seconds
MIN_SEC = 2
MAX_SEC = 5
proxies = ''

def open_FirstPage():
    global proxies
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
    global proxies
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







def loop_hashworldland():
    # start
    logger.warning('********** Start from loop_hashworldland() ...')

    global proxies
    proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")

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

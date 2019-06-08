# coding=utf-8

import json
import logging
import os
import random
import time
import urllib
from urllib.parse import urlparse

import requests
import requests.packages.urllib3.util.ssl_
from requests.packages import urllib3

from common import send_email

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_star163.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_star163.log', mode='w')
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

# Random seconds
MIN_SEC = 1
MAX_SEC = 3


def start163_api_starUser_getCookie(k, p):
    urllib3.disable_warnings()
    url = "https://star.8.163.com/api/starUser/getCookie"

    payload = "{\n\t\"k\": \"" + k + "\",\n\t\"p\": \"" + p + "\"\n}"
    headers = {
        'appMeta': "ewogICJkZXZpY2VJZCIgOiAie1wiaWRfdmVyXCI6XCJJT1NfMS4zLjAuMVwiLFwicmtcIjpcIlpGbmR6OWhxdU1DVlJBZVA0SFRpcUFXZlBrdFRyMzlpMHhcXFwvbnZ5eWFBVW1PVU1KRm9qalNidVpOaFB0eWVHWHdTZTFKdnZZdmhLVUQwTEpxT3pDVUtcXFwvNThDRHJVcnlaajNhWEcrc0VQYThNQk5MdWdYdEFRb0xLZko2bVRPNDdSU3lTaWpNREluWGVkU1ljWVl6Nm0rOXZGSU1DRzZxeEI3bG5GdWZaTVxcXC94RT1cIixcInJkYXRhXCI6XCJScmJrbjIwUzROb2xDc2RlZUEzeHJkNWVvMHA1dzdrM3loZXFcXFwvZEZ3OVhDZEtOR2JBTDZnaTllVW4ySW5GTTB5XCIsXCJkYXRhdHlwZVwiOlwiYWltdF9kYXRhc1wifSIsCiAgImFwcFZlcnNpb24iIDogIjEuOS4yIiwKICAiYXBwTmFtZSIgOiAi572R5piT5pif55CDIiwKICAiZGV2aWNlTmFtZSIgOiAiaVBob25lNlAiLAogICJtb2RlbCIgOiAiQTE1MjJcL0ExNTI0XC9BMTU5MyIsCiAgImFwcElkIiA6ICJjb20ubmV0ZWFzZS5QbGFuZXRQbGFuIiwKICAiYW50aVNwYW1JbmZvIiA6ICJ7XCJpZF92ZXJcIjpcIklPU18xLjMuMC4xXCIsXCJya1wiOlwiRjVTVnYrYytNVmJRRFhmUk1vWHcrNTBYQWsybVRJUlBkOEVlSUY1ZjFHaDhZWUxPY1FyeGUyU0pPMlR0QTJ3S3Rqb1ViQjJWZFBjMTltc0dhaHlkSUdPZGpDR2VPVXpJOFRtS1lPVWk2VzRvN0NhTVVEdnRPcnYzMVxcXC9WV01LQjIyT1RmS1dwdjhiV1dKNmJjdHhKT3pwTzdhU0ZzTGZzdWZLNnZqdll1VjhZPVwiLFwicmRhdGFcIjpcIjI4ZndrOWxjWmJWN3ZYWXVWREFkTlpMVmYwRnY4YlZEV0tnN2kxQUhudXp0RmdCUDAwbkRIMnJYM2gzcElWY0ppQ2w3NzgxMEpibElDSHczcGJCVnFpK1pTaHJmQXpwYjhtbzNjamU3amhCNnU2UjNHY2ZHVDVzQmJqaTdDeVhFSElSWk40T1ZyeDRzT0NGU2haVkFjQXpsYldnT2VDbkN1SFZMR2oxWUNJczZWSk53S0grN3lUZFZLMWt1dFUwVDR1OXZnTlFubExCWjR3bTNVTU8yTGVRdjZuVUp6T1psWERPUkZBSUJyR0lYc2luSFZcXFwvSjlEekN0UkM1OUhkaVVBR2VKWFRpaERCekFabXdnRHBXa2FaK2NVTUpTRWY0bkxZWU5YcDdjM0QwTERqRmY5RFdCMEtWOVpvcVFHbk9IaTZYVWkzUTdURUVOOVRQOXdmbEd2SG92Ykg0bG5ZUFNyXFxcL3hjdTZaU1E4RVczZHFPbEdFRTkxZW1tclg0NjVkQ2JRbGhjUTFYbWJVUUJvS0hKSTl2Wk9YVmtMMEhkQWFDUVFzOUZ4VE5sRVU9XCIsXCJkYXRhdHlwZVwiOlwiYWltdF9kYXRhc1wifSIsCiAgIk9TIiA6ICJpT1NfMTIuMy4xIgp9",
        'Content-Type': "application/json; charset=utf-8",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "application/gzip",
        'User-Agent': "okhttp/3.9.1",
        'Cache-Control': "no-cache"
    }

    try:
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)

        res = response.json()["code"]
        if res == 200:
            cookie = response.json()["data"]["cookie"]
            logger.warning("********** Get Cookie = " + cookie)
            return cookie
        else:
            logger.warning(">>>>>>>>>> Get Cookie failed.")
            return -1
    except Exception as e:
        print(e)
        return -1


def start163_api_home_index(cookie):
    url = "https://star.8.163.com/api/home/index"

    headers = {
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'X-Requested-With': "XMLHttpRequest",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'User-Agent': "application/x-www-form-urlencoded",
        'Content-Type': "application/json",
        'Cookie': "NTES_YD_SESS=" + cookie,
        'Cache-Control': "no-cache"
    }

    try:
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, headers=headers, verify=False)

        res = response.json()["code"]
        if res == 200:
            collectCoins = response.json()["data"]["collectCoins"]
            logger.warning(">>>>>>>>>> Get collectCoins length = " + str(len(collectCoins)))
            return collectCoins
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def star163_api_collectUserCoin(cookie, id):
    url = "https://star.8.163.com/api/starUserCoin/collectUserCoin"

    payload = "{\"id\":\"" + str(id) + "\"}"

    headers = {
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'X-Requested-With': "XMLHttpRequest",
        'Content-Type': "application/json",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'Cookie': "NTES_YD_SESS=" + cookie,
        'Cache-Control': "no-cache"
    }

    try:
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)

        res = response.json()["code"]
        if res == 200:
            logger.warning(">>>>>>>>>> Collect black diamond ...  " + str(id))
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def star163_api_starUserOrigin_getTaskUrl(cookie):
    url = "https://star.8.163.com/api/starUserOrigin/getTaskUrl"

    payload = "{\"task\":12}"
    headers = {
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'X-Requested-With': "XMLHttpRequest",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'User-Agent': "application/x-www-form-urlencoded",
        'Content-Type': "application/json",
        'Cookie': "NTES_YD_SESS=" + cookie,
        'Cache-Control': "no-cache"
    }

    try:
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)

        res = response.json()["code"]
        if res == 200:
            TaskUrl = response.json()["data"]["url"]
            logger.warning(">>>>>>>>>> Get TaskUrl = " + TaskUrl)
            return TaskUrl
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def star163_access_channel_list(TaskUrl):
    # 需要signature
    # 可访问URL格式
    url_access = "https://youliao.163yun.com/api-server/api/v1/info/view/list?appkey=50a07a16210f4a648cef0190d30ad828&attachPlatform=1&channelTag=cb349a1183584b16bc7333b7890d86de&group=2&history=1&num=10&platform=3&scene=f&signature=d0246201d85de349f9af52804d5ef6db&timestamp=1527307808000&userId=YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE&version=v1.8.0"

    # taskurl的格式, 调用返回值 “You need to enable JavaScript to run this app.”
    _taskurl = "https://youliao.163yun.com/h5/list/?ak=50a07a16210f4a648cef0190d30ad828&sk=2a67c201957242dc85a7e191afb194e2&extra=%7B%22msg%22%3A%22aklNVnVXbk50R3UwY2dqczkvb01ENUFlNE1TNnh3R3ZVdDVwdjlrNHkzMksrNnRxeE9tU0RFUXJBUGpjbkt3d3hwSExyRUdGQmV3RUl6eU9CRFQ2c1BoTGFCQkdOWk9VNncxZGxUbVdJclZCSXpWZXdjMkExbEk5UXhNMUM1aWx3Y0Vha1RrenpBRE9tKzgyY0ozaHRVenBZZGFhSFhDbmFBOG9saENpdWk0alVFRlNWQ09kTlVTb1JNeTNBUXMrRG95dGtmRkxhcXNBYWErOWF2OU81bU1NY3VWZWpsSVpXSko1U2FiVXRid3RFZFV5ZkZmdTQxL0pBU2dhekYrTUVKeWoxcG10OTIxK0x2Q2Y1UjM0SFprZ1AyTisxd1BaeGhpZWFIOC83NW1hVGt4TDZXQUNwMFI1ME9ZTThDdGxtcHQrUEI1d3BKeGhISmNRZnZJVjNZak9RZzlFa0E9PQ%22%2C%22add%22%3A%22YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE%22%7D&unid=YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE"

    # 构造新的new_url
    query_dict = urllib.parse.parse_qs(urlparse(TaskUrl).query)
    ak = query_dict.get('ak', 'NA')[0]
    sk = query_dict.get('sk', 'NA')
    extra = query_dict.get('extra', 'NA')
    unid = query_dict.get('unid', 'NA')[0]

    timestamp = int(round(time.time() * 1000))

    signature = "d0246201d85de349f9af52804d5ef6db"
    # "9d5720830aba54c4bff378b8ae49c83a"

    url_new = "https://youliao.163yun.com/api-server/api/v1/info/view/list?appkey=" + ak + \
              "&attachPlatform=1" + \
              "&channelTag=cb349a1183584b16bc7333b7890d86de" + \
              "&group=2" + \
              "&history=1" + \
              "&num=10" + \
              "&platform=3" + \
              "&scene=f" + \
              "&signature=" + signature + \
              "&timestamp=" + str(timestamp) + \
              "&userId=" + unid + \
              "&version=v1.8.0"

    headers = {
        'Host': "youliao.163yun.com",
        'Connection': "Keep-Alive",
        'Accept': "*/*",
        'Accept-Encoding': "gzip,deflate",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.4; MuMu Build/V417IR) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 hybrid/1 star_client_1.0.1",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.netease.blockchain",
        'Cache-Control': "no-cache"
    }

    # response = requests.request("GET", url, headers=headers, params=querystring)
    response = requests.request("GET", url_new, headers=headers)

    print(response.text)
    # {"requestId":"66af50cbb53a4f0798af6e08b36c5e31","code":1001,"message":"invalid signature","data":null}


def star163_access_default_url(Taskurl):
    headers = {
        'Host': "youliao.163yun.com",
        'Connection': "Keep-Alive",
        'Accept': "*/*",
        'Accept-Encoding': "gzip,deflate",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.4; MuMu Build/V417IR) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 hybrid/1 star_client_1.0.1",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.netease.blockchain",
        'Cache-Control': "no-cache"
    }

    # response = requests.request("GET", url, headers=headers, params=querystring)
    response = requests.request("GET", Taskurl, headers=headers)


def star163_get_channel_list(TaskUrl):
    # 138
    # 53627a28b6d668d1e3d4e00a92a06cc1
    # 136
    # aaaec827671ab0ed7a0be838514c2c60

    url = "https://youliao.163yun.com/api-server/api/v1/channel/list"

    # TaskUrl='https://youliao.163yun.com/h5/list/?ak=50a07a16210f4a648cef0190d30ad828&sk=2a67c201957242dc85a7e191afb194e2&extra=%7B%22msg%22%3A%22WGpmWElNQUl6WkN2b2Nmc0t0VUNZUmVEd2JkSWRzOW1UK0ZiNmJFYU1WalljcWZieXY5cFkzRHg5QnNRTjhLQ1IvUHc3NjZOSmZtazBuWnBObllyWGU3b21mMGRDRUtnVkE1bDB5T3dDTGRvU0JLOFJBcmJxZWRhcmZFNlhnK3FwcjBWTDFSZCtNMk9JTWFZaHNjdm1hNGZEWEFzZVIzb2x2bXFud1VHM1BjPQ%22%2C%22add%22%3A%22YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE%22%7D&unid=YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE'
    query_dict = urllib.parse.parse_qs(urlparse(TaskUrl).query)
    ak = query_dict.get('ak', 'NA')[0]
    sk = query_dict.get('sk', 'NA')
    extra = query_dict.get('extra', 'NA')
    unid = query_dict.get('unid', 'NA')

    timestamp = int(round(time.time() * 1000))

    url_new = "https://youliao.163yun.com/api-server/api/v1/channel/list?appkey=" + ak + \
              "&platform=3&signature=aaaec827671ab0ed7a0be838514c2c60&timestamp=" + str(timestamp) + "&version=v1.8.0"

    # querystring = {"appkey":"50a07a16210f4a648cef0190d30ad828","platform":"3","signature":"60ac74a4f5ec329c9e67afddbf25a099","timestamp":"1525682745640","version":"v1.8.0"}
    querystring = {"appkey": ak, "platform": "3", "signature": "aaaec827671ab0ed7a0be838514c2c60",
                   "timestamp": timestamp, "version": "v1.8.0"}

    headers = {
        'Host': "youliao.163yun.com",
        'Connection': "Keep-Alive",
        'Accept': "*/*",
        'Accept-Encoding': "gzip,deflate",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.4; MuMu Build/V417IR) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 hybrid/1 star_client_1.0.1",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.netease.blockchain",
        'Cache-Control': "no-cache"
    }

    # response = requests.request("GET", url, headers=headers, params=querystring)
    response = requests.request("GET", url_new, headers=headers)

    print(response.text)


def get_allTotal(cookie):
    url = "https://star.8.163.com/api/home/index"

    headers = {
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'X-Requested-With': "XMLHttpRequest",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'User-Agent': "application/x-www-form-urlencoded",
        'Content-Type': "application/json",
        'Cookie': "NTES_YD_SESS=" + cookie,
        'Cache-Control': "no-cache"
    }

    try:
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, headers=headers, verify=False)

        res = response.json()["code"]
        if res == 200:
            coin = response.json()["data"]["coin"]
            origin = response.json()["data"]["origin"]
            logger.warning(">>>>>>>>>> Black diamond:" + str(coin) + ", Calculate:" + str(origin))
            return coin, origin
        else:
            return -1, -1
    except Exception as e:
        print(e)
        return -1, -1


def loop_star163():
    curpath = os.getcwd()
    file = open(curpath + '/star163/data_star163.json', 'r', encoding='utf-8')
    data_dict = json.load(file)


    number = 0
    # collect black diamond
    for item in data_dict['data']:
        number += 1
        # break
        # content_list = []
        phone = item.get('phone', 'NA')
        k = item.get('k', 'NA')
        p = item.get('p', 'NA')

        logger.warning("========== Checking number: " + str(number))

        cookie = start163_api_starUser_getCookie(k, p)
        if cookie == -1:
            continue
        else:
            collectCoins = start163_api_home_index(cookie)

            for i in range(len(collectCoins)):
                star_id = collectCoins[i]["id"]
                star163_api_collectUserCoin(cookie, star_id)
        logger.warning('>>>>>>>>>> Collect black diamond complete!')

        # taskUrl = star163_api_starUserOrigin_getTaskUrl(cookie)
        # 有签名问题，未完成
        # star163_access_channel_list(taskUrl)

        # calculate value
        coin, origin = get_allTotal(cookie)
        content = ">>>>>>>>>> Calculate=" + str(origin) + ", Black diamond=" + str(coin)
        send_email.send_star163_HtmlEmail('newseeing@163.com', str(phone) + '的原力及黑钻', content)
        logger.warning('********** Sending Collect Email Complete!')

    # thread136 = AppiumStar163.AppiumStar('4.4.4', '127.0.0.1:7555', 4723, '13601223469')
    # # thread136.setName('13601223469')
    # # thread136.setDaemon(True)
    # thread136.start()
    # # thread136.join(10)
    # time.sleep(20)
    #
    # thread138 = AppiumStar163.AppiumStar('4.4.2', '127.0.0.1:62001', 4725, '13826090504')
    # # # thread138.setName('13826090504')
    # # # thread136.setDaemon(True)
    # thread138.start()
    # # thread136.join(10)

# Start from here...
# logger.warning('***** Start ...')
# loop_star163()

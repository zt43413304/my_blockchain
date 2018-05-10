# coding=utf-8

import json
import logging
import os
import subprocess
import time
import urllib
from urllib.parse import urlparse

import AppiumStar163
import requests

# 日志
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'star163.log'
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

logger.removeHandler(ch)
logger.removeHandler(fh)
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')

# start
logging.warning('***** Start ...')


def start163_api_starUser_login():
    url = "https://star.8.163.com/api/starUser/login"

    payload = "{\n\t\"k\": \"Hc8JxvLd0acZjgDzBMEHOrMdBfXlgfsFuXKw2EVT3ZRvrHlrE+IpE7bqwm4kRt/xjlXZ0P2JY0xvDtmCvG6oSBpqyYJWk+BbQRofvR7bNaDMD2/hSm1WyR7UuqYuqxIBem5FuvGW3cod22H9K1BhFGiq963LnyxYXpzu8R1FBcQ=\",\n\t\"p\": \"tyHo+vXjBdqHzL/OTy0PUcgNeL+WnlKXMvo7vTqPShb60LyqJubewOGr+E/8B7lZLCyFCqUY0Rm1F05kZnV32Dz5ymP4gJAMiYnZkuqHi9Lu1qssmfAsuK9oSzAusWbU77JFmAHDqxbspx5mtPmFz7C+RGl8udIMb92sVTLi0mf12IEYDvw/MmL7TKdkxblHK13KSk93ty4PzTVvVEp38YzwIi2wNzs7P1WWi3PZraiIwXeIhOv2UODGZohppkzQylKpuzkn2RvggkM3O4gK3R6AJxZ4heN+MMmfvOADSZf/VIlRWmA4vkVK4kS99z0aSkn+Ta5hBCY6FDxxDoAcU36n/MKe00iNluMpI1opO567mW37xbtsK0tsNKJmK/NE\"\n}"
    headers = {
        'appMeta': "eyJhcHBOYW1lIjoi5pif55CDIiwibW9kZWwiOiJNdU11IiwicGFja2FnZU5hbWUiOiJjb20ubmV0ZWFzZS5ibG9ja2NoYWluIiwiYXBwVmVyc2lvbiI6IjEuMC4xIiwiYXBwVmVyc2lvbkNvZGUiOiI2OSIsIk9TIjoiQW5kcm9pZF8xOSIsImNoYW5uZWwiOiJlMDExNzAwMjMiLCJkZXZpY2VJZCI6IntcImRhdGF0eXBlXCI6XCJhaW10X2RhdGFzXCIsXCJpZF92ZXJcIjpcIkFuZHJvaWRfMS4wLjFcIixcInJkYXRhXCI6XCJ0ZkNpcC9ETDJoL1p2dVlqQmo4clZJcFh5aGt2bHNIQzZhUzJnbkppUnNvbzNpdHU4VjNQRnloMkVlYy84a0h6XCIsXCJya1wiOlwiSUdpUUQ4eXNkRksvalVPN2FiSTdYSWhSd05sb3RXS0lRMjFMbCsrVW9wendGOElJVjFEaEZOZEVOM2srZ0w2Q2NFYXF6YVlWV3QweUJjUGU2WTZRanZCS0RtS214T1dweXc5Y0Ztb3p4SlQ4VHRBNm9CY2pub0NsQ3pBcUFlRXJudUxmSDBPM3hTeWdGK0xMTzFPaW1lZ0d5a1B0NU1iZ2FBamQ4YXZtcTRNXHUwMDNkXCJ9XG4ifQ==",
        'Content-Type': "application/json",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "application/gzip",
        'User-Agent': "okhttp/3.9.1",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def start163_api_starUser_checkIn():
    url = "https://star.8.163.com/api/starUser/checkIn"

    payload = "{\n\t\"k\": \"hbfj5QpcTAEf9A7FtLtLLqVZp4XY1k3DrGo7T7oJlRZi/vtGgIQWWcI+AzviTK9xnISAfrL/Tpl5lrmBO6aLgBhOLv0zydWN8C6VnRkhDODBPLXnQwJuDo/nIk4Yd7F7EaLlYbnKm3csAHsJzYPgco6qThcLlWSEwSTOAsle1HU=\",\n\t\"p\": \"uRFGFjtIXFpK0LmJ/lXJylYt03XRhn0DMER/ydDFTRbmueczwS2ljRHEeOzgSvsZ7u7S8+Euhl9D7X2X1E8iFFkh3TV3j3jMOPeLhUpYh6Te7VjL8qyG0LwcGImhAc3InF83GQEHlEieAR84nWGXuw==\"\n}"
    headers = {
        'appMeta': "eyJhcHBOYW1lIjoi5pif55CDIiwibW9kZWwiOiJNdU11IiwicGFja2FnZU5hbWUiOiJjb20ubmV0ZWFzZS5ibG9ja2NoYWluIiwiYXBwVmVyc2lvbiI6IjEuMC4xIiwiYXBwVmVyc2lvbkNvZGUiOiI2OSIsIk9TIjoiQW5kcm9pZF8xOSIsImNoYW5uZWwiOiJlMDExNzAwMjMiLCJkZXZpY2VJZCI6IntcImRhdGF0eXBlXCI6XCJhaW10X2RhdGFzXCIsXCJpZF92ZXJcIjpcIkFuZHJvaWRfMS4wLjFcIixcInJkYXRhXCI6XCJ0ZkNpcC9ETDJoL1p2dVlqQmo4clZJcFh5aGt2bHNIQzZhUzJnbkppUnNvbzNpdHU4VjNQRnloMkVlYy84a0h6XCIsXCJya1wiOlwiSUdpUUQ4eXNkRksvalVPN2FiSTdYSWhSd05sb3RXS0lRMjFMbCsrVW9wendGOElJVjFEaEZOZEVOM2srZ0w2Q2NFYXF6YVlWV3QweUJjUGU2WTZRanZCS0RtS214T1dweXc5Y0Ztb3p4SlQ4VHRBNm9CY2pub0NsQ3pBcUFlRXJudUxmSDBPM3hTeWdGK0xMTzFPaW1lZ0d5a1B0NU1iZ2FBamQ4YXZtcTRNXHUwMDNkXCJ9XG4ifQ==",
        'Content-Type': "application/json",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "application/gzip",
        'User-Agent': "okhttp/3.9.1",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def start163_api_starUser_getCookie(k, p):
    url = "https://star.8.163.com/api/starUser/getCookie"

    payload = "{\n\t\"k\": \"" + k + "\",\n\t\"p\": \"" + p + "\"\n}"
    headers = {
        'appMeta': "eyJhcHBOYW1lIjoi5pif55CDIiwibW9kZWwiOiJNdU11IiwicGFja2FnZU5hbWUiOiJjb20ubmV0ZWFzZS5ibG9ja2NoYWluIiwiYXBwVmVyc2lvbiI6IjEuMC4xIiwiYXBwVmVyc2lvbkNvZGUiOiI2OSIsIk9TIjoiQW5kcm9pZF8xOSIsImNoYW5uZWwiOiJlMDExNzAwMjMiLCJkZXZpY2VJZCI6IntcImRhdGF0eXBlXCI6XCJhaW10X2RhdGFzXCIsXCJpZF92ZXJcIjpcIkFuZHJvaWRfMS4wLjFcIixcInJkYXRhXCI6XCJ0ZkNpcC9ETDJoL1p2dVlqQmo4clZJcFh5aGt2bHNIQzZhUzJnbkppUnNvbzNpdHU4VjNQRnloMkVlYy84a0h6XCIsXCJya1wiOlwiSUdpUUQ4eXNkRksvalVPN2FiSTdYSWhSd05sb3RXS0lRMjFMbCsrVW9wendGOElJVjFEaEZOZEVOM2srZ0w2Q2NFYXF6YVlWV3QweUJjUGU2WTZRanZCS0RtS214T1dweXc5Y0Ztb3p4SlQ4VHRBNm9CY2pub0NsQ3pBcUFlRXJudUxmSDBPM3hTeWdGK0xMTzFPaW1lZ0d5a1B0NU1iZ2FBamQ4YXZtcTRNXHUwMDNkXCJ9XG4ifQ==",
        'Content-Type': "application/json; charset=utf-8",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "application/gzip",
        'User-Agent': "okhttp/3.9.1",
        'Cache-Control': "no-cache"
    }

    try:
        time.sleep(1)
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["code"]
        if res == 200:
            cookie = response.json()["data"]["cookie"]
            logging.warning(">>>>>>>>>> Get Cookie = " + cookie)
            return cookie
        else:
            logging.warning(">>>>>>>>>> Get Cookie failed.")
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
        time.sleep(1)
        response = requests.request("POST", url, headers=headers)

        res = response.json()["code"]
        if res == 200:
            collectCoins = response.json()["data"]["collectCoins"]
            logging.warning(">>>>>>>>>> Get collectCoins length = " + str(len(collectCoins)))
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
        time.sleep(1)
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["code"]
        if res == 200:
            logging.warning(">>>>>>>>>> Collect black diamond ...  " + str(id))
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
        time.sleep(1)
        response = requests.request("POST", url, data=payload, headers=headers)

        res = response.json()["code"]
        if res == 200:
            TaskUrl = response.json()["data"]["url"]
            logging.warning(">>>>>>>>>> Get TaskUrl = " + TaskUrl)
            return TaskUrl
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def star163_access_channel_list(TaskUrl):
    url = "https://youliao.163yun.com/api-server/api/v1/channel/list"

    # TaskUrl='https://youliao.163yun.com/h5/list/?ak=50a07a16210f4a648cef0190d30ad828&sk=2a67c201957242dc85a7e191afb194e2&extra=%7B%22msg%22%3A%22WGpmWElNQUl6WkN2b2Nmc0t0VUNZUmVEd2JkSWRzOW1UK0ZiNmJFYU1WalljcWZieXY5cFkzRHg5QnNRTjhLQ1IvUHc3NjZOSmZtazBuWnBObllyWGU3b21mMGRDRUtnVkE1bDB5T3dDTGRvU0JLOFJBcmJxZWRhcmZFNlhnK3FwcjBWTDFSZCtNMk9JTWFZaHNjdm1hNGZEWEFzZVIzb2x2bXFud1VHM1BjPQ%22%2C%22add%22%3A%22YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE%22%7D&unid=YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE'
    query_dict = urllib.parse.parse_qs(urlparse(TaskUrl).query)
    ak = query_dict.get('ak', 'NA')[0]
    sk = query_dict.get('sk', 'NA')
    extra = query_dict.get('extra', 'NA')
    unid = query_dict.get('unid', 'NA')

    timestamp = int(round(time.time() * 1000))

    url_new = "https://youliao.163yun.com/api-server/api/v1/info/view/list?appkey=" + ak + \
              "&attachPlatform=1&channelTag=cb349a1183584b16bc7333b7890d86de&group=2&history=1&num=10&platform=3&" + \
              "scene=f&signature=9d5720830aba54c4bff378b8ae49c83a&timestamp=" + str(timestamp) + \
              "&userId=YzEwZjE0ODJkZDAwYmVkY2MwMTZmNzZjMzlkYjIzZmE&version=v1.8.0"

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


# def get_allTotal(unique, uid):


# url = "http://tui.yingshe.com/user/property"
# querystring = {"xxx":"swh6XfD8FvRBZr17Hufua"}

# url = bixiang_property_url(unique, uid)
# logging.warning(">>>>>>>>>> Property URL = " + url)
#
# payload_total = payload + "&unique=" + unique + "&uid=" + uid
#
# try:
#
#     time.sleep(5)
#     # response = requests.request("GET", url, data=payload_total, headers=headers)
#     response = requests.request("GET", url, headers=headers)
#     logging.warning(">>>>>>>>>> response.status_code = " + str(response.status_code))
#     return response.content
#
# except Exception as e:
#     print(e)
#     return -1


def execute_command(cmd):
    print('***** start executing cmd...')
    p = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderrinfo, stdoutinfo = p.communicate()
    for line in stdoutinfo.splitlines():
        print(line)

        # print('stderrinfo is -------> %s and stdoutinfo is -------> %s' % (stderrinfo, stdoutinfo))
    print('stdoutinfo is -------> %s' % stdoutinfo)
    print('stderrinfo is -------> %s' % stderrinfo)
    print('finish executing cmd....')
    return p.returncode


def loop_star163():
    file = open('data_star163.json', 'r', encoding='utf-8')
    data_dict = json.load(file)

    # collect black diamond
    for item in data_dict['data']:
        # content_list = []
        k = item.get('k', 'NA')
        p = item.get('p', 'NA')
        # logging.warning("========== Checking [" + k + "] ==========")

        cookie = start163_api_starUser_getCookie(k, p)
        if cookie == -1:
            continue
        else:
            collectCoins = start163_api_home_index(cookie)

            for i in range(len(collectCoins)):
                star_id = collectCoins[i]["id"]
                star163_api_collectUserCoin(cookie, star_id)
        logging.warning('********** Collect black diamond complete!')

    # Get Calculate
    for item in data_dict['data']:
        # content_list = []
        k = item.get('k', 'NA')
        p = item.get('p', 'NA')
        # logging.warning("========== Reading [" + k + "] ==========")

        # cmd_clean = r'cmd.exe C:/DevTools/my_blockchain/star163/clean.bat'
        # result1 = execute_command(cmd_clean)
        # print('result:------>', result1)


        output = os.system("C:/DevTools/MuMu/emulator/nemu/EmulatorShell/NemuPlayer.exe")
        logging.warning(">>>>>>>>>> Start NemuPlayer.exe, output = " + str(output))
        time.sleep(30)

        cmd_adb = r'adb connect 127.0.0.1:7555'
        result1 = execute_command(cmd_adb)
        print('result:------>', result1)

        cmd_adb1 = r'adb devices -l'
        result2 = execute_command(cmd_adb1)
        print('result:------>', result2)

        # python执行直接用【os.system(要执行的命令)】即可，如果是windows下\n和\a需要转义，所以用下面的内容
        # cmd_app_desktop = r'start /b node C:\Users\Jackie.Liu\AppData\Local\appium-desktop\app-1.6.0\resources\app\node_modules\appium\build\lib\main.js'

        # cmd_appium = r'start /b node C:\DevTools\Appium\node_modules\appium\lib\server\main.js --address 127.0.0.1 --port 4723'
        # result3 = execute_command(cmd_app_desktop)

        output3 = os.system(
            "start node C:/Users/Jackie.Liu/AppData/Local/appium-desktop/app-1.6.0/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4723")
        print('result:------>' + str(output3))
        time.sleep(30)

        # 需要手动确定启动Server
        # output3 = os.system("C:/Users/Jackie.Liu/AppData/Local/appium-desktop/Appium.exe -a 127.0.0.1 -p 4723")

        appium = AppiumStar163.AppiumStar()
        appium.appium_zixun()

        break
    # logging.warning('********** Sending Email Complete!')

    # # calculate value
    # content = get_allTotal(unique, uid)

    # Send_email.send_SimpleHtmlEmail('newseeing@163.com', uid, content)
    logging.warning('********** Sending Email Complete!')


# Start from here...
loop_star163()

# ssl._create_default_https_context = ssl._create_unverified_context
# schedule.every(120).minutes.do(loop_star163)
# schedule.every(8).hours.do(loop_star163)
# schedule.every().day.at("01:05").do(loop_star163)
# schedule.every().monday.do(loop_star163)
# schedule.every().wednesday.at("13:15").do(loop_star163)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

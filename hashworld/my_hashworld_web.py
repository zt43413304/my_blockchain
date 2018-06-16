# coding=utf-8

import json
import logging
import os
import random
import re
import ssl
import subprocess
import time

import requests

# 第一步，创建一个logger,并设置级别
from hashworld import Appium_hashworld

# from common import daxiang_proxy
# from common import send_email

logger = logging.getLogger("my_hashworld_web.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_hashworld_web.log', mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
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
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=60, verify=False)
        res = response.status_code
        logger.warning('********** open_FirstPage(), status_code=' + str(res))

        if res == 200:
            return res
        else:
            return -1
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


# Random seconds
MIN_SEC = 1
MAX_SEC = 3


def execute_command(cmd):
    print('***** start executing cmd...')
    p = subprocess.Popen(str(cmd), stderr=os.subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderrinfo, stdoutinfo = p.communicate()
    for line in stdoutinfo.splitlines():
        print(line)

        # print('stderrinfo is -------> %s and stdoutinfo is -------> %s' % (stderrinfo, stdoutinfo))
    print('stdoutinfo is -------> %s' % stdoutinfo)
    print('stderrinfo is -------> %s' % stderrinfo)
    print('finish executing cmd....')
    return p.returncode


def startup_emulator():
    output = os.system("/Applications/NemuPlayer.app")
    logger.warning(">>>>>>>>>> Start NemuPlayer.app, output = " + str(output))
    time.sleep(15)
    # cmd_adb = r'adb connect 127.0.0.1:7555'
    # result1 = execute_command(cmd_adb)
    # print('result:------>', result1)
    # cmd_adb1 = r'adb devices -l'
    # result2 = execute_command(cmd_adb1)
    # print('result:------>', result2)

    output = os.system(
        "node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4723")
    print('result:------>' + str(output))
    time.sleep(5)


def loop_Lottery(filename):
    all_total = 0
    content_list = []

    file = open(curpath + '/hashworld/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)
    # print(data_dict)
    # print(type(data_dict))

    number = 0
    for item in data_dict['data']:
        number += 1
        phone = item.get('phone', 'NA')
        password = item.get('password', 'NA')
        data = dict(phone=phone, password=password)

        logger.warning('\n')
        logger.warning("========== Checking " + str(number) + ". [" + phone + "] ==========")

        lands = Appium_hashworld.lands()

        result = lands.selenium_login(phone, password)
        time.sleep(random.randint(3, 5))
        result = lands.bixiang_clickland()
        break

        # token = login_GetAccessToken(data)
        # if token == -1:
        #     logger.warning('********** Login fail!')
        #     continue
        # else:
        #     logger.warning('********** Login success! token:' + token)
        #
        #     # 体力值
        #     strength = get_strength_info(token)
        #
        #     # 土地列表
        #     wonder_list = get_prize_wheel(token)
        #     if wonder_list == -1 or strength == -1:
        #         continue
        #
        #     click_hashworld_land(token, strength, wonder_list)
        #
        #     value = check_UserTotal(token)
        #     all_total = all_total + value
        #     logger.warning("========== End[" + phone + "], Total[ " + str(all_total) + " ] ==========")
        #
        #     # 构建Json数组，用于发送HTML邮件
        #     # Python 字典类型转换为 JSON 对象
        #     content_data = {
        #         "phone": phone,
        #         "value": value
        #     }
        #     content_list.append(content_data)
        #     time.sleep(random.randint(MIN_SEC, MAX_SEC))
        #     # break

    # sending email
    # server = filename.split('.')[0][-5:]
    # send_email.send_HashWorld_HtmlEmail('newseeing@163.com', content_list, server)
    # logger.warning('********** Sending Email Complete!')
    # logger.warning('\n')


loop_Lottery('data_hashworld_Tokyo.json')

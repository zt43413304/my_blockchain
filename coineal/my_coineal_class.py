# coding=utf-8


import logging
import os
import random
import ssl
import time

import requests
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_coineal_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_coineal_class.log', mode='w')
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

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# Random seconds
MIN_SEC = 2
MAX_SEC = 5
proxies = ''

class trader_class:
    def __init__(self):
        logger.warning("start __init__...")

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['clearSystemFiles'] = 'True'
        # desired_caps['automationName'] = 'Appium'
        # desired_caps['autoWebview'] = 'True'
        desired_caps['app'] = PATH(
            # '/Users/Jackie.Liu/DevTools/Android_apk/one213.apk'
            'C:\DevTools\Android_apk\one213.apk'
        )
        desired_caps['appPackage'] = 'oneapp.onechain.androidapp'
        desired_caps['appActivity'] = 'oneapp.onechain.androidapp.onemessage.view.activity.UnlockActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def login(phone):
        url = "https://server.diwuqu.vip/api/app/v1/login/captcha"
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
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
            time.sleep(random.randint(MIN_SEC, MAX_SEC))
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

    def login01():

        
        url = 'http://tvp.daxiangdaili.com/ip/?tid=559810758325225&num=1&delay=1&category=2&protocol=https&filter=on&sortby=speed'

        try:
            response = requests.get(url)
            proxy_ip = response.text

            # ERROR|没有找到符合条件的IP
            nPos = proxy_ip.find('ERROR')
            if nPos > -1:
                logger.warning(">>>>>>>>>> Get proxy ip = " + proxy_ip)
                proxy_ip = ''
                logger.warning(">>>>>>>>>> Return proxy_ip = " + proxy_ip)
                return proxy_ip
            else:
                return proxy_ip
        except Exception as e:
            print(e)
            logger.warning(">>>>>>>>>> Get proxy ip error, sleep 5 seconds...")
            logger.warning(">>>>>>>>>> Zzzzzzzzzzzzzzzz...")
            time.sleep(5)

            try:
                response = requests.get(url)
                proxy_ip = response.text

                if proxy_ip is None or proxy_ip is '':
                    return ''
                else:
                    return proxy_ip
            except Exception as f:
                print(f)
                return ''
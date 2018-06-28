# coding=utf-8
import configparser
import logging
import os
import random
import re
import sys
import threading
import time

import requests

from common import daxiang_proxy

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
# user_agent = cf.get('info'+str(infoNum), 'user_agent').strip()
# device_id = cf.get('info'+str(infoNum), 'device_id').strip()

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

# Random seconds
MIN_SEC = 2
MAX_SEC = 5
proxies = ''


class readnews(threading.Thread):
    unique = None
    uid = None
    phone = None
    logger = None

    def __init__(self, unique, uid, phone):
        threading.Thread.__init__(self)
        global proxies
        self.unique = unique
        self.uid = uid
        self.phone = phone

        # 第一步，创建一个logger,并设置级别
        # self.logger = logging.getLogger("bixiang_readnews_class.py")
        self.logger = logging.getLogger("Thread_" + self.phone)
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        fh = logging.FileHandler('./logs/bixiang_readnews_' + self.phone + '.log', mode='w')
        fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")

        self.logger.warning("========== __init()__, Checking. [" + phone + "] ==========")

    def bixiang_login(self):
        global proxies

        self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")

        url = "http://tui.yingshe.com/check/index"

        payload_login = payload + "&unique=" + self.unique + "&uid=" + self.uid

        try:
            # self.logger.warning("********** selenium_login(), proxies = " + str(proxies))
            response = requests.request("POST", url, data=payload_login, headers=headers, timeout=60,
                                        proxies=proxies, allow_redirects=False)
            time.sleep(random.randint(MIN_SEC, MAX_SEC))

            res = response.json()["status"]
            if res == 1:
                self.logger.warning('********** Login success.')
                # bixiang_userInfo(self.unique, self.uid)
                return 1
            else:
                self.logger.warning('********** Login fail. uid:' + self.uid)
                return -1
        except Exception as e:
            print(e)
            proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

    def run(self):

        if self.bixiang_login() == -1:
            sys.exit(0)

        self.bixiang_loop_reading_news()

    def bixiang_loop_reading_news(self):

        channels = ["__all__", "news_hot", "news_entertainment", "news_tech", "news_travel", "news_sports"]
        for i in range(len(channels)):
            self.logger.warning("********** [" + self.phone + "]. channel = " + channels[i])

            JRTT_list = self.get_JRTT_list(channels[i])
            if JRTT_list == -1:
                continue

            for j in range(len(JRTT_list)):
                news_id = JRTT_list[j]["id"]
                time.sleep(random.randint(90, 120))
                return_code = self.post_newsRecord(news_id)
                if return_code == -1:
                    continue

            if i == len(channels) - 1:
                self.bixiang_loop_reading_news()

    def get_JRTT_list(self, channel):
        global proxies

        url = "http://lockscreen.mobile7.cn/newsfeed/jrtt_news"

        headers = {
            'Host': "lockscreen.mobile7.cn",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'User-Agent': "okhttp/3.4.1",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

        payload_JRTT = payload + "&unique=" + self.unique + \
                       "&uid=" + self.uid + \
                       "&xversioncode=241" \
                       "&xversionname=1.4.9" \
                       "&xphonemodel=MuMu" \
                       "&xchannel=Y1032" \
                       "&xmnc=" \
                       "&xosversion=4.4.4" \
                       "&reqfrom=bx" \
                       "&xbrand=Android" \
                       "&ximei=" + self.unique + \
                       "&ximsi=0" \
                       "&chlid=" + channel + \
                       "&xmcc=" \
                       "&xresolution=640*1024" \
                       "&page=1" \
                       "&joinads=admctl" \
                       "&xwifimac=08:00:27:37:05:c5" \
                       "&newsfeed=jrtt" \
                       "&xnettype=WIFI"

        try:

            self.logger.warning("********** get_JRTT_list(), proxies = " + str(proxies))

            response = requests.request("POST", url, data=payload_JRTT, headers=headers, timeout=60,
                                        proxies=proxies, allow_redirects=False)

            while response.status_code != 200:
                self.logger.warning("********** [" + self.phone + "]. get_JRTT_list Error. try again ...")
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url, data=payload_JRTT, headers=headers, timeout=60,
                                            proxies=proxies, allow_redirects=False)

            if response.status_code == 200:
                res = response.json()["status"]
                if res == 1:
                    JRTT_list = response.json()["data"]
                    self.logger.warning("********** [" + self.phone + "]. get_JRTT_list success, len(JRTT_list) = "
                                        + str(len(JRTT_list)))
                    return JRTT_list
                else:
                    self.logger.warning("********** [" + self.phone + "]. get_JRTT_list Error.")
                    return -1
            else:
                self.logger.warning("********** [" + self.phone + "]. get_JRTT_list Error.")
                return -1
        except Exception as e:
            print(e)
            proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

    def post_newsRecord(self, news_id):
        global proxies

        url = "http://tui.yingshe.com/mumayi/newsRecord"

        payload = "is_ad_ios=" + is_ad_ios + \
                  "&versioncode=" + versioncode + \
                  "&devicetype=" + devicetype + \
                  "&channel=" + channel + \
                  "&token=" + token + \
                  "&ps=" + ps + \
                  "&key=" + key

        payload_newsRecord = payload + "&unique=" + self.unique + \
                             "&uid=" + self.uid + \
                             "&new_id=" + news_id

        try:

            # self.logger.warning(">>>>>>>>>> [" + self.phone + "]. post_newsRecord. news_id=" + news_id)

            response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                        timeout=60, proxies=proxies, allow_redirects=False)

            while response.status_code != 200:
                self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error. try again ...")
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                            timeout=60, proxies=proxies, allow_redirects=False)

            if response.status_code == 200:
                res = response.json()["status"]
                if res == 1:
                    bxc = response.json()["info"]["bxc"]
                    self.logger.warning(">>>>>>>>>> [" + self.phone + "]. post_newsRecord success, bxc = " + str(bxc))
                    return 0
                else:
                    self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error.")
                    return -1
            else:
                self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error.")
                return -1
        except Exception as e:
            print(e)
            proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

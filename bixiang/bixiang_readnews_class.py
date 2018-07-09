# coding=utf-8
import configparser
import json
import logging
import os
import random
import re
import sys
import threading
import time

import requests

from common import c2567
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


class readnews(threading.Thread):
    unique = None
    uid = None
    phone = None
    logger = None
    stopevt = None
    proxies = ''

    def __init__(self, unique, uid, phone, stopevt=None):
        threading.Thread.__init__(self)
        # global proxies
        self.unique = unique
        self.uid = uid
        self.phone = phone
        self.stopevt = stopevt

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

        # self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        self.proxies = ''

        self.logger.warning("========== __init()__, Checking. [" + phone + "] ==========")

    def bixiang_login(self):
        # global proxies

        # if self.proxies is None or proxies is '':
        # proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")

        url = "http://tui.yingshe.com/check/index"

        payload_login = payload + "&unique=" + self.unique + "&uid=" + self.uid

        try:
            # self.logger.warning("********** selenium_login(), proxies = " + str(proxies))
            response = requests.request("POST", url, data=payload_login, headers=headers, timeout=60,
                                        proxies=self.proxies, allow_redirects=False)
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
            self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

    def run(self):

        if self.bixiang_login() == -1:
            sys.exit(0)

        while not self.stopevt.isSet():
            # channels = ["news_hot", "news_entertainment", "news_tech", "news_travel", "news_sports", "news_fashion",
            #             "news_finance", "news_edu", "news_house", "news_photography", "news_comic", "news_story",
            #             "news_health", "news_food", "news_car", "news_game", "news_culture", "news_discovery"]
            channels = ["news_hot"]
            for i in range(len(channels)):
                self.logger.warning("********** [" + self.phone + "]. channel = " + channels[i])

                JRTT_list = self.get_JRTT_list(channels[i])
                if JRTT_list == -1:
                    continue

                for j in range(len(JRTT_list)):
                    news_id = JRTT_list[j]["id"]
                    time.sleep(random.randint(70, 90))
                    return_code = self.post_newsRecord(news_id)
                    if return_code == -1:
                        continue

        self.logger.warning('********** exit thread. ' + self.phone)

    def bixiang_loop_reading_news(self):

        channels = ["news_hot", "news_entertainment", "news_tech", "news_travel", "news_sports", "news_fashion",
                    "news_finance", "news_edu", "news_house", "news_photography", "news_comic", "news_story",
                    "news_health", "news_food", "news_car", "news_game", "news_culture", "news_discovery"]
        for i in range(len(channels)):
            self.logger.warning("********** [" + self.phone + "]. channel = " + channels[i])

            JRTT_list = self.get_JRTT_list(channels[i])
            if JRTT_list == -1:
                continue

            for j in range(len(JRTT_list)):
                news_id = JRTT_list[j]["id"]
                time.sleep(random.randint(70, 90))
                return_code = self.post_newsRecord(news_id)
                if return_code == -1:
                    continue

            if i == len(channels) - 1:
                self.bixiang_loop_reading_news()

    def get_JRTT_list(self, channel):
        # global proxies

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

            self.logger.warning("********** get_JRTT_list(), proxies = " + str(self.proxies))

            response = requests.request("POST", url, data=payload_JRTT, headers=headers, timeout=60,
                                        proxies=self.proxies, allow_redirects=False)

            while response.status_code != 200:
                self.logger.warning("********** [" + self.phone + "]. get_JRTT_list Error. try again ...")
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url, data=payload_JRTT, headers=headers, timeout=60,
                                            proxies=self.proxies, allow_redirects=False)

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
            self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

    def post_newsRecord(self, news_id):
        # global proxies

        url = "http://tui.yingshe.com/mumayi/newsRecord"

        payload_newsRecord = payload + "&unique=" + self.unique + \
                             "&uid=" + self.uid + \
                             "&new_id=" + news_id

        try:

            # self.logger.warning(">>>>>>>>>> [" + self.phone + "]. post_newsRecord. news_id=" + news_id)
            self.logger.warning("********** [" + self.phone + "], post_newsRecord(), proxies = " + str(self.proxies))
            response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                        timeout=60, proxies=self.proxies, allow_redirects=False)

            while response.status_code != 200:
                self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error. try again ...")
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                            timeout=60, proxies=self.proxies, allow_redirects=False)

            if response.status_code == 200:
                res = response.json()["status"]
                if res == 1:
                    bxc = response.json()["info"]["bxc"]
                    self.logger.warning(">>>>>>>>>> [" + self.phone + "]. post_newsRecord success, bxc = " + str(bxc))
                    return 0
                else:
                    # response status==0, captcha needed
                    self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error. call captcha ...")
                    (gt, challenge) = self.getverify()
                    if gt != -1 and gt is not None and len(gt.strip()) != 0 \
                            and challenge != -1 and challenge is not None and len(challenge.strip()) != 0:
                        # call captcha hack
                        (challenge, validate) = c2567.get_captcha(gt, challenge)

                        if challenge != -1 and validate != -1:
                            self.post_newsRecord_with_captcha(news_id, challenge, validate)
            else:
                self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error.")
                return -1
        except Exception as e:
            print(e)
            self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

    def post_newsRecord_with_captcha(self, news_id, challenge, validate):
        # global proxies

        url = "http://tui.yingshe.com/mumayi/newsRecord"

        payload_newsRecord = payload + "&unique=" + self.unique + \
                             "&uid=" + self.uid + \
                             "&new_id=" + news_id + \
                             "&geetest_challenge=" + challenge + \
                             "&geetest_validate=" + validate + \
                             "&geetest_seccode=" + validate + "|jordan"

        try:

            self.logger.warning(
                "********** [" + self.phone + "], post_newsRecord_with_captcha(), proxies = " + str(self.proxies))
            response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                        timeout=60, proxies=self.proxies, allow_redirects=False)

            while response.status_code != 200:
                self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord Error. try again ...")
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                            timeout=60, proxies=self.proxies, allow_redirects=False)

            if response.status_code == 200:
                res = response.json()["status"]
                if res == 1:
                    msg = response.json()["msg"]
                    self.logger.warning(
                        ">>>>>>>>>> [" + self.phone + "]. post_newsRecord_with_captcha success, msg = " + msg)
                    return 0
                else:
                    self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord_with_captcha Error.")
                    return -1
            else:
                self.logger.warning("<<<<<<<<<< [" + self.phone + "]. post_newsRecord_with_captcha Error.")
                return -1
        except Exception as e:
            print(e)
            self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1

    def getverify(self):
        url = "http://tui.yingshe.com/veritys/getverify"

        payload_verify = payload + "&unique=" + self.unique + "&uid=" + self.uid

        try:
            self.logger.warning("^^^^^^^^^^ [" + self.phone + "], getverify()")
            response = requests.request("GET", url, data=payload_verify, headers=headers,
                                        timeout=60, proxies=self.proxies, allow_redirects=False)

            res = response.json()["success"]
            if res == 1:
                gt = response.json()["gt"]
                challenge = response.json()["challenge"]
                return gt, challenge
            else:
                return -1, -1
        except Exception as e:
            print(e)
            self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
            return -1, -1


class checkThread(threading.Thread):
    unique = None
    uid = None
    phone = None
    logger = None
    stopevt = None
    proxies = ''

    def __init__(self, filename, sleeptimes=600, initThreadsName=[], stopevt=None):
        threading.Thread.__init__(self)
        # global proxies

        self.filename = filename
        self.sleeptimes = sleeptimes
        self.initThreadsName = initThreadsName
        self.stopevt = stopevt

        # 第一步，创建一个logger,并设置级别
        # self.logger = logging.getLogger("bixiang_readnews_class.py")
        self.logger = logging.getLogger("Thread_Checking")
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        fh = logging.FileHandler('./logs/bixiang_readnews_Thread_Checking.log', mode='w')
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

        # self.proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        self.proxies = ''

        # self.logger.warning("========== __init()__, Checking. [" + phone + "] ==========")

    # 每180s获取当前线程名，并跟初始线程组比较，某一线程停止后自动运行
    def run(self):
        # 循环运行
        while not self.stopevt.isSet():
            # 用来保存当前线程名称
            nowThreadsName = []
            # 获取当前线程名
            now = threading.enumerate()
            for i in now:
                # 保存当前线程名称
                nowThreadsName.append(i.getName())

            for thread_news in self.initThreadsName:
                if thread_news in nowThreadsName:
                    # 当前某线程名包含在初始化线程组中，可以认为线程仍在运行
                    self.logger.warning('********** Thread is running, [' + thread_news + ']')
                else:
                    # 重启线程
                    (unique, uid) = self.get_id_by_phone(self.filename, thread_news)
                    thread_readnews = self.bixiang_readnews_class.readnews(unique, uid, thread_news, self.stopevt)
                    # 重设name
                    thread_readnews.setName(thread_news)
                    thread_readnews.setDaemon(True)
                    thread_readnews.start()
                    self.logger.warning('********** Thread was stopped, restart [' + thread_news + ']')
            # 隔一段时间重新运行，检测有没有线程down
            time.sleep(self.sleeptimes)

    def get_id_by_phone(self, filename, phone_no):
        curpath = os.getcwd()
        file = open(curpath + '/bixiang/' + filename, 'r', encoding='utf-8')
        data_dict = json.load(file)

        for item in data_dict['data']:
            unique = item.get('unique', 'NA')
            uid = item.get('uid', 'NA')
            phone = item.get('phone', 'NA')
            if phone == phone_no:
                return unique, uid
            else:
                continue

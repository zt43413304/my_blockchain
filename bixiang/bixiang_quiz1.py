# coding=utf-8

import configparser
import json
import logging
import os
import random
import re
import time
import urllib.parse
from io import StringIO

import requests
from lxml import etree

from common import daxiang_proxy
from common import send_email

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("bixiang_quiz.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang_quiz.log', mode='w')
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


# http://tui.yingshe.com/user/newtask?xxx=HK%3DXvJCHh66Wi68ZhJKI4
# <p id="xxx" style="display:none">hfoz9fZ1%3DfYz-fZ17goj-</p>

url = "http://tui.yingshe.com/user/newtask?xxx=BEMTZGKAkE87YHaEqD8PV"

def get_xxx():
    # global proxies

    headers = {
        'Host': "tui.yingshe.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/3.4.1",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    try:
        # logger.warning("********** quiz(), proxies = " + str(proxies))
        # response = requests.request("POST", url,  headers=headers, proxies=proxies)
        response = requests.request("GET", url,  headers=headers)
        # time.sleep(random.randint(MIN_SEC, MAX_SEC))

        html = response.text

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)

        # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
        # print(result)



        xxx = tree.xpath('//*[@id="xxx"]')
        logger.warning(">>>>> xxx = " + xxx[0].text)
        return xxx[0].text




        # res = response.json()["status"]


        # if res == 1:
        #     logger.warning('********** Login success.')
        #     bixiang_userInfo(unique, uid)
        #     return 1
        # else:
        #     logger.warning('********** Login fail. uid:' + uid)
        #     return -1
    except Exception as e:
        print(e)
        # return -1

def quiz():

    xxx = get_xxx()
    # xxx = 'abbc'
    url_quiz = "http://tui.yingshe.com/user/taskCheck?xxx="+xxx

    answer_list = '{"1": "A", "2": "D", "3": "D", "4": "C", "5": "A", "6": "D", "7": "B", "8": "A", "9": "A", "10": "D"}'
    answer_dict = json.loads(answer_list)
    # print(ans, type(ans))
    # print(ans[2])

    headers = {
        'Host': "tui.yingshe.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/3.4.1",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Referer': url
    }

    payload = "CNZZDATA1273207201=285046352-1527133912-%7C1527133912"  + \
              "&CNZZDATA1273839213=2082437917-1527980171-%7C1527980171" + \
              "&CNZZDATA1272182233=572908881-1527138621-%7C1528033921" + \
              "&UM_distinctid=163909605f40-0a32cd23b-5d7e0559-47339-163909605f9ff"

    try:
        for i in range(1, 11):
            time.sleep(4)
            # index = "'"+i+"'"
            answer = answer_dict[str(i)]
            # print(answer)

            url_answer = url_quiz + "&task_id="+str(i)+"&answer="+answer
            print(url_answer)
            # logger.warning("********** quiz(), proxies = " + str(proxies))
            # response = requests.request("POST", url,  headers=headers, proxies=proxies)
            response = requests.request("POST", url_answer,  headers=headers, data=payload)
            # time.sleep(random.randint(MIN_SEC, MAX_SEC))
            print(response.text.encode('utf-8').decode('unicode_escape'))
    except Exception as e:
        print(e)

print(get_xxx())
# quiz()
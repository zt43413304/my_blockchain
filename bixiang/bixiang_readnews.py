# coding=utf-8
import datetime
import json
import logging
import os
import random
import sys
import threading
import time

from bixiang import bixiang_readnews_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("bixiang_readnews.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang_readnews.log', mode='w')
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


def start_reading_news(filename):
    # 保存初始化线程组名字
    initThreadsName = []

    # start
    logger.warning('********** Start from start_reading_news() ...')
    stopevt = threading.Event()

    curpath = os.getcwd()
    file = open(curpath + '/bixiang/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)

    thread_readnews_list = []
    for item in data_dict['data']:
        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        phone = item.get('phone', 'NA')

        thread_readnews = bixiang_readnews_class.readnews(unique, uid, phone, stopevt)
        thread_readnews.setName(phone)
        thread_readnews.setDaemon(True)
        thread_readnews_list.append(thread_readnews)

    number = 0
    for t in thread_readnews_list:
        number += 1
        t.start()
        time.sleep(random.randint(30, 60))
        logger.warning('********** Start thread [' + str(number) + ']: ' + t.getName())
        # break

    # init = threading.enumerate()  # 获取初始化的线程对象
    # for i in init:
    #     initThreadsName.append(i.getName())  # 保存初始化线程组名字
    #     logger.warning('********** Store thread [' + str(i.getName()) + '] ')

    # 用来检测是否有线程down并重启down线程
    # check_tread = bixiang_readnews_class.checkThread(filename, 60, initThreadsName, stopevt)
    # check_tread.setName('Thread:check')
    # check_tread.setDaemon(True)
    # check_tread.start()
    # check_tread.join(3)
    # logger.warning('********** Start thread [' + check_tread.getName() + ']')

    while True:
        # 定时退出
        now = datetime.datetime.now()
        exit_time = [8, 18, 28, 38, 48, 58]
        if now.minute in exit_time:
            # 退出线程组
            # stopevt = threading.Event()
            stopevt.set()
            logger.warning('~~~~~~~~~~ hour='+str(now.hour)+', minute='+str(now.minute))
            sys.exit(0)





        # if now.hour== 6 and now.minute==55 and (now.second == 0 or now.second == 1):
        #     logger.warning('********** sys.exit(0)')
        #     return
        #
        # if now.hour== 14 and now.minute==55 and (now.second == 0 or now.second == 1):
        #     logger.warning('********** sys.exit(0)')
        #     return
        #
        # if now.hour== 22 and now.minute==55 and (now.second == 0 or now.second == 1):
        #     logger.warning('********** sys.exit(0)')
        #     return

# start_reading_news("data_bixiang_readnews.json")

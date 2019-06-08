# coding=utf-8
import datetime
import json
import logging
import os
import random
import threading
import time

from bixiang import bixiang_news_video_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("bixiang_news_video.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang_news_video.log', mode='w')
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


def start_news_video(filename):
    # 保存初始化线程组名字
    initThreadsName = []

    # start
    logger.warning('********** Start from start_news_video() ...')
    stopevt = threading.Event()

    curpath = os.getcwd()
    file = open(curpath + '/bixiang/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)

    thread_readnews_list = []
    number = 0
    for item in data_dict['data']:
        number += 1
        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        phone = item.get('phone', 'NA')

        thread_readnews = bixiang_news_video_class.news_video(unique, uid, phone, stopevt)
        thread_readnews.setName(phone)
        thread_readnews.setDaemon(True)
        thread_readnews.start()
        thread_readnews.join(10)
        time.sleep(random.randint(3, 5))
        logger.warning('********** Start thread [' + str(number) + ']: ' + thread_readnews.getName())
        # thread_readnews_list.append(thread_readnews)
        # if number == 10:
        #     break

    # number = 0
    # for t in thread_readnews_list:
    #     number += 1
    #     t.start()
    #     time.sleep(random.randint(5, 10))
    #     logger.warning('********** Start thread [' + str(number) + ']: ' + t.getName())
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
        exit_time = [11]
        if now.hour in exit_time and now.minute < 30:
            # 退出线程
            stopevt.set()
            break

# start_news_video("data_bixiang__Seoul.json")
# start_news_video("data_bixiang_Aliyun.json")

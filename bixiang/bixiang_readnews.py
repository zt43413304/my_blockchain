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


def get_id_by_phone(filename, phone_no):
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


# 每180s获取当前线程名，并跟初始线程组比较，某一线程停止后自动运行
def checkThread(filename, sleeptimes=600, initThreadsName=[]):
    # 循环运行
    while True:
        # 用来保存当前线程名称
        nowThreadsName = []
        # 获取当前线程名
        now = threading.enumerate()
        for i in now:
            # 保存当前线程名称
            nowThreadsName.append(i.getName())

        for thread_news in initThreadsName:
            if thread_news in nowThreadsName:
                # 当前某线程名包含在初始化线程组中，可以认为线程仍在运行
                logger.warning('********** Thread is running, [' + thread_news + ']')
            else:
                # 重启线程
                (unique, uid) = get_id_by_phone(filename, thread_news)
                thread_readnews = bixiang_readnews_class.readnews(unique, uid, thread_news)
                # 重设name
                thread_readnews.setName(thread_news)
                thread_readnews.start()
                logger.warning('********** Thread was stopped, restart [' + thread_news + ']')
        # 隔一段时间重新运行，检测有没有线程down
        time.sleep(sleeptimes)


def start_reading_news(filename):
    # 保存初始化线程组名字
    initThreadsName = []

    # start
    logger.warning('********** Start from start_reading_news() ...')

    curpath = os.getcwd()
    file = open(curpath + '/bixiang/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)

    number = 0
    for item in data_dict['data']:
        number += 1

        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        phone = item.get('phone', 'NA')

        thread_readnews = bixiang_readnews_class.readnews(unique, uid, phone)
        thread_readnews.setName(phone)
        thread_readnews.setDaemon(True)
        thread_readnews.start()
        time.sleep(random.randint(30, 60))
        logger.warning('********** Start thread [' + str(number) + ']: ' + phone)
        # break

    init = threading.enumerate()  # 获取初始化的线程对象
    for i in init:
        initThreadsName.append(i.getName())  # 保存初始化线程组名字
        logger.warning('********** Store thread [' + str(i.getName()) + '] ')

    # 用来检测是否有线程down并重启down线程
    check = threading.Thread(target=checkThread, args=(filename, 600, initThreadsName))
    check.setName('Thread:check')
    check.setDaemon(True)
    check.start()
    logger.warning('********** Start thread [' + check.getName() + ']')

    # 定时退出
    exit_time = [8, 18, 28, 38, 48, 58]
    while True:
        now = datetime.datetime.now()
        logger.warning('~~~~~~~~~~ hour='+str(now.hour)+', minute='+str(now.minute))
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
        if now.minute in exit_time:
            logger.warning('********** return')
            return

# start_reading_news("data_bixiang_readnews.json")

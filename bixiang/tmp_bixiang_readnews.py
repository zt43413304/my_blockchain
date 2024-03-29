# coding=utf-8
import json
import logging
import os
import random
import time

from bixiang import bixiang_news_video_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("tmp_bixiang_readnews.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/tmp_bixiang_readnews.log', mode='w')
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


def start_reading_news(filename):
    # bixiang_login_test()

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

        thread_readnews = bixiang_news_video_class.readnews(unique, uid, phone)
        thread_readnews.start()
        time.sleep(random.randint(30, 60))
        logger.warning('********** Start thread [' + str(number) + ']: ' + phone)
        # break


start_reading_news("tmp_data_bixiang_readnews.json")

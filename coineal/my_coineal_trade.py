# coding=utf-8
import configparser
import logging
import random
import re
from datetime import datetime, timedelta

import os

from coineal import my_coineal_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_coineal_trade.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_coineal_trade.log', mode='w')
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


def load_quota():
    # get config information
    curpath = os.getcwd()
    content = open(curpath + '/coineal/config.ini').read()
    content = re.sub(r"\xfe\xff", "", content)
    content = re.sub(r"\xff\xfe", "", content)
    content = re.sub(r"\xef\xbb\xbf", "", content)
    open(curpath + '/coineal/config.ini', 'w').write(content)

    cf = configparser.ConfigParser()
    cf.read(curpath + '/coineal/config.ini')
    ETH_Price = cf.get('info', 'ETH_Price').strip()
    Deal_Quota = cf.get('info', 'Deal_Quota').strip()
    return ETH_Price, Deal_Quota


# start from here ......
day = 0
hour = 0
min = 1
second = 45


trader = my_coineal_class.trader_class()
# trade_buy_first(trader)
res = trader.one_login()
# trade_sell_first(trader)

if res == 0:
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    logger.warning("********** Now: " + strnow)
    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    logger.warning("********** Next_run: " + strnext_time)
    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            # logger.warning("start trade: " +iter_now_time)
            # Call task func
            trade_buy_first(trader)
            # logger.warning("trade done.")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            logger.warning("********** Next_run: " + strnext_time)
            # Continue next iteration
            continue

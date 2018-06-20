# coding=utf-8

import configparser
import json
import logging
import os
import random
import re
import time

import requests

from common import daxiang_proxy
from common import send_email
from onechain import my_onechain_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_onechain_trade.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_onechain_trade.log', mode='w')
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

# get config information
curpath = os.getcwd()
content = open(curpath + '/onechain/config.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/onechain/config.ini', 'w').write(content)

headers = {
    'User-Agent': "okhttp/3.5.0",
    'Host': "hkopenservice1.yuyin365.com:8000",
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-Hans-CN;q=1',
    'Accept-Encoding': 'gzip',
    'Cache-Control': "no-cache"
}



def load_account(trade_pair):
    # start
    logger.warning('********** load_account() ...')

    # global proxies
    # proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")

    file = open(curpath + '/onechain/'+trade_pair, 'r', encoding='utf-8')
    data_dict = json.load(file)

    account_id = data_dict['data'][0].get('account_id', 'NA')
    account_name = data_dict['data'][0].get('account_name', 'NA')
    signed_message = data_dict['data'][0].get('signed_message', 'NA')
    version = data_dict['data'][0].get('version', 'NA')
    l = data_dict['data'][0].get('l', 'NA')
    user_agent = data_dict['data'][0].get('user_agent', 'NA')
    device_id = data_dict['data'][0].get('device_id', 'NA')
    data = dict(account_id=account_id, account_name=account_name, signed_message=signed_message,
                version=version, l=l, user_agent=user_agent, device_id=device_id)

    trader01 = my_onechain_class.trade_class(data)
    trader01.loginGetAccessToken()
    # logger.warning("========== Load Account 1 ==========")

    account_id = data_dict['data'][1].get('account_id', 'NA')
    account_name = data_dict['data'][1].get('account_name', 'NA')
    signed_message = data_dict['data'][1].get('signed_message', 'NA')
    version = data_dict['data'][1].get('version', 'NA')
    l = data_dict['data'][1].get('l', 'NA')
    user_agent = data_dict['data'][1].get('user_agent', 'NA')
    device_id = data_dict['data'][1].get('device_id', 'NA')
    data = dict(account_id=account_id, account_name=account_name, signed_message=signed_message,
                version=version, l=l, user_agent=user_agent, device_id=device_id)

    trader02 = my_onechain_class.trade_class(data)
    trader02.loginGetAccessToken()
    # logger.warning("========== Load Account 2 ==========")
    return trader01, trader02


def onechain_trade(trade_pair):

    logger.warning('********** Start from onechain_trade() ...')

    (trader01, trader02) = load_account(trade_pair)





# Start from here...
onechain_trade('one_chain_data1.json')
# onechain_trade('one_chain_data2.json')
# onechain_trade('one_chain_data3.json')
# onechain_trade('one_chain_data4.json')



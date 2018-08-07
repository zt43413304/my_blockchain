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

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_onechain.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_onechain.log', mode='w')
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

# Random seconds
MIN_SEC = 2
MAX_SEC = 5
proxies = ''


def getInfoNum(infoNum):
    global version, l, user_agent, device_id
    cf = configparser.ConfigParser()
    cf.read(curpath + '/onechain/config.ini')
    version = cf.get('info', 'version').strip()
    l = cf.get('info', 'l').strip()
    user_agent = cf.get('info' + str(infoNum), 'user_agent').strip()
    device_id = cf.get('info' + str(infoNum), 'device_id').strip()
    return version, l, user_agent, device_id


def loginGetAccessToken(user_agent, device_id, l, version):
    global proxies
    url_login = 'http://hkopenservice1.yuyin365.com:8000/one-chain/login?user_agent=' + user_agent + \
                '&device_id=' + device_id + '&l=' + l + '&token=&version=' + version

    try:
        logger.warning("********** loginGetAccessToken(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_login, data=data, headers=headers, proxies=proxies, timeout=60)

        # if bProxy == 0:
        #     r = requests.post(url_login, headers=headers, verify=False) #headers=headers,
        # else:
        #     r = requests.post(url_login, headers=headers, proxies=proxies, verify=False) #headers=headers,

        res = r.json()["msg"]
        if res == '成功':
            token = r.json()["data"]["map"]["token"]
            return token
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return -1


def open_mining(user_agent, device_id, l, token, version):
    global proxies
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/start?user_agent=' + user_agent + \
                '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    try:
        logger.warning("********** open_mining(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            logger.warning('********** open_mining() 成功.')
            return 0
        else:
            return -1

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return


def get_calculated(user_agent, device_id, l, token, version):
    global proxies
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/user/infoString?user_agent=' + user_agent + \
                '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    try:
        logger.warning("********** get_calculated(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            mining_flag = r.json()['data']['map']['mining_flag']
            if mining_flag == "NO":
                open_mining(user_agent, device_id, l, token, version)
                logger.warning('********** mining opened')

            calculated = r.json()['data']['map']['calculated']
            logger.warning('>>>>>>>>>> calculated: ' + calculated)
            return calculated
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return -1


def mining_click(user_agent, device_id, l, token, version, mining_detail_uuid):
    global proxies
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/detail/click?user_agent=' + user_agent + \
                '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version + \
                '&mining_detail_uuid=' + mining_detail_uuid

    try:
        # logger.warning("********** mining_click(), proxies =  " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            logger.warning('>>>>>>>>>> mining...... ' + str(mining_detail_uuid))
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return


def mining_check(user_agent, device_id, l, token, version):
    global proxies
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/detail/list?user_agent=' + user_agent + \
                '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    try:
        logger.warning("********** mining_check(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            contentlist = r.json()['data']['list']
            i = 0
            for i in range(len(contentlist)):
                uni_uuid = contentlist[i]['uni_uuid']
                mining_click(user_agent, device_id, l, token, version, str(uni_uuid))
                time.sleep(random.random())

            if i == 0:
                logger.warning('>>>>>>>>>> mining_clicked: ' + str(i))
            else:
                logger.warning('>>>>>>>>>> mining_clicked: ' + str(i + 1))
            return 0
        else:
            return -1

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return


def check_allTotal(user_agent, device_id, l, token, version):
    global proxies
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/allTotal?user_agent=' + user_agent + \
                '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    headers = {
        'User-Agent': "okhttp/3.5.0",
        'Host': "hkopenservice1.yuyin365.com:8000",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip',
        'Cache-Control': "no-cache"
    }


    try:
        logger.warning("********** check_allTotal(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            totallist = r.json()['data']['list']
            return totallist
        else:
            return -1

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return -1


def coin_from_online_to_transaction_wallet(user_agent, device_id, l, token, version):
    global proxies

    url_online = 'http://hkopenservice1.yuyin365.com:8000/one-chain/offchain/list?user_agent=' + user_agent + \
                 '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    headers = {
        'User-Agent': "okhttp/3.5.0",
        'Host': "hkopenservice1.yuyin365.com:8000",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip',
        'Cache-Control': "no-cache"
    }

    try:
        logger.warning("********** coin_from_online_to_transaction_wallet(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_online, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            coinlist = r.json()['data']['list']

            for i in range(len(coinlist)):
                coin = coinlist[i]
                amount = coin.get('amount_available', 0)
                asset_code = coin.get('asset_code', 'NA')
                asset_name = coin.get('short_name', 'NA')

                if amount > 0.0001:
                    coin_offline_transfer(user_agent, device_id, l, token, version, asset_code, asset_name, amount)

            return 0
        else:
            return -1

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return -1


def coin_offline_transfer(user_agent, device_id, l, token, version, asset_code, asset_name, amount):
    global proxies

    url_referer = 'http://hkopenserviceui1.yuyin365.com:8000/withdrawals.html?user_agent=' + user_agent + \
                  '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version + \
                  'asset_code=' + asset_code + '&asset_name=' + asset_name

    url_envelopes = 'http://hkopenservice1.yuyin365.com:8000/one-chain/offchain/envelopes'

    headers = {
        'User-Agent': "okhttp/3.5.0",
        'Host': "hkopenservice1.yuyin365.com:8000",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip',
        'Cache-Control': "no-cache",
        'Host': "hkopenservice1.yuyin365.com:8000",
        'Referer': url_referer
    }

    data['amount'] = amount
    data['asset_code'] = asset_code
    data['token'] = token
    data['user_agent'] = user_agent
    data['l'] = l

    try:
        logger.warning("********** coin_offline_transfer(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_envelopes, data=data, headers=headers, proxies=proxies, timeout=60)

        res = r.json()["msg"]
        if res == '成功':
            logger.warning("********** coin_offline_transfer(), 成功。" + asset_code + ":" + str(amount))
            return 0
        else:
            return -1

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
        return -1



def loop_onechain():
    global data
    global token

    # start
    logger.warning('********** Start from loop_onechain() ...')

    global proxies
    proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")

    file = open(curpath + '/onechain/one_chain_data.json', 'r', encoding='utf-8')
    data_dict = json.load(file)
    content_list = []
    # print(data_dict)
    # print(type(data_dict))

    # value = 1
    # hashCode=(int)(value ^ (value >> 32))
    # index=hashCode%20
    # print(index)
    # result is "0 ~ 19"

    # determine info number
    i = 0
    for item in data_dict['data']:
        i = i + 1
        hashCode = (int)(i ^ (i >> 32))
        infoNum = hashCode % 20
        (version, l, user_agent, device_id) = getInfoNum(infoNum)

        account_id = item.get('account_id', 'NA')
        account_name = item.get('account_name', 'NA')
        signed_message = item.get('signed_message', 'NA')
        data = dict(account_id=account_id, account_name=account_name, signed_message=signed_message)

        logger.warning('\n')
        logger.warning("========== Checking " + str(i) + ". [" + account_name + "] ==========")

        token = loginGetAccessToken(user_agent, device_id, l, version)
        if token == -1:
            logger.warning('********** Login fail!')
            continue
        else:
            logger.warning('********** Login 成功! token:' + token)

            calculated = get_calculated(user_agent, device_id, l, token, version)
            mining_check(user_agent, device_id, l, token, version)
            time.sleep(random.randint(MIN_SEC, MAX_SEC))

            (coinlist) = coin_from_online_to_transaction_wallet(user_agent, device_id, l, token, version)

            (totallist) = check_allTotal(user_agent, device_id, l, token, version)


            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            content_data = {}
            content_data['account_name'] = account_name
            content_data['calculated'] = calculated
            for j in range(len(totallist)):
                item = totallist[j]
                content_data[item['asset_code']] = item['total']


            content_list.append(content_data)

        # if i > 3:
        #     break

    cont_data = content_list[0]
    keys = cont_data.keys()

    sum_data = {}
    sum_data['account_name'] = ''
    for key in keys:
        if key == 'account_name':
            continue

        value = 0
        for item in content_list:
            value = value + float(item.get(key, 0))
        sum_data[key] = round(value, 4)

    content_list.append(sum_data)

    # sending email
    send_email.send_OneChain_HtmlEmail('newseeing@163.com', content_list)
    logger.warning('********** Sending Email Complete!')

# Start from here...
# loop_onechain()



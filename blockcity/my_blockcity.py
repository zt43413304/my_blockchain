# coding=utf-8
import logging
import time

import requests
import requests.packages.urllib3.util.ssl_
from requests.packages import urllib3

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_blockcity.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_blockcity.log', mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

pre_headers = {

    # OPTIONS /customer/sH3pFFtok2LpLDsdVXC073863426 HTTP/1.1
    'Host': "walletgateway.gxb.io",
    'Origin': "https://blockcity.gxb.io",
    'Access-Control-Request-Method': "GET",
    'Content-Length': "0",
    'Access-Control-Request-Headers': "authorization,channel,model,os,version",
    'Connection': "keep-alive",
    'Accept': "*/*",
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 (4529972224)",
    'Referer': "https://blockcity.gxb.io/",
    'Accept-Language': "zh-cn",
    'Accept-Encoding': "br, gzip, deflate"

}

headers = {
    'Authorization': "c0gzcEZGdG9rMkxwTERzZFZYQzA3Mzg2MzQyNjo5ODI5Q1hacldYUmpSVTJ0dFpVNElaZDg3MzM=",
    'Referer': "https://blockcity.gxb.io/",
    'Origin': "https://blockcity.gxb.io",
    'Host': "walletgateway.gxb.io",
    'Version': "1.3.9",
    'Os': "ios",
    'Accept-Encoding': "br, gzip, deflate",
    'Accept-Language': "zh-CN",
    'Accept': "application/json, text/plain, */*",
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 (5075211776)",
    'Connection': "keep-alive",
    'Model': "iPhone7%2C1",
    'Cache-Control': "no-cache"
}


def pre_verify():
    try:
        url01 = 'https://walletgateway.gxb.io/application/list'
        urllib3.disable_warnings()
        response = requests.request("OPTIONS", url01, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 01 = " + str(response.status_code))
        time.sleep(1)

        url02 = 'https://walletgateway.gxb.io/customer/sH3pFFtok2LpLDsdVXC073863426'
        response = requests.request("OPTIONS", url02, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 02 = " + str(response.status_code))
        time.sleep(1)

        url03 = 'https://walletgateway.gxb.io/auth/sH3pFFtok2LpLDsdVXC073863426/data/list'
        response = requests.request("OPTIONS", url03, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 03 = " + str(response.status_code))
        time.sleep(1)

        url04 = 'https://walletgateway.gxb.io/config/view'
        response = requests.request("OPTIONS", url04, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 04 = " + str(response.status_code))
        time.sleep(1)

        url05 = 'https://walletgateway.gxb.io/barrage/receive/list'
        response = requests.request("OPTIONS", url05, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 05 = " + str(response.status_code))
        time.sleep(1)

        url06 = 'https://walletgateway.gxb.io/application/minerAdvert'
        response = requests.request("OPTIONS", url06, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 06 = " + str(response.status_code))
        time.sleep(1)

        url07 = 'https://walletgateway.gxb.io/miner/sH3pFFtok2LpLDsdVXC073863426/info'
        response = requests.request("OPTIONS", url07, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 07 = " + str(response.status_code))
        time.sleep(1)

        url08 = 'https://walletgateway.gxb.io/miner/sH3pFFtok2LpLDsdVXC073863426/mine/list/v2'
        response = requests.request("OPTIONS", url08, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 08 = " + str(response.status_code))
        time.sleep(1)

        url09 = 'https://walletgateway.gxb.io/config/coins'
        response = requests.request("OPTIONS", url09, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 09 = " + str(response.status_code))
        time.sleep(1)

        url10 = 'https://walletgateway.gxb.io/customer/miner/type'
        response = requests.request("OPTIONS", url10, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 10 = " + str(response.status_code))
        time.sleep(1)

        url11 = 'https://walletgateway.gxb.io/customer/miner/steal'
        response = requests.request("OPTIONS", url11, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 11 = " + str(response.status_code))
        time.sleep(1)

        url12 = 'https://walletgateway.gxb.io/operator/activity/sH3pFFtok2LpLDsdVXC073863426/mine/list'
        response = requests.request("OPTIONS", url12, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 12 = " + str(response.status_code))
        time.sleep(1)

        url13 = 'https://walletgateway.gxb.io/customer/sH3pFFtok2LpLDsdVXC073863426/identity?operateType='
        response = requests.request("OPTIONS", url13, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 13 = " + str(response.status_code))
        time.sleep(1)

        url14 = 'https://walletgateway.gxb.io/application/hotSpotApp/list'
        response = requests.request("OPTIONS", url14, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 14 = " + str(response.status_code))
        time.sleep(1)

        url15 = 'https://walletgateway.gxb.io/blockchain'
        response = requests.request("OPTIONS", url15, headers=pre_headers, verify=False)
        logger.warning(">>>>>>>>>> pre_verify 15 = " + str(response.status_code))
        time.sleep(1)

        return 0
    except Exception as e:
        print(e)
        return -1


def mine_myself():
    url_mylist = "https://walletgateway.gxb.io/miner/sH3pFFtok2LpLDsdVXC073863426/mine/list/v2"

    try:
        response = requests.request("OPTIONS", url_mylist, headers=pre_headers, verify=False)
        response = requests.request("GET", url_mylist, headers=headers, verify=False)

        if response.status_code == 200:
            mylist = response.json()["data"]["mines"]

            for i in range(len(mylist)):
                id = mylist[i]['id']
                my_url = "https://walletgateway.gxb.io/miner/sH3pFFtok2LpLDsdVXC073863426/mine/" + str(id) + "/v2"
                response = requests.request("OPTIONS", my_url, headers=pre_headers, verify=False)
                response = requests.request("GET", my_url, headers=headers, verify=False)
                if response.status_code == 200:
                    drawAmount = response.json()["data"]["drawAmount"]
                    logger.warning(">>>>>>>>>> mine myself = " + str(drawAmount))
        return 0

    except Exception as e:
        print(e)
        return -1

    # querystring = {"change":"false","hasLocation":"true"}

    # try:
    #     response = requests.request("GET", url_mylist, headers=headers)
    #
    #     if response.status_code == 200:
    #         namelist = response.json()["data"]["list"]
    #
    #         for i in range(len(namelist)):
    #             pass
    #             if namelist[i]['canSteal']:
    #                 userid = namelist[i]['userId']
    #                 logger.warning(">>>>>>>>>> Name = " + userid)
    #                 get_minelist(namelist[i]['userId'])
    #
    # except Exception as e:
    #     print(e)
    #     return -1

def get_namelist():
    url = "https://walletgateway.gxb.io/miner/steal/user/list/v2"

    querystring = {"change":"false","hasLocation":"true"}


    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 200:
            namelist = response.json()["data"]["list"]

            for i in range(len(namelist)):
                pass
                if namelist[i]['canSteal']:
                    userid = namelist[i]['userId']
                    logger.warning(">>>>>>>>>> Name = " + userid)
                    get_minelist(namelist[i]['userId'])
            return 0

    except Exception as e:
        print(e)
        return -1

def get_minelist(userid):
    url = "https://walletgateway.gxb.io/miner/steal/"+userid+"/mine/list"

    try:
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            minelist = response.json()["data"]

            for i in range(len(minelist)):
                pass
                if minelist[i]['canSteal']:
                    mineid = minelist[i]['mineId']
                    symbol = minelist[i]['symbol']
                    logger.warning(">>>>>>>>>> Coin = " + str(mineid))
                    mine_steal(userid, mineid, symbol)


    except Exception as e:
        print(e)
        return -1

def mine_steal(userid, mineid, symbol):
    url = "https://walletgateway.gxb.io/miner/steal/"+userid+"/mine/"+str(mineid)


    try:
        response = requests.request("POST", url, headers=headers)

        if response.status_code == 200:
            data = response.json()["data"]
            stealAmount = data['stealAmount']
            logger.warning(">>>>>>>>>> Steal: " + symbol + ", " + float(stealAmount))
            # for i in range(len(coinlist)):
            #     pass
            #     if coinlist[i]['canSteal']:
            #         logger.warning(">>>>>>>>>> Coin list = " + str(coinlist[i]['mineId']))


    except Exception as e:
        print(e)
        return -1


def loop_blockcity():
    # start
    logger.warning('********** Start from loop_blockcity() ...')

    pre_verify()
    status = mine_myself()


loop_blockcity()

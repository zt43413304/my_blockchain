# coding=utf-8
import logging
import sys

import requests

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


headers = {
    'Authorization': "c0gzcEZGdG9rMkxwTERzZFZYQzA3Mzg2MzQyNjoyMDczUk11N2xyWWNVT1VvalJFM2IxazY3MzU=",
    'Cache-Control': "no-cache",
}


def mine_self():

    myinfo = "https://walletgateway.gxb.io/miner/sH3pFFtok2LpLDsdVXC073863426/mine/list/v2"
    mymine = "https://walletgateway.gxb.io/miner/sH3pFFtok2LpLDsdVXC073863426/mine/436965272/v2"



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

    except Exception as e:
        print(e)
        return -1

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

get_namelist()
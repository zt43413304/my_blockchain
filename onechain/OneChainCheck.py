# coding=utf-8

import configparser
import json
import logging
import os
import re
import time

import requests
import schedule

import Send_email

# 日志
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'new.log'
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

ch.setFormatter(formatter)
logger.addHandler(ch)

# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')


# get config information
curpath = os.getcwd()
content = open(curpath + '/config.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/config.ini', 'w').write(content)


# start
logging.warning('***** Start ...')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-Hans-CN;q=1',
    'Accept-Encoding': 'gzip',
    'Cache-Control': "no-cache"
}


def getInfoNum(infoNum):
    global version, l, user_agent, device_id
    cf = configparser.ConfigParser()
    cf.read(curpath + '/config.ini')
    version = cf.get('info', 'version').strip()
    l = cf.get('info', 'l').strip()
    user_agent = cf.get('info'+str(infoNum), 'user_agent').strip()
    device_id = cf.get('info'+str(infoNum), 'device_id').strip()
    return version, l, user_agent, device_id


def loginGetAccessToken(user_agent, device_id, l, version):
    url_login = 'http://hkopenservice1.yuyin365.com:8000/one-chain/login?user_agent=' + user_agent + '&device_id=' + device_id + '&l=' + l + '&token=&version=' + version

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_login, data=data, headers=headers)

        # if bProxy == 0:
        #     r = requests.post(url_login, headers=headers, verify=False) #headers=headers,
        # else:
        #     r = requests.post(url_login, headers=headers, proxies=proxies, verify=False) #headers=headers,

        res = r.json()["msg"]
        if res == 'Success':
            token = r.json()["data"]["map"]["token"]
            return token
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def open_mining(user_agent, device_id, l, token, version):
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/start?user_agent=' + user_agent + '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers)

        res = r.json()["msg"]
        if res == 'Success':
            logging.warning('>>>>>>>>>> mining_opened.')
            return 0
        else:
            return -1

    except Exception as e:
        print(e)
        return


def get_calculated(user_agent, device_id, l, token, version):
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/user/infoString?user_agent=' + user_agent + '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers)

        res = r.json()["msg"]
        if res == 'Success':
            mining_flag = r.json()['data']['map']['mining_flag']
            if mining_flag == "NO":
                open_mining(user_agent, device_id, l, token, version)
                logging.warning('>>>>>>>>>> mining opened')

            calculated = r.json()['data']['map']['calculated']
            logging.warning('>>>>>>>>>> calculated: ' + calculated)
            return calculated
    except Exception as e:
        print(e)
        return -1


def mining_click(user_agent, device_id, l, token, version, mining_detail_uuid):
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/detail/click?user_agent=' + user_agent + '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version + '&mining_detail_uuid=' + mining_detail_uuid

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers)

        res = r.json()["msg"]
        if res == 'Success':
            logging.warning('>>>>>>>>>> mining...... ' + str(mining_detail_uuid))
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        return


def mining_check(user_agent, device_id, l, token, version):
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/detail/list?user_agent=' + user_agent + '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers)

        res = r.json()["msg"]
        if res == 'Success':
            contentlist = r.json()['data']['list']
            i = 0
            for i in range(len(contentlist)):
                uni_uuid = contentlist[i]['uni_uuid']
                mining_click(user_agent, device_id, l, token, version, str(uni_uuid))

            if i == 0:
                logging.warning('>>>>>>>>>> mining_clicked: ' + str(i))
            else:
                logging.warning('>>>>>>>>>> mining_clicked: ' + str(i + 1))
            return 0
        else:
            return -1

    except Exception as e:
        print(e)
        return


def check_allTotal(user_agent, device_id, l, token, version):
    url_check = 'http://hkopenservice1.yuyin365.com:8000/one-chain/mining/allTotal?user_agent=' + user_agent + '&device_id=' + device_id + '&l=' + l + '&token=' + token + '&version=' + version

    one = 0
    oneluck = 0

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_check, data=data, headers=headers)

        res = r.json()["msg"]
        if res == 'Success':
            totallist = r.json()['data']['list']
            i = 0
            for i in range(len(totallist)):
                asset_code = totallist[i]['asset_code']
                total = totallist[i]['total']
                if asset_code == "ONE":
                    one = total
                if asset_code == "ONELUCK":
                    oneluck = total
                logging.warning('>>>>>>>>>> ' + asset_code + ': ' + str(total))
            return one, oneluck
        else:
            return -1, -1

    except Exception as e:
        print(e)
        return -1, -1

def postman_login():
    url = "http://hkopenservice1.yuyin365.com:8000/one-chain/login"

    querystring = {"user_agent":"android","l":"zh-CN","device_id":"008796747873160","token":"","version":"128"}

    payload = "account_id=1.2.470628&account_name=xudaisi&signed_message=G6gWd1Uv%2BjknXrJBxO%2FqvjMmBntXu5MZZOBM2JFIINHdUp%2BQvZn%2FN0y8P9mlLs8gOwuzn0aIkDPRqQzGXLnTKWg%3D"


    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    print(response.text)

def postman_getCalculated():
    url = "http://hkopenservice1.yuyin365.com:8000/one-chain/mining/user/infoString"

    querystring = {"user_agent":"android","l":"zh-CN","device_id":"008796747873160","token":"0404abe7478949d0abdbd71858066446","version":"128"}


    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def postman_getList():

    url = "http://hkopenservice1.yuyin365.com:8000/one-chain/mining/detail/list"

    querystring = {"user_agent":"android","l":"zh-CN","device_id":"008796747873160","token":"0404abe7478949d0abdbd71858066446","version":"128"}


    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def postman_miningClick():

    url = "http://hkopenservice1.yuyin365.com:8000/one-chain/mining/detail/click"

    querystring = {"user_agent":"android","l":"zh-CN","device_id":"008796747873160","token":"0404abe7478949d0abdbd71858066446","version":"128"}

    payload = "account_id=1.2.470628&account_name=xudaisi&signed_message=G6gWd1Uv%2BjknXrJBxO%2FqvjMmBntXu5MZZOBM2JFIINHdUp%2BQvZn%2FN0y8P9mlLs8gOwuzn0aIkDPRqQzGXLnTKWg%3D&mining_detail_uuid%3Dcab375674834408e846305af3d58936d="

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    print(response.text)

def postman_allTotal():

    url = "http://hkopenservice1.yuyin365.com:8000/one-chain/mining/allTotalString"

    querystring = {"user_agent":"android","l":"zh-CN","device_id":"008796747873160","token":"0404abe7478949d0abdbd71858066446","version":"128"}


    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def loop_data_mining():
    global data
    global token
    one_total = 0
    oneluck_total = 0
    content = "\t\n"

    file = open('one_chain_data.json', 'r', encoding='utf-8')
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

        logging.warning("========== Checking [" + account_name + "] ==========")

        token = loginGetAccessToken(user_agent, device_id, l, version)
        if token == -1:
            logging.warning('********** Login fail!')
            continue
        else:
            logging.warning('********** Login success! token:' + token)

            calculated = get_calculated(user_agent, device_id, l, token, version)
            mining_check(user_agent, device_id, l, token, version)
            (one, oneluck) = check_allTotal(user_agent, device_id, l, token, version)
            one_total = one_total + float(one)
            oneluck_total = oneluck_total + float(oneluck)
            content = content + " [" + account_name + "], Total[ONE:" + str(one_total) + ", ONELUCK:" + str(
                oneluck_total) + "] \t\n"
            logging.warning("========== End[" + account_name + "], Total[ONE:" + str(one_total) + ", ONELUCK:" + str(
                oneluck_total) + "] ==========")
            logging.warning('\n')

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            content_data = {
                "account_name": account_name,
                "calculated": calculated,
                "ONE": one,
                "ONELUCK": oneluck
            }
            content_list.append(content_data)
            time.sleep(2)

    # sending email
    Send_email.send_HtmlEmail('newseeing@163.com', content_list)
    logging.warning('********** Sending Email Complete!')


# Start from here...
loop_data_mining()

# ssl._create_default_https_context = ssl._create_unverified_context
# schedule.every(120).minutes.do(loop_data_mining)
schedule.every(8).hours.do(loop_data_mining)
# schedule.every().day.at("01:05").do(loop_data_mining)
# schedule.every().monday.do(loop_data_mining)
# schedule.every().wednesday.at("13:15").do(loop_data_mining)

while True:
    schedule.run_pending()
    time.sleep(1)

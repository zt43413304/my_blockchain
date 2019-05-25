# coding=utf-8

import json
import logging
import os
import random
import ssl
import sys
import time

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import send_email


# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_epay.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_epay.log', mode='w')
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

# # get config information
curpath = os.getcwd()

# Random seconds
mail_subject = ''
MIN_SEC = 1
MAX_SEC = 3


def epay_login(account_id):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/user/login"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "7ef85768-3c06-4e8d-92c4-11b8c880b7e7"
    }

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"name\"\r\n\r\n" + account_id + "\r\n" \
                                                                "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
                                                                "form-data; name=\"pwd\"\r\n\r\nLiuxb0504\r\n" \
                                                                "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    try:
        # logger.warning("********** epay_login(), account_id = " + str(account_id))

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, data=payload, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            logger.warning('********** Login success. account_id:' + account_id)
            token = response.json()["data"]["user-token"]
            return token
        else:
            logger.warning('********** Login fail. account_id:' + account_id)
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_logout(token):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/user/logout"

    headers = {
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'user-token': token,
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "f4e6c2f9-4e70-4ce4-b760-a72d4f060fd6"
    }

    try:
        # logger.warning("********** epay_logout()" )

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            logger.warning('********** Logout success.')
            return token
        else:
            logger.warning('********** Logout fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_get_info(token, account_id):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/asset/data"

    querystring = {"include_market": "1", "include_address": "1"}

    headers = {
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'user-token': token,
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "f4e6c2f9-4e70-4ce4-b760-a72d4f060fd6"
    }

    try:
        # logger.warning("********** epay_get_info() ")
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("GET", url, headers=headers, params=querystring, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:

            # 静态收益
            income = response.json()["data"]["income"]
            if income != "0":
                epay_collect(token, "income")

            # 动态收益
            commission = response.json()["data"]["commission"]
            if commission != "0":
                epay_collect(token, "commission")

            # 社区奖金
            award = response.json()["data"]["award"]
            if award != "0":
                epay_collect(token, "award")

            # 拉新奖励
            activity = response.json()["data"]["activity"]
            if float(activity) >= 1000:
                epay_collect(token, "activity")

            # 积分
            score = response.json()["data"]["score"]

            # 当前ET美元单价
            currency_price = response.json()["data"]["et_data"]["currency_price"]

            # 当前ET美元价值
            currency_value = response.json()["data"]["et_data"]["currency_value"]

            # ET合计
            response = requests.request("GET", url, headers=headers, params=querystring, timeout=60, verify=False)
            et = response.json()["data"]["et"]

            # investment_sum, investment_earliest_amount, investment_earliest_days
            (investment_sum, investment_earliest_amount, investment_earliest_days) = epay_get_investment(token)

            # subprofile
            subprofile_data = epay_get_subprofile(token)
            my_level = subprofile_data.get('my_level', 'NA')
            team_member_count = subprofile_data.get('team_member_count', 'NA')
            investment_sum_team = subprofile_data.get('investment_sum', 'NA')

            # Python 字典类型转换为 JSON 对象
            content_data = {
                "account_id": account_id,
                "income": income,
                "commission": commission,
                "award": award,
                "score": score,
                "activity": activity,
                "currency_price": currency_price,
                "currency_value": currency_value,
                "et": et,
                "investment_sum": investment_sum,
                "investment_earliest_amount": investment_earliest_amount,
                "investment_earliest_days": investment_earliest_days,
                "my_level": my_level,
                "team_member_count": team_member_count,
                "investment_sum_team": investment_sum_team
            }

            logger.warning('********** epay_get_info() success.')
            return content_data

        else:
            logger.warning('********** epay_get_info() fail.')
            return -1
    except Exception as e:
        print(e)
        logger.warning('********** epay_get_info() Exception.')
        return -1


def epay_get_investment(token):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/asset/data"

    querystring = {"include_investment": "1", "include_market": "1", "include_address": "1"}

    headers = {
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'user-token': token,
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "f4e6c2f9-4e70-4ce4-b760-a72d4f060fd6"
    }

    try:
        # logger.warning("********** epay_get_investment() ")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("GET", url, headers=headers, params=querystring, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            # investment_sum
            investment_sum = response.json()["data"]["investment_sum"]
            investment_list = response.json()["data"]["investment"]

            # earliest element
            investment_ele = investment_list[len(investment_list)-1]
            investment_earliest_amount = investment_ele["amount"]
            investment_earliest_days = investment_ele["days"]

            logger.warning('********** epay_get_investment() success.')

            return investment_sum, investment_earliest_amount, investment_earliest_days
        else:
            logger.warning('********** epay_get_investment() fail.')
            return -1, -1, -1
    except Exception as e:
        print(e)
        return -1, -1, -1


def epay_get_profile(token):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/user/profile"

    headers = {
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'user-token': token,
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "f4e6c2f9-4e70-4ce4-b760-a72d4f060fd6"
    }

    try:
        # logger.warning("********** epay_get_profile() ")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("GET", url, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:

            mail = response.json()["data"]["mail"]

            name = response.json()["data"]["name"]

            id = response.json()["data"]["id"]

            # Python 字典类型转换为 JSON 对象
            profile_data = {
                "mail": mail,
                "name": name,
                "id": id
            }

            logger.warning('********** epay_get_profile() success.')

            return profile_data
        else:
            logger.warning('********** epay_get_profile() fail.')
            return -1
    except Exception as e:
        print(e)
        return -1

def epay_get_subprofile(token):

    sub_url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/user/subordinate"

    headers = {
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'user-token': token,
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "f4e6c2f9-4e70-4ce4-b760-a72d4f060fd6"
    }

    try:
        # logger.warning("********** epay_get_subprofile() ")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("GET", sub_url, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:

            my_level = response.json()["data"]["my_level"]

            team_member_count = response.json()["data"]["team_member_count"]

            investment_sum = response.json()["data"]["investment_sum"]

            # Python 字典类型转换为 JSON 对象
            profile_data = {
                "my_level": my_level,
                "team_member_count": team_member_count,
                "investment_sum": investment_sum
            }

            logger.warning('********** epay_get_subprofile() success.')

            return profile_data
        else:
            logger.warning('********** epay_get_subprofile() fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_collect(token, type):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/asset/et/collect"

    headers = {
        'user-token': token,
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "7ef85768-3c06-4e8d-92c4-11b8c880b7e7"
    }

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"zone\"\r\n\r\n" + type + "\r\n" \
                                                          "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    try:
        # logger.warning("********** epay_collect()")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, data=payload, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            logger.warning('********** epay_collect() success. type = ' + type)

            return 0
        else:
            logger.warning('********** epay_collect() fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_send_captcha(token):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/user/mail/send_captcha"

    headers = {
        'user-token': token,
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "7ef85768-3c06-4e8d-92c4-11b8c880b7e7"
    }

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"purpose\"\r\n\r\nasset\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    try:
        # logger.warning("********** epay_send_captcha()")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, data=payload, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            logger.warning('********** epay_send_captcha() success.')

            return 0
        else:
            logger.warning('********** epay_send_captcha() fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_validate_captcha(token, captcha):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/user/mail/validate_captcha"

    headers = {
        'user-token': token,
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "7ef85768-3c06-4e8d-92c4-11b8c880b7e7"
    }

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"captcha\"\r\n\r\n" + captcha + "\r\n" \
                                                                "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    try:
        # logger.warning("********** epay_validate_captcha()")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, data=payload, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            logger.warning('********** epay_validate_captcha() success.')

            return 0
        else:
            logger.warning('********** epay_validate_captcha() fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_do_transfer(token, amount):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/asset/et/transfer"

    headers = {
        'user-token': token,
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "7ef85768-3c06-4e8d-92c4-11b8c880b7e7"
    }

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"account_name\"\r\n\r\n13601223469\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"amount\"\r\n\r\n" + amount + "\r\n" \
                                                              "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    try:
        # logger.warning("********** epay_do_transfer()")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, data=payload, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 200:
            logger.warning('********** epay_do_transfer() success.')

            return 0
        else:
            logger.warning('********** epay_do_transfer() fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def epay_transfer(token, amount):
    url = "https://epkkpd5dai.execute-api.ap-northeast-1.amazonaws.com/pub/asset/et/transfer"

    headers = {
        'user-token': token,
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'User-Agent': "ESHOP/5 CFNetwork/976 Darwin/18.2.0",
        'Accept-Encoding': "br, gzip, deflate",
        'Cache-Control': "no-cache",
        'Postman-Token': "7ef85768-3c06-4e8d-92c4-11b8c880b7e7"
    }

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"account_name\"\r\n\r\n13601223469\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"amount\"\r\n\r\n" + amount + "\r\n" \
                                                              "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    try:
        # logger.warning("********** epay_transfer()")

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context

        response = requests.request("POST", url, data=payload, headers=headers, timeout=60, verify=False)

        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["code"]
        if res == 101:
            logger.warning('********** 需要校验邮箱验证码.')

            # 取邮箱地址
            profile_data = epay_get_profile(token)
            mail = profile_data.get('mail', 'NA')

            # 发送邮箱验证码
            return_code = epay_send_captcha(token)
            time.sleep(10)

            # 收取邮件
            captcha = send_email.get_email_epay(mail, "epay1234")
            logger.warning('^^^^^^^^^^ 第一次取邮箱验证码. captcha = ' + captcha)

            if len(str(captcha)) != 6:
                time.sleep(30)
                captcha = send_email.get_email_epay(mail, "epay1234")
                logger.warning('^^^^^^^^^^ 第二次取邮箱验证码. captcha = ' + captcha)

            # 校验验证码
            return_code = epay_validate_captcha(token, captcha)

            # 实际转账
            return_code = epay_do_transfer(token, amount)
            # logger.warning('********** 实际转账. return_code = ' + str(return_code))

            return 0
        else:
            logger.warning('********** epay_transfer fail.')
            return -1
    except Exception as e:
        print(e)
        return -1


def loop_epay(filename):
    global mail_subject
    # total_bx_all = 0
    # today_bx_all = 0

    # start
    logger.warning('********** Start from loop_epay() ...')

    file = open(curpath + '/epayapp/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)
    content_list = []

    number = 0
    for item in data_dict['data']:
        number += 1
        # content_list = []
        account_id = item.get('account_id', 'NA')
        # uid = item.get('uid', 'NA')
        # phone = item.get('phone', 'NA')

        logger.warning('\n')
        logger.warning("========== Checking " + str(account_id) + ". [" + account_id + "] ==========")

        token = epay_login(account_id)
        if token == -1:
            continue
        else:
            # 获取状态
            content_data = epay_get_info(token, account_id)
            if content_data == -1:
                continue

            amount = content_data.get('et', 'NA')
            if amount != "0" and account_id != "13601223469":
                epay_transfer(token, amount)

            # 退出
            epay_logout(token)

            content_list.append(content_data)
            time.sleep(random.randint(MIN_SEC, MAX_SEC))
    #     # break

    send_email.send_Epay_HtmlEmail('newseeing@163.com', content_list)
    logger.warning('********** Sending Email Complete!')


# loop_epay("my_epay_data.json")

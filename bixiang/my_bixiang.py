# coding=utf-8

import configparser
import json
import logging
import os
import random
import re
import time
from io import StringIO

import requests
from lxml import etree

from bixiang import Appium_bixiang
from common import daxiang_proxy
from common import send_email

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_bixiang.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang.log', mode='w')
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
content = open(curpath + '/bixiang/config_bixiang.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/bixiang/config_bixiang.ini', 'w').write(content)

cf = configparser.ConfigParser()
cf.read(curpath + '/bixiang/config_bixiang.ini')
# unique = cf.get('info', 'unique').strip()
# uid = cf.get('info', 'uid').strip()
is_ad_ios = cf.get('info', 'is_ad_ios').strip()
versioncode = cf.get('info', 'versioncode').strip()
devicetype = cf.get('info', 'devicetype').strip()
channel = cf.get('info', 'channel').strip()
token = cf.get('info', 'token').strip()
ps = cf.get('info', 'ps').strip()
key = cf.get('info', 'key').strip()

headers = {
    'Host': "tui.yingshe.com",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'User-Agent': "okhttp/3.4.1",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}

payload = "is_ad_ios=" + is_ad_ios + \
          "&versioncode=" + versioncode + \
          "&devicetype=" + devicetype + \
          "&channel=" + channel + \
          "&token=" + token + \
          "&ps=" + ps + \
          "&key=" + key + \
          "&ceshi=1"

# user_agent = cf.get('info'+str(infoNum), 'user_agent').strip()
# device_id = cf.get('info'+str(infoNum), 'device_id').strip()

# Random seconds
mail_subject = ''
MIN_SEC = 1
MAX_SEC = 1
proxies = ''


def bixiang_login_test():
    url = "http://tui.yingshe.com/check/index"

    payload = "unique=868687787575888&uid=395488&is_ad_ios=1&versioncode=229&devicetype=1&channel=Y1032&token=3824ea69dd6a26c4f476167e627693a9&ps=MTIzNTg0MTUyNg%3D%3D&key=MTUyNTQ0OTYxMjM1ODQxNTI2"
    # headers = {
    #     'Host': "tui.yingshe.com",
    #     'Connection': "Keep-Alive",
    #     'Accept-Encoding': "gzip",
    #     'User-Agent': "okhttp/3.4.1",
    #     'Content-Type': "application/x-www-form-urlencoded",
    #     'Cache-Control': "no-cache",
    #     'Postman-Token': "bfda041f-affb-4e05-b867-021e7b7e14f9"
    # }

    response = requests.request("POST", url, data=payload, headers=headers, timeout=120)

    print(response.text)


def bixiang_userinfo(unique, uid):
    global proxies
    url = "http://tui.yingshe.com/member/userInfo"

    payload_userinfo = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_userinfo(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_userinfo, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            show_id = response.json()["info"]["show_id"]
            phone = response.json()["info"]["phone"]
            nickname = response.json()["info"]["nickname"]
            bxc = response.json()["info"]["bxc"]
            logger.warning(
                '********** uid=' + uid + ', show_id=' + show_id + ', nickname=' + nickname +
                ', phone=' + phone + ', bxc=' + bxc)
            return show_id, phone, nickname
        else:
            return -1, -1, -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1, -1, -1


def bixiang_login(unique, uid):
    global proxies
    url = "http://tui.yingshe.com/check/index"

    payload_login = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** selenium_login(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_login, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            logger.warning('********** Login success.')
            bixiang_userinfo(unique, uid)
            return 1
        else:
            logger.warning('********** Login fail. uid:' + uid)
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def bixiang_infoList(unique, uid):
    global proxies
    url = "http://tui.yingshe.com/live/info"

    payload_infoList = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_infoList(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_infoList, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            info = response.json()["info"]
            return info
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def bixiang_sharing(unique, uid, id):
    global proxies
    url = "http://tui.yingshe.com/live/infofrist"

    payload_id = payload + "&live_id=" + id + "&unique=" + unique + "&uid=" + uid

    try:
        # logger.warning("********** bixiang_sharing(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_id, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            # logger.warning('^^^^^^^^^^ Sharing.')
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def bixiang_shared(unique, uid, id):
    global proxies
    url = "http://tui.yingshe.com/share/getShareCircle"

    payload_id = payload + "&live_id=" + id + "&unique=" + unique + "&uid=" + uid

    try:
        # logger.warning("********** bixiang_shared(), proxies = " + str(proxies))
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload_id, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            # logger.warning('^^^^^^^^^^ Shared.')
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


# 返回值：出错-1，第一次签到成功1，第二次检查2
def bixiang_sign(unique, uid):
    global proxies
    url_check = "http://tui.yingshe.com/check/index"
    url_add = "http://tui.yingshe.com/check/add"

    payload_sign = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_sign(), proxies = " + str(proxies))
        response = requests.request("POST", url_check, data=payload_sign, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            is_check = int(response.json()["info"]["is_check"])
            # "is_check == 0",not signed
            if is_check == 0:
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                response = requests.request("POST", url_add, data=payload_sign, headers=headers)
                time.sleep(random.randint(MIN_SEC, MAX_SEC))
                checked = int(response.json()["info"]["is_check"])
                if checked == 1:
                    logger.warning('>>>>>>>>>> Not Sign, Just Signed.')
                    return 1
                else:
                    logger.warning('********** Not Sign, Sign fail.')
                    return -1
            else:
                logger.warning('********** Have Signed.')
                return 2
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def bixiang_upgrade(unique, uid):
    global mail_subject
    global proxies
    url = "http://tui.yingshe.com/member/getNoLevel"
    url_upgrade = "http://tui.yingshe.com/member/getLevelReward"

    payload_upgrade = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_upgrade(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_upgrade, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            now_bxc = response.json()["info"]["now_bxc"]
            level_bxc = response.json()["info"]["level_bxc"]
            logger.warning('********** Upgrade. now_bxc=' + str(now_bxc))
            logger.warning('********** Upgrade. level_bxc=' + str(level_bxc))

            if now_bxc > level_bxc:
                # logger.warning('********** now_bxc > level_bxc, before upgrade')
                response = requests.request("POST", url_upgrade, data=payload_upgrade, headers=headers)
                # logger.warning('********** now_bxc > level_bxc, after upgrade')
                # logger.warning('********** now_bxc > level_bxc, response status = ' + str(response.json()["status"]))
                mail_subject = mail_subject + ', Upgrade'
                if response.json()["status"] == 1:
                    logger.warning('>>>>>>>>>>  Upgrade Success! ')
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def bixiang_property_url(unique, uid):
    global proxies
    url = "http://tui.yingshe.com/member/miningBxc"

    payload_property = payload + "&unique=" + unique + "&uid=" + uid

    try:
        logger.warning("********** bixiang_property_url(), proxies = " + str(proxies))
        response = requests.request("POST", url, data=payload_property, headers=headers, timeout=60, proxies=proxies)
        time.sleep(random.randint(MIN_SEC, MAX_SEC))

        res = response.json()["status"]
        if res == 1:
            property_url = response.json()["info"]["bxc_details"]
            return property_url
        else:
            return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def get_allTotal(unique, uid):
    global proxies
    # url = "http://tui.yingshe.com/user/property"
    # querystring = {"xxx":"swh6XfD8FvRBZr17Hufua"}

    headers = {
        'Host': "tui.yingshe.com",
        'Connection': "close",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/3.4.1",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    url = bixiang_property_url(unique, uid)

    try:
        logger.warning("********** get_allTotal(), proxies = " + str(proxies))
        response = requests.request("GET", url, headers=headers, timeout=60, proxies=proxies)

        html = response.text

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)

        # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
        # print(result)

        total_bx_list = tree.xpath('//*[@id="wallet"]/a[1]/li/span[2]/text()')
        total_bx = float(total_bx_list[0].encode('utf-8'))

        today_bx_list = tree.xpath('//*[@id="wallet"]/a[1]/li/span[3]/span/text()')
        today_bx = float(today_bx_list[0].encode('utf-8'))
        # logger.warning("********** response.status_code = " + str(response.status_code))
        return total_bx, today_bx

    except requests.exceptions.ConnectionError as f:
        print(f)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1, -1
    except Exception as e:
        print(e)
        return -1, -1


def get_lottery_url(unique, uid):
    global proxies
    url = "http://tui.yingshe.com/member/miningBxc"

    payload_property = payload + "&unique=" + unique + "&uid=" + uid

    try:
        response = requests.request("POST", url, data=payload_property, headers=headers, timeout=60, proxies=proxies)
        image_url_list = response.json()["info"]["image_url"]

        for i in range(len(image_url_list)):
            url = image_url_list[i]
            nPos = url.find('lottery')

            if nPos > -1:
                return url
        return -1
    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def get_lottery_chance(url):
    global proxies

    try:

        response = requests.request("GET", url, headers=headers, timeout=60, proxies=proxies)

        html = response.text

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)

        chance = tree.xpath('//*[@id="free_number_remaining"]')
        # logger.warning(">>>>> chance = " + chance[0].text)

        xxx = tree.xpath('//*[@id="xxx"]')
        # logger.warning(">>>>> xxx = " + xxx[0].text)

        return chance[0].text, xxx[0].text

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1, -1


def bixiang_lottery(unique, uid):
    global proxies

    try:
        logger.warning("********** bixiang_lottery(), proxies = " + str(proxies))

        url = get_lottery_url(unique, uid)
        (chance, xxx) = get_lottery_chance(url)

        for i in range(int(chance)):
            lottery_enter = 'http://tui.yingshe.com/lottery/turntableFree?psid=' + uid + '&xxx=' + xxx
            response = requests.request("GET", lottery_enter, headers=headers, timeout=60, proxies=proxies)
            # print(response.text.encode('utf-8').decode('unicode_escape'))
            if response.json()["status"] == 1:
                logger.warning(
                    ">>>>>>>>>> " + response.json()["message"] + ", bxc_add = " + str(response.json()["bxc_add"]))
            time.sleep(random.randint(MIN_SEC, MAX_SEC))
        return 0

    except Exception as e:
        print(e)
        proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")
        return -1


def loop_bixiang(filename):
    global mail_subject
    total_bx_all = 0
    today_bx_all = 0

    # bixiang_login_test()

    # start
    logger.warning('********** Start from loop_bixiang() ...')

    global proxies
    proxies = daxiang_proxy.get_proxy("http://tui.yingshe.com/check/index")

    file = open(curpath + '/bixiang/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)
    content_list = []

    number = 0
    for item in data_dict['data']:
        number += 1
        # content_list = []
        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        phone = item.get('phone', 'NA')

        logger.warning('\n')
        logger.warning("========== Checking " + str(number) + ". [" + phone + "] ==========")

        status = bixiang_login(unique, uid)
        if status == -1:
            continue
        else:

            # 如已签到就退出
            signed = bixiang_sign(unique, uid)
            # if signed == 2:
            #     continue

            # 幸运大转盘
            bixiang_lottery(unique, uid)

            # 分享列表
            infoList = bixiang_infoList(unique, uid)
            if infoList == -1:
                continue
            # if infoList is None:
            #     continue
            # if len(infoList) == 0:
            #     continue

            count = 0
            for i in range(len(infoList)):
                if count > 4:
                    break
                if int(infoList[i]["share_total"]) < 20:
                    continue
                lv_id = infoList[i]["lv_id"]
                bixiang_sharing(unique, uid, lv_id)
                bixiang_shared(unique, uid, lv_id)
                logger.warning('>>>>>>>>>> ' + str(count) + '. Shared info ' + str(lv_id))
                count = count + 1

            # upgrade
            bixiang_upgrade(unique, uid)

            # calculate value
            (total_bx, today_bx) = get_allTotal(unique, uid)
            total_bx_all = total_bx_all + total_bx
            today_bx_all = today_bx_all + today_bx
            logger.warning("========== End[" + phone + "], total_bx:" + str(total_bx) + ", today_bx:" + str(
                today_bx) + "] ==========")

            # userinfo
            (show_id, phone, nickname) = bixiang_userinfo(unique, uid)

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            content_data = {
                "phone": phone,
                "nickname": nickname,
                "uid": uid,
                "show_id": show_id,
                "unique": unique,
                "total_bx": total_bx,
                "today_bx": today_bx
            }
            content_list.append(content_data)
            time.sleep(random.randint(MIN_SEC, MAX_SEC))
        # break

    content_list = sorted(content_list, reverse=True, key=lambda x: (x["total_bx"], x["today_bx"]))
    server = filename.split('.')[0][-5:]
    send_email.send_Bixiang_HtmlEmail('newseeing@163.com', content_list, server)
    logger.warning('********** Sending Email Complete!')


def loop_elephant(filename):
    content_list = []
    # start
    logger.warning('********** Start from loop_elephant() ...')

    file = open(curpath + '/bixiang/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)

    number = 0
    for item in data_dict['data']:
        number += 1
        # content_list = []
        unique = item.get('unique', 'NA')
        uid = item.get('uid', 'NA')
        phone = item.get('phone', 'NA')

        logger.warning("========== Elephant account: " + str(number) + ". [" + unique + "] ==========")

        # unique = '847069402404905'
        url = 'https://tui.yingshe.com/game?xxx=' + unique

        signup = Appium_bixiang.Signup()
        content = signup.firefox_elephant(url)
        if content != -1:
            content_list.append(content)
        # if number == 3:
        #     break

    send_email.send_Elephant_htmlmail('newseeing@163.com', 'Bixiang Elephant.', content_list)
    logger.warning('********** Sending Email Complete!')


def loop_bixiang_test():
    # start
    logger.warning('********** Start from loop_bixiang_test() ...')

    unique = '682927952795063'
    uid = '10027134'
    phone = '17132656549'

    logger.warning('\n')
    logger.warning("========== Checking [" + phone + "] ==========")

    status = bixiang_login(unique, uid)
    # if status != -1:
    # bixiang_lottery(unique, uid)
    # bixiang_quiz(unique, uid)

# Start from here...
# loop_bixiang_test()
# loop_bixiang('/data_bixiang_Tokyo.json')
# loop_elephant('/data_bixiang_Tokyo.json')

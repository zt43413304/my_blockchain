# coding=utf-8

import json
import logging
import os
import random
import re
import ssl
import time

import requests

from common import send_email
# 第一步，创建一个logger,并设置级别
from hashworld import Appium_hashworld, Appium_hashworld_Test

logger = logging.getLogger("my_hashworld_Test.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_hashworld_Test.log', mode='w')
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

curpath = os.getcwd()

# get config information
content = open(curpath + '/hashworld/config.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/hashworld/config.ini', 'w').write(content)

# Random seconds
MIN_SEC = 2
MAX_SEC = 5
proxies = ''


def open_FirstPage():
    global proxies
    url = "https://game.hashworld.top/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** open_FirstPage(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=180, verify=False)
        res = response.status_code
        logger.warning('********** open_FirstPage(), status_code=' + str(res))

        if res == 200:
            return res
        else:
            return -1
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def login_GetAccessToken(payload):
    global proxies
    url = "https://game.hashworld.top/apis/accounts/token/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** login_GetAccessToken(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers, proxies=proxies, timeout=180,
                                    verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            token = response.json()["data"]["token"]
            return token
        else:
            return -1
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def get_strength_info(token):
    global proxies
    url = "https://game.hashworld.top/apis/game/strength/get_strength_info/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_strength_info(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=180, verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            strength = response.json()['data']['strength']
            logger.warning(">>>>>>>>>> strength = " + str(strength))
            return strength
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def get_prize_wheel(token):
    global proxies
    url = "https://game.hashworld.top/apis/game/prize_wheel/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_prize_wheel(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=180, verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            wonder_list = response.json()['data']
            return wonder_list
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def click_Lottery(token, block_number):
    global proxies
    url = "https://game.hashworld.top/apis/game/lottery/"

    captcha_token = "https://game.hashworld.top/apis/accounts/captcha/?captcha_token=%257B%2522a%2522%253A%2522FFFF0N00000000005F93%2522%252C%2522c%2522%253A%25221528966794097%253A0.5570543240755796%2522%252C%2522d%2522%253A%2522nvc_message_h5%2522%252C%2522j%2522%253A%257B%2522test%2522%253A1%257D%252C%2522b%2522%253A%2522109%25236zPa7RfVapz%252FAjnQpCFbCzS%252BznvERMZGCqNiewbXGMXoQTvSesjXuaHpwtrGYulcrF5DYBWG%252FANxXXoCzGp2arK%252FlaRDNlTY7KDWV08C%252F2qqJiFK0zaVXQUdsPtNhU23vG418D4mYK2RjzAs2jC07xtwgjzWNu2M9i1bSiRrlX8FGux2iqzPWXBH504vyVvuzl31ksth79BpcnDSrODDJLBODjQCimaYgyUaDDEXliY3beCI4bDeKOguzUjB4DMxguOaaWYTliYmfCCaJ%252BfVEU%252BSaktR4e31gT2apNcElnblSjaR377exU9NGacE4VrbgjN6apJmli9Sgjchz%252FDeEz8hl7iB4suYEizaF3vBlL2JLaCa4bbaEuwHGGrE4TW6guOJG%252FYE4ixugHba9lYBNOgdac5E%252FtBbgzlja5tBli9SjePaiN2VEAZ90eiE%252FdObgUMaa75Rlm%252BpgFVPz27eEzwaG7iESM6YgrnPpNcElnb6ICGcdb1LWzgdaacEXmIYqQ6aaHLMli9Sgjavz%252F1BEboSa5jlztaYgzlcpWDGBiYJTgCI4bDeKUguuMYE4rzfguOaaWbhliDplj7F1%252BXjEz%252BS%252BaiR4sjbgrp4pNcElnYt96CaRkeerDwKpaiE4sd4guRoGWYH%252BcepgCaa%252B27VETZxGac70SI1gzla125Efnbd7mOPz27eEzwBG7iELn7ngTdopNcElnbQpCcOzu9e425hpaiIucCYDYIMaXSBo41SCgCaaR2eidXgacbEumSGnUzaaWYE2n6ugB7X4r0jEul5jCGc0tI1iljHad4mli1gUsWaM%252B3VEjPFaSA6ztG37Ozan%252BwRlMXdiaaaF2%252BVEevkaC7PrSI1zx7GaXvMliYk4ula4TDCEuQpaachztpG7oPoadIJli9SgjaHz%252FDybugutriRzSuYgsjMaSmgtt9S4u%252FM41yDEz8vZ7iB24uFg9UjpWYpl%252BXSgDOMz%252FbrOU8ny7iEon71gDyMpNcElnYBzgCaUgGEwO8HugiB4suYsDrMaHEg2i0SPvaM4bDeETVPpacE4sS6BOIaaWYECi%252Bugaaa40QzEulsqC7ssmIYgzlaE2ERlgE4bC7Yb2XjEz%252BScBiR44Lj7CL0ZN5BlnDSVjCM4rIjYu%252BS40iRzSuYgjIMacSnlwgknBCa4bb1Eu%252BgNavEneWbgUMaaE5RlKxs%252BT9jz27eEzlzpacjKSaY29OMGWYElnfugIX84b17gugdaacEwsabgTbGuWDPMiepgCaaBDXeZOMZa7sSzSI1gzlaCN5E5Tzp7ZzfzN3jEz%252BSqccBq8JVajaO8NXZlcVxh7i1zNHREURpp76ezmH1gOLUGN5Bln9SgjMr4bDe9zkkaaGl4saDgzlBGlYElBDn1ZZuzWDjDjrZq%252FC7KYiXVpNivuKd1khN%252B1WyQPMwMJQmtYEkryCisBdqcw%252F53OUkaIfyi3A%252B4FMHzsZSk6rGRmMHo4ApOD%252Ffb0vI7EXHpkb62QL6%252FZ4c6VLVPDLlI%252F8dfJMSsfUmKoxv%252FnddOwEbFqA%252Fj%252Ffm4ElqOK%252BuUoZykar%252F9wTg7dmC4YdKeFFOCCdkO0brIeROj5z7iwVhoFgXOOl2B8XDi2qaJSgMIyRUP%252FioX3jRPJEyx8DRkSJtgp3Q%252B400mu3bI0PRGuh5d7EmPJiSH6r%253D%2522%252C%2522e%2522%253A%25222aOt8P9F_ykXL0VHwa_YN0XFI1xtNCPMqF2PrQn456xhRldlz_zD9moXjfwq3TzrykhFIH3xpkH6nLiBFhQCOOXOcOG8JIhPz4gvKWwRmtg5WoNJI38-25zLhNmAke1HJLy-hrjr3Bctpe8I39gRvNtexwRKTE190IQA-RdyyRNHKzTa8h306sUUOTQ5BNHs7k1vLK1JVTM5uuLyO_vJRKqoL4EO5t4YPFVXkLT-o58%2522%257D"

    headers = {
        'user-agent': "application/x-www-form-urlencoded",
        'referer': "https://game.hashworld.top/",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    try:
        # logger.warning("********** click_Lottery(), proxies = " + str(proxies))
        payload = "{\n\t\"block_number\": " + str(block_number) + "\n}"

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("PUT", url, data=payload, headers=headers, proxies=proxies, timeout=180,
                                    verify=False)
        response = requests.request("GET", captcha_token, headers=headers, proxies=proxies, timeout=180, verify=False)
        time.sleep(random.randint(8, 10))
        response = requests.request("PUT", url, data=payload, headers=headers, proxies=proxies, timeout=180,
                                    verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            coin_name = response.json()["data"]["coin_name"]
            # amount = response.json()["data"]["amount"]
            logger.warning('********** lottery...... ' + coin_name)
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def check_UserTotal(token):
    global proxies
    url = "https://game.hashworld.top/apis/coin/gift_wallet/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "close"
    }

    total = 0

    try:
        logger.warning("********** check_UserTotal(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=180, verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            totallist = response.json()['data']
            for i in range(len(totallist)):
                market_price_cny = totallist[i]['coin']['market_price_cny']
                active_balance = totallist[i]['active_balance']
                total = total + market_price_cny * active_balance
            logger.warning('********** Total: ' + str(total))
            return total
        else:
            return -1
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1
    finally:
        requests.session().close()


def click_hashworld_land(token, strength, wonder_list, lands):
    strength_ori = strength
    # 根据体力值判断循环次数
    while strength > 0:

        # reveal = 0
        # for i in range(len(wonder_list)):
        #     has_reveal = wonder_list[i]['has_reveal']
        #     if bool(has_reveal):
        #         reveal = reveal + 1
        # logger.warning('********** Has revealed: ' + str(reveal))

        # click Jackielg's land
        for j in range(len(wonder_list)):
            if strength < 1:
                break
            has_reveal = wonder_list[j]['has_reveal']
            if not bool(has_reveal):
                if wonder_list[j]['land']['user']['nickname'] != "Jackielg":
                    continue
                # lottery = click_Lottery(token, j)
                lottery = lands.selenium_clickland(j + 1)

                if lottery == -1:
                    logger.warning('********** Click Jackielg land failed.')
                    continue
                else:
                    logger.warning('>>>>>>>>>> Click Jackielg land success.')
                    strength = strength - 1

        # click others land
        for k in range(len(wonder_list)):
            if strength < 1:
                break
            has_reveal = wonder_list[k]['has_reveal']
            if not bool(has_reveal):
                # lottery = click_Lottery(token, k)
                lottery = lands.selenium_clickland(k + 1)

                if lottery == -1:
                    logger.warning('********** Click Others land failed.')
                    continue
                else:
                    logger.warning('>>>>>>>>>> Click Others land success.')
                    strength = strength - 1

        # 值相等，即有体力，但没土地可挖，跳过
        if strength == strength_ori:
            logger.warning('>>>>>>>>>> Have strength, but no land to mine, break......')
            break



def get_Landlist(token):
    global proxies
    url = "https://game.hashworld.top/apis/land/lbsland/"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        logger.warning("********** get_Landlist(), proxies = " + str(proxies))
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=180, verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            land_list = response.json()['data']
            return land_list
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return -1


def get_LandPrice(token, land_number):
    global proxies
    url = "https://game.hashworld.top/apis/land/hall/"

    headers = {
        # 不能用这个user-agent
        # 'user-agent': "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044033 Mobile Safari/537.36",
        'referer': "https://game.hashworld.top/",
        'user-agent': "application/x-www-form-urlencoded",
        'content-type': "application/json",
        'accept': "application/json, text/plain, */*",
        'accept-language': "zh-CN,zh;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'authorization': "Token " + token,
        'cache-control': "no-cache",
        'connection': "keep-alive"
    }

    try:
        # logger.warning("********** get_LandPrice(), proxies = " + str(proxies))
        payload = "{\n\t\"land\": {\n\t\t\"id\": [" + str(land_number) + "]\n\t}\n}"

        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        time.sleep(random.randint(MIN_SEC, MAX_SEC))
        response = requests.request("POST", url, data=payload, headers=headers, proxies=proxies, timeout=180,
                                    verify=False)

        res = response.json()["status"]
        if res == 'common_OK':
            land_name = response.json()["data"][0]["land_name"]
            price = response.json()["data"][0]["price"]
            tradable_status = response.json()["data"][0]["tradable_status"]
            gen_time = response.json()["data"][0]["gen_time"]
            nickname = response.json()["data"][0]["user"]["nickname"]
            return land_name, price, tradable_status, gen_time, nickname
        else:
            return "error", 0, "untradable", 0, ""
    except Exception as e:
        print(e)
        # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
        return "error", 0, "untradable", 0, ""


def loop_Lottery(filename):
    all_total = 0
    content_list = []

    file = open(curpath + '/hashworld/' + filename, 'r', encoding='utf-8')
    data_dict = json.load(file)
    # print(data_dict)
    # print(type(data_dict))

    lands = Appium_hashworld_Test.lands()
    number = 0
    for item in data_dict['data']:
        number += 1
        phone = item.get('phone', 'NA')
        password = item.get('password', 'NA')
        data = dict(phone=phone, password=password)

        logger.warning('\n')
        logger.warning("========== Checking " + str(number) + ". [" + phone + "] ==========")

        # selenium login
        result = lands.selenium_login(phone, password)

        # normal login
        token = login_GetAccessToken(data)
        if token == -1 or result == -1:
            logger.warning('********** Login fail!')
            continue
        else:
            logger.warning('********** Login success! token:' + token)

            # 体力值
            strength = get_strength_info(token)

            # 土地列表
            wonder_list = get_prize_wheel(token)
            if wonder_list == -1 or strength == -1:
                continue

            click_hashworld_land(token, strength, wonder_list, lands)
            # break

            value = check_UserTotal(token)
            all_total = all_total + value
            logger.warning("========== End[" + phone + "], Total[ " + str(all_total) + " ] ==========")

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            content_data = {
                "phone": phone,
                "value": value
            }
            content_list.append(content_data)
            time.sleep(random.randint(MIN_SEC, MAX_SEC))
            # break
            lands.selenium_close()
    lands.selenium_quit()

    # sending email
    server = filename.split('.')[0][-5:]
    send_email.send_HashWorld_HtmlEmail('newseeing@163.com', content_list, server)
    logger.warning('********** Sending Email Complete!')
    logger.warning('\n')


def loop_Land():
    content_land_list = []

    data = dict(phone="+8614716980512", password="Liuxb0504")

    token = login_GetAccessToken(data)
    if token == -1:
        logger.warning('********** Login fail!')
    else:
        logger.warning('********** Login success! token:' + token)

        # find land list and price
        land_list = get_Landlist(token)
        for i in range(len(land_list)):
            land_Num = land_list[i][0]
            (land_name, price, tradable_status, gen_time, nickname) = get_LandPrice(token, land_Num)
            logger.warning(
                '********** Land_Num:' + str(land_Num) + ", Land_Name:" + land_name + ", Price = " + str(price))

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            land_data = {
                "land_num": land_Num,
                "land_name": land_name,
                "price": price,
                "tradable_status": tradable_status,
                "gen_time": gen_time,
                "nickname": nickname
            }
            content_land_list.append(land_data)
            # if i == 2:
            #     break

        # sending email
        # content_land_list = sorted(content_land_list, key=lambda x: x["price"])
        content_land_list = sorted(content_land_list, key=lambda x: (x["tradable_status"], x["price"]))
        send_email.send_HashWorld_LandEmail('newseeing@163.com', content_land_list)
        logger.warning('********** Sending Land Email Complete!')
        logger.warning('\n')


def loop_hashworld_land():
    # start
    logger.warning('********** Start from loop_hashworld_land() ...')

    global proxies
    # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
    proxies = ''

    status_code = open_FirstPage()
    while status_code != 200:
        time.sleep(120)
        status_code = open_FirstPage()
    loop_Land()


def loop_hashworld_no_land(filename):
    # start
    logger.warning('********** Start from loop_hashworld_no_land() ...')

    global proxies
    # proxies = daxiang_proxy.get_proxy("https://game.hashworld.top/")
    proxies = ''

    status_code = open_FirstPage()
    while status_code != 200:
        time.sleep(120)
        status_code = open_FirstPage()
    loop_Lottery(filename)


# Start from here...
# loop_hashworld_no_land('data_hashworld_Tokyo.json')

# schedule.every(120).minutes.do(loop_hashworld_land)
# schedule.every(8).hours.do(loop_hashworld_land)
# schedule.every().day.at("18:30").do(loop_hashworld_land)
# schedule.every().monday.do(loop_hashworld_land)
# schedule.every().wednesday.at("13:15").do(loop_hashworld_land)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

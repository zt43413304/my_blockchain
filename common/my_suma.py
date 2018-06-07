# coding=utf-8

import logging
import time

import requests

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_suma.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/suma.log', mode='w')
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


class suma:
    headers = {
        'accept': "*/*",
        'connection': "Keep-Alive",
        'Content-Type': "text/html;charset=UTF-8",
        'user-agent': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)",
        'Cache-Control': "no-cache"
    }

    token = ''

    def login(self):
        global token

        url = "http://api.eobzz.com/httpApi.do"

        querystring = {"action": "loginIn", "uid": "newseeing", "pwd": "Liuxb0504$"}

        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=60)
            result = response.text
            token = result.split('|')[1]
            logger.warning("********** token = " + token)
            # return token
        except Exception as e:
            print(e)

    def getMobilenum(self):
        if self.token is '':
            self.login()

        url = "http://api.eobzz.com/httpApi.do"

        querystring = {"action": "getMobilenum", "uid": "newseeing", "token": token, "pid": "43795", "mobile": "",
                       "size": "1"}

        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=60)
            result = response.text
            phone = result.split('|')[0]
            logger.warning(">>>>>>>>>> phone = " + phone)
            return phone
        except Exception as e:
            print(e)

    def getVcodeAndHoldMobilenum(self, phone):
        if self.token is '':
            self.login()

        url = "http://api.eobzz.com/httpApi.do"

        querystring = {"action": "getVcodeAndHoldMobilenum", "uid": "newseeing", "token": token, "pid": "43795",
                       "next_pid": "43795", "mobile": phone, "author_uid": "newseeing"}

        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=120)
            result = response.text
            logger.warning(">>>>>>>>>> response.text = " + result)
            code = self.get_sms_code(result)

            count = 0
            while code == -1:
                if count > 24:
                    break
                # logger.warning("********** Waiting for sms......")
                time.sleep(5)
                response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=120)
                result = response.text
                logger.warning(">>>>>>>>>> response.text = " + result)
                code = self.get_sms_code(result)
                count += 1

            if code != -1:
                return code
            else:
                return -1
        except Exception as e:
            print(e)


    def get_sms_code(self, sms):
        # 【币响App】您的验证码为3088，请于3内正确输入，如非本人操作，请忽略此短信。
        str1 = sms
        str2 = '为'
        nPos = str1.find(str2)
        # print(nPos)
        if nPos > -1:
            # print(str1[nPos+1:nPos+5])
            return str1[nPos+1:nPos+5]
        else:
            return nPos


    # str_a = "重新发送(59)"
    # if '重新发送' in str_a:
    #     print('Exist')
    # else:
    #     print('Not exist')

# get_sms_code('【币响App】您的验证码为3088，请于3内正确输入，如非本人操作，请忽略此短信。')

# suma = suma()
# suma.getMobilenum()
# suma.getVcodeAndHoldMobilenum('15873864640')

# print(get_sms_code('【币响App】您的验证码为3088，请于3内正确输入，如非本人操作，请忽略此短信'))

# -*- coding: utf-8 -*-

import logging
import time
from urllib import request

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_51ym.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_51ym.log', mode='w')
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


class ym:
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

    ITEMID = '14616'  # 项目id
    token = ''
    phone = ''
    sms = ''

    def __init__(self):
        global token

        # 登陆/获取TOKEN
        username = 'newseeing'  # 账号
        password = 'Liuxb0504'  # 密码
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username=' + \
              username + '&password=' + password

        TOKEN1 = request.urlopen(request.Request(
            url=url, headers=self.header_dict)).read().decode(encoding='utf-8')

        if TOKEN1.split('|')[0] == 'success':
            token = TOKEN1.split('|')[1]
            logger.warning("********** token = " + token)
        else:
            logger.warning(
                '获取TOKEN错误,错误代码' + TOKEN1 + '。代码释义：1001:参数token不能为空;1002:参数action不能为空;1003:参数action错误;1004:token失效;1005:用户名或密码错误;1006:用户名不能为空;1007:密码不能为空;1008:账户余额不足;1009:账户被禁用;1010:参数错误;1011:账户待审核;1012:登录数达到上限')

    # 获取账户信息
    def get_userinfo(self):

        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=' + token + '&format=1'
        ACCOUNT1 = request.urlopen(request.Request(
            url=url, headers=self.header_dict)).read().decode(encoding='utf-8')
        if ACCOUNT1.split('|')[0] == 'success':
            ACCOUNT = ACCOUNT1.split('|')[1]
            logger.warning(ACCOUNT)
        else:
            logger.warning('获取TOKEN错误,错误代码' + ACCOUNT1)

    # 获取手机号码
    def get_phoneNumber(self):
        global token
        # global phone

        EXCLUDENO = ''  # 排除号段170_171
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + \
              token + '&itemid=' + self.ITEMID + '&excludeno=' + EXCLUDENO
        MOBILE1 = request.urlopen(request.Request(
            url=url, headers=self.header_dict)).read().decode(encoding='utf-8')
        if MOBILE1.split('|')[0] == 'success':
            self.phone = MOBILE1.split('|')[1]
            logger.warning('获取号码是: ' + self.phone)
            return self.phone
        else:
            logger.warning('获取TOKEN错误,错误代码' + MOBILE1)
            return -1

    # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
    def get_sms(self):
        global token
        # global phone

        WAIT = 150  # 接受短信时长60s
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=' + \
              token + '&itemid=' + self.ITEMID + '&mobile=' + self.phone + '&release=1'

        text1 = request.urlopen(request.Request(
            url=url, headers=self.header_dict)).read().decode(encoding='utf-8')
        logger.warning(">>>>>>>>>> response.text = " + text1)

        TIME1 = time.time()
        TIME2 = time.time()
        ROUND = 1
        while (TIME2 - TIME1) < WAIT and not text1.split('|')[0] == "success":
            time.sleep(5)
            text1 = request.urlopen(request.Request(
                url=url, headers=self.header_dict)).read().decode(encoding='utf-8')
            logger.warning(">>>>>>>>>> response.text = " + text1)
            TIME2 = time.time()
            ROUND = ROUND + 1

        ROUND = str(ROUND)
        if text1.split('|')[0] == "success":
            text = text1.split('|')[1]
            TIME = str(round(TIME2 - TIME1, 1))
            logger.warning('********** ' + text + '\n耗费时长' + TIME + 's,循环数是' + ROUND)

            # 提取短信内容中的数字验证码
            return self.get_sms_code(text)
        else:
            logger.warning('获取短信超时，错误代码是' + text1 + ',循环数是' + ROUND)
            self.block_phoneNumber()
            return -1

    # 拉黑
    def block_phoneNumber(self):
        global token
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=' + \
              token + '&itemid=' + self.ITEMID + '&mobile=' + self.phone
        RELEASE = request.urlopen(request.Request(
            url=url, headers=self.header_dict)).read().decode(encoding='utf-8')
        logger.warning('拉黑号码:' + RELEASE)

    # 释放号码
    def release_phoneNumber(self):
        global token
        # global phone

        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + \
              token + '&itemid=' + self.ITEMID + '&mobile=' + self.phone
        RELEASE = request.urlopen(request.Request(
            url=url, headers=self.header_dict)).read().decode(encoding='utf-8')
        logger.warning('释放号码:' + RELEASE)

    def get_sms_code(self, sms):
        # 【币响App】您的验证码为3088，请于3内正确输入，如非本人操作，请忽略此短信。
        str1 = sms
        str2 = '为'
        nPos = str1.find(str2)
        # print(nPos)
        if nPos > -1:
            # print(str1[nPos+1:nPos+5])
            return str1[nPos + 1:nPos + 5]
        else:
            return nPos

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

# coding=utf-8

import logging
import os
import subprocess
import time

from bixiang import Appium_bixiang
# 第一步，创建一个logger,并设置级别
from common import my_51ym

logger = logging.getLogger("bixiang_signup.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang_signup.log', mode='w')
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

# Random seconds
MIN_SEC = 1
MAX_SEC = 3


def execute_command(cmd):
    print('***** start executing cmd...')
    p = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderrinfo, stdoutinfo = p.communicate()
    for line in stdoutinfo.splitlines():
        print(line)

        # print('stderrinfo is -------> %s and stdoutinfo is -------> %s' % (stderrinfo, stdoutinfo))
    print('stdoutinfo is -------> %s' % stdoutinfo)
    print('stderrinfo is -------> %s' % stderrinfo)
    print('finish executing cmd....')
    return p.returncode


def startup_emulator():
    output = os.system("/Applications/NemuPlayer.app")
    logger.warning(">>>>>>>>>> Start NemuPlayer.app, output = " + str(output))
    time.sleep(15)
    # cmd_adb = r'adb connect 127.0.0.1:7555'
    # result1 = execute_command(cmd_adb)
    # print('result:------>', result1)
    # cmd_adb1 = r'adb devices -l'
    # result2 = execute_command(cmd_adb1)
    # print('result:------>', result2)

    output = os.system(
        "node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4723")
    print('result:------>' + str(output))
    time.sleep(5)


def signup_html():
    pass
    # App_signup = Appium_bixiang.Signup('4.4.4', '127.0.0.1:7555', 4723)
    # App_signup.html_signup()
    # send_email.send_star163_HtmlEmail('newseeing@163.com', '136获取原力完成.', '')
    # logger.warning('********** Sending 136获取原力完成 Email Complete!')


def signup_app():
    pass
    # App_signup = Appium_bixiang.Signup('4.4.4', '127.0.0.1:7555', 4723)
    # App_signup.registry()
    # send_email.send_star163_HtmlEmail('newseeing@163.com', '136获取原力完成.', '')
    # logger.warning('********** Sending 136获取原力完成 Email Complete!')


# Star from here......

# 自动“币响知识小课堂”
# quiz_url = input("********** Quiz url is: ")
# signup = Appium_bixiang.Signup()
# signup.quiz_by_html(quiz_url)
# sys.exit(0)


# startup_emulator()
# 注意：邀请链接要再三确认
url01 = 'http://bixiang8.com/8P7nA1'
url02 = 'http://bixiang8.com/dz5vU'
url03 = 'http://bixiang8.com/yW5rX'
url04 = 'http://bixiang8.com/55hym'
url05 = 'http://bixiang8.com/exTI83'
url06 = 'http://bixiang8.com/7g4C32'
# 下无层级
url07 = 'http://bixiang8.com/uTxq13'
url08 = 'http://bixiang8.com/PgU0a2'
url09 = 'http://bixiang8.com/4HbUg4'
url10 = 'http://bixiang8.com/vXoPR1'

invite_url = url06
phone = input("********** Phone Number (enter for new): ")
logger.warning('********** Your input is: ' + phone)
ym = my_51ym.ym()

try:
    if phone is '':
        ym.get_phoneNumber()
    else:
        ym.set_phone(phone)

    signup = Appium_bixiang.Signup()

    # result = 0
    result = signup.html_signup(ym, invite_url)

    if result == 0:
        result = signup.app_signup(ym)

    if result == 0:
        # 手工“币响知识小课堂”
        quiz_url = input("********** Quiz url is: ")
        signup.quiz_by_html(quiz_url)


except Exception as e:
    print(e)

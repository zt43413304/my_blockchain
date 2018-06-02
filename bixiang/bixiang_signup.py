# coding=utf-8

import logging
import os
import subprocess
import time

from bixiang import Appium_bixiang

# 第一步，创建一个logger,并设置级别
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


# startup_emulator()
# HTML_signup = Appium_bixiang.Signup()
# HTML_signup.html_signup()

APP_signup = Appium_bixiang.Signup('4.4.4')
APP_signup.app_signup()

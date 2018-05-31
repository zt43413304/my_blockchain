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


def signup():
    # cmd_clean = r'cmd.exe C:/DevTools/my_blockchain/star163/clean.bat'
    # result1 = execute_command(cmd_clean)
    # print('result:------>', result1)

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
    time.sleep(15)

    # python执行直接用【os.system(要执行的命令)】即可，如果是windows下\n和\a需要转义，所以用下面的内容
    # cmd_app_desktop = r'start /b node C:\Users\Jackie.Liu\AppData\Local\appium-desktop\app-1.6.0\resources\app\node_modules\appium\build\lib\main.js'
    # cmd_appium = r'start /b node C:\DevTools\Appium\node_modules\appium\lib\server\main.js --address 127.0.0.1 --port 4723'
    # result3 = execute_command(cmd_app_desktop)
    # 需要手动确定启动Server
    # output3 = os.system("C:/Users/Jackie.Liu/AppData/Local/appium-desktop/Appium.exe -a 127.0.0.1 -p 4723")

    App_signup = Appium_bixiang.Signup('4.4.4', '127.0.0.1:7555', 4723)
    App_signup.registry()
    # send_email.send_star163_HtmlEmail('newseeing@163.com', '136获取原力完成.', '')
    # logger.warning('********** Sending 136获取原力完成 Email Complete!')

signup()
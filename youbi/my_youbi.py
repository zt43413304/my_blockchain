# coding=utf-8

import datetime
import logging
import os
import subprocess
import sys
import time

import AppiumStarYoubi
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

sys.path.append('..')
import common.Send_email

# 日志
# 第一步，创建一个logger
logger = logging.getLogger("my_youbi.py")
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'youbi.log'
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

# logger.removeHandler(ch)
# logger.removeHandler(fh)
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')


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

def appium_calculate136():

    output = os.system("C:/DevTools/MuMu/emulator/nemu/EmulatorShell/NemuPlayer.exe")
    logging.warning(">>>>>>>>>> Start NemuPlayer.exe, output = " + str(output))
    time.sleep(15)
    cmd_adb = r'adb connect 127.0.0.1:7555'
    result1 = execute_command(cmd_adb)
    print('result:------>', result1)
    cmd_adb1 = r'adb devices -l'
    result2 = execute_command(cmd_adb1)
    print('result:------>', result2)

    output3 = os.system(
        "start node C:/Users/Jackie.Liu/AppData/Local/appium-desktop/app-1.6.1/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4723")
    # output3 = os.system(
    # "start /b node C:/Users/jacki/AppData/Local/appium-desktop/app-1.6.1/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4723")
    print('result:------>' + str(output3))
    time.sleep(10)

    appium = AppiumStarYoubi.AppiumStar('4.4.4', '127.0.0.1:7555', 4723)
    appium.appium_youbi()
    # common.Send_email.send_163HtmlEmail('newseeing@163.com', '136获取原力完成.', '')
    logging.warning('********** Check youbi in NemuPlayer complete!')

def appium_calculate138():

    output = os.system("C:/DevTools/Nox/Nox/bin/Nox.exe")
    logging.warning("========== Start Nox.exe, output = " + str(output))
    time.sleep(15)

    cmd_adb = r'adb connect 127.0.0.1:62001'
    result1 = execute_command(cmd_adb)
    print('result:------>', result1)
    cmd_adb1 = r'adb devices -l'
    result2 = execute_command(cmd_adb1)
    print('result:------>', result2)

    output3 = os.system(
        "start node C:/Users/Jackie.Liu/AppData/Local/appium-desktop/app-1.6.1/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4725")
    # output3 = os.system(
    #     "start /b node C:/Users/jacki/AppData/Local/appium-desktop/app-1.6.1/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4725")
    print('result:------>' + str(output3))
    time.sleep(10)

    appium = AppiumStarYoubi.AppiumStar('4.4.2', '127.0.0.1:62001', 4725)
    appium.appium_youbi()

    # common.Send_email.send_163HtmlEmail('newseeing@163.com', '138获取原力完成.', '')
    logging.warning('********** Check youbi in Nox complete!')

def test136():
    print("now 136 is '%s' " % datetime.datetime.now())
    return

def test138():
    print("now 138 is '%s' " % datetime.datetime.now())
    return

# start
logging.warning('***** Start ...')
scheduler = BlockingScheduler()
# scheduler = BackgroundScheduler()

# @scheduler.scheduled_job("cron", second="*/3")
# scheduler.add_job(test136, "cron", second="0, 30")
# scheduler.add_job(test138, "cron", second="0, 30")

# scheduler.add_job(appium_calculate136, "cron", second="0, 30", max_instances=2)
# scheduler.add_job(appium_calculate138, "cron", second="0, 30", max_instances=2)

scheduler.add_job(appium_calculate136, "cron", minute="*/5", max_instances=2)
scheduler.add_job(appium_calculate138, "cron", minute="*/5", max_instances=2)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

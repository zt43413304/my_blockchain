# coding=utf-8

import datetime
import logging
import os
import subprocess
import sys
import time
from test import testing
from bixiang import my_bixiang
from common import Send_email
from diwuqu import my_diwuqu
from hashworld import HashWorldCheck
from hashworld import HashWorldLand
from onechain import OneChainCheck
from star163 import my_star163
from youbi import my_youbi

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

sys.path.append('..')
import common.Send_email

# 日志
# 第一步，创建一个logger
logger = logging.getLogger("start_all.py")
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'start_all.log'
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




# start
logging.warning('***** Start from start_all.py ...')
scheduler = BlockingScheduler()
# scheduler = BackgroundScheduler()

# @scheduler.scheduled_job("cron", second="*/3")
# scheduler.add_job(testing.test136, "cron", second="30")
# scheduler.add_job(testing.test138, "cron", second="30")

# scheduler.add_job(appium_calculate136, "cron", minute="*/5", max_instances=2)
# scheduler.add_job(appium_calculate138, "cron", minute="*/3", max_instances=2)

scheduler.add_job(my_bixiang.loop_bixiang, "cron", hour="1, 11", max_instances=1)

scheduler.add_job(OneChainCheck.loop_data_mining, "cron", hour="3, 13", max_instances=1)


scheduler.add_job(HashWorldCheck.daily_job(), "cron", hour="5, 15", max_instances=1)
scheduler.add_job(HashWorldLand.loop_Land, "cron", hour="*/2", max_instances=1)

scheduler.add_job(my_diwuqu.loop_diwuqu, "cron", hour="7, 17", max_instances=1)


# scheduler.add_job(my_star163.loop_star163, "cron", minute="0,5,30,35", hour="8-23", max_instances=2)
# scheduler.add_job(my_youbi., "cron", minute="0,5,30,35", hour="8-23", max_instances=2)


try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

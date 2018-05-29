# coding=utf-8

import logging
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from hashworld import HashWorldCheck
from star163 import my_star163

# 第一步，创建一个logger
logger = logging.getLogger("start_lenovo.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_lenovo_' + rq + '.log'
logfile = log_name

fh = logging.FileHandler(logfile, mode='w', encoding='UTF-8')
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

# start
logger.warning('********** Start from start_lenovo.py ...')
scheduler = BlockingScheduler()

# Tokyo Sever
# scheduler.add_job(OneChainCheck.loop_onechain, "cron", hour="3,11,19", max_instances=1)
# scheduler.add_job(my_diwuqu.loop_diwuqu, "cron", hour="5,13,21", max_instances=1)
# scheduler.add_job(my_bixiang.loop_bixiang, "cron", hour="7,15,23", max_instances=1)

# Lenovo Sever
scheduler.add_job(HashWorldCheck.loop_hashworldcheck, "cron", hour="1,9,17", max_instances=1)
scheduler.add_job(my_star163.loop_star163, "cron", hour="6-23/2", max_instances=1)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

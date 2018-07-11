# coding=utf-8

import logging
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from hashworld import my_hashworld
from bixiang import bixiang_readnews


# 第一步，创建一个logger
from star163 import my_star163

logger = logging.getLogger("start_hp.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_hp' + rq + '.log'
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
logger.warning('********** Start from start_hp.py ...')
scheduler = BlockingScheduler()

# HP Sever
scheduler.add_job(bixiang_readnews.start_reading_news, "cron", hour="7,15,23", args=["data_bixiang_Seoul.json"], max_instances=4)
# scheduler.add_job(bixiang_readnews.start_reading_news, "cron", minute="0, 10, 20, 30, 40, 50",args=["data_bixiang_readnews_HP.json"], max_instances=4)

# scheduler.add_job(my_hashworld.loop_hashworld_no_land, "cron", hour="5,13,21", minute="30", args=["data_hashworld_Seoul.json"], max_instances=2)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

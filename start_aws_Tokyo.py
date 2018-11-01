# coding=utf-8

import logging
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from bixiang import bixiang_news_video
from bixiang import my_bixiang
from hashworld import my_hashworld

# 第一步，创建一个logger
logger = logging.getLogger("start_aws_Tokyo.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_aws_Tokyo_' + rq + '.log'
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
logger.warning('********** Start from start_aws_Tokyo.py ...')
scheduler = BlockingScheduler()

# Tokyo Server
scheduler.add_job(bixiang_news_video.start_news_video, "cron", hour="8",
                  args=["data_bixiang_Tokyo.json"], max_instances=6)

scheduler.add_job(my_bixiang.loop_elephant, "cron", hour="11",
                  args=["data_bixiang_Tokyo.json"], max_instances=6)

scheduler.add_job(my_hashworld.loop_hashworld_no_land, "cron", hour="0,16",
                  args=["data_hashworld_Tokyo.json"], max_instances=6)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

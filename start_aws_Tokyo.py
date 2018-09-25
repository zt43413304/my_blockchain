# coding=utf-8

import logging
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from bixiang import my_bixiang
from diwuqu import my_diwuqu

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

# Tokyo Sever
scheduler.add_job(my_bixiang.loop_bixiang, "cron", hour="6,14,22", args=["data_bixiang_Tokyo.json"], max_instances=4)
scheduler.add_job(my_diwuqu.loop_diwuqu, "cron", hour="4,12,20", max_instances=4)
# scheduler.add_job(my_onechain.loop_onechain, "cron", hour="5,13,21", minute="30", max_instances=4)


# scheduler.add_job(my_bixiang.loop_bixiang, "cron", minute="*/3", args=["data_bixiang_Tokyo.json"], max_instances=1)
# scheduler.add_job(my_hashworld.loop_hashworld_land, "cron", minute="*/3", args=["data_hashworld_Tokyo.json"], max_instances=1)
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

# coding=utf-8

import logging
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from hashworld import my_hashworld
from onechain import my_onechain
from star163 import my_star163
from bixiang import my_bixiang
from diwuqu import my_diwuqu

# 第一步，创建一个logger


logger = logging.getLogger("start_all_tmp.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_all_tmp_' + rq + '.log'
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
logger.warning('********** Start from start_all_tmp.py ...')
scheduler = BlockingScheduler()

# @scheduler.scheduled_job("cron", second="*/3")
# scheduler.add_job(testing1.test136, "cron", second="30")
# scheduler.add_job(testing2.test138, "cron", second="30")


my_bixiang.loop_bixiang("data_bixiang_Seoul.json")
# my_bixiang.loop_bixiang("data_bixiang_Tokyo.json")
# OneChainCheck.loop_onechain("data_hashworld_Seoul.json")
# OneChainCheck.loop_onechain("data_hashworld_Tokyo.json")
# my_diwuqu.loop_diwuqu()
# my_hashworld.loop_hashworld_land()
# my_star163.loop_star163()
# my_diwuqu.save_token()


# scheduler.add_job(my_bixiang.loop_bixiang, "cron", minute="*/3", max_instances=1)
# scheduler.add_job(OneChainCheck.loop_onechain, "cron", minute="*/3", max_instances=1)
# scheduler.add_job(my_diwuqu.loop_diwuqu, "cron", minute="*/3", max_instances=1)
# scheduler.add_job(HashWorldCheck.loop_hashworld_land, "cron", minute="*/3", max_instances=1)
# scheduler.add_job(HashWorldLand.loop_hashworldland, "cron", minute="*/3", max_instances=1)

# scheduler.add_job(my_bixiang.loop_bixiang, "cron", hour="1,9,17", max_instances=1)
# scheduler.add_job(OneChainCheck.loop_onechain, "cron", hour="3,11,19", max_instances=1)
# scheduler.add_job(my_diwuqu.loop_diwuqu, "cron", hour="5,13,21", max_instances=1)
# scheduler.add_job(HashWorldCheck.loop_hashworld_land, "cron", hour="7,15,23", max_instances=1)
# scheduler.add_job(HashWorldLand.loop_hashworldland, "cron", hour="8,12,16,20,0,4", max_instances=1)

# scheduler.add_job(my_star163.loop_star163, "cron", hour="0-10/2", max_instances=1)
# scheduler.add_job(my_star163.loop_star163_136, "cron", hour="0-10/2", max_instances=1)
# scheduler.add_job(my_star163.loop_star163_138, "cron", hour="0-10/2", max_instances=1)

# scheduler.add_job(my_youbi., "cron", minute="0,5,30,35", hour="8-23", max_instances=2)


# try:
#     scheduler.start()
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()

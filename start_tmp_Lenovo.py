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


logger = logging.getLogger("start_tmp_Lenovo.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_tmp_Lenovo' + rq + '.log'
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
logger.warning('********** Start from start_tmp_Lenovo.py ...')



# my_bixiang.loop_bixiang("data_bixiang_Tokyo.json")
# my_bixiang.loop_bixiang("data_bixiang_Seoul.json")

my_hashworld.loop_hashworld_no_land("data_hashworld_Tokyo.json")
# my_hashworld.loop_hashworld_no_land("data_hashworld_Seoul.json")





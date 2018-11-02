# coding=utf-8

import logging
import os
import subprocess
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from bixiang import bixiang_news_video
from bixiang import my_bixiang
from hashworld import my_hashworld

# 第一步，创建一个logger
logger = logging.getLogger("start_Aliyun.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_Aliyun_' + rq + '.log'
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


def execute_command(cmd):
    print('***** start executing cmd...')
    p = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderrinfo, stdoutinfo = p.communicate()
    # for line in stdoutinfo.splitlines():
    #     print(line)
    #
    # print('stdoutinfo is -------> %s' % stdoutinfo)
    # print('stderrinfo is -------> %s' % stderrinfo)
    # print('finish executing cmd....')
    return p.returncode

# start
logger.warning('********** Start from start_Aliyun.py ...')

cmd = r'del *.log'
result1 = execute_command(cmd)
print('result:------>', result1)
time.sleep(1)

cmd = r'del logs\*.log'
result2 = execute_command(cmd)
print('result:------>', result2)

scheduler = BlockingScheduler()

# Server
scheduler.add_job(bixiang_news_video.start_news_video, "cron", hour="8",
                  args=["data_bixiang_Aliyun.json"], max_instances=6)

scheduler.add_job(my_bixiang.loop_elephant, "cron", hour="10", minitue="30",
                  args=["data_bixiang_Aliyun.json"], max_instances=6)

scheduler.add_job(my_hashworld.loop_hashworld_no_land, "cron", hour="0,16",
                  args=["data_hashworld_Aliyun.json"], max_instances=6)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

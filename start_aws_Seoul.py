# coding=utf-8

import logging
import os
import time
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

from bixiang import my_bixiang
from blockcity import my_blockcity
from diwuqu import my_diwuqu
from star163 import my_star163
from epayapp import my_epay

# 第一步，创建一个logger
logger = logging.getLogger("start_aws_Seoul.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + 'start_aws_Seoul_' + rq + '.log'
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


cmd = r'del *.log'
result1 = execute_command(cmd)
print('result:------>', result1)
time.sleep(1)

cmd = r'del logs\*.log'
result2 = execute_command(cmd)
print('result:------>', result2)


# start
logger.warning('********** Start from start_aws__Seoul.py ...')
scheduler = BlockingScheduler()

# E-Pay
# scheduler.add_job(my_epay.loop_epay, "cron", hour="0,4,6", minute="20",
#                   args=["my_epay_data__Seoul.json"], max_instances=6)

# Seoul Sever
scheduler.add_job(my_bixiang.loop_bixiang, "cron", hour="8,16", minute="30", args=["data_bixiang_Aliyun.json"], max_instances=6)
scheduler.add_job(my_bixiang.loop_bixiang, "cron", hour="12,20", minute="30", args=["data_bixiang__Seoul.json"], max_instances=6)

scheduler.add_job(my_blockcity.loop_blockcity, "cron", hour="8,12,16,20", max_instances=6)
scheduler.add_job(my_star163.loop_star163, "cron", hour="8,12,16,20", minute="15", max_instances=6)

# scheduler.add_job(my_diwuqu.loop_diwuqu, "cron", hour="11,19", minute="30", max_instances=6)
# scheduler.add_job(my_hashworld.loop_hashworld_land, "cron", hour="2", max_instances=6)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

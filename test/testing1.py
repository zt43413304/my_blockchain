import datetime
import logging
import os
import subprocess
import sys
import time


# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("testing1.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('logs/testing1.log', mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)



def test136():
    logger.info("in info 136 is '%s' " % datetime.datetime.now())
    logger.warning("in warning 136 is '%s' " % datetime.datetime.now())
    return


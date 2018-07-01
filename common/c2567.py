import logging
import sys

import requests

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("c2567.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/c2567.log', mode='w')
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


def get_captcha(gt, challenge):
    url = "http://jiyanapi.c2567.com/shibie?gt=" + gt + \
          "&challenge=" + challenge + \
          "&referer=http://tui.yingshe.com" \
          "&user=jackielg" \
          "&pass=Liuxb0504$" \
          "&return=json" \
          "&model=3" \
          "&format=utf8"

    try:
        response = requests.get(url)
        # proxy_ip = response.text
        res = response.json()["status"]
        if res == "stop":
            logger.warning(">>>>>>>>>> get captcha stop.")
            sys.exit(0)

        if res == "ok":
            challenge = response.json()["challenge"]
            validate = response.json()["validate"]
            logger.warning(">>>>>>>>>> get captcha success.")
            return challenge, validate
        else:
            logger.warning(">>>>>>>>>> get captcha error.")
            return -1, -1

    except Exception as e:
        print(e)
        return -1, -1

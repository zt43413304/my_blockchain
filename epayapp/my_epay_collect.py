# coding=utf-8

import json
import logging
import os
import re
import time

from epayapp import my_epay_collect_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_epay_collect.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_epay_collect.log', mode='w')
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

try:

    epay_collect = my_epay_collect_class.Collect()

    # get config information
    curpath = os.getcwd()
    content = open(curpath + '/epayapp/my_epay_data.json').read()
    content = re.sub(r"\xfe\xff", "", content)
    content = re.sub(r"\xff\xfe", "", content)
    content = re.sub(r"\xef\xbb\xbf", "", content)
    open(curpath + '/epayapp/my_epay_data.json', 'w').write(content)

    file = open(curpath + '/epayapp/my_epay_data.json', 'r', encoding='utf-8')
    data_dict = json.load(file)
    content_list = []

    # determine info number
    for item in data_dict['data']:
        sum_data = {}

        account_id = item.get('account_id', 'NA')
        result = epay_collect.app_login(account_id)
        sum_data['id'] = account_id

        income_amount = epay_collect.app_income()
        sum_data['income'] = round(income_amount, 2)

        result = epay_collect.app_transfer(account_id)

        rev_amount = epay_collect.app_revenue()
        sum_data['revenue'] = round(rev_amount, 2)

        content_list.append(sum_data)

        result = epay_collect.app_logout()
        time.sleep(3)

    for item in content_list:
        print(item)


except Exception as e:
    print(e)

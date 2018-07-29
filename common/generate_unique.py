# coding=utf-8

import json
import logging
import os

import random

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("generate_unique.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/generate_unique.log', mode='w')
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

# get config information
curpath = os.getcwd()


# content = open(curpath + '/bixiang/config_diwuqu.ini').read()
# content = re.sub(r"\xfe\xff", "", content)
# content = re.sub(r"\xff\xfe", "", content)
# content = re.sub(r"\xef\xbb\xbf", "", content)
# open(curpath + '/diwuqu/config_diwuqu.ini', 'w').write(content)

def save_unique():
    # file = open('data_diwuqu.json', 'r', encoding='utf-8')
    # data_dict = json.load(file)

    # Reading data
    with open(curpath + '/bixiang/data_bixiang_new_user.json', 'r') as file:
        data_dict = json.load(file)

    for item in data_dict['data']:
        # unique = item.get('unique', 'NA')
        # logger.warning("========== Checking [" + phone + "] ==========")
        unique = ''.join(str(random.choice(range(10))) for _ in range(15))
        print(unique)
        item['unique'] = unique

    # Writing JSON data
    with open(curpath + '/bixiang/data_bixiang_new_user.json', 'w') as file_new:
        json.dump(data_dict, file_new)

    file_new.close()
    file.close()


save_unique()

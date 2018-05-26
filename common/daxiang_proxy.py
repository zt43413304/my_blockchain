import logging

import requests

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("daxiang_proxy.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/daxiang_proxy.log', mode='w')
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


def get_proxy():
    url = 'http://tvp.daxiangdaili.com/ip/?tid=559810758325225&num=1&delay=1&category=2&protocol=https&filter=on&sortby=speed'

    try:
        response = requests.get(url)
        proxy = response.text
        logger.warning(">>>>>>>>>> Get proxy = " + proxy)
        return proxy
    except Exception as e:
        print(e)
        logger.warning(">>>>>>>>>> Get proxy error!")
        return -1


def test_ip(proxy):
    # url = 'http://ip.chinaz.com/getip.aspx'
    url = 'https://www.baidu.com'

    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        result = response.text
        logger.warning(">>>>>>>>>> Test proxy = " + result)
    except Exception as e:
        print(e)
        logger.warning(">>>>>>>>>> Test proxy error!")


# proxy = get_proxy()
proxy = '117.36.103.170:8118'
if proxy != -1:
    test_ip(proxy)

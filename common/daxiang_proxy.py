import logging
import time

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


def get_proxyIP():
    url = 'http://tvp.daxiangdaili.com/ip/?tid=559810758325225&num=1&delay=1&category=2&protocol=https&filter=on&sortby=speed'

    try:
        response = requests.get(url)
        proxy_ip = response.text

        # ERROR|没有找到符合条件的IP
        nPos = proxy_ip.find('ERROR')
        if nPos > -1:
            logger.warning(">>>>>>>>>> Get proxy ip = " + proxy_ip)
            proxy_ip = ''
            logger.warning(">>>>>>>>>> Return proxy_ip = " + proxy_ip)
        else:
            return proxy_ip
    except Exception as e:
        print(e)
        logger.warning(">>>>>>>>>> Get proxy ip error, sleep 5 seconds...")
        logger.warning(">>>>>>>>>> Zzzzzzzzzzzzzzzz...")
        time.sleep(5)

        try:
            response = requests.get(url)
            proxy_ip = response.text

            if proxy_ip is None or proxy_ip is '':
                return ''
            else:
                return proxy_ip
        except Exception as f:
            print(f)
            return ''

def test_ip(url, proxy_ip):
    # url = 'http://ip.chinaz.com/getip.aspx'
    # url = 'https://www.baidu.com'
    # url = "https://game.hashworld.top/"
    # url = 'https://www.whatismyip.com/'

    proxies = {
        # 'http': 'http://' + proxy_ip,
        'https': 'https://' + proxy_ip
    }

    # proxies = {'http': 'http://182.113.169.222:36269', 'https': 'https://182.113.169.222:36269'}
    # requests.get('http://example.org', proxies=proxies, timeout=10)

    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        result = response.status_code
        logger.warning(">>>>>>>>>> Test url = " + url)
        logger.warning(">>>>>>>>>> Test proxies = " + str(proxies))
        logger.warning(">>>>>>>>>> Test proxies result = " + str(result))
        if result == 200:
            return proxies
        else:
            return ''
    except Exception as e:
        print(e)
        logger.warning(">>>>>>>>>> Test proxies error!")
        return ''


def get_proxy(url):
    proxies = ''
    count = 0
    while proxies == '':
        if count > 1:
            break
        proxy_ip = get_proxyIP()
        proxies = test_ip(url, proxy_ip)
        count += 1
    return proxies

# get_proxy("https://game.hashworld.top/")

# coding=utf-8

import logging

import requests

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_onechain_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_onechain_class.log', mode='w')
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


class trade_class:
    headers = {
        'User-Agent': "okhttp/3.5.0",
        'Host': "hkopenservice1.yuyin365.com:8000",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip',
        'Cache-Control': "no-cache"
    }

    proxies = ''
    data = None

    def __init__(self, data):
        # logger.warning("start __init__...")
        self.data = data

    def loginGetAccessToken(self):
        # global proxies
        global data
        url_login = 'http://hkopenservice1.yuyin365.com:8000/one-chain/login?user_agent=' + self.data['user_agent'] + \
                    '&device_id=' + self.data['device_id'] + '&l=' + self.data['l'] + '&token=&version=' + self.data[
                        'version']
        login_data = dict(account_id=self.data['account_id'], account_name=self.data['account_name'],
                          signed_message=self.data['signed_message'])

        try:
            # logger.warning("********** loginGetAccessToken(), proxies = " + str(proxies))
            requests.packages.urllib3.disable_warnings()
            # r = requests.post(url_login, data=self.data, headers=self.headers, proxies=self.proxies, timeout=60)
            r = requests.post(url_login, data=login_data, headers=self.headers, timeout=60)

            # if bProxy == 0:
            #     r = requests.post(url_login, headers=headers, verify=False) #headers=headers,
            # else:
            #     r = requests.post(url_login, headers=headers, proxies=proxies, verify=False) #headers=headers,

            res = r.json()["msg"]
            if res == 'Success':
                token = r.json()["data"]["map"]["token"]
                logger.warning("********** Login success, " + self.data['account_name'])
                return token
            else:
                return -1
        except Exception as e:
            print(e)
            # proxies = daxiang_proxy.get_proxy("http://hkopenservice1.yuyin365.com:8000/one-chain/login")
            return -1


def get_depth():
    pass
    # p2_currencies = ['eth'] # 用usdt同时买进、卖出ft
    # p1_currencies = ['usdt']
    # urls[p2_currencies[i] + p1_currencies[j]] = "https://api.fcoin.com/v2/market/depth/L20/" + p2_currencies[i] + p1_currencies[j] # 获取深度的api地址
    # req = urllib.request.Request(urls[[p2_currencies[i] + p1_currencies[j]])
    # res=urllib.request.urlopen(req, timeout=FETCH_DEPTH_TIMEOUT)
    # json_res=json.loads(res.read().decode("utf-8"))
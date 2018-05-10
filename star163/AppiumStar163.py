# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import logging
import os
import time

from appium import webdriver
# Returns abs path relative to this file and not cwd
from appium.webdriver.common.touch_action import TouchAction

# 日志
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'star163_appium.log'
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

ch.setFormatter(formatter)
logger.addHandler(ch)

logger.removeHandler(ch)
logger.removeHandler(fh)
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class AppiumStar:

    def __init__(self):
        print("start __init__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'Android'
        desired_caps['noReset'] = 'True'
        desired_caps['app'] = PATH(
            'C:/DevTools/Star163/blockchain112_163-e01170001.apk'
        )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def isElementExist(self, id):
        try:
            self.driver.find_element_by_accessibility_id(id)
            return True
        except Exception as e:
            print(e)
            return False

    def appium_calculate(self):
        # level 1 main page
        logging.warning(">>>>>>>>>> Start from level 1 main page ...")
        time.sleep(5)
        self.driver.find_element_by_accessibility_id("获取原力").click()
        logging.warning(">>>>>>>>>> Level 2, 获取原力")
        time.sleep(15)

        # level 2 main page
        self.driver.find_element_by_accessibility_id("资讯").click()
        logging.warning(">>>>>>>>>> 资讯")
        time.sleep(15)
        if self.isElementExist("立即阅读"):
            self.driver.find_element_by_accessibility_id("立即阅读").click()
            time.sleep(5)

        # channel "区块链"
        self.driver.find_element_by_accessibility_id("区块链").click()
        logging.warning(">>>>>>>>>> 区块链")
        time.sleep(15)

        # Article 1
        TouchAction(self.driver).tap(x=600, y=300).perform()
        logging.warning(">>>>>>>>>> Article 1")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # Article 2
        TouchAction(self.driver).tap(x=600, y=600).perform()
        logging.warning(">>>>>>>>>> Article 2")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # Article 3
        TouchAction(self.driver).tap(x=600, y=900).perform()
        logging.warning(">>>>>>>>>> Article 3")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # Article 4
        TouchAction(self.driver).tap(x=600, y=1200).perform()
        logging.warning(">>>>>>>>>> Article 4")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # level 2 main page
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        logging.warning(">>>>>>>>>> Back to Level 2, 获取原力")
        time.sleep(15)

        # Music
        self.driver.find_element_by_accessibility_id("网易云音乐").click()
        logging.warning(">>>>>>>>>> 网易云音乐")
        time.sleep(15)
        if self.isElementExist("立即收听"):
            self.driver.find_element_by_accessibility_id("立即收听").click()

        # level 2 main page
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        logging.warning(">>>>>>>>>> Back to Level 2, 获取原力")
        time.sleep(15)

        # level 1 main page
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        logging.warning(">>>>>>>>>> Back to level 1 ...")
        time.sleep(15)

# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import logging
import os
import time

from appium import webdriver
# Returns abs path relative to this file and not cwd
from appium.webdriver.common.touch_action import TouchAction

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_star163.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_star163.log', mode='w')
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

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class AppiumStar:

    def __init__(self, version, deviceName, port):
        print("start __init__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = deviceName
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['app'] = PATH(
            'C:/DevTools/Star163/blockchain112_163-e01170001.apk'
        )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'
        self.driver = webdriver.Remote('http://localhost:' + str(port) + '/wd/hub', desired_caps)

    def isElementExist(self, id):
        try:
            self.driver.find_element_by_accessibility_id(id)
            return True
        except Exception as e:
            print(e)
            return False

    def appium_calculate(self):
        # close "0.01黑钻换..."       

        time.sleep(5)

        if self.isElementExist("Link"):
            TouchAction(self.driver).tap(x=332, y=104).perform()
        #    self.driver.find_element_by_accessibility_id("Link").click()

        time.sleep(5)

        # level 1 main page
        logging.warning("========== Start from level 1 main page ...")
        time.sleep(30)
        self.driver.find_element_by_accessibility_id("获取原力").click()
        logging.warning("========== Level 2, 获取原力")
        time.sleep(30)

        self.appium_zixun()

        self.appium_music()

        # level 1 main page
        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # logging.warning(">>>>>>>>>> Back to level 1 ...")
        # time.sleep(15)
        return

    def appium_music(self):
        # Music
        self.driver.find_element_by_accessibility_id("网易云音乐").click()
        logging.warning("========== 网易云音乐")
        time.sleep(30)
        if self.isElementExist("立即收听"):
            self.driver.find_element_by_accessibility_id("立即收听").click()
        time.sleep(90)

        TouchAction(self.driver).tap(x=329, y=425).perform()
        logging.warning("========== Play music 1")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=485).perform()
        logging.warning("========== Play music 2")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=545).perform()
        logging.warning("========== Play music 3")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=605).perform()
        logging.warning("========== Play music 4")
        time.sleep(300)

        # level 2 main page
        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # logging.warning(">>>>>>>>>> Back to Level 2, 获取原力")
        # time.sleep(15)
        return

    def appium_zixun(self):
        # level 2 main page
        self.driver.find_element_by_accessibility_id("资讯").click()
        logging.warning("========== 资讯")
        time.sleep(30)
        if self.isElementExist("立即阅读"):
            self.driver.find_element_by_accessibility_id("立即阅读").click()
            time.sleep(15)
        # channel "区块链"
        self.driver.find_element_by_accessibility_id("区块链").click()
        logging.warning("========== 区块链")
        time.sleep(45)

        # Article 1
        TouchAction(self.driver).tap(x=200, y=185).perform()
        logging.warning("========== Article 1")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # Article 2
        TouchAction(self.driver).tap(x=200, y=315).perform()
        logging.warning("========== Article 2")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # Article 3
        TouchAction(self.driver).tap(x=200, y=445).perform()
        logging.warning("========== Article 3")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # Article 4
        TouchAction(self.driver).tap(x=200, y=575).perform()
        logging.warning("========== Article 4")
        time.sleep(15)
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)

        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(15)

        # level 2 main page
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        logging.warning("========== Back to Level 2, 获取原力")
        time.sleep(15)
        return

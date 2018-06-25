# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import logging
import os
import random
import time

from appium import webdriver
# Returns abs path relative to this file and not cwd
from appium.webdriver.common.touch_action import TouchAction

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("AppiumStar163.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/AppiumStar163.log', mode='w')
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
    MIN_SEC = 15
    MAX_SEC = 20

    def __init__(self, version, deviceName, port):
        print("start __init__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = deviceName
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['clearSystemFiles'] = 'True'
        desired_caps['app'] = PATH(
            'C:\DevTools\Android_apk\protect_163-e01170001_121-4.apk'
        # desired_caps['app'] = PATH(
        # '/Users/Jackie.Liu/Documents/MuMu共享文件夹/protect_163-e01170001_121-4.apk'
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
        logger.warning("========== Start from level 1 main page ...")
        time.sleep(30)
        self.driver.find_element_by_accessibility_id("获取原力").click()
        logger.warning("========== Level 2, 获取原力")
        time.sleep(30)

        self.appium_yuedu()
        self.appium_zixun()
        # self.appium_music()

        # level 1 main page
        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # logger.warning(">>>>>>>>>> Back to level 1 ...")
        # time.sleep(15)
        return

    def appium_music(self):
        time.sleep(10)
        # Music
        self.driver.find_element_by_accessibility_id("网易云音乐").click()
        logger.warning("========== 网易云音乐")
        time.sleep(30)
        if self.isElementExist("立即收听"):
            self.driver.find_element_by_accessibility_id("立即收听").click()
        time.sleep(90)

        TouchAction(self.driver).tap(x=329, y=425).perform()
        logger.warning("========== Play music 1")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=485).perform()
        logger.warning("========== Play music 2")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=545).perform()
        logger.warning("========== Play music 3")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=605).perform()
        logger.warning("========== Play music 4")
        time.sleep(300)

        # level 2 main page
        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # logger.warning(">>>>>>>>>> Back to Level 2, 获取原力")
        # time.sleep(15)
        return

    def appium_zixun(self):
        time.sleep(10)
        # level 2 main page
        self.driver.find_element_by_accessibility_id("资讯").click()
        logger.warning("========== 资讯")
        time.sleep(30)
        if self.isElementExist("立即阅读"):
            self.driver.find_element_by_accessibility_id("立即阅读").click()
            time.sleep(15)
        # channel "区块链"
        self.driver.find_element_by_accessibility_id("区块链").click()
        logger.warning("========== 区块链")
        time.sleep(45)

        # Article 1
        TouchAction(self.driver).tap(x=200, y=185).perform()
        logger.warning("========== Article 1")
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        # Article 2
        TouchAction(self.driver).tap(x=200, y=315).perform()
        logger.warning("========== Article 2")
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        # Article 3
        TouchAction(self.driver).tap(x=200, y=445).perform()
        logger.warning("========== Article 3")
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        # Article 4
        TouchAction(self.driver).tap(x=200, y=575).perform()
        logger.warning("========== Article 4")
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        if self.isElementExist("查看全文"):
            self.driver.find_element_by_accessibility_id("查看全文").click()
        time.sleep(85)

        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        # level 2 main page
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        logger.warning("========== Back to Level 2, 获取原力")
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        return

    def appium_yuedu(self):
        time.sleep(10)
        # level 2 main page
        self.driver.find_element_by_accessibility_id("阅读").click()
        logger.warning("========== 阅读")
        time.sleep(30)
        if self.isElementExist("去读书"):
            self.driver.find_element_by_accessibility_id("去读书").click()
            time.sleep(15)

        # reading
        TouchAction(self.driver).tap(x=113, y=533).perform()
        logger.warning("========== Reading......")

        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        if self.isElementExist("显示/隐藏操作栏"):
            self.driver.find_element_by_accessibility_id("显示/隐藏操作栏").click()
        time.sleep(85)

        count = 0
        while True:
            if count > 12:
                break
            self.swipeUp(1000)
            time.sleep(60)
            count += 1
            logger.warning("========== Reading count: " + str(count))


        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        # level 2 main page
        self.driver.find_element_by_id("com.netease.blockchain:id/iv_close").click()
        logger.warning("========== Back to Level 2, 获取原力")
        time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        return


    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    #屏幕向上滑动
    def swipeUp(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  #x坐标
        y1 = int(l[1] * 0.75)   #起始y坐标
        y2 = int(l[1] * 0.25)   #终点y坐标
        self.driver.swipe(x1, y1, x1, y2,t)
    #屏幕向下滑动
    def swipeDown(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  #x坐标
        y1 = int(l[1] * 0.25)   #起始y坐标
        y2 = int(l[1] * 0.75)   #终点y坐标
        self.driver.swipe(x1, y1, x1, y2,t)
    #屏幕向左滑动
    def swipLeft(self, t):
        l=self.getSize()
        x1=int(l[0]*0.75)
        y1=int(l[1]*0.5)
        x2=int(l[0]*0.05)
        self.driver.swipe(x1,y1,x2,y1,t)
    #屏幕向右滑动
    def swipRight(self, t):
        l=self.getSize()
        x1=int(l[0]*0.05)
        y1=int(l[1]*0.5)
        x2=int(l[0]*0.75)
        self.driver.swipe(x1,y1,x2,y1,t)

    # #调用向左滑动
    # swipLeft(1000)
    # sleep(3)
    # #调用向右滑动
    # swipRight(1000)
    # 调用向上滑动
    # swipeUp(1000)
    # 调用向下滑动
    # swipeDown(1000)

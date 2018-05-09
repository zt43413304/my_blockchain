# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import os
import time

from appium import webdriver

# Returns abs path relative to this file and not cwd
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
            'C:\\Tools\\star163\\blockchain112_163-e01170001.apk'
        )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def appium_zixun(self):
        # 测试导航页
        print("start test...")

        time.sleep(10)
        el1 = self.driver.find_element_by_accessibility_id("获取原力")
        el1.click()
        time.sleep(10)
        el2 = self.driver.find_element_by_accessibility_id("资讯")
        el2.click()
        time.sleep(10)
        # el3 = self.driver.find_element_by_accessibility_id("立即阅读")
        # el3.click()
        # el4 = self.driver.find_element_by_accessibility_id("区块链")
        # el4.click()
        # el5 = self.driver.find_element_by_accessibility_id("比特币跌破一万美元关口！虚拟货币们究竟是泡沫还是数字资产？财富日记说 Link")
        # el5.click()
        # el6 = self.driver.find_element_by_id("com.netease.blockchain:id/iv_back")
        # el6.click()
        # el7 = self.driver.find_element_by_accessibility_id("区块链要让淘宝给用户们分钱！马云：这个锅我不背财视传媒 Link")
        # el7.click()
        # el8 = self.driver.find_element_by_id("com.netease.blockchain:id/iv_back")
        # el8.click()
        # el9 = self.driver.find_element_by_accessibility_id("权重飙升国家队再出手？巨量资金涌入这类股望爆发巨丰财经 Link")
        # el9.click()
        # el10 = self.self.driver.find_element_by_accessibility_id("查看全文")
        # el10.click()
        # el11 = self.driver.find_element_by_id("com.netease.blockchain:id/iv_back")
        # el11.click()
        # el12 = self.driver.find_element_by_id("com.netease.blockchain:id/iv_back")
        # el12.click()
        # el13 = self.driver.find_element_by_accessibility_id("网易云音乐")
        # el13.click()
        # el14 = self.driver.find_element_by_accessibility_id("立即收听")
        # el14.click()
        # el15 = self.driver.find_element_by_id("com.netease.blockchain:id/iv_back")
        # el15.click()
        # el16 = self.driver.find_element_by_id("com.netease.blockchain:id/iv_back")
        # el16.click()

# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import logging
import os
import random
import subprocess
import threading
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from common import send_email

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class AppiumStar(threading.Thread):
    MIN_SEC = 5
    MAX_SEC = 10
    phone = None
    version = None
    deviceName = None
    port = None

    def __init__(self, version, deviceName, port, phone):
        threading.Thread.__init__(self)
        self.phone = phone
        self.version = version
        self.deviceName = deviceName
        self.port = port

        rq = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))

        # 第一步，创建一个logger,并设置级别
        # self.logger = logging.getLogger("bixiang_news_video_class.py")
        self.logger = logging.getLogger("Appium163_%s" % rq)
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        fh = logging.FileHandler('./logs/star163_Appium163_%s.log' % rq, mode='w')
        fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        if self.phone == '13601223469':
            self.starup_136()
        else:
            self.starup_138()

    def isElementExist(self, id):
        try:
            self.driver.find_element_by_accessibility_id(id)
            return True
        except Exception as e:
            # print(e)
            return False

    def isElementExist_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except Exception as e:
            # print(e)
            return False

    def appium_calculate(self):
        # close "0.01黑钻换..."       

        time.sleep(5)

        pop_xpath = '//android.view.View[@content-desc="Link"]'
        if self.isElementExist_by_xpath(pop_xpath):
            self.driver.find_element(By.XPATH, pop_xpath).click()

        # if self.isElementExist("Link"):
        # "el1 = driver.find_element_by_accessibility_id("Link")"
        # TouchAction(self.driver).tap(x=332, y=104).perform()
        # self.driver.find_element_by_accessibility_id("Link").click()

        time.sleep(5)

        # level 1 main page
        self.logger.warning("========== " + str(self.phone) + ", Start from tab 2 main page ...")
        # time.sleep(30)
        # self.driver.find_element_by_accessibility_id("获取原力").click()
        # self.logger.warning("========== Level 2, 获取原力")
        # time.sleep(30)

        self.driver.find_element_by_id("com.netease.blockchain:id/tvTwo").click()

        self.appium_yuedu()
        time.sleep(15)
        self.appium_zixun()
        # self.appium_music()

        # level 1 main page
        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # logger.warning(">>>>>>>>>> Back to level 1 ...")
        # time.sleep(15)

        # if self.phone == '13601223469':
        #     cmd_clean = r'cmd.exe C:/DevTools/my_blockchain/star163/clean136.bat'
        #     result1 = self.execute_command(cmd_clean)
        #     print('result:------>', result1)
        #
        #     send_email.send_star163_HtmlEmail('newseeing@163.com', '136获取原力完成.', '')
        #     self.logger.warning('********** Sending 136获取原力完成 Email Complete!')
        # else:
        #     cmd_clean = r'cmd.exe C:/DevTools/my_blockchain/star163/clean138.bat'
        #     result1 = self.execute_command(cmd_clean)
        #     print('result:------>', result1)

        send_email.send_star163_HtmlEmail('newseeing@163.com', '获取原力完成 ' + str(self.phone), '')
        self.logger.warning('********** Sending Email Complete!')

        return

    def appium_music(self):
        time.sleep(10)
        # Music
        self.driver.find_element_by_accessibility_id("网易云音乐").click()
        self.logger.warning("========== 网易云音乐")
        time.sleep(30)
        if self.isElementExist("立即收听"):
            self.driver.find_element_by_accessibility_id("立即收听").click()
        time.sleep(90)

        TouchAction(self.driver).tap(x=329, y=425).perform()
        self.logger.warning("========== Play music 1")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=485).perform()
        self.logger.warning("========== Play music 2")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=545).perform()
        self.logger.warning("========== Play music 3")
        time.sleep(300)

        TouchAction(self.driver).tap(x=329, y=605).perform()
        self.logger.warning("========== Play music 4")
        time.sleep(300)

        # level 2 main page
        # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
        # logger.warning(">>>>>>>>>> Back to Level 2, 获取原力")
        # time.sleep(15)
        return

    def appium_zixun(self):
        try:
            self.driver.find_element_by_id("com.netease.blockchain:id/tvTwo").click()
            time.sleep(30)
            # level 2 main page

            # self.driver.find_element_by_accessibility_id("资讯").click()
            # self.driver.find_element_by_xpath('//android.view.View[@content-desc=\"原力任务\"]/android.view.View[21]').click()
            # self.driver.find_element_by_xpath('//android.view.View[32]').click()
            self.my_find_elements_by_classname('android.view.View', 21).click()
            # self.my_find_elements_by_classname('android.view.View', '21').click()
            # TouchAction(self.driver).tap(x=531, y=827).perform()

            self.logger.warning("========== " + str(self.phone) + ", 资讯")
            time.sleep(30)
            if self.isElementExist("立即阅读"):
                self.driver.find_element_by_accessibility_id("立即阅读").click()
                time.sleep(5)
            # channel "区块链"
            self.driver.find_element_by_accessibility_id("头条").click()
            self.logger.warning("========== " + str(self.phone) + ", 头条")
            self.swipeDown(1000)
            time.sleep(30)

            # news_list = self.my_find_elements_by_size('android.view.View')
            #
            # for i in range(len(news_list)):
            #
            #     # self.my_find_elements_by_classname('android.view.View', i).click()
            #     position = news_list[i].location
            #     TouchAction(self.driver).tap(x=position['x'] + 100, y=position['y'] + 50).perform()
            #
            #     self.logger.warning(">>>>>>>>>> " + str(self.phone) + ": Article " + str(i))
            #     time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            #     if self.isElementExist("查看全文"):
            #         self.driver.find_element_by_accessibility_id("查看全文").click()
            #
            #     self.swipeUp(1000)
            #     time.sleep(20)
            #     self.swipeUp(1000)
            #     time.sleep(20)
            #     self.swipeUp(1000)
            #     time.sleep(20)
            #     self.swipeUp(1000)
            #     time.sleep(20)
            #     self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
            #     # self.swipeDown(1000)
            #     time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            #     return
        except Exception as e:
            print(e)

        try:
            # Article 1
            # self.my_find_elements_by_classname('android.view.View', 40).click()
            TouchAction(self.driver).tap(x=300, y=270).perform()
            self.logger.warning(">>>>>>>>>> " + str(self.phone) + ": Article 1")
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            if self.isElementExist("查看全文"):
                self.driver.find_element_by_accessibility_id("查看全文").click()
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
            self.swipeDown(1000)
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        except Exception as e:
            print(e)

        try:
            # Article 2
            TouchAction(self.driver).tap(x=300, y=500).perform()
            self.logger.warning(">>>>>>>>>> " + str(self.phone) + ": Article 2")
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            if self.isElementExist("查看全文"):
                self.driver.find_element_by_accessibility_id("查看全文").click()
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
            self.swipeDown(1000)
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        except Exception as e:
            print(e)

        try:
            # Article 3
            TouchAction(self.driver).tap(x=300, y=730).perform()
            self.logger.warning(">>>>>>>>>> " + str(self.phone) + ": Article 3")
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            if self.isElementExist("查看全文"):
                self.driver.find_element_by_accessibility_id("查看全文").click()
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()
            self.swipeDown(1000)
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        except Exception as e:
            print(e)

        try:
            # Article 4
            TouchAction(self.driver).tap(x=300, y=960).perform()
            self.logger.warning(">>>>>>>>>> " + str(self.phone) + ": Article 4")
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            if self.isElementExist("查看全文"):
                self.driver.find_element_by_accessibility_id("查看全文").click()
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
            time.sleep(15)
            self.swipeUp(1000)
        except Exception as e:
            print(e)

        # level 2 main page
        if self.phone == "13826090504":
            self.driver.back()
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            self.driver.back()
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
        else:
            if self.isElementExist("com.netease.blockchain:id/iv_back"):
                self.driver.find_element_by_accessibility_id("com.netease.blockchain:id/iv_back").click()
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

            if self.isElementExist("com.netease.blockchain:id/iv_back"):
                self.driver.find_element_by_accessibility_id("com.netease.blockchain:id/iv_back").click()
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

        self.logger.warning("========== " + str(self.phone) + ", Back to Level 2, 获取原力")
        return

    def my_find_elements_by_classname(self, classname, index):

        # android.widget.TextView
        views = self.driver.find_elements(By.CLASS_NAME, classname)
        return views[index]
        # for i in range(len(views)):
        #     print(views[i].text)
        #     if views[i].id == name:
        #         return views[i]

    def my_find_elements_by_size(self, classname):

        news_list = []
        # android.widget.TextView
        news = self.driver.find_elements(By.CLASS_NAME, classname)

        for i in range(len(news)):
            # print(views[i].text)
            if news[i].size['width'] == 600:
                # news_list.append(i)
                news_list.append(news[i])
        self.logger.warning("========== news_list length = " + str(len(news_list)))
        return news_list

    def appium_yuedu(self):
        try:
            self.driver.find_element_by_id("com.netease.blockchain:id/tvTwo").click()
            time.sleep(15)

            # print(self.driver.current_context)
            # cons = self.driver.contexts
            # 0: 'NATIVE_APP'
            # 1: 'WEBVIEW_com.netease.blockchain'
            # for i in range(len(cons)):
            # print(">>>>> " + cons[i].id)
            # print(">>>>> " + cons[i].text)

            # self.driver.switch_to.context(cons[1])
            # print(self.driver.current_context)

            # level 2 main page
            # self.driver.find_element_by_xpath("//android.view.View[@content-desc=\"原力任务\"]/android.view.View[18]").click()
            # self.driver.find_element_by_xpath("//android.view.View[18]").click()
            # self.driver.find_element_by_xpath('//android.view.View[28]').click()
            self.my_find_elements_by_classname('android.view.View', 18).click()
            # TouchAction(self.driver).tap(x=113, y=524).perform()

            # self.driver.find_element_by_accessibility_id("阅读").click()
            self.logger.warning("========== " + str(self.phone) + ", 阅读")
            time.sleep(15)
            if self.isElementExist("去读书"):
                self.driver.find_element_by_accessibility_id("去读书").click()
                time.sleep(5)

            # reading
            # TouchAction(self.driver).tap(x=113, y=533).perform()
            self.driver.find_element_by_xpath("(//android.view.View[@content-desc=\"Link\"])[1]").click()
            # self.my_find_elements_by_classname('android.view.View', 23).click()
            # self.driver.find_element_by_xpath("(//android.view.View[1]").click()
            # self.logger.warning("========== Reading......")

            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))

            if self.isElementExist("显示/隐藏操作栏"):
                self.driver.find_element_by_accessibility_id("显示/隐藏操作栏").click()
            time.sleep(5)

            count = 0
            while True:
                if count > 8:
                    break
                self.swipeUp(1000)
                time.sleep(15)
                self.swipeUp(1000)
                time.sleep(15)
                self.swipeUp(1000)
                time.sleep(15)
                self.swipeUp(1000)
                time.sleep(15)
                count += 1
                self.logger.warning(">>>>>>>>>> " + str(self.phone) + ", Reading count: " + str(count))

            # level 2 main page
            # self.driver.back()
            self.driver.find_element_by_id("com.netease.blockchain:id/iv_close").click()
            # self.driver.find_element_by_id("com.netease.blockchain:id/iv_back").click()

            # if self.isElementExist("com.netease.blockchain:id/iv_back"):
            #     self.driver.find_element_by_accessibility_id("com.netease.blockchain:id/iv_back").click()
            # time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            #
            # if self.isElementExist("com.netease.blockchain:id/iv_back"):
            #     self.driver.find_element_by_accessibility_id("com.netease.blockchain:id/iv_back").click()
            # time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            # self.logger.warning("========== " + str(self.phone) + ", Back to Level 2")
            time.sleep(random.randint(self.MIN_SEC, self.MAX_SEC))
            return
        except Exception as e:
            print(e)
            return

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    # 屏幕向上滑动
    def swipeUp(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.75)  # 起始y坐标
        y2 = int(l[1] * 0.25)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向下滑动
    def swipeDown(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.25)  # 起始y坐标
        y2 = int(l[1] * 0.75)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向左滑动
    def swipLeft(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.05)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 屏幕向右滑动
    def swipRight(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.05)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, t)

    # #调用向左滑动
    # swipLeft(1000)
    # sleep(3)
    # #调用向右滑动
    # swipRight(1000)
    # 调用向上滑动
    # swipeUp(1000)
    # 调用向下滑动
    # swipeDown(1000)

    def run(self):
        self.appium_calculate()

    def execute_command(self, cmd):
        print('***** start executing cmd...')
        p = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stderrinfo, stdoutinfo = p.communicate()
        for line in stdoutinfo.splitlines():
            print(line)

        print('stdoutinfo is -------> %s' % stdoutinfo)
        print('stderrinfo is -------> %s' % stderrinfo)
        print('finish executing cmd....')
        return p.returncode

    def starup_136(self):
        # cmd_clean = r'cmd.exe C:/DevTools/my_blockchain/star163/clean136.bat'
        # result1 = self.execute_command(cmd_clean)
        # print('result:------>', result1)
        #
        # output = os.system("C:/DevTools/Nemu/EmulatorShell/NemuPlayer.exe")
        # self.logger.warning(">>>>>>>>>> Start NemuPlayer.exe, output = " + str(output))
        # time.sleep(120)

        cmd_adb = r'adb connect 127.0.0.1:7555'
        result1 = self.execute_command(cmd_adb)
        print('result:------>', result1)
        cmd_adb1 = r'adb devices -l'
        result2 = self.execute_command(cmd_adb1)
        print('result:------>', result2)

        output3 = os.system(
            "start node C:/Users/Jackie.Liu/AppData/Local/Programs/Appium/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4723")
        print('result:------>' + str(output3))
        time.sleep(60)

        print("start __init__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = self.version
        desired_caps['deviceName'] = self.deviceName
        desired_caps['noReset'] = True
        desired_caps['newCommandTimeout'] = 600
        desired_caps['clearSystemFiles'] = True
        desired_caps['app'] = PATH(
            'C:\DevTools\Android_apk\com.netease.blockchain-2.apk'
        )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'
        self.driver = webdriver.Remote('http://127.0.0.1:' + str(self.port) + '/wd/hub', desired_caps)

    def starup_138(self):
        # cmd_clean = r'cmd.exe C:/DevTools/my_blockchain/star163/clean138.bat'
        # result1 = self.execute_command(cmd_clean)
        # print('result:------>', result1)
        #
        # output = os.system("C:/DevTools/Nox/Nox/bin/Nox.exe")
        # self.logger.warning("========== Start Nox.exe, output = " + str(output))
        # time.sleep(120)

        cmd_adb = r'adb connect 127.0.0.1:62001'
        result1 = self.execute_command(cmd_adb)
        print('result:------>', result1)
        cmd_adb1 = r'adb devices -l'
        result2 = self.execute_command(cmd_adb1)
        print('result:------>', result2)

        output3 = os.system(
            "start node C:/Users/Jackie.Liu/AppData/Local/Programs/Appium/resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p 4725")
        print('result:------>' + str(output3))
        time.sleep(30)

        print("start __init__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = self.version
        desired_caps['deviceName'] = self.deviceName
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['clearSystemFiles'] = 'True'
        desired_caps['app'] = PATH(
            'C:\DevTools\Android_apk\com.netease.blockchain-2.apk'
            # desired_caps['app'] = PATH(
            # '/Users/Jackie.Liu/Documents/MuMu共享文件夹/protect_163-e01170001_121-4.apk'
        )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'
        self.driver = webdriver.Remote('http://127.0.0.1:' + str(self.port) + '/wd/hub', desired_caps)

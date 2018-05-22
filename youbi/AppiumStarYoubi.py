# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import logging
import os
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
# Returns abs path relative to this file and not cwd

# 日志
# 第一步，创建一个logger
logger = logging.getLogger("AppiumStarYoubi.py")

logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'youbi_appium.log'
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

# logger.removeHandler(ch)
# logger.removeHandler(fh)
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
        self.logger = logging.getLogger("=== AppiumStarYoubi.py")
        self.logger.info("=== info creating an instance in AppiumStarYoubi.py")
        self.logger.warning("=== warning creating an instance in AppiumStarYoubi.py")

    def __init__(self, version, deviceName, port):
        logger.warning("********** start __init__..." + str(port))
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = deviceName
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['app'] = PATH(
            'C:/DevTools/youbi/com.manymanycoin.android_1.4.5_liqucn.com.apk'
        )
        desired_caps['appPackage'] = 'com.manymanycoin.android'
        desired_caps['appActivity'] = 'com.manymanycoin.android.activity.MainActivity'
        self.driver = webdriver.Remote('http://localhost:' + str(port) + '/wd/hub', desired_caps)

    def isElementExist(self, id):
        try:
            self.driver.find_element_by_accessibility_id(id)
            return True
        except Exception as e:
            print(e)
            return False

    def sign_get_coin(self, phone):
        # 抢币
        element_list = self.driver.find_elements_by_class_name("android.widget.Button")
        for i in range(len(element_list)):
            ele = element_list[i]
            # logger.warning(">>>>>>>>>> sign_get_coin(" + phone + "), ele.text = " + ele.text)
            if ele.text == "立即领取" or ele.text == "签到领10个币":
                ele.click()
                logger.warning(">>>>>>>>>> sign_get_coin(" + phone + "), after click, ele.text = " + ele.text)



    def appium_youbi(self, phone):
        time.sleep(3)
        # 中间图片按钮“领币”
        # TouchAction(self.driver).tap(x=200, y=612).perform()
        self.driver.find_element_by_id("com.manymanycoin.android:id/get_coin").click()
        time.sleep(3)

        # 签到
        # if self.isElementExist("com.manymanycoin.android:id/sign_bt"):
        #     el1 = self.driver.find_element_by_id("com.manymanycoin.android:id/sign_bt")
        #     el1.click()

        try:
            i = 0
            while i < 8:
                self.sign_get_coin(phone)
                action = TouchAction(self.driver)
                action.press(x=200,y=400).move_to(x=200,y=320).wait(200).release().wait(200).perform()
                time.sleep(3)
                self.driver.get_screenshot_as_file("file_"+phone+"_"+str(i)+".png")
                i = i + 1
                logger.warning(">>>>>>>>>> appium_youbi(" + phone + "), i = " + str(i))
        except Exception as e:
            print(e)
        return






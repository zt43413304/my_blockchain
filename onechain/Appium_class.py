# coding=utf-8


import logging
import os
import random
import time

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("Appium_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/Appium_class.log', mode='w')
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


class trader_class:

    def __init__(self):
        logger.warning("start __init__...")

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['clearSystemFiles'] = 'True'
        # desired_caps['automationName'] = 'Appium'
        # desired_caps['autoWebview'] = 'True'
        desired_caps['app'] = PATH(
            '/Users/Jackie.Liu/Documents/Blockchain/Android APK/one208.apk'
        )
        desired_caps['appPackage'] = 'oneapp.onechain.androidapp'
        desired_caps['appActivity'] = 'oneapp.onechain.androidapp.onemessage.view.activity.UnlockActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def isElementExist_by_id(self, id):
        try:
            self.driver.find_element_by_id(id)
            return True
        except Exception as e:
            print(e)
            return False

    def my_find_elements_by_classname(self, classname, name):
        wait = WebDriverWait(self.driver, 60)
        # android.widget.TextView
        views = self.driver.find_elements(By.CLASS_NAME, classname)
        # views = wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        for i in range(len(views)):
            if views[i].text == name:
                return views[i]

    def get_value(self):
        value = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/tv_available_fund_value")
        return value.text

    def get_price(self):
        time.sleep(random.randint(1, 3))
        wait = WebDriverWait(self.driver, 10)
        try:
            # 是否存在登录界面
            if self.isElementExist_by_id("oneapp.onechain.androidapp:id/dialog_edit_et"):
                password = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/dialog_edit_et")
                password.clear()
                password.send_keys("Liuxb0504$")
                self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit").click()

            # el3 = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/ib_profile")
            # el3.click()
            # el4 = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/tvmsg")
            # el4.click()
            # el5 = self.driver.find_element_by_accessibility_id("ONE")
            # el5.click()

            time.sleep(random.randint(1, 3))
            # 点击“交易”
            trade = wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/tv_exchange")))
            trade.click()

            # 点击“USDA”
            self.my_find_elements_by_classname("android.widget.TextView", "USDA").click()
            time.sleep(random.randint(1, 3))

            # 点击“ETH/USDA”
            self.my_find_elements_by_classname("android.widget.TextView", "ETH/USDA").click()
            time.sleep(random.randint(1, 3))

            # 获取交易价格
            views = self.driver.find_elements(By.ID, "oneapp.onechain.androidapp:id/tv_bid_price")
            # views = wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
            for i in range(len(views)):
                # if views[i].text == name:
                #     return views[i]
                print(views[i].text)

            # 点击“卖出”
            self.my_find_elements_by_classname("android.widget.TextView", "卖出").click()
            print("可用ETH = " + str(self.get_value()))

            avg_price = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/tv_price_new")))
            print("卖出均价 = " + str(avg_price.text))

            price = wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_input_price")))
            price.clear()
            price.send_keys("900.09")

            amount = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_input_amount")))
            amount.clear()
            amount.send_keys("0.00001")

            # trade_button = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_user_trade_confirm")
            trade_button = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/btn_user_trade_confirm")))
            # trade_button.click()
            time.sleep(random.randint(5, 8))

            # 是否存在交易确认，输入密码界面
            if self.isElementExist_by_id("oneapp.onechain.androidapp:id/dialog_edit_et"):
                password = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/dialog_edit_et")
                password.clear()
                password.send_keys("Liuxb0504$")
                self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit").click()

            # 点击“买入”
            self.my_find_elements_by_classname("android.widget.TextView", "买入").click()
            print("可用USDA = " + str(self.get_value()))

            avg_price = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/tv_price_new")))
            print("买入均价 = " + str(avg_price.text))
        except Exception as e:
            print(e)

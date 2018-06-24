# coding=utf-8
import configparser
import logging
import os
import random
import re
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
            # '/Users/Jackie.Liu/DevTools/Android_apk/one213.apk'
            'C:\DevTools\Android_apk\one213.apk'
        )
        desired_caps['appPackage'] = 'oneapp.onechain.androidapp'
        desired_caps['appActivity'] = 'oneapp.onechain.androidapp.onemessage.view.activity.UnlockActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

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

    def isElementExist_by_id(self, id):
        try:
            self.driver.find_element_by_id(id)
            return True
        except Exception as e:
            # print(e)
            return False

    def my_find_elements_by_classname(self, classname, name):
        wait = WebDriverWait(self.driver, 60)
        # android.widget.TextView
        views = self.driver.find_elements(By.CLASS_NAME, classname)
        # views = wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        for i in range(len(views)):
            if views[i].text == name:
                return views[i]

    def my_find_elements_by_id(self, id):
        wait = WebDriverWait(self.driver, 60)
        # android.widget.TextView
        ids = self.driver.find_elements(By.ID, id)
        return ids

    def get_value(self):
        value = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/tv_available_fund_value")
        return value.text

    def load_quota(self):
        # get config information
        curpath = os.getcwd()
        content = open(curpath + '/onechain/quota.ini').read()
        content = re.sub(r"\xfe\xff", "", content)
        content = re.sub(r"\xff\xfe", "", content)
        content = re.sub(r"\xef\xbb\xbf", "", content)
        open(curpath + '/onechain/quota.ini', 'w').write(content)

        cf = configparser.ConfigParser()
        cf.read(curpath + '/onechain/quota.ini')
        ETH_Price = cf.get('info', 'ETH_Price').strip()
        Deal_Quota = cf.get('info', 'Deal_Quota').strip()
        return ETH_Price, Deal_Quota

    def one_login(self):
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
            self.my_find_elements_by_classname("android.widget.TextView", "ETH").click()
            time.sleep(random.randint(1, 3))

            # 点击“ETH/USDA”
            self.my_find_elements_by_classname("android.widget.TextView", "ONE/ETH").click()
            time.sleep(random.randint(1, 3))
            logger.warning("********** Login success!")
            return 0

        except Exception as e:
            print(e)
            return -1

    def get_price(self):

        (ETH_Price, Deal_Quota) = self.load_quota()

        wait = WebDriverWait(self.driver, 10)
        try:

            self.swipeDown(1000)

            logger.warning("\n")
            logger.warning("========== Refreshing price ......")

            # 点击“卖出”
            self.my_find_elements_by_classname("android.widget.TextView", "卖出").click()
            sell_balance = self.get_value()

            # 点击“买入”
            self.my_find_elements_by_classname("android.widget.TextView", "买入").click()
            buy_balance = self.get_value()

            avg_price = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/tv_price_new")))
            avg_price_value = avg_price.text.split(' ')[0]
            logger.warning("========== 当前均价: " + str(avg_price.text) +
                           " (~"+str(round(int(ETH_Price)*float(avg_price_value),4))+" RMB)")

            # # 获取交易价格
            # views = self.driver.find_elements(By.ID, "oneapp.onechain.androidapp:id/tv_bid_price")
            # # views = wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
            # # for i in range(len(views)):
            # #     # if views[i].text == name:
            # #     #     return views[i]
            # #     print(views[i].text)
            # sell01 = views[4].text
            # buy01 = views[5].text
            # logger.warning("========== 卖一价: " + str(sell01) + ", 买一价: " + str(buy01))
            logger.warning("========== 卖余额: " + str(sell_balance) + ", 买余额: " + str(buy_balance))

            # back = wait.until(
            #     EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back")))
            # back.click()

            return avg_price_value, sell_balance, buy_balance

        except Exception as e:
            print(e)
            return -1, -1, -1, -1

    def buy(self, amount):
        # time.sleep(random.randint(1, 3))
        wait = WebDriverWait(self.driver, 10)
        # price = str('{:.8f}'.format(round(float(price) * (1+0.0001),8)))
        try:
            # 点击“买入”
            self.my_find_elements_by_classname("android.widget.TextView", "买入").click()

            # 获取价格
            views = self.driver.find_elements(By.ID, "oneapp.onechain.androidapp:id/tv_bid_price")
            # price = views[4].text
            price = views[5].text

            price = str('{:.8f}'.format(float(price) + 0.00000001))


            # 输入价格
            input_price = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_input_price")))
            input_price.clear()
            input_price.send_keys(price)

            # 输入数量
            input_amount = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_input_amount")))
            input_amount.clear()
            input_amount.send_keys(amount)

            # 交易按钮
            trade_button = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/btn_user_trade_confirm")))
            self.driver.implicitly_wait(10)
            trade_button.click()

            logger.warning("<<<<<<<<<< buy ONE, price=" + str(price) + ", amount=" + str(amount))

            # 是否存在交易确认，输入密码界面
            if self.isElementExist_by_id("oneapp.onechain.androidapp:id/dialog_edit_et"):
                password = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/dialog_edit_et")
                password.clear()
                password.send_keys("Liuxb0504$")
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit").click()

            return 0
        except Exception as e:
            print(e)
            return -1

    def sell(self, amount):
        # time.sleep(random.randint(1, 3))
        wait = WebDriverWait(self.driver, 10)
        # price = str('{:.8f}'.format(round(float(price) * (1-0.0001),8)))
        try:
            # 点击“卖出”
            self.my_find_elements_by_classname("android.widget.TextView", "卖出").click()

            # 获取价格
            views = self.driver.find_elements(By.ID, "oneapp.onechain.androidapp:id/tv_bid_price")
            # price = views[4].text
            price = views[5].text

            price = str('{:.8f}'.format(float(price) - 0.00000001))

            # 输入价格
            input_price = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_input_price")))
            input_price.clear()
            input_price.send_keys(price)

            # 输入数量
            input_amount = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_input_amount")))
            input_amount.clear()
            input_amount.send_keys(amount)

            # 交易按钮
            trade_button = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/btn_user_trade_confirm")))
            self.driver.implicitly_wait(10)
            trade_button.click()

            logger.warning(">>>>>>>>>> sell ONE, price=" + str(price) + ", amount=" + str(amount))

            # 是否存在交易确认，输入密码界面
            if self.isElementExist_by_id("oneapp.onechain.androidapp:id/dialog_edit_et"):
                password = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/dialog_edit_et")
                password.clear()
                password.send_keys("Liuxb0504$")
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit").click()

            return 0
        except Exception as e:
            print(e)
            return -1

    def cancel_order(self):
        # time.sleep(random.randint(1, 3))
        wait = WebDriverWait(self.driver, 10)
        # price = str('{:.8f}'.format(round(float(price) * (1+0.0001),8)))
        try:
            # 点击“当前委托”
            self.my_find_elements_by_classname("android.widget.TextView", "当前委托").click()

            # 获取“卖出订单”
            order_lists = self.my_find_elements_by_id("oneapp.onechain.androidapp:id/tv_trade_type")

            # 获取“卖出撤单按钮”
            cancel_buttons = self.my_find_elements_by_id("oneapp.onechain.androidapp:id/tv_cancel_order")

            for i in range(len(order_lists)):
                element = order_lists[i]
                # print(element.text)
                if element.text == "买入":
                    left = element.location['x']
                    top = element.location['y']
                    right = element.location['x'] + element.size['width']
                    bottom = element.location['y'] + element.size['height']
                    # print("element >>>>>>>")
                    # print(left, top, right, bottom)
                    self.click_cancel_button(cancel_buttons, top)
            return 0
        except Exception as e:
            print(e)
            return -1

    def click_cancel_button(self, cancel_buttons, position):
        try:
            for i in range(len(cancel_buttons)):
                element = cancel_buttons[i]
                # print(element.text)
                left = element.location['x']
                top = element.location['y']
                right = element.location['x'] + element.size['width']
                bottom = element.location['y'] + element.size['height']

                if top == position:
                    element.click()
                    # 是否存在取消确认按钮
                    if self.isElementExist_by_id("oneapp.onechain.androidapp:id/btn_commit"):
                        confirm = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit")
                        confirm.click()
                    # 撤销成功按钮
                    if self.isElementExist_by_id("oneapp.onechain.androidapp:id/btn_commit"):
                        confirm = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit")
                        confirm.click()
            return 0
        except Exception as e:
            print(e)
            return -1
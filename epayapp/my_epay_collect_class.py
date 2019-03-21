# coding=utf-8

import logging
import os
import re
import time

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("my_epay_collect_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_epay_collect_class.log', mode='w')
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


class Collect:

    def __init__(self):
        logger.warning("********** start __init()__...")

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    # 屏幕向上滑动
    def swipeUp(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.75)  # 起始y坐标
        y2 = int(l[1] * 0.5)  # 终点y坐标
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

    def get_app_driver(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['clearSystemFiles'] = 'True'
        # desired_caps['automationName'] = 'Appium'
        # desired_caps['autoWebview'] = 'True'
        desired_caps['app'] = PATH(
            '/Users/Jackie.Liu/DevTools/Android_apk/EPAY1-4.apk'
        )
        desired_caps['appPackage'] = 'pro.epayapp.app'
        desired_caps['appActivity'] = 'pro.epayapp.app.MainActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        time.sleep(10)

    def isElementExist_by_classname(self, classname):
        try:
            self.driver.find_element(By.CLASS_NAME, classname)
            return True
        except Exception as e:
            print(e)
            return False

    def isElementExist_by_classname_name(self, classname, name):
        try:
            wait = WebDriverWait(self.driver, 30)
            names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, classname)))
            for i in range(len(names)):
                if names[i].text == name:
                    return names[i]
            return False
        except Exception as e:
            print(e)
            return False

    def isElementExist_by_id(self, id):
        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located((By.ID, id)))
            # self.driver.find_element_by_id(id)
            return True
        except Exception as e:
            print(e)
            return False

    def locate_and_do_transfer(self):
        wait = WebDriverWait(self.driver, 30)
        for count in range(4):
            # 逐行点击
            lines = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.ImageView")))

            for i in range(len(lines)):
                if lines[i].location['x'] != 27:
                    continue

                lines[i].click()
                time.sleep(1)
                # logger.warning("********** locate_and_do_transfer(): " + str(i))

                # 进入一行内部
                (result) = self.isElementExist_by_classname_name("android.widget.TextView", "闪电转账")
                if result is not False:
                    result.click()
                    time.sleep(1)
                    self.do_transfer()

                # 进入一行内部
                (result) = self.isElementExist_by_classname_name("android.widget.TextView", "转出")
                if result is not False:
                    result.click()
                    time.sleep(1)
                    self.do_transfer()

            self.swipeUp(1000)
            time.sleep(1)

    def do_transfer(self):
        wait = WebDriverWait(self.driver, 30)
        try:
            # 可用
            tv_amount_status = wait.until(
                EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/tv_amount_status")))

            # 余额不足
            nPos = tv_amount_status.text.find("余额不足")
            if nPos > -1:
                # 返回到转账页面
                wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
                time.sleep(1)

                # 返回到交易钱包页面，LinearLayout
                wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
                time.sleep(1)
                return 0

            tv_amount = float(tv_amount_status.text.split(' ')[0])
            coin = tv_amount_status.text.split(' ')[1]
            if coin in ("EATT", "ONE", "ONELUCK"):
                # 返回到转账页面
                wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
                time.sleep(1)

                # 返回到交易钱包页面，LinearLayout
                wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
                time.sleep(1)
                return 0

            # 手续费
            tv_fee = 0
            try:
                tv_fee_value = wait.until(
                    EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/tv_fee_value")))
                tv_fee = float(re.findall(r"\d+\.?\d*", tv_fee_value.text.split(':')[1])[0])
            except Exception as e:
                print(e)

            # 可转账额度
            amount = tv_amount - tv_fee
            if amount <= 0:
                # 返回到转账页面
                wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()

                # 返回到交易钱包页面，LinearLayout
                wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
                return 0

            # 发送给
            et_to = wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_to")))
            et_to.send_keys('jackielg')

            # 转账金额
            et_amount = wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/et_amount")))
            et_amount.send_keys(str(amount))

            # 转账确认
            self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_ok").click()
            time.sleep(3)

            # 如果需要输入密码
            if self.isElementExist_by_id("oneapp.onechain.androidapp:id/dialog_edit_et"):
                login = self.driver.find_element_by_id("oneapp.onechain.androidapp:id/dialog_edit_et")
                login.send_keys('Liuxb0504$')
                self.driver.find_element_by_id("oneapp.onechain.androidapp:id/btn_commit").click()
            time.sleep(5)

            # 返回到转账页面
            wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
            time.sleep(1)

            # 返回到交易钱包页面，LinearLayout
            wait.until(EC.presence_of_element_located((By.ID, "oneapp.onechain.androidapp:id/img_back"))).click()
            time.sleep(1)

            logger.warning(">>>>>>>>>>  do_transfer(), " + coin + " = " + str(amount))
            return 0
        except Exception as e:
            print(e)
            return -1

    def app_login(self, account_id):
        try:
            self.get_app_driver()

            logger.warning("========== app_login(" + account_id + ")......")

            wait = WebDriverWait(self.driver, 30)

            # 登录
            xpath_username = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.EditText"
            login = wait.until(EC.presence_of_element_located((By.XPATH, xpath_username)))
            login.clear()
            login.send_keys(account_id)
            time.sleep(1)

            xpath_passwd = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText"
            login = wait.until(EC.presence_of_element_located((By.XPATH, xpath_passwd)))
            login.clear()
            login.send_keys('Liuxb0504')
            time.sleep(1)

            xpath_login = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[5]/android.widget.TextView"
            login = wait.until(EC.presence_of_element_located((By.XPATH, xpath_login)))
            login.click()
            time.sleep(1)

            return 0
        except Exception as e:
            print(e)
            return -1

    def app_income(self):
        try:
            logger.warning("********** app_income()......")

            wait = WebDriverWait(self.driver, 30)

            # 静态收益
            xpath_static = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[4]/android.widget.TextView[3]"
            income = wait.until(EC.presence_of_element_located((By.XPATH, xpath_static)))
            income.click()
            time.sleep(3)

            # 动态收益
            xpath_dynamic = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[5]/android.widget.TextView[3]"
            income = wait.until(EC.presence_of_element_located((By.XPATH, xpath_dynamic)))
            income.click()
            time.sleep(3)

            # 收益合计
            xpath_income = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView[2]"
            income = wait.until(EC.presence_of_element_located((By.XPATH, xpath_income)))
            income_amount = float(income.text.replace(',', ''))
            logger.warning("********** income_amount = " + str(income_amount))
            # tv_amount = float(income.text.split(' ')[0])
            # income.click()
            time.sleep(1)

            return income_amount
        except Exception as e:
            print(e)
            return -1

    def app_revenue(self):
        try:
            logger.warning("********** app_revenue()......")

            wait = WebDriverWait(self.driver, 30)

            # 量化tab
            xpath_rev_tab = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[3]/android.widget.TextView"
            rev = wait.until(EC.presence_of_element_located((By.XPATH, xpath_rev_tab)))
            rev.click()
            time.sleep(1)

            # 量化本金
            xpath_rev_cost = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView[2]"
            rev = wait.until(EC.presence_of_element_located((By.XPATH, xpath_rev_cost)))
            rev_amount = float(rev.text.replace(',', ''))
            logger.warning("********** revenue_amount = " + str(rev_amount))
            time.sleep(1)

            return rev_amount
        except Exception as e:
            print(e)
            return -1

    def app_logout(self):
        try:
            logger.warning("********** app_logout()......")
            logger.warning('\n')

            wait = WebDriverWait(self.driver, 30)

            # Mine_tab
            xpath_logout_tab = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[5]/android.widget.TextView"
            income = wait.until(EC.presence_of_element_located((By.XPATH, xpath_logout_tab)))
            income.click()
            time.sleep(1)

            # logout
            xpath_logout = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[12]/android.widget.TextView"
            income = wait.until(EC.presence_of_element_located((By.XPATH, xpath_logout)))
            income.click()
            time.sleep(1)

            return 0
        except Exception as e:
            print(e)
            return -1

    def app_transfer(self, account_id):
        try:
            logger.warning("********** app_transfer()......")

            if account_id == '13601223469':
                return 0

            wait = WebDriverWait(self.driver, 30)

            # 点击transfer
            xpath_transfer = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView"
            transfer = wait.until(EC.presence_of_element_located((By.XPATH, xpath_transfer)))
            transfer.click()
            time.sleep(1)

            # 转账给~
            xpath_username = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"
            username = wait.until(EC.presence_of_element_located((By.XPATH, xpath_username)))
            username.clear()
            username.send_keys('13601223469')

            # 获取转账金额
            xpath_amount = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[4]"
            amount = wait.until(EC.presence_of_element_located((By.XPATH, xpath_amount)))
            amount = amount.text.split(':')[1]
            # amount = round(float(amount.replace(',', '')), 2)
            amount = str('{:.2f}'.format(float(amount.replace(',', '')) - 0.01))

            # 输入转账金额
            xpath_trans_amount = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText"
            trans_amount = wait.until(EC.presence_of_element_located((By.XPATH, xpath_trans_amount)))
            trans_amount.clear()
            trans_amount.send_keys(str(amount))

            # 短信验证
            xpath_sms = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.widget.TextView"
            sms = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sms)))
            sms.click()

            xpath_sms = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.widget.TextView"
            sms = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sms)))
            sms.click()

            code = input("********** Enter your sms code: ")
            logger.warning('**********  input is: ' + code)

            xpath_smscode = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.EditText"
            smscode = wait.until(EC.presence_of_element_located((By.XPATH, xpath_smscode)))
            smscode.clear()
            smscode.send_keys(code)

            xpath_sms_confirm = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.widget.TextView"
            sms_confirm = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sms_confirm)))
            sms_confirm.click()

            return 0
        except Exception as e:
            print(e)
            return -1

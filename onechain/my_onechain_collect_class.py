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
logger = logging.getLogger("my_onechain_collect_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/my_onechain_collect_class.log', mode='w')
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

# get config information
curpath = os.getcwd()
content = open(curpath + '/onechain/config.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/onechain/config.ini', 'w').write(content)

cf = configparser.ConfigParser()
cf.read(curpath + '/onechain/config.ini')
# unique = cf.get('info', 'unique').strip()
# uid = cf.get('info', 'uid').strip()
is_ad_ios = cf.get('info', 'is_ad_ios').strip()
versioncode = cf.get('info', 'versioncode').strip()
devicetype = cf.get('info', 'devicetype').strip()
channel = cf.get('info', 'channel').strip()
token = cf.get('info', 'token').strip()
ps = cf.get('info', 'ps').strip()
key = cf.get('info', 'key').strip()

headers = {
    'Host': "tui.yingshe.com",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'User-Agent': "okhttp/3.4.1",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}

payload = "is_ad_ios=" + is_ad_ios + \
          "&versioncode=" + versioncode + \
          "&devicetype=" + devicetype + \
          "&channel=" + channel + \
          "&token=" + token + \
          "&ps=" + ps + \
          "&key=" + key


class Collect:
    pass

    def __init__(self):
        logger.warning("********** start __init()__...")

    def get_app_driver(self):
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
            '/Users/Jackie.Liu/DevTools/Android_apk/one231.apk'
        )

        desired_caps['appPackage'] = 'oneapp.onechain.androidapp'
        desired_caps['appActivity'] = 'oneapp.onechain.androidapp.onemessage.view.activity.UnlockActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def app_transfer(self):

        try:
            logger.warning("********** app_transfer()......")
            self.get_app_driver()

            time.sleep(random.randint(5, 7))

            wait = WebDriverWait(self.driver, 30)

            # 新用户签到
            if self.isElementExist_by_id("com.coinstation.bixiang:id/btn_sign"):
                self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_sign").click()
                self.driver.back()
                time.sleep(random.randint(1, 3))
            # if self.isElementExist_by_id("com.coinstation.bixiang:id/signed_close"):
            #     self.driver.find_element_by_id("com.coinstation.bixiang:id/signed_close").click()
            # time.sleep(random.randint(3, 5))

            # 右下角“我的”
            self.my_find_elements_by_classname('android.widget.TextView', '我的').click()
            time.sleep(random.randint(2, 3))

            # 账号设置
            # self.driver.find_element(By.ID, "com.coinstation.bixiang:id/tv_set").click()
            button = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/tv_set')))
            button.click()
            time.sleep(random.randint(2, 3))

            # 点击“去绑定”按钮 - 手机号
            # self.driver.find_element(By.ID, "com.coinstation.bixiang:id/btn_bindphone").screenshot("phone.png")
            # self.driver.find_element(By.ID, "com.coinstation.bixiang:id/btn_bindphone").click()
            button = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/btn_bindphone')))
            button.click()
            time.sleep(random.randint(2, 3))

            # 输入手机号
            # phone = self.driver.find_element(By.ID, "com.coinstation.bixiang:id/et_phone")
            phone = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/et_phone')))
            phone.send_keys(ym.get_phone())
            time.sleep(random.randint(2, 3))

            # 点击获取短信验证码
            # 步骤一：先点击按钮，弹出没有缺口的图片
            # self.driver.find_element(By.ID, "com.coinstation.bixiang:id/btn_sendsms").click()
            button = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/btn_sendsms')))
            button.click()
            logger.warning(">>>>>>>>>> 1. 开始进行滑块验证。")

            # cons1 = self.driver.contexts
            # webview = self.driver.contexts.last
            # self.driver.switch_to_alert()
            # self.driver.switch_to('WEBVIEW_com.coinstation.bixiang')
            # self.driver.switch_to_window()

            # print(self.driver.current_context)
            # print(self.driver.current_url)
            # print(self.driver.current_window_handle)

            # views = self.driver.find_element(By.CLASS_NAME, 'android.view.View')
            # for i in range(len(views)):
            #     print(">>>>> " + views[i].id)
            #     print(">>>>> " + views[i].text)

            # 方法一：driver.switch_to.context("NATIVE_APP")   # 这个NATIVE_APP是固定的参数
            # 方法二：driver.switch_to.context(contexts[0])      # 从contexts里取第一个参数

            # 当没有通过滑块验证时，循环多次进行验证

            # 步骤八：滑块验证通过，短信登录
            time.sleep(10)

            sms_code = ym.get_sms()

            # 输入短信验证码
            # sms = self.driver.find_element_by_id("com.coinstation.bixiang:id/et_sms")
            sms = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/et_sms')))
            sms.send_keys(sms_code)
            logger.warning(">>>>>>>>>> 2. 短信验证码: " + sms_code)

            # 点击“绑定”按钮
            # self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_save").click()
            button = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/btn_save')))
            button.click()
            logger.warning(">>>>>>>>>> 3. 收到短信，完成登录。 ")
            time.sleep(random.randint(3, 5))
            ym.release_phoneNumber()

            # 关闭，返回
            # self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_back").click()
            button = wait.until(EC.presence_of_element_located((By.ID, 'com.coinstation.bixiang:id/btn_back')))
            button.click()

            return 0


        except Exception as e:
            print(e)
            return -1
        # finally:
        #     self.driver.close()

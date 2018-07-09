# coding=utf-8
import configparser
import datetime
import logging
import os
import random
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("web_coineal_two_account_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/web_coineal_two_account_class.log', mode='w')
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
    config_data = None
    price_data = None

    def __init__(self, account):
        logger.warning("start __init__...")
        self.load_config_data(account)
        self.login(self.config_data['phone'], self.config_data['password'])

    def load_config_data(self, account):
        # get config information
        curpath = os.getcwd()
        content = open(curpath + '/coineal/web_config_two_account.ini').read()
        content = re.sub(r"\xfe\xff", "", content)
        content = re.sub(r"\xff\xfe", "", content)
        content = re.sub(r"\xef\xbb\xbf", "", content)
        open(curpath + '/coineal/web_config_two_account.ini', 'w').write(content)

        cf = configparser.ConfigParser()
        cf.read(curpath + '/coineal/web_config_two_account.ini')
        ETH_Price = cf.get(account, 'ETH_Price').strip()
        Deal_Quota = cf.get(account, 'Deal_Quota').strip()
        phone = cf.get(account, 'phone').strip()
        password = cf.get(account, 'password').strip()
        cancel_order_flag = cf.get(account, 'cancel_order_flag').strip()
        cancel_order_timeout = cf.get(account, 'cancel_order_timeout').strip()
        delta = cf.get(account, 'delta').strip()

        self.config_data = {'ETH_Price': ETH_Price, 'Deal_Quota': Deal_Quota, 'phone': phone, 'password': password,
                            'cancel_order_flag': cancel_order_flag, 'cancel_order_timeout': cancel_order_timeout,
                            'delta': delta}

    def isElementExist_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except Exception as e:
            # print(e)
            return False

    def waitForPageLoad(self):
        STR_READY_STATE = ''
        # 而直接操作页面就需要类似于下面的代码等待页面加载完成
        while STR_READY_STATE != 'complete':
            time.sleep(0.001)
            STR_READY_STATE = self.driver.execute_script('return document.readyState')
            logger.warning(('STR_READY_STATE : %s', STR_READY_STATE))

    def login(self, phone, password):
        try:
            # chrome_options = Options()
            # option.add_argument('headless')
            # chrome_options.add_argument('--kiosk')
            # chrome_options = Options()
            # chrome_options.add_argument("start-fullscreen")
            # self.driver = webdriver.Chrome(chrome_options=chrome_options)
            # self.driver.manage().window().Fullscreen()

            # self.driver = webdriver.Chrome()

            # self.driver = webdriver.Firefox()


            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.startup.homepage", "about:blank")
            profile.set_preference("startup.homepage_welcome_url", "about:blank")
            profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")

            # options = webdriver.FirefoxOptions()
            # options.add_argument('-headless')
            # options.add_argument(profile)
            # options.add_argument("extensions.logging.enabled", False)
            # self.driver = webdriver.Firefox(firefox_options=options)
            self.driver = webdriver.Firefox(profile)

            self.driver.set_window_size(1600, 2560)
            self.driver.set_window_position(y=0, x=0)

            self.driver.get('https://www.coineal.com/#zh_CN')

            wait = WebDriverWait(self.driver, 60)

            xpath_login = '//*[@id="userUnLogin"]/a[2]'
            login = wait.until(EC.presence_of_element_located((By.XPATH, xpath_login)))
            login.click()

            xpath_phone = '//*[@id="loginDiv"]/ul/li[2]/div/span[1]/input[2]'
            input_phone = wait.until(EC.presence_of_element_located((By.XPATH, xpath_phone)))
            input_phone.clear()
            input_phone.send_keys(phone)
            time.sleep(random.random())

            xpath_password = '//*[@id="loginDiv"]/ul/li[4]/input'
            input_password = wait.until(EC.presence_of_element_located((By.XPATH, xpath_password)))
            input_password.clear()
            input_password.send_keys(password)
            time.sleep(random.random())

            xpath_slide = '//*[@id="nc_1_n1z"]'
            slide = wait.until(EC.presence_of_element_located((By.XPATH, xpath_slide)))
            # 在元素上执行按下鼠标左键，并保持
            # ActionChains(self.driver).click(slide).perform()
            ActionChains(self.driver).click_and_hold(slide).perform()
            ActionChains(self.driver).move_by_offset(xoffset=300, yoffset=0).perform()
            time.sleep(random.random())

            xpath_loginbutton = '//*[@id="login-submit-phone-id"]'
            button_login = wait.until(EC.presence_of_element_located((By.XPATH, xpath_loginbutton)))
            button_login.click()
            time.sleep(random.randint(5, 8))

            xpath_sms = '//*[@id="smsAuthCode"]'
            xpath_sms_link = '//*[@id="code"]'
            xpath_confirm_button = '/html/body/div[11]/div/ul/div/a[2]'
            if self.isElementExist_by_xpath(xpath_sms):
                pass
                input_sms = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sms)))
                input_sms.clear()
                input_sms.send_keys(phone)
                button_sms = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sms_link)))
                button_sms.click()

                time.sleep(3)

                sms = input("********** Enter your sms: ")
                logger.warning('********** SMS input is: ' + sms)
                input_sms = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sms)))
                input_sms.clear()
                input_sms.send_keys(sms)

                time.sleep(1)

                button_sms = wait.until(EC.presence_of_element_located((By.XPATH, xpath_confirm_button)))
                button_sms.click()

            logger.warning("********** login success!")
            return 0

        except Exception as e:
            print(e)
            return -1

    def load_coin(self):

        wait = WebDriverWait(self.driver, 60)

        try:

            logger.warning("********** Loading coin ......")

            # 点击“交易中心”
            # xpath_trade = '//*[@id="headerTab"]/li[2]/a'
            # trade_center = wait.until(EC.presence_of_element_located((By.XPATH, xpath_trade)))
            # trade_center.click()
            # time.sleep(5)
            # trade_center.click()
            # time.sleep(5)
            self.driver.find_element(By.LINK_TEXT, "交易中心").click()
            self.waitForPageLoad()

            # 点击“ETH”
            id_eth = 'market-eth'
            myMarket = wait.until(EC.presence_of_element_located((By.ID, id_eth)))
            myMarket.click()
            time.sleep(5)
            myMarket.click()
            time.sleep(5)
            self.waitForPageLoad()

            # "NEAL/ETH"
            id_mteth = 'symbots-nealeth'
            mteth = wait.until(EC.presence_of_element_located((By.ID, id_mteth)))
            mteth.click()
            time.sleep(5)
            mteth.click()
            time.sleep(15)
            self.waitForPageLoad()

        except Exception as e:
            self.driver.refresh()
            self.waitForPageLoad()
            print(e)

    def get_price(self):
        # 0 无挂单， -1有挂单
        flag = 0

        wait = WebDriverWait(self.driver, 60)
        (countCoinBalance, baseCoinBalance) = self.get_balance()

        try:

            logger.warning("\n")
            logger.warning("========== Refreshing price ......")

            # 撤单
            # (ETH_Price, Deal_Quota, phone, password, cancel_order_flag, cancel_order_timeout)
            xpath_order = '//*[@id="my_entrty_bottom"]/div[2]/div[1]'
            if self.isElementExist_by_xpath(xpath_order):
                # 有挂单
                flag = -1

                buy_or_sell = self.driver.find_element(By.XPATH, '//*[@id="my_entrty_bottom"]/div[2]/div[2]').text
                deal_price = self.driver.find_element(By.XPATH, '//*[@id="my_entrty_bottom"]/div[2]/div[3]').text
                amount = self.driver.find_element(By.XPATH, '//*[@id="my_entrty_bottom"]/div[2]/div[4]').text
                has_dealed = self.driver.find_element(By.XPATH, '//*[@id="my_entrty_bottom"]/div[2]/div[5]').text
                logger.warning("========== 挂  单: [" + str(buy_or_sell) + "] [价:" + str(deal_price) + "] [数量:"
                               + str(amount) + "] [已成:" + str(has_dealed) + "]")

                order_time = self.driver.find_element(By.XPATH, xpath_order).text
                order_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(' ')[0]
                order_datetime = order_date + ' ' + order_time
                # logger.warning("========== order_datetime = " + str(order_datetime))

                st = datetime.datetime.strptime(order_datetime, "%Y-%m-%d %H:%M:%S")
                dt = datetime.datetime.now()

                if str(self.config_data['cancel_order_flag']) == 'True':
                    if (int((dt - st).seconds) > int(self.config_data['cancel_order_timeout'])):
                        self.driver.find_element(By.LINK_TEXT, "撤单").click()
                        # 撤销挂单
                        flag = 0
                        logger.warning("========== order_datetime = " + str(order_datetime) + ", 已撤单。")

            # 买余额
            # xpath_buy_balance = '//*[@id="price_bottom"]/div[1]/div[1]/span[2]/s'
            # buy_balance = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy_balance))).text
            buy_balance = countCoinBalance

            # 卖余额
            # xpath_sell_balance = '//*[@id="price_bottom"]/div[2]/div[1]/span[2]/s'
            # sell_balance = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell_balance))).text
            sell_balance = baseCoinBalance

            # 获取交易均价
            xpath_avg_price = '//*[@id="depTrade"]/div[2]/div[2]/span[2]'
            avg_price_value = wait.until(EC.presence_of_element_located((By.XPATH, xpath_avg_price))).text

            # 卖一
            xpath_sell01 = '//*[@id="depTrade"]/div[2]/div[1]/div/div[150]/div[2]/s[1]'
            sell01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell01))).text

            # 买一
            xpath_buy01 = '//*[@id="depTrade"]/div[2]/div[3]/div/div[1]/div[2]/s[1]'
            buy01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy01))).text

            logger.warning("========== 均  价: " + avg_price_value)
            logger.warning("========== 买一价: " + str(buy01) + ", 卖一价: " + str(sell01))
            logger.warning("========== 买余额: " + str(buy_balance) + ", 卖余额: " + str(sell_balance))

            avg_price_value = avg_price_value.strip()
            # buy_balance = buy_balance.split(' ')[0].strip()
            # sell_balance = sell_balance.split(' ')[0].strip()

            self.price_data = {'avg_price_value': avg_price_value, 'sell_balance': sell_balance,
                               'buy_balance': buy_balance,
                               'sell01': sell01, 'buy01': buy01}

            return flag

        except Exception as e:
            print(e)
            self.driver.refresh()
            self.waitForPageLoad()
            return -1

    def account_balance(self, sign):
        # sign = buy or sell

        wait = WebDriverWait(self.driver, 60)

        if sign == 'buy':

            if self.price_data['buy_balance'] > self.config_data['Deal_Quota']:
                pass
            else:
                # ETH不够，需要卖出NEAL
                self.driver.find_element(By.LINK_TEXT, "市价交易").click()

                # 输入数量
                input_amount = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="getBaseCoin"]')))
                input_amount.clear()
                # input_amount.send_keys(str(amount))

                # 交易按钮
                trade_button = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="maket_deal"]/div[2]/button')))
                # trade_button.click()
        else:
            if self.price_data['sell_balance'] > self.config_data['Deal_Quota'] / self.price_data['avg_price_value']:
                pass
            else:
                # NEAL不够卖，需要买入NEAL
                self.driver.find_element(By.LINK_TEXT, "市价交易").click()

                # 输入数量
                input_amount = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="getCountCoin"]')))
                input_amount.clear()
                # input_amount.send_keys(str(amount))

                # 交易按钮
                trade_button = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="maket_deal"]/div[1]/button/span')))
                # trade_button.click()

    def buy(self, price, amount):

        wait = WebDriverWait(self.driver, 60)

        try:

            self.driver.find_element(By.LINK_TEXT, "限价交易").click()

            # 卖一
            # xpath_sell01 = '//*[@id="depTrade"]/div[2]/div[1]/div/div[150]/div[2]/s[1]'
            # sell01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell01))).text

            # 买一
            # xpath_buy01 = '//*[@id="depTrade"]/div[2]/div[3]/div/div[1]/div[2]/s[1]'
            # buy01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy01))).text

            # if (float(sell01) - float(buy01) >= 0.00000002):
            #     price = str('{:.8f}'.format(float(buy01) + 0.00000002))
            # else:
            #     price = str('{:.8f}'.format(float(buy01)))

            # 输入价格
            input_price = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getCountPrice"]')))
            input_price.clear()
            input_price.send_keys(price)

            # 买余额
            # xpath_buy_balance = '//*[@id="price_bottom"]/div[1]/div[1]/span[2]/s'
            # buy_balance = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy_balance))).text
            # buy_balance = buy_balance.split(' ')[0].strip()
            # amount = round(float(buy_balance)/float(buy01), 4)

            # amount = str(int(float(buy_balance) / float(price)))

            # 输入数量
            input_amount = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getCountCoin"]')))
            input_amount.clear()
            input_amount.send_keys(str(amount))

            # 交易按钮
            trade_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="price_bottom"]/div[1]/button')))
            # trade_button.click()
            # self.driver.implicitly_wait(5)

            logger.warning("<<<<<<<<<< buy, price=" + str(price) + ", amount=" + str(amount))

            return 0
        except Exception as e:
            print(e)
            return -1

    def sell(self, price, amount):

        wait = WebDriverWait(self.driver, 60)

        try:

            self.driver.find_element(By.LINK_TEXT, "限价交易").click()

            # 卖一
            # xpath_sell01 = '//*[@id="depTrade"]/div[2]/div[1]/div/div[150]/div[2]/s[1]'
            # sell01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell01))).text

            # 买一
            # xpath_buy01 = '//*[@id="depTrade"]/div[2]/div[3]/div/div[1]/div[2]/s[1]'
            # buy01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy01))).text

            # if (float(sell01) - float(buy01) >= 0.00000002):
            #     price = str('{:.8f}'.format(float(sell01) - 0.00000002))
            # else:
            #     price = str('{:.8f}'.format(float(sell01)))

            # 输入价格
            input_price = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getBasePrice"]')))
            input_price.clear()
            input_price.send_keys(price)

            # 卖余额
            # xpath_sell_balance = '//*[@id="price_bottom"]/div[2]/div[1]/span[2]/s'
            # sell_balance = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell_balance))).text
            # sell_balance = sell_balance.split(' ')[0].strip()
            # amount = round(float(sell_balance), 4)

            # 输入数量
            input_amount = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getBaseCoin"]')))
            input_amount.clear()
            input_amount.send_keys(str(amount))

            # 交易按钮
            trade_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="price_bottom"]/div[2]/button')))
            # trade_button.click()
            # self.driver.implicitly_wait(5)

            logger.warning(">>>>>>>>>> sell, price=" + str(price) + ", amount=" + str(amount))

            return 0
        except Exception as e:
            print(e)
            return -1

    def get_balance(self):

        url = "https://www.coineal.com/web/account/symbol/balance?symbol=nealeth"

        try:

            cookies = self.driver.get_cookies()
            s = requests.Session()
            for cookie in cookies:
                s.cookies.set(cookie['name'], cookie['value'])

            # self.driver.get(url)
            # response = requests.get(url)
            response = s.get(url)

            res = response.json()["code"]

            if res == '0':
                countCoinBalance = response.json()["data"]['countCoinBalance']
                baseCoinBalance = response.json()["data"]['baseCoinBalance']
                # logger.warning(">>>>>>>>>> get_balance success.")
                return countCoinBalance, baseCoinBalance
            else:
                logger.warning(">>>>>>>>>> get_balance error.")
                return -1, -1

        except Exception as e:
            print(e)
            return -1, -1

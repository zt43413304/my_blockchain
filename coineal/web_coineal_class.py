# coding=utf-8
import logging
import os
import random
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("web_coineal_class.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/web_coineal_class.log', mode='w')
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

    def login(self, phone, password):
        try:
            # chrome_options = Options()
            # option.add_argument('headless')
            # chrome_options.add_argument('--kiosk')
            # chrome_options = Options()
            # chrome_options.add_argument("start-fullscreen")
            # self.driver = webdriver.Chrome(chrome_options=chrome_options)
            # self.driver.manage().window().Fullscreen()

            self.driver = webdriver.Firefox()
            # self.driver = webdriver.Chrome()

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

            logger.warning(">>>>>>>>>> login success!")
            return 0

        except Exception as e:
            print(e)
            return -1

    def load_coin(self):

        wait = WebDriverWait(self.driver, 60)

        try:

            logger.warning("========== Loading coin ......")

            # 点击“交易中心”
            xpath_trade = '//*[@id="headerTab"]/li[2]/a'
            trade_center = wait.until(EC.presence_of_element_located((By.XPATH, xpath_trade)))
            trade_center.click()
            time.sleep(random.randint(8, 10))

            # 点击“ETH”
            id_eth = 'market-eth'
            myMarket = wait.until(EC.presence_of_element_located((By.ID, id_eth)))
            myMarket.click()
            time.sleep(random.randint(3, 5))

            # "NEAL/ETH"
            id_mteth = 'symbots-nealeth'
            mteth = wait.until(EC.presence_of_element_located((By.ID, id_mteth)))
            mteth.click()
            time.sleep(random.randint(3, 5))


        except Exception as e:
            print(e)

    def get_price(self):

        wait = WebDriverWait(self.driver, 60)

        try:

            logger.warning("\n")
            logger.warning("========== Refreshing price ......")

            # 买余额
            xpath_buy_balance = '//*[@id="price_bottom"]/div[1]/div[1]/span[2]/s'
            buy_balance = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy_balance))).text

            # 卖余额
            xpath_sell_balance = '//*[@id="price_bottom"]/div[2]/div[1]/span[2]/s'
            sell_balance = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell_balance))).text

            # 获取交易均价
            xpath_avg_price = '//*[@id="depTrade"]/div[2]/div[2]/span[2]'
            avg_price_value = wait.until(EC.presence_of_element_located((By.XPATH, xpath_avg_price))).text

            # 卖一
            xpath_sell01 = '//*[@id="depTrade"]/div[2]/div[1]/div/div[150]/div[2]/s[1]'
            sell01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell01))).text

            # 买一
            xpath_buy01 = '//*[@id="depTrade"]/div[2]/div[3]/div/div[1]/div[2]/s[1]'
            buy01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy01))).text

            logger.warning("========== 当前均价: " + avg_price_value)
            logger.warning("========== 卖一价: " + str(sell01) + ", 买一价: " + str(buy01))
            logger.warning("========== 卖余额: " + str(sell_balance) + ", 买余额: " + str(buy_balance))

            avg_price_value = avg_price_value.strip()
            buy_balance = buy_balance.split(' ')[0].strip()
            sell_balance = sell_balance.split(' ')[0].strip()

            return avg_price_value, sell_balance, buy_balance, sell01, buy01

        except Exception as e:
            print(e)
            return -1, -1, -1, -1, -1

    def buy(self, amount):

        wait = WebDriverWait(self.driver, 60)

        try:
            # 买一
            xpath_buy01 = '//*[@id="depTrade"]/div[2]/div[3]/div/div[1]/div[2]/s[1]'
            buy01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy01))).text
            price = str('{:.8f}'.format(float(buy01) + 0.00000003))

            # 输入价格
            input_price = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getCountPrice"]')))
            input_price.clear()
            input_price.send_keys(price)

            # 输入数量
            input_amount = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getCountCoin"]')))
            input_amount.clear()
            input_amount.send_keys(amount)

            # 交易按钮
            trade_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="price_bottom"]/div[1]/button')))
            # self.driver.implicitly_wait(10)
            # trade_button.click()

            logger.warning("<<<<<<<<<< buy , price=" + str(price) + ", amount=" + str(amount))

            return 0
        except Exception as e:
            print(e)
            return -1

    def sell(self, amount):

        wait = WebDriverWait(self.driver, 60)

        try:
            # 卖一
            # xpath_sell01 = '//*[@id="depTrade"]/div[2]/div[1]/div/div[150]/div[2]/s[1]'
            # sell01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_sell01))).text
            # price = str('{:.8f}'.format(float(sell01) - 0.00000001))

            # 买一
            xpath_buy01 = '//*[@id="depTrade"]/div[2]/div[3]/div/div[1]/div[2]/s[1]'
            buy01 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_buy01))).text
            price = str('{:.8f}'.format(float(buy01) + 0.00000002))

            # 输入价格
            input_price = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getBasePrice"]')))
            input_price.clear()
            input_price.send_keys(price)

            # 输入数量
            input_amount = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="getBaseCoin"]')))
            input_amount.clear()
            input_amount.send_keys(amount)

            # 交易按钮
            trade_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="price_bottom"]/div[2]/button')))
            # self.driver.implicitly_wait(10)
            # trade_button.click()

            logger.warning("<<<<<<<<<< buy , price=" + str(price) + ", amount=" + str(amount))

            return 0
        except Exception as e:
            print(e)
            return -1

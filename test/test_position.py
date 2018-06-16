# coding=utf-8

import logging
import random
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("test_position.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/test_position.log', mode='w')
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


class lands:
    def __init__(self):
        logger.warning("********** start __init()__...")
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # self.driver = webdriver.Chrome(chrome_options=option)

        # driver = webdriver.Chrome()
        # # driver = webdriver.PhantomJS()
        # driver.get('https://www.baidu.com/')
        # print('打开浏览器')
        # print(driver.title)
        # driver.find_element_by_id('kw').send_keys('测试')
        # print('关闭')
        # driver.quit()
        # print('测试完成')

        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Safari()
        # driver.maximize_window()
        self.driver.set_window_size(480, 750)
        self.driver.set_window_position(y=0, x=0)

    def selenium_login(self, phone, password):
        try:
            self.driver.get('https://game.hashworld.top/#!/login')
            wait = WebDriverWait(self.driver, 10)
            self.get_page_pic()

            input_phone = self.driver.find_element(By.XPATH, '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/div[1]/hw-input/div/input')
            input_phone.clear()
            input_phone.send_keys(phone[-11:])
            time.sleep(random.randint(1, 3))

            input_password = self.driver.find_element(By.XPATH, '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/div[2]/hw-input/div/input')
            input_password.clear()
            input_password.send_keys(password)
            time.sleep(random.randint(1, 3))

            button_login = self.driver.find_element(By.XPATH, '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/button')
            button_login.click()
            time.sleep(random.randint(1, 3))

            logger.warning(">>>>>>>>>> login success!")

            self.get_page_pic()
            # self.get_element_pic()

            self.driver.close()
            return 0
        except Exception as e:
            print(e)
            return -1

    def get_page_pic(self):
        self.driver.save_screenshot('screenshot1.png')

        element = self.driver.find_element_by_tag_name("body")
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        print("get_page_pic >>>>>>>")
        print(left, top, right, bottom)

        im = Image.open('screenshot1.png')
        logger.warning(
            "********** 1. size, width=" + str(im.size[0]) + ", height=" + str(
                im.size[1]))

        # im = im.crop((left, top, right, bottom))
        im = im.crop((left * 2, top * 2, right * 2, bottom * 2))
        im.save('screenshot_body.png')
        logger.warning(
            "********** 2. size, width=" + str(im.size[0]) + ", height=" + str(
                im.size[1]))


    def get_element_pic(self):
        self.driver.save_screenshot('screenshot2.png')

        # element = self.driver.find_element_by_tag_name("body")
        element = self.driver.find_element(By.XPATH, '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/button')
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        print("get_element_pic >>>>>>>")
        print(left, top, right, bottom)

        im = Image.open('screenshot2.png')
        # im = im.crop((left, top, right, bottom))
        # im = im.crop((176, 712, 787, 925))
        im = im.crop((left * 2, top * 2, right * 2, bottom * 2))
        im.save('screenshot_element.png')



lands = lands()
result = lands.selenium_login('18522505438', 'Liuxb0504')

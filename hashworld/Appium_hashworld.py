# coding=utf-8

import logging
import random
import sys
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("Appium_hashworld.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/Appium_hashworld.log', mode='w')
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
    MIN_SEC = 15
    MAX_SEC = 20

    def __init__(self):
        logger.warning("********** start __init()__...")

        # driver = webdriver.Chrome()
        # # driver = webdriver.PhantomJS()
        # driver.get('https://www.baidu.com/')
        # print('打开浏览器')
        # print(driver.title)
        # driver.find_element_by_id('kw').send_keys('测试')
        # print('关闭')
        # driver.quit()
        # print('测试完成')


        # chrome_options = webdriver.ChromeOptions()
        # mobile_emulation = {"deviceName": "iPhone 6/7/8 Plus"}
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        # self.driver = webdriver.Chrome(chrome_options = chrome_options)

        # firefox_options = webdriver.FirefoxOptions()
        # firefox_options.set_preference("mobileEmulation", mobile_emulation)
        # self.driver = webdriver.Firefox(firefox_options=firefox_options)



    def get_snap(self):
        '''
        对整个网页截图，保存成图片，然后用PIL.Image拿到图片对象
        :return: 图片对象
        '''
        rq = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        name = './logs/page_%s.png' % rq
        self.driver.save_screenshot(name)
        page_snap_obj = Image.open(name)
        return page_snap_obj

    def get_image(self, rate):
        '''
        从网页的网站截图中，截取验证码图片
        :return: 验证码图片
        '''
        wait = WebDriverWait(self.driver, 180)
        time.sleep(2)  # 保证图片刷新出来
        # print(self.driver.page_source)
        # img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        img = self.driver.find_element(By.XPATH, '//*[@id="nc_1_canvas"]')
        # img = self.driver.find_element(By.CLASS_NAME, 'nc_1_canvas.nc-canvas-node')
        location = img.location
        size = img.size
        print(size)

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # top = 0
        rate = 2
        print(left, top, right, bottom)
        print(left * rate, top * rate, right * rate, bottom * rate)
        page_snap_obj = self.get_snap()
        # 由于浏览器基于屏幕分辨率的自动缩放功能，截图图片和网页实际大小可能不同，所以需要乘以一个比例
        # crop_imag_obj = page_snap_obj.crop((left * rate, top * rate, right * rate, bottom * rate))

        # crop_imag_obj0 = page_snap_obj.crop((314, 778, 896, 962))
        crop_imag_obj0 = page_snap_obj.crop((left * rate, top * rate, right * rate, bottom * rate))
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        crop_imag_obj0.save('./logs/snap0_%s.png' % rq)

        crop_imag_obj = page_snap_obj.crop((left, top * rate, right * rate, top * rate + size['height'] * rate))
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        crop_imag_obj.save('./logs/snap_%s.png' % rq)

        return crop_imag_obj

    def isElementExist_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except Exception as e:
            print(e)
            return False

    def isElementExist_by_classname(self, classname):
        try:
            self.driver.find_element(By.CLASS_NAME, classname)
            return True
        except Exception as e:
            print(e)
            return False

    def isElementExist_by_id(self, id):
        try:
            self.driver.find_element_by_id(id)
            return True
        except Exception as e:
            print(e)
            return False

    def my_find_elements_by_classname(self, classname, name):
        wait = WebDriverWait(self.driver, 180)
        # android.widget.TextView
        views = self.driver.find_elements(By.CLASS_NAME, classname)
        # views = wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        for i in range(len(views)):
            if views[i].text == name:
                return views[i]

    def my_find_elements_by_classname_instance(self, classname, instance):
        # android.widget.TextView
        views = self.driver.find_elements(By.CLASS_NAME, classname)
        return views[instance]

    def get_rate(self):
        # 计算网页缩放比，部分浏览器会根据屏幕分辨率自动缩放网页，所以图片中滑块的距离和网页中需要拖动的距离可能不同
        body = self.driver.find_element_by_tag_name("body")

        page_snap_obj = self.get_snap()
        rate = page_snap_obj.size[0] / body.size['width']
        logger.warning(
            "********** HTML body size, width=" + str(body.size['width']) + ", height=" + str(body.size['height']))
        logger.warning(
            "********** Rendered body size, width=" + str(page_snap_obj.size[0]) + ", height=" + str(
                page_snap_obj.size[1]))
        logger.warning("********** Body change rate = " + str(rate))
        return rate

    # 此方法是关闭当前窗口，或最后打开的窗口
    def selenium_close(self):
        self.driver.close()

    # 执行这个方法后，driver会关闭所有关联窗口
    def selenium_quit(self):
        self.driver.quit()

    def get_page_pic(self):

        self.driver.save_screenshot('screenshot1.png')

        element = self.driver.find_element_by_tag_name("body")
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']

        im = Image.open('screenshot1.png')
        im = im.crop((left, top, right, bottom))
        im.save('screenshot_body.png')
        print("get_page_pic >>>>>>>")
        print(left, top, right, bottom)

    def get_element_pic(self):

        self.driver.save_screenshot('screenshot2.png')

        # element = self.driver.find_element_by_tag_name("body")
        element = self.driver.find_element(By.XPATH, '//*[@id="nc_1_canvas"]')
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']

        im = Image.open('screenshot2.png')
        # im = im.crop((left, top, right, bottom))
        # im = im.crop((176, 712, 787, 925))
        im = im.crop((left * 2, top * 2, right * 2, bottom * 2))
        im.save('screenshot_element.png')
        print("get_element_pic >>>>>>>")
        print(left, top, right, bottom)

    def selenium_login(self, phone, password):
        try:

            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            self.driver = webdriver.Firefox(firefox_options=options)

            # option = webdriver.ChromeOptions()
            # option.add_argument('headless')
            # driver = webdriver.Chrome(chrome_options=option)

            # self.driver = webdriver.Firefox()

            # self.driver = webdriver.Chrome()

            self.driver.set_window_size(480, 750)
            self.driver.set_window_position(y=0, x=0)
            self.driver.get('https://game.hashworld.top/#!/login')

            wait = WebDriverWait(self.driver, 180)

            xpath_phone = '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/div[1]/hw-input/div/input'
            input_phone = wait.until(EC.presence_of_element_located((By.XPATH, xpath_phone)))
            input_phone.clear()
            input_phone.send_keys(phone[-11:])
            time.sleep(random.random())

            xpath_password = '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/div[2]/hw-input/div/input'
            input_password = wait.until(EC.presence_of_element_located((By.XPATH, xpath_password)))
            input_password.clear()
            input_password.send_keys(password)
            time.sleep(random.random())

            xpath_login = '/html/body/ui-view/hw-login/hw-container/div/div[2]/hw-container-main/button'
            button_login = wait.until(EC.presence_of_element_located((By.XPATH, xpath_login)))
            button_login.click()
            time.sleep(random.randint(1, 2))

            logger.warning(">>>>>>>>>> login success!")
            return 0

        except Exception as e:
            print(e)
            return -1

    def selenium_clickland(self, block_number):

        try:
            self.driver.refresh()
            time.sleep(random.randint(2, 3))
            wait = WebDriverWait(self.driver, 180)

            xpath_strength = '/html/body/ui-view/hw-index/hw-tabbar/ui-view/hw-treasure/div/hw-treasure-list/div/div[2]/span[2]/span'
            web_strength = wait.until(EC.presence_of_element_located((By.XPATH, xpath_strength)))
            strength1 = web_strength.text.split('/')[0]
            logger.warning(">>>>>>>>>> selenium strength = " + str(strength1))

            # /html/body/ui-view/hw-index/hw-tabbar/ui-view/hw-treasure/div/hw-treasure-list/div/div[1]/hw-treasure-block[1]/div/div[3]/div[3]/div[2]/div[1]/div
            # /html/body/ui-view/hw-index/hw-tabbar/ui-view/hw-treasure/div/hw-treasure-list/div/div[1]/hw-treasure-block[2]/div/div[3]/div[3]/div[2]/div[1]/div
            # /html/body/ui-view/hw-index/hw-tabbar/ui-view/hw-treasure/div/hw-treasure-list/div/div[1]/hw-treasure-block[3]/div/div[3]/div[3]/div[2]/div[1]/div

            xpath_block = "/html/body/ui-view/hw-index/hw-tabbar/ui-view/hw-treasure/div/hw-treasure-list/div/div[1]/hw-treasure-block[" + \
                          str(block_number) + "]/div/div[3]/div[3]/div[2]/div[1]/div"
            block = wait.until(EC.presence_of_element_located((By.XPATH, xpath_block)))
            block.click()
            logger.warning(">>>>>>>>>> selenium click block......")
            time.sleep(random.randint(3, 5))

            xpath_box = '//*[@id="box"]'
            box = wait.until(EC.presence_of_element_located((By.XPATH, xpath_box)))
            box.click()
            logger.warning(">>>>>>>>>> selenium click box......")
            time.sleep(random.randint(3, 5))

            xpath_canvas = '//*[@id="nc_1_canvas"]'
            if self.isElementExist_by_xpath(xpath_canvas):
                canvas = wait.until(EC.presence_of_element_located((By.XPATH, xpath_canvas)))

                # 在元素上执行按下鼠标左键，并保持
                ActionChains(self.driver).click(canvas).perform()
                ActionChains(self.driver).click_and_hold(canvas).perform()
                ActionChains(self.driver).move_by_offset(xoffset=-130, yoffset=45).perform()
                # ActionChains(self.driver).move_by_offset(xoffset=5, yoffset=-80).perform()
                # ActionChains(self.driver).move_by_offset(xoffset=5, yoffset=80).perform()

                count = 0
                for track in range(25):
                    count += 1

                    if count % 2 == 0:
                        yoff = random.randint(70, 75)
                    else:
                        yoff = random.randint(70, 75) * -1

                    print(track, yoff)

                    ActionChains(self.driver).move_by_offset(xoffset=10, yoffset=yoff).perform()
                logger.warning(">>>>>>>>>> selenium click canvas......")
                time.sleep(random.randint(3, 5))

            xpath_playagain = '/html/body/ui-view/hw-treasure-result/div/button'
            if self.isElementExist_by_xpath(xpath_playagain):
                button_playagain = wait.until(EC.presence_of_element_located((By.XPATH, xpath_playagain)))
                button_playagain.click()
                logger.warning(">>>>>>>>>> selenium click playagain......")
                time.sleep(random.randint(3, 5))

            return 0
        except Exception as e:
            print(e)
            # sys.exit(0)
            return -1

# App_signup = Signup()
# App_signup.registry()

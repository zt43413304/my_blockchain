# coding=utf-8

import configparser
import json
import logging
import os
import random
import re
import sys
import time
import urllib
from urllib.parse import urlparse

import requests
import selenium
from PIL import Image
from appium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("Appium_bixiang.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/Appium_bixiang.log', mode='w')
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
content = open(curpath + '/bixiang/config_bixiang.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '/bixiang/config_bixiang.ini', 'w').write(content)

cf = configparser.ConfigParser()
cf.read(curpath + '/bixiang/config_bixiang.ini')
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


class Signup:
    MIN_SEC = 15
    MAX_SEC = 20
    rate = 1
    error_count = 0

    def __init__(self):
        logger.warning("********** start __init()__...")

    def get_html_driver(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['browserName'] = 'Chrome'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

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
            '/Users/Jackie.Liu/DevTools/Android_apk/bixiang-257-1.6.1-Y1032_AB62F32E80B15B0BD82AA1A199CE72CC.apk'
        )
        # desired_caps['app'] = PATH(
        #     'C:/Users/jacki/Documents/MuMu共享文件夹/bixiang-259-1.6.2-Y1032_2AAAD8832BFDECB47B656864157AE1ED.apk'
        # )
        desired_caps['appPackage'] = 'com.coinstation.bixiang'
        desired_caps['appActivity'] = 'com.coinstation.bixiang.view.activity.MainActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def isElementExist_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except Exception as e:
            # print(e)
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
        wait = WebDriverWait(self.driver, 10)
        time.sleep(2)  # 保证图片刷新出来
        # print(self.driver.page_source)
        img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        location = img.location
        size = img.size
        # print(size)

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        top = 65
        # print(left, top, right, bottom)
        # print(left * rate,top * rate,right * rate,bottom * rate)
        page_snap_obj = self.get_snap()
        # 由于浏览器基于屏幕分辨率的自动缩放功能，截图图片和网页实际大小可能不同，所以需要乘以一个比例
        # crop_imag_obj = page_snap_obj.crop((left * rate, top * rate, right * rate, bottom * rate))
        crop_imag_obj = page_snap_obj.crop((left * rate, top, right * rate, top + size['height'] * rate))
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        crop_imag_obj.save('./logs/snap_%s.png' % rq)

        return crop_imag_obj

    def is_pixel_equal(self, img1, img2, x, y):
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    def get_gap3(self, image1, image2, rate):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """

        left = int(70 * rate)
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                # print(">>>>> i="+str(i)+", j="+str(j))
                if not self.is_pixel_equal(image1, image2, i, j) \
                        and not self.is_pixel_equal(image1, image2, i + 50, j) \
                        and not self.is_pixel_equal(image1, image2, i, j + 50) \
                        and not self.is_pixel_equal(image1, image2, i + 50, j + 50):
                    left = i
                    return left - 6 * rate
        return left - 6 * rate

    def get_gap2(self, image1, image2, rate):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """

        left = int(100 * rate)
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                # print(">>>>> i="+str(i)+", j="+str(j))
                if not self.is_pixel_equal(image1, image2, i, j) \
                        and not self.is_pixel_equal(image1, image2, i, j + 20) \
                        and not self.is_pixel_equal(image1, image2, i, j + 40) \
                        and not self.is_pixel_equal(image1, image2, i, j + 60):
                    left = i
                    return left - 6 * rate
        return left - 6 * rate

    def get_gap(self, img1, img2, rate):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :param rate: 网页缩放比
        :return:
        """
        left = int(57.5 * rate)
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left - 6 * rate
        return left - 6 * rate

    def get_tracks2(self, distance):
        # 移动距离的列表
        track = []
        # 当前距离
        current = 0
        # 改变加速度的时间点
        mid = distance * 3 / 5
        # 计算移动距离所需的时间间隔
        t = 0.3
        # 速度
        speed = 0

        while current < distance:
            if current < mid:
                a = 3
                # 距离的计算公式
                move_distance = speed * t + 0.5 * a * t * t
                # 将生成的移动距离添加到列表中
                track.append(round(move_distance))
                speed += (a * t)
                current += move_distance
            else:
                # 当距离大于五分之三的position时，添加减速轨迹，并跳出循环
                track.extend([3, 3, 2, 2, 1, 1])
                break
        # 识别当前总共移动距离是大于还是小于position
        # 大于则补连续的-1，小于则补连续的1
        offset = int(sum(track) - distance)
        print(">>>>> offset=" + str(offset))
        if offset > 0:
            track.extend([-1 for i in range(offset)])
        elif offset < 0:
            track.extend([1 for i in range(abs(offset))])

        # 模拟终点附近的左右移动
        track.extend(
            [0, 1, -1, 0])
        logger.warning("********** 4. 计算轨迹后，偏差值 = " + str(sum(track) - distance))
        return track

    def get_tracks1(self, distance):
        '''
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+½at²
        ③v²-v0²=2as
        :param distance: 需要移动的距离
        :return: 存放每0.3秒移动的距离
        '''
        v = 0
        t = 0.3
        tracks = []
        current = 0
        mid = distance * 4 / 5

        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 3
            else:
                a = -3
            v0 = v
            s = v0 * t + 0.5 * a * (t ** 2)
            current += s
            tracks.append(round(s))
            v = v0 + a * t
        return tracks

    def get_tracks3(self, distance):
        len_ori = distance
        # pass
        tracks = [0, 0]
        # 间隔通过随机范围函数来获得,每次移动一步或者两步
        x = random.randint(1, 3)
        # 生成轨迹并保存到list内
        while distance - x >= 5:
            tracks.append(x)
            distance = distance - x
            x = random.randint(3, 6)
        # 最后五步都是一步步移动
        for i in range(int(distance)):
            tracks.append(1)

        # 识别当前总共移动距离是大于还是小于position
        # 大于则补连续的-1，小于则补连续的1
        offset = int(sum(tracks) - len_ori)
        # print(">>>>> offset=" + str(offset))
        if offset > 0:
            tracks.extend([-1 for i in range(offset)])
        elif offset < 0:
            tracks.extend([1 for i in range(abs(offset))])

        # 模拟终点附近的左右移动
        tracks.extend(
            [0, 0, 1, -1, 0, 0])
        logger.warning("********** 4. 计算轨迹后，偏差值 = " + str(sum(tracks) - len_ori))

        return tracks

    def get_tracks(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 3 / 5
        # 计算间隔
        t = 0.3
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))

        # 识别当前总共移动距离是大于还是小于position
        # 大于则补连续的-1，小于则补连续的1
        offset = int(sum(track) - distance)
        print(">>>>> offset=" + str(offset))
        if offset > 0:
            track.extend([-1 for i in range(offset)])
        elif offset < 0:
            track.extend([1 for i in range(abs(offset))])

        # 模拟终点附近的左右移动
        track.extend([0, -1, 1])
        logger.warning("********** 4. 计算轨迹后，偏差值 = " + str(sum(track) - distance))
        return track

    def slide_button(self, tracks, rate):
        """
        获取缺口偏移量
        :param tracks: 轨迹
        :return: success
        """
        wait = WebDriverWait(self.driver, 10)
        slide = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
        # logger.warning(">>>>>>>>>> 5. 滑动验证前，滑块位置：" + str(slide.location))
        x1 = slide.location['x']

        # ActionChains(self.driver).click_and_hold(slide).perform()
        # for track in tracks:
        #     ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        # else:
        #     ActionChains(self.driver).move_by_offset(xoffset=2, yoffset=0).perform()  # 先移过一点
        #     ActionChains(self.driver).move_by_offset(xoffset=-2, yoffset=0).perform()  # 再退回来，是不是更像人了

        ActionChains(self.driver).click_and_hold(slide).perform()
        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=random.randint(-1, 1)).perform()
        else:
            ActionChains(self.driver).move_by_offset(xoffset=2, yoffset=random.randint(-1, 1)).perform()  # 先移过一点
            ActionChains(self.driver).move_by_offset(xoffset=-2,
                                                     yoffset=random.randint(-1, 1)).perform()  # 再退回来，是不是更像人了

        time.sleep(random.random())
        ActionChains(self.driver).release().perform()
        # logger.warning(">>>>>>>>>> 5. 滑动验证后，滑块位置：" + str(slide.location))
        x2 = slide.location['x']

        logger.warning(">>>>>>>>>> 5. 滑动距离 = " + str(x2 - x1) + ", Rendered 滑动距离 = " + str((x2 - x1) * rate))

        try:
            time.sleep(5)
            webelement = wait.until(EC.presence_of_element_located((By.ID, 'getCode')))
            result = webelement.get_attribute("value")
            # result = driver.find_element(By.ID,'getCode').get_attribute("value")
            # print('++++++++++' + result)

            if '重新发送' in result:
                return True
            else:
                return False

        except Exception as f:
            print(f)
            return False

    def login_with_sms(self, sms_code):
        """
        打开网页输入用户名密码
        :return: None
        """
        wait = WebDriverWait(self.driver, 60)
        # self.driver.get(self.url)
        # phones = self.wait.until(EC.presence_of_element_located((By.ID, 'phones')))

        code2 = wait.until(EC.presence_of_element_located((By.ID, 'code2')))
        # phones.send_keys(self.phones)
        code2.send_keys(sms_code)
        wait.until(EC.presence_of_element_located((By.ID, 'download'))).click()
        logger.warning(">>>>>>>>>> 2. 短信验证码: " + sms_code)

    def my_find_elements_by_classname(self, classname, name):
        wait = WebDriverWait(self.driver, 60)
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

    def html_signup1(self, suma_phone, suma):
        global rate

        try:
            self.get_html_driver()
            # suma = my_suma.suma()

            logger.warning("********** suma_phone = " + suma_phone)

            # /Users/Jackie.Liu/DevTools/Selenium/chromedriver

            # driver = webdriver.Chrome()
            # driver.maximize_window()
            # self.driver.set_window_size(600, 800)
            # self.driver.set_window_position(y=0, x=0)

            self.driver.get('http://bixiang8.com/dz5vU')
            wait = WebDriverWait(self.driver, 10)
            phones = self.driver.find_element_by_id('phones')
            # code2 = driver.find_element_by_id('code2')
            phones.send_keys(suma_phone)
            # code2.send_keys('123456')

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

            result = self.driver.find_element(By.ID, 'getCode').get_attribute("value")
            # print('---' + result)

            # 步骤一：先点击按钮，弹出没有缺口的图片
            button = wait.until(EC.presence_of_element_located((By.ID, 'getCode')))
            button.click()

            # 当没有通过滑块验证时，循环多次进行验证
            geetest = False
            while not geetest:
                # 步骤二：拿到没有缺口的图片
                image1 = self.get_image(rate)
                logger.warning(
                    ">>>>>>>>>> 1. 没有缺口的图片. Rendered size = " + str(image1.size[0]) + " * " + str(image1.size[1]))

                # 步骤三：点击拖动按钮，弹出有缺口的图片
                button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
                button.click()

                # 步骤四：拿到有缺口的图片
                image2 = self.get_image(rate)
                logger.warning(
                    ">>>>>>>>>> 2. 有缺口的图片. Rendered size = " + str(image2.size[0]) + " * " + str(image2.size[1]))
                # print(image1.size, image2.size)

                # 步骤五：对比两张图片的所有RBG像素点，得到不一样像素点的x值，即要移动的距离
                gap = self.get_gap3(image1, image2, rate)
                logger.warning(">>>>>>>>>> 3. 缺口距离. Rendered gap = " + str(gap))

                # 步骤六：模拟人的行为习惯（先匀加速拖动后匀减速拖动），把需要拖动的总距离分成一段一段小的轨迹
                tracks = self.get_tracks3(gap / rate)
                print(tracks)

                result = self.driver.find_element(By.ID, 'getCode').get_attribute("value")
                # print('======' + result)

                # 步骤七：按照轨迹拖动，完全验证
                success = self.slide_button(tracks, rate)
                logger.warning(">>>>>>>>>> 5. 滑块验证结果. " + str(success))

                if success:
                    # 步骤八：滑块验证通过，短信登录
                    time.sleep(5)
                    suma_code = suma.getVcodeAndHoldMobilenum(suma_phone)

                    if suma_code == -1:
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1'))).click()
                        logger.warning(">>>>>>>>>> 8. 滑块验证成功，但未收到短信，重新验证. ")
                        logger.warning("\n")
                        geetest = False
                    else:
                        self.login_with_sms(suma_code)
                        logger.warning(">>>>>>>>>> 6. 滑块验证成功，短信登录. ")
                        # 退出循环
                        geetest = True
                else:
                    # 刷新再试
                    time.sleep(random.random())
                    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1')))
                    button.click()
                    logger.warning(">>>>>>>>>> 7. 滑块验证不成功，重新验证. ")
                    time.sleep(random.randint(3, 4))
                    logger.warning("\n")
                time.sleep(3)
            return 0
        except Exception as e:
            print(e)
            return -1
        finally:
            self.driver.close()

    def html_signup(self, ym, invite_url):
        global rate

        try:
            self.get_html_driver()

            logger.warning("********** html_signup(), suma_phone = " + ym.get_phone())

            # /Users/Jackie.Liu/DevTools/Selenium/chromedriver

            # driver = webdriver.Chrome()
            # driver.maximize_window()
            # self.driver.set_window_size(600, 800)
            # self.driver.set_window_position(y=0, x=0)

            # 输入手机号
            self.driver.get(invite_url)
            time.sleep(1)

            # 获取UID
            current_url = self.driver.current_url

            query_dict = urllib.parse.parse_qs(urlparse(current_url).query)
            uid = query_dict.get('uid', 'NA')[0]

            wait = WebDriverWait(self.driver, 10)
            phones = self.driver.find_element_by_id('phones')
            phones.send_keys(ym.get_phone())

            # 点击‘立即领取’，弹出滑块验证
            download = self.driver.find_element_by_id('download')
            download.click()

            # (gt, challenge) = self.getverify(uid)
            #
            # if gt != -1 and gt is not None and len(gt.strip()) != 0 \
            #         and challenge != -1 and challenge is not None and len(challenge.strip()) != 0:
            #     # call captcha hack
            #     (challenge, validate) = c2567.get_captcha(gt, challenge)
            #
            #     if challenge != -1 and validate != -1:
            #         self.post_with_captcha(86, ym.get_phone(), uid, challenge, validate)

            time.sleep(30)
            return 0

        except Exception as e:
            print(e)
            return -1
        finally:
            self.driver.close()

    def app_signup(self, ym):

        try:
            logger.warning("********** app_signup(), suma_phone = " + ym.get_phone())
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

    def quiz_app(self):
        pass
        # http://tui.yingshe.com/user/newtask?xxx=F3pHv1-IXGuea3pHt0u4e

        self.get_app_driver()
        cons = self.driver.contexts
        print(self.driver.current_context)

        # 右下角“我的”
        self.my_find_elements_by_classname('android.widget.TextView', '我的').click()

        print(self.driver.current_context)
        # cons = self.driver.contexts
        # appium.webdriver.switch_to(cons[1])
        # self.driver.switch_to(cons[1])

        handles = self.driver.window_handles
        for i in range(len(handles)):
            print(">>>>> " + handles[i].id)
            print(">>>>> " + handles[i].text)

        # print(self.driver.current_window_handle)

        views = self.driver.find_element(By.CLASS_NAME, 'android.widget.TextView')
        for i in range(len(views)):
            print(">>>>> " + views[i].id)
            print(">>>>> " + views[i].text)

    def quiz_by_html(self, quiz_url):
        try:
            self.get_html_driver()

            # logger.warning("********** quiz_by_html() ......")
            logger.warning('********** quiz_url = ' + quiz_url)

            # /Users/Jackie.Liu/DevTools/Selenium/chromedriver

            # driver = webdriver.Chrome()
            # driver.maximize_window()
            # self.driver.set_window_size(600, 800)
            # self.driver.set_window_position(y=0, x=0)

            self.driver.get(quiz_url)
            wait = WebDriverWait(self.driver, 10)

            # 第1题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[1]/input[1]')))
            button.click()
            logger.warning(">>>>>>>>>> 1. 完成第1题 ......")

            # 第2题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[2]/input[4]')))
            button.click()
            logger.warning(">>>>>>>>>> 2. 完成第2题 ......")

            # 第3题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[3]/input[4]')))
            button.click()
            logger.warning(">>>>>>>>>> 3. 完成第3题 ......")

            # 第4题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[4]/input[3]')))
            button.click()
            logger.warning(">>>>>>>>>> 4. 完成第4题 ......")

            # 第5题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[5]/input[1]')))
            button.click()
            logger.warning(">>>>>>>>>> 5. 完成第5题 ......")

            # 第6题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[6]/input[4]')))
            button.click()
            logger.warning(">>>>>>>>>> 6. 完成第6题 ......")

            # 第7题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[7]/input[2]')))
            button.click()
            logger.warning(">>>>>>>>>> 7. 完成第7题 ......")

            # 第8题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[8]/input[1]')))
            button.click()
            logger.warning(">>>>>>>>>> 8. 完成第8题 ......")

            # 第9题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[9]/input[1]')))
            button.click()
            logger.warning(">>>>>>>>>> 9. 完成第9题 ......")

            # 第10题
            time.sleep(random.randint(5, 7))
            button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[10]/input[4]')))
            button.click()
            logger.warning(">>>>>>>>>> 10. 完成第10题 ......")

            time.sleep(random.randint(1, 2))
            logger.warning("********** quiz complete ......")
            logger.warning('\n')

            # if self.isElementExist_by_id("com.coinstation.bixiang:id/btn_back"):
            #     self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_back").click()
            #
            # time.sleep(random.randint(1, 2))

            return 0

        except Exception as e:
            print(e)
            return -1
        finally:
            self.driver.close()

    def get_quiz_url(self, unique, uid):

        url = "http://tui.yingshe.com/member/miningBxc"

        payload_property = payload + "&unique=" + unique + "&uid=" + uid

        try:
            response = requests.request("POST", url, data=payload_property, headers=headers, timeout=60)
            activity_list = response.json()["info"]["activity"]

            for i in range(len(activity_list)):
                head = activity_list[i]["head"]
                status = activity_list[i]["status"]
                url = activity_list[i]["url"]

                if head == "币响知识小课堂":
                    return status, url
            return -1, -1
        except Exception as e:
            print(e)

            return -1, -1

    def bixiang_login(self, unique, uid):
        url = "http://tui.yingshe.com/check/index"

        payload_login = payload + "&unique=" + unique + "&uid=" + uid

        try:
            logger.warning("********** selenium_login()......")
            response = requests.request("POST", url, data=payload_login, headers=headers)

            res = response.json()["status"]
            if res == 1:
                logger.warning('********** Login success.')
                return 1
            else:
                logger.warning('********** Login fail. uid:' + uid)
                return -1
        except Exception as e:
            print(e)
            return -1

    def quiz_bixiang(self):
        # start
        logger.warning('********** Start from quiz_bixiang() ...')

        file = open(curpath + '/bixiang/data_bixiang_Seoul.json', 'r', encoding='utf-8')
        data_dict = json.load(file)

        for item in data_dict['data']:
            unique = item.get('unique', 'NA')
            uid = item.get('uid', 'NA')
            phone = item.get('phone', 'NA')

            logger.warning("========== Quizing [" + phone + "] ==========")

            # status = self.selenium_login(unique, uid)
            # if status != -1:
            #     (status, url) = self.get_quiz_url(unique, uid)
            #     if status == 1:
            #         self.quiz_by_html_auto(url)

            (status, url) = self.get_quiz_url(unique, uid)
            if status == 1:
                self.quiz_by_html(url)
            else:
                logger.warning('********** 已做过，币响知识小课堂。')
        logger.warning('********** All Quiz Complete!')

    def getverify(self, uid):
        url = "http://bi.bxtg88.com/down/getverify"

        payload_verify = "uid=" + uid

        try:
            logger.warning("^^^^^^^^^^ [" + uid + "], getverify()")
            response = requests.request("GET", url, data=payload_verify, headers=headers,
                                        timeout=60, allow_redirects=False)

            res = response.json()["message"]
            if res == '验证成功！':
                gt = response.json()["gt"]
                challenge = response.json()["challenge"]
                return gt, challenge
            else:
                return -1, -1
        except Exception as e:
            print(e)
            return -1, -1

    def post_with_captcha(self, getDialCode, phones, uid, challenge, validate):
        # global proxies

        url = "http://bi.bxtg88.com/down/verifyLoginNew"

        payload_newsRecord = "uid=" + uid + \
                             "&getDialCode=" + getDialCode + \
                             "&phones=" + phones + \
                             "&geetest_challenge=" + challenge + \
                             "&geetest_validate=" + validate + \
                             "&geetest_seccode=" + validate + "|jordan"

        try:

            logger.warning(
                "********** [" + phones + "], post_with_captcha()")
            response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                        timeout=60, allow_redirects=False)

            while response.status_code != 200:
                logger.warning("<<<<<<<<<< [" + phones + "]. post_with_captcha Error. try again ...")
                time.sleep(random.randint(1, 3))
                response = requests.request("POST", url, data=payload_newsRecord, headers=headers,
                                            timeout=60, allow_redirects=False)

            if response.status_code == 200:
                res = response.json()["message"]
                if res == '验证成功！':
                    msg = response.json()["message"]
                    logger.warning(
                        ">>>>>>>>>> [" + phones + "]. post_with_captcha success, msg = " + msg)
                    return 0
                else:
                    logger.warning("<<<<<<<<<< [" + phones + "]. post_with_captcha Error.")
                    self.error_count += 1
                    if self.error_count == 2:
                        sys.exit(0)
                    return -1
            else:
                logger.warning("<<<<<<<<<< [" + phones + "]. post_with_captcha Error.")
                return -1
        except Exception as e:
            print(e)
            return -1

    def firefox_elephant(self, url):
        try:

            options = selenium.webdriver.FirefoxOptions()
            options.add_argument('-headless')
            self.driver = selenium.webdriver.Firefox(firefox_options=options)

            # option = webdriver.ChromeOptions()
            # option.add_argument('headless')
            # driver = webdriver.Chrome(chrome_options=option)

            # self.driver = webdriver.Firefox()

            # self.driver = webdriver.Chrome()

            self.driver.set_window_size(480, 750)
            self.driver.set_window_position(y=0, x=0)
            self.driver.get(url)

            wait = WebDriverWait(self.driver, 60)
            time.sleep(3)

            # 立即领取
            elements = self.driver.find_elements(By.TAG_NAME, 'p')
            for i in range(len(elements)):
                if elements[i].text == '立即领取':
                    elements[i].click()
                    # 确认收取
                    if self.isElementExist_by_xpath("/html/body/div[8]/div[2]/p[2]"):
                        self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/p[2]").click()
                        time.sleep(2)
                        # 不足，取消
                        if self.isElementExist_by_xpath("/html/body/div[5]/div/p[1]"):
                            self.driver.find_element(By.XPATH, "/html/body/div[5]/div/p[1]").click()
                            time.sleep(1)

            logger.warning(">>>>>>>>>> done. 立即领取1")

            button_refresh = wait.until(EC.presence_of_element_located((By.ID, 'button_refresh')))
            button_refresh.click()
            time.sleep(1)

            # 新泡泡
            elements = self.driver.find_elements(By.TAG_NAME, 'p')
            for i in range(len(elements)):
                txt = elements[i].text
                nPos = txt.find('泡泡')

                if nPos > -1:
                    num = txt.split(' ')[1].split('/')[0]

                    for j in range(10 - int(num)):
                        self.driver.find_element_by_class_name('add_pop').click()
                        time.sleep(1)
            logger.warning(">>>>>>>>>> done. 吹泡泡")

            button_refresh = wait.until(EC.presence_of_element_located((By.ID, 'button_refresh')))
            button_refresh.click()
            time.sleep(1)

            # 立即领取
            elements = self.driver.find_elements(By.TAG_NAME, 'p')
            for i in range(len(elements)):
                if elements[i].text == '立即领取':
                    elements[i].click()
                    # 确认收取
                    if self.isElementExist_by_xpath("/html/body/div[8]/div[2]/p[2]"):
                        self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/p[2]").click()
                        time.sleep(2)
                        # 不足，取消
                        if self.isElementExist_by_xpath("/html/body/div[5]/div/p[1]"):
                            self.driver.find_element(By.XPATH, "/html/body/div[5]/div/p[1]").click()
                            time.sleep(1)
            logger.warning(">>>>>>>>>> done. 立即领取2")

            button_refresh = wait.until(EC.presence_of_element_located((By.ID, 'button_refresh')))
            button_refresh.click()
            time.sleep(1)

            # 邮件
            touru = ''
            pop = ''
            elements = self.driver.find_elements(By.TAG_NAME, 'p')
            for i in range(len(elements)):
                txt = elements[i].text
                nPos = txt.find('投入')
                if nPos > -1:
                    touru = txt

                nPos = txt.find('泡泡')
                if nPos > -1:
                    pop = txt
            logger.warning(">>>>>>>>>> done. email")

            # 构建Json数组，用于发送HTML邮件
            # Python 字典类型转换为 JSON 对象
            content_data = {
                "url": url,
                "touru": touru,
                "pop": pop,
                "other": ''
            }


            self.driver.close()

            return content_data

        except Exception as e:
            print(e)
            self.driver.close()
            return -1



# App_signup = Signup()
# App_signup.registry()

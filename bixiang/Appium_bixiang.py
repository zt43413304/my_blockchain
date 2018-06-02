# coding=utf-8

import logging
import os
import random
import time

from PIL import Image
# from appium import webdriver
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common import my_suma

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


class Signup:
    MIN_SEC = 15
    MAX_SEC = 20

    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['browserName'] = 'Chrome'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        logger.warning("********** start __init()__...")

    def __init__(self, version):
        print("start __init(version)__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['app'] = PATH(
            '/Users/Jackie.Liu/Documents/MuMu共享文件夹/bixiang-229-1.4.1-Y1032_1BA281650150FE92ADA35DB3DF335D28.apk'
        )
        desired_caps['appPackage'] = 'com.coinstation.bixiang'
        desired_caps['appActivity'] = 'com.coinstation.bixiang.view.activity.MainActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def isElementExist(self, id):
        try:
            self.driver.find_element_by_accessibility_id(id)
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
        print(">>>>> offset=" + str(offset))
        if offset > 0:
            tracks.extend([-1 for i in range(offset)])
        elif offset < 0:
            tracks.extend([1 for i in range(abs(offset))])

        # 模拟终点附近的左右移动
        tracks.extend(
            [0, 0, 1, -1, 0, 0])
        # logger.warning("********** 4. 计算轨迹后，偏差值 = " + str(sum(tracks) - distance))
        print("********** 42. 计算轨迹后，偏差值 = " + str(sum(tracks) - len_ori))

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
        track.extend(
            [0, 1, -1, 0])
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

    def login_with_sms(self, sms):
        """
        打开网页输入用户名密码
        :return: None
        """
        wait = WebDriverWait(self.driver, 60)
        # self.driver.get(self.url)
        # phones = self.wait.until(EC.presence_of_element_located((By.ID, 'phones')))

        code2 = wait.until(EC.presence_of_element_located((By.ID, 'code2')))
        # phones.send_keys(self.phones)
        code2.send_keys(sms)
        print(">>>>> login with SMS=" + sms)

        button = wait.until(EC.presence_of_element_located((By.ID, 'download')))
        button.click()

    def html_signup(self):

        try:
            suma = my_suma.suma()
            # suma_phone = suma.getMobilenum()
            suma_phone = '13945860933'
            logger.warning("********** suma_phone = " + suma_phone)

            # driver = webdriver.Chrome()
            # driver.maximize_window()
            # self.driver.set_window_size(600, 800)
            # self.driver.set_window_position(y=0, x=0)

            self.driver.get('http://bixiang8.com/inVdO')
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
                    suma_sms = suma.getVcodeAndHoldMobilenum(suma_phone)
                    if suma_sms == '':
                        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1')))
                        button.click()
                        logger.warning(">>>>>>>>>> 8. 滑块验证成功，但未收到短信，重新验证. ")
                        logger.warning("\n")
                        geetest = False
                    else:
                        self.login_with_sms(suma_sms)
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

        except Exception as e:
            print(e)
        finally:
            self.driver.close()

    def my_find_elements_by_classname(self, classname, name):
        # android.widget.TextView
        views = self.driver.find_elements(By.CLASS_NAME, classname)
        for i in range(len(views)):
            if views[i].text == name:
                return views[i]

    def app_signup(self):

        element = self.my_find_elements_by_classname('android.widget.TextView', '我的')
        element.click()

        el1 = self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_sign")
        el1.click()
        el2 = self.driver.find_element_by_id("com.coinstation.bixiang:id/signed_close")
        el2.click()
        el3 = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.TextView")
        el3.click()
        el4 = self.driver.find_element_by_id("com.coinstation.bixiang:id/tv_set")
        el4.click()
        el5 = self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_bindphone")
        el5.click()
        el6 = self.driver.find_element_by_id("com.coinstation.bixiang:id/et_phone")
        el6.send_keys("13601334563")
        el7 = self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_sendsms")
        el7.click()
        el8 = self.driver.find_element_by_id("com.coinstation.bixiang:id/et_sms")
        el8.send_keys("4563")
        el9 = self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_save")
        el9.click()
        el10 = self.driver.find_element_by_id("com.coinstation.bixiang:id/btn_back")
        el10.click()

# App_signup = Signup()
# App_signup.registry()

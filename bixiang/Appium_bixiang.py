# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python


import logging
import os
import time

from PIL import Image
from appium import webdriver
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Returns abs path relative to this file and not cwd

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

    def __init__(self, version, deviceName, port):
        print("start __init(version, deviceName, port)__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = deviceName
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['app'] = PATH(
            '/Users/Jackie.Liu/Documents/MuMu共享文件夹/bixiang-229-1.4.1-Y1032_1BA281650150FE92ADA35DB3DF335D28.apk'
        )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'
        self.driver = webdriver.Remote('http://localhost:' + str(port) + '/wd/hub', desired_caps)

    def __init__(self):
        print("start __init()__...")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['noReset'] = 'True'
        desired_caps['newCommandTimeout'] = '600'
        desired_caps['browserName'] = 'Chrome'
        # desired_caps['app'] = PATH(
        #     '/Users/Jackie.Liu/Documents/MuMu共享文件夹/bixiang-229-1.4.1-Y1032_1BA281650150FE92ADA35DB3DF335D28.apk'
        # )
        # desired_caps['appPackage'] = 'com.example.android.contactmanager'
        # desired_caps['appActivity'] = '.ContactManager'
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
        name = 'snap_%s.png' % time.time()
        self.driver.save_screenshot(name)
        page_snap_obj = Image.open(name)
        return page_snap_obj

    def get_image(self, rate):
        '''
        从网页的网站截图中，截取验证码图片
        :return: 验证码图片
        '''
        wait = WebDriverWait(self.driver, 10)
        img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)  # 保证图片刷新出来
        localtion = img.location
        size = img.size

        top = localtion['y']
        left = localtion['x']
        bottom = localtion['y'] + size['height']
        right = localtion['x'] + size['width']
        print(top, bottom, left, right)
        page_snap_obj = self.get_snap()
        # 由于浏览器基于屏幕分辨率的自动缩放功能，截图图片和网页实际大小可能不同，所以需要乘以一个比例
        crop_imag_obj = page_snap_obj.crop((left * rate, top * rate, right * rate, bottom * rate))
        crop_imag_obj.save('%s.png' % time.time())
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

    def get_tracks(self, distance):
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
                a = 2
            else:
                a = -3
            v0 = v
            s = v0 * t + 0.5 * a * (t ** 2)
            current += s
            tracks.append(round(s))
            v = v0 + a * t
        return tracks

    def registry(self):
        try:
            # driver = webdriver.Chrome()
            # driver.maximize_window()
            # driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", cap)
            self.driver.get('http://bixiang8.com/dz5vU')
            wait = WebDriverWait(self.driver, 15)
            phones = self.driver.find_element_by_id('phones')
            code2 = self.driver.find_element_by_id('code2')
            phones.send_keys('13845632312')
            code2.send_keys('123456')

            # 计算网页缩放比，部分浏览器会根据屏幕分辨率自动缩放网页，所以图片中滑块的距离和网页中需要拖动的距离可能不同
            body = self.driver.find_element_by_tag_name("body")
            page_snap_obj = self.get_snap()
            rate = page_snap_obj.size[0] / body.size['width']

            print(body.size)

            # 步骤一：先点击按钮，弹出没有缺口的图片
            button = wait.until(EC.presence_of_element_located((By.ID, 'getCode')))
            button.click()

            # 步骤二：拿到没有缺口的图片
            image1 = self.get_image(rate)
            print('拿到没有缺口的图片')

            # 步骤三：点击拖动按钮，弹出有缺口的图片
            button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
            button.click()

            # 步骤四：拿到有缺口的图片
            image2 = self.get_image(rate)
            print('拿到有缺口的图片')
            print(image1.size, image2.size)
            # 步骤五：对比两张图片的所有RBG像素点，得到不一样像素点的x值，即要移动的距离
            distance = self.get_gap(image1, image2, rate)
            print(distance)
            # 步骤六：模拟人的行为习惯（先匀加速拖动后匀减速拖动），把需要拖动的总距离分成一段一段小的轨迹
            tracks = self.get_tracks(distance / rate)

            # 步骤七：按照轨迹拖动，完全验证
            button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
            print(button.location)
            ActionChains(self.driver).click_and_hold(button).perform()
            for track in tracks:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
            else:
                ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()  # 先移过一点
                ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()  # 再退回来，是不是更像人了

            time.sleep(0.5)
            ActionChains(self.driver).release().perform()
            print(button.location)

            # 步骤八：完成登录
            button = wait.until(EC.element_to_be_clickable((By.ID, 'download')))

            button.click()
            time.sleep(10)
        finally:
            self.driver.close()


App_signup = Signup()
App_signup.registry()
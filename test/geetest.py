import time
from io import BytesIO
from PIL import Image
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

EMAIL = 'newseeing@163.com'
PASSWORD = ''
BORDER = 19
INIT_LEFT = 60


class CrackGeetest():
    def __init__(self):
        self.url = 'http://bixiang8.com/dz5vU'
        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()
        # opt = webdriver.FirefoxOptions()

        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        # opt.add_argument('headless')

        # 创建chrome无界面对象
        self.driver = webdriver.Chrome(chrome_options=opt)
        self.driver.set_window_size(1440, 900)
        self.wait = WebDriverWait(self.driver, 20)

        self.phones = '13678563454'
        self.sms_code = 'abcde'

    def __del__(self):
        self.driver.close()

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_panel')))
        # img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice.geetest_absolute')))
        # img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice.geetest_absolute')))


        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        # print('position:' + str(top) +','+str(bottom) +','+str(left) +','+str(right))
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        screenshot.save('screenshot.png')
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def input_phone(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.driver.get(self.url)
        phones = self.wait.until(EC.presence_of_element_located((By.ID, 'phones')))
        # code2 = self.wait.until(EC.presence_of_element_located((By.ID, 'code2')))
        phones.send_keys(self.phones)
        # code2.send_keys(self.code2)

    def get_geetest_button(self):
        """
        获取geetest验证按钮
        :return:
        """
        button = self.wait.until(EC.presence_of_element_located((By.ID, 'getCode')))
        return button

    def input_sms(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        # self.driver.get(self.url)
        # phones = self.wait.until(EC.presence_of_element_located((By.ID, 'phones')))
        code2 = self.wait.until(EC.presence_of_element_located((By.ID, 'code2')))
        # phones.send_keys(self.phones)
        code2.send_keys(self.code2)

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """

        left = 120
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                print(">>>>> i="+str(i)+", j="+str(j))
                if not self.is_pixel_equal(image1, image2, i, j) \
                        and not self.is_pixel_equal(image1, image2, i, j+20) \
                        and not self.is_pixel_equal(image1, image2, i, j+40) \
                        and not self.is_pixel_equal(image1, image2, i, j+60):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        print("pixel1(rgb)="+str(pixel1[0])+","+str(pixel1[1])+","+str(pixel1[2]))
        print("pixel2(rgb)="+str(pixel2[0])+","+str(pixel2[1])+","+str(pixel2[2]))
        print("\n")
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False


    def get_track(self, distance):
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
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
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
        return track

    # 生成滑动轨迹
    # 由于极验的后台在不断的训练识别模型，所以移动轨迹可能是有实效性的，时常需要修改
    # 轨迹要尽量的靠近人类的行为习惯
    def slide_track(self, distance):

        # 移动距离的列表
        track = []
        # 当前距离
        current = 0
        # 改变加速度的时间点
        mid = distance * 3 / 5
        # 计算移动距离所需的时间间隔
        t = 0.2
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
        offset = sum(track) - distance
        if offset > 0:
            track.extend([-1 for i in range(offset)])
        elif offset < 0:
            track.extend([1 for i in range(abs(offset))])

        # 模拟终点附近的左右移动
        track.extend(
            [0, 0, 0, -1, 1, -1, 1, -1, 1, 0, 0, 0])
        print(">>>>>" + str(sum(track) - distance))
        return track




    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        startlocation = slider.location
        print("startlocation="+str(startlocation['x']))
        ActionChains(self.driver).click_and_hold(slider).perform()


        # for x in track:
        #     ActionChains(self.driver).move_by_offset(xoffset=(x-last), yoffset=0).perform()
        #     dist+=x
        #     last=x
        #     location=self.driver.find_element_by_class_name("geetest_slider_button").location
        #     print("理论移动",dist,"实际移动",location['x']-startlocation["x"])

        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            # location=self.driver.find_element_by_class_name("geetest_slider_button").location
            location = slider.location
            print("location="+str(location['x']))
            # print("实际移动",location['x']-startlocation["x"])
        time.sleep(0.1)
        ActionChains(self.driver).release().perform()


    # 滑动滑块
    def slide_button(self, slider, track):
        try:
            # 点击并拿起滑块
            ActionChains(self.driver).click_and_hold(slider).perform()
            # 根据我们生成的移动轨迹，逐步移动鼠标
            for x in track:
                ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            # 松开鼠标
            time.sleep(1)
            ActionChains(self.driver).release().perform()
        except Exception as e:
            print('滑动滑块出错：%s' % e)
            self.driver.quit()


    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'download')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    # 截图处理
    def get_image(self, name):
        time.sleep(3)
        # WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable(
        #     (By.XPATH, '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')))
        # element = self.driver.find_element_by_xpath(
        #     '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')



        # 保存登录页面截图
        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")

        # 打开截图，获取element的坐标和大小
        # left = element.location.get("x")
        # top = element.location.get("y")
        # right = left + element.size.get("width")
        # bottom = top + element.size.get("height")
        left = 1162
        # 无头
        # top = 618
        # 有头
        top = 438
        right = left + 550
        bottom = top + 280

        # 对此区域进行截图，然后灰度处理
        cropImg = image.crop((left, top, right, bottom))
        # full_Img = cropImg.convert("L")
        cropImg.save(name)


    # 截图处理
    def first_image(self):
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable(
            (By.XPATH, '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')))
        element = self.driver.find_element_by_xpath(
            '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')



        # 保存登录页面截图
        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")

        # 打开截图，获取element的坐标和大小
        # left = element.location.get("x")
        # top = element.location.get("y")
        # right = left + element.size.get("width")
        # bottom = top + element.size.get("height")
        left = 1162
        # 无头
        # top = 618
        # 有头
        top = 438
        right = left + 550
        bottom = top + 280

        # 对此区域进行截图，然后灰度处理
        cropImg = image.crop((left, top, right, bottom))
        # full_Img = cropImg.convert("L")
        cropImg.save("fullimage.png")

    # 截图处理
    def second_image(self):
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_slider_button"]')))
        move_btn = self.driver.find_element_by_xpath('//*[@class="geetest_slider_button"]')

        ActionChains(self.driver).move_to_element(move_btn).click_and_hold(move_btn).perform()

        WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//canvas[@class="geetest_canvas_slice geetest_absolute"]')))
        element = self.driver.find_element_by_xpath('//canvas[@class="geetest_canvas_slice geetest_absolute"]')

        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")

        # left = element.location.get("x")
        # top = element.location.get("y")
        # right = left + element.size.get("width")
        # bottom = top + element.size.get("height")

        left = 1162
        # 无头
        # top = 618
        # 有头
        top = 438
        right = left + 550
        bottom = top + 280

        cropImg = image.crop((left, top, right, bottom))
        # cut_Img = cropImg.convert("L")
        cropImg.save()

    def calc_cut_offset(self, cut_img, full_img):

        cut_img = Image.open(cut_img)
        full_img = Image.open(full_img)

        x, y = 1, 1
        find_one = False
        top = 0
        left = 0
        right = 0
        while x < cut_img.width:
            y = 1
            while y < cut_img.height:
                cpx = cut_img.getpixel((x, y))
                fpx = full_img.getpixel((x, y))
                if abs(cpx - fpx) > 50:
                    if not find_one:
                        find_one = True
                        x += 60
                        y -= 10
                        continue
                    else:
                        if left == 0:
                            left = x
                            top = y
                        right = x
                        break
                y += 1
            x += 1
        return left, right - left

    def start_move(self, distance, element, click_hold=False):
        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= 7
        print(distance)

        # 按下鼠标左键
        if click_hold:
            ActionChains(self.driver).click_and_hold(element).perform()

        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                time.sleep(random.randint(10, 50) / 100)
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span

        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()

    def analog_move(self):
        #鼠标移动到拖动按钮，显示出拖动图片
        element = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(3)

        # 刷新一下极验图片
        element = self.driver.find_element_by_xpath('//a[@class="gt_refresh_button"]')
        element.click()
        time.sleep(1)

        # 获取图片地址和位置坐标列表
        cut_image_url, cut_location = self.get_image_url('//div[@class="gt_cut_bg_slice"]')
        full_image_url, full_location = self.get_image_url('//div[@class="gt_cut_fullbg_slice"]')

        # 根据坐标拼接图片
        cut_image = self.mosaic_image(cut_image_url, cut_location)
        full_image = self.mosaic_image(full_image_url, full_location)

        # 保存图片方便查看
        cut_image.save("cut.jpg")
        full_image.save("full.jpg")

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

        # 如果出现error

        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_ajax_tip gt_error"]')))
            print("验证失败")
            return
        except TimeoutException as e:
            pass

        # 判断是否验证成功
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_ajax_tip gt_success"]')))
        except TimeoutException:
            print("again times")
            time.sleep(5)
            # 失败后递归执行拖动
            self.analog_drag()
        else:
            # 成功后输入手机号，发送验证码
            self.register()

    def bixiang_registry(self):
        # 输入手机号
        self.input_phone()

        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()
        # 点击验证按钮后加载图片需要时间
        time.sleep(5)

        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

        self.get_image("fullimage.png")

        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        # 点击验证按钮后加载图片需要时间
        time.sleep(5)

        self.get_image("cutimage.png")

        image1 = Image.open("/Users/Jackie.Liu/DevTools/my_blockchain/test/fullimage.png")
        image2 = Image.open("/Users/Jackie.Liu/DevTools/my_blockchain/test/cutimage.png")


        # 获取缺口位置
        # self.calc_cut_offset("/Users/Jackie.Liu/DevTools/my_blockchain/test/cutimage.png","/Users/Jackie.Liu/DevTools/my_blockchain/test/fullimage.png")
        gap = self.get_gap(image1, image2)

        # 减去缺口位移
        gap -= BORDER
        print('缺口位置', gap)


        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(slider).perform()
        time.sleep(0.5)
        while gap > 0:
            if gap > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            gap -= span
            time.sleep(random.randint(10,50)/100)

        ActionChains(self.driver).move_by_offset(gap, 1).perform()
        ActionChains(self.driver).release(on_element=slider).perform()



        # 获取移动轨迹
        track = self.slide_track(gap)
        print('滑动轨迹,slide_track()=', track)

        track1 = self.get_track(gap)
        print('滑动轨迹,get_track()=', track1)
        # 拖动滑块
        self.move_to_gap(slider, track)

        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_slider_button'), '验证成功'))

            # EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_panel_success_title'), '通过验证')

            # EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        # <div class="geetest_panel_success_title">通过验证</div>


        print(success)

        # 输入密码
        self.input_sms()

        # 失败后重试
        # if not success:
        #     self.crack()
        # else:
        #     self.login()


        # self.calc_cut_offset("/Users/Jackie.Liu/DevTools/my_blockchain/test/cutimage.png", "/Users/Jackie.Liu/DevTools/my_blockchain/test/fullimage.png")

        # self.analog_move()


        # self.driver.quit()

        # 获取验证码图片
        # image1 = self.get_geetest_image('captcha1_'+rq+'.png')


        # 获取带缺口的验证码图片
        # image2 = self.get_geetest_image('captcha2_'+rq+'.png')



if __name__ == '__main__':
    crack = CrackGeetest()
    crack.bixiang_registry()



    # 判断是否登录成功
    # tip_btn = self.driver.find_element_by_xpath('//*[@id="tip_btn"]')
    # if tip_btn.text.find("登录成功") == -1:
    #     try:
    #         WebDriverWait(self.driver, 3, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_reset_tip_content"]')))
    #         reset_btn = self.driver.find_element_by_xpath('//*[@class="geetest_reset_tip_content"]')
    #         #判断是否需要重新打开滑块框
    #         if reset_btn.text.find("重试") != -1:
    #             reset_btn.click()
    #     except:
    #         pass
    #     else:
    #         time.sleep(1)
    #     # 刷新滑块验证码图片
    #     refresh_btn = self.driver.find_element_by_xpath('//*[@class="geetest_refresh_1"]')
    #     refresh_btn.click()
    #     time.sleep(0.5)
    #
    #     # 重新进行截图、分析、计算、拖动处理
    #     analog_move()
    # else:
    #     print("登录成功")

    # cookies = self.driver.get_cookies()
    # with open("cookies.txt", "w") as fp:
    #     json.dump(cookies, fp)
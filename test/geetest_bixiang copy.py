"""
极验滑块验证
"""
import logging

import selenium
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import time
from common import my_suma

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("geetest_bixiang.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/geetest_bixiang.log', mode='w')
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

def get_snap():
    '''
    对整个网页截图，保存成图片，然后用PIL.Image拿到图片对象
    :return: 图片对象
    '''
    rq = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    name = './test/page_%s.png' % rq
    driver.save_screenshot(name)
    page_snap_obj=Image.open(name)
    return page_snap_obj


def  get_image(rate):
    '''
    从网页的网站截图中，截取验证码图片
    :return: 验证码图片
    '''
    img=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_canvas_img')))
    time.sleep(2) #保证图片刷新出来
    localtion=img.location
    size=img.size
    # print(size)

    left = localtion['x']
    top=localtion['y']
    right=localtion['x']+size['width']
    bottom=localtion['y']+size['height']

    # print(left, top, right, bottom)
    # print(left * rate,top * rate,right * rate,bottom * rate)
    page_snap_obj=get_snap()
    # 由于浏览器基于屏幕分辨率的自动缩放功能，截图图片和网页实际大小可能不同，所以需要乘以一个比例
    crop_imag_obj=page_snap_obj.crop((left * rate,top * rate,right * rate,bottom * rate))

    rq = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    crop_imag_obj.save('./test/snap_%s.png' % rq)

    return crop_imag_obj


def is_pixel_equal(img1, img2, x, y):
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
            pix1[2] - pix2[2] < threshold)):
        return True
    else:
        return False

def get_gap2(image1, image2, rate):
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
                if not is_pixel_equal(image1, image2, i, j) \
                        and not is_pixel_equal(image1, image2, i, j+20) \
                        and not is_pixel_equal(image1, image2, i, j+40) \
                        and not is_pixel_equal(image1, image2, i, j+60):
                    left = i
                    return left -6 * rate
        return left-6 * rate

def get_gap(img1, img2, rate):
    """
    获取缺口偏移量
    :param img1: 不带缺口图片
    :param img2: 带缺口图片
    :param rate: 网页缩放比
    :return:
    """
    left = int(57.5*rate)
    for i in range(left, img1.size[0]):
        for j in range(img1.size[1]):
            if not is_pixel_equal(img1, img2, i, j):
                left = i
                return left - 6 * rate
    return left - 6 * rate

def slide_tracks(distance):

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
    offset = int(sum(track) - distance)
    if offset > 0:
        track.extend([-1 for i in range(offset)])
    elif offset < 0:
        track.extend([1 for i in range(abs(offset))])

    # 模拟终点附近的左右移动
    track.extend(
        [0, 0, 0, -1, 1, -1, 1, -1, 1, 0, 0, 0])
    logger.warning("********** 4. Internal distance gap = " + str(sum(track) - distance))
    return track

def get_tracks(distance):
    '''
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+½at²
    ③v²-v0²=2as
    :param distance: 需要移动的距离
    :return: 存放每0.3秒移动的距离
    '''
    v=0
    t=0.3
    tracks=[]
    current=0
    mid=distance*4/5

    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a= 2
        else:
            a=-3
        v0=v
        s=v0*t+0.5*a*(t**2)
        current+=s
        tracks.append(round(s))
        v=v0+a*t
    return tracks

def slide_button(tracks):
    """
    获取缺口偏移量
    :param tracks: 轨迹
    :return: success
    """
    wait = WebDriverWait(driver, 10)
    slide = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
    logger.warning(">>>>>>>>>> 4. Before slide, slide.location")
    logger.warning(slide.location)
    ActionChains(driver).click_and_hold(slide).perform()
    for track in tracks:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    else:
        ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()  # 先移过一点
        ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()  # 再退回来，是不是更像人了
    time.sleep(0.5)
    ActionChains(driver).release().perform()
    logger.warning(">>>>>>>>>> 4. After slide, slide.location")
    logger.warning(slide.location)


    try:
        time.sleep(3)


        # WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located(By.CLASS_NAME,'geetest_result_title'))
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.CLASS_NAME,'geetest_result_title'))


        # presence_of_element_located
        # visibility_of_element_located
        # text_to_be_present_in_element
        # text_to_be_present_in_element_value
        # invisibility_of_element_located
        # element_to_be_clickable

        # print('01.' + str(wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_panel_success_title')))))
        # print('02.' + str(wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'geetest_panel_success_title')))))
        # print('011.' + str(wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_result_title')))))
        # print('021.' + str(wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'geetest_result_title')))))
        # print('03.' + str(wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_panel_success_title'),u"验证通过"))))
        # print('04.' + str(wait.until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, 'geetest_panel_success_title'),u"验证通过"))))
        # print('031.' + str(wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_panel_success_title'),u"验证通过:"))))
        # print('041.' + str(wait.until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, 'geetest_panel_success_title'),u"验证通过:"))))


        print('1.'+driver.find_element(By.CLASS_NAME,'geetest_result').text.strip())
        print('2.'+driver.find_element(By.CLASS_NAME,'geetest_result_box').text.strip())
        print('3.'+driver.find_element(By.CLASS_NAME,'geetest_result_icon').text.strip())
        print('4.'+driver.find_element(By.CLASS_NAME,'geetest_result_title').text.strip())
        print('5.'+driver.find_element(By.CLASS_NAME,'geetest_result_content').text.strip())

        print('6.'+driver.find_element(By.CLASS_NAME,'geetest_slider').text.strip())
        print('7.'+driver.find_element(By.CLASS_NAME,'geetest_slider_track').text.strip())
        print('8.'+driver.find_element(By.CLASS_NAME,'geetest_slider_tip').text.strip())

        print('9.'+driver.find_element(By.CLASS_NAME,'geetest_slider_button').text.strip())

        # print('10.'+driver.find_element(By.CLASS_NAME,'geetest_panel').text.strip())
        # print('11.'+driver.find_element(By.CLASS_NAME,'geetest_panel_box').text.strip())
        print('12.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success').text.strip())
        print('13.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_box').text.strip())
        print('14.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_show').text.strip())
        print('15.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_correct').text.strip())
        print('16.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_title').text.strip())

        # print('17.'+driver.find_element(By.CLASS_NAME,'geetest_panel_next').text)

        elements = driver.find_elements_by_class_name('geetest_result_title')
        for i in range(len(elements)):
            element = elements[i]
            print('##### ' + str(i)+ element.text)

        print('@@@@@ '+driver.find_element(By.ID,'getCode').get_attribute("value"))

        # success = wait.until(
        #     EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_panel_success_title'), '验证通过'))

        result = driver.find_element(By.CLASS_NAME,'geetest_result_content').text
        if result is not '' or result is not None:
            print('result='+str(result))
            return True
        else:
            return False

    except selenium.common.exceptions.TimeoutException as e:
        print(e)
        return False
    except Exception as f:
        print(f)

def login_with_sms(sms):
    """
    打开网页输入用户名密码
    :return: None
    """
    wait = WebDriverWait(driver, 60)
    # self.driver.get(self.url)
    # phones = self.wait.until(EC.presence_of_element_located((By.ID, 'phones')))

    code2 = wait.until(EC.presence_of_element_located((By.ID, 'code2')))
    # phones.send_keys(self.phones)
    code2.send_keys(sms)
    print(">>>>> login with SMS=" + sms)

    button = wait.until(EC.presence_of_element_located((By.ID, 'download')))
    button.click()


try:
    suma = my_suma.suma()
    # suma_phone = suma.getMobilenum()
    suma_phone='15584126740'
    logger.warning("********** suma_phone = " + suma_phone)

    driver=webdriver.Chrome()
    # driver.maximize_window()
    driver.set_window_size(600,800)
    driver.set_window_position(y=0, x=0)
    driver.get('http://bixiang8.com/inVdO')
    wait=WebDriverWait(driver, 10)
    phones = driver.find_element_by_id('phones')
    # code2 = driver.find_element_by_id('code2')
    phones.send_keys(suma_phone)
    # code2.send_keys('123456')


    print('@ '+driver.find_element(By.ID,'getCode').get_attribute("value"))




    # 计算网页缩放比，部分浏览器会根据屏幕分辨率自动缩放网页，所以图片中滑块的距离和网页中需要拖动的距离可能不同
    body = driver.find_element_by_tag_name("body")
    page_snap_obj=get_snap()
    rate = page_snap_obj.size[0] / body.size['width']
    logger.warning("********** Page_body size, width=" + str(body.size['width']) + ", height=" + str(body.size['height']))
    logger.warning("********** page_snap_obj size, width=" + str(page_snap_obj.size[0]) + ", height=" + str(page_snap_obj.size[1]))
    logger.warning("********** Page body rate = " + str(rate))



    # 步骤一：先点击按钮，弹出没有缺口的图片
    button=wait.until(EC.presence_of_element_located((By.ID,'getCode')))
    button.click()

    # 当没有通过滑块验证时，循环多次进行验证
    geetest = False
    while not geetest:
        # 步骤二：拿到没有缺口的图片
        image1=get_image(rate)
        logger.warning(">>>>>>>>>> 1. 没有缺口的图片.size = " + str(image1.size[0]) + " * " + str(image1.size[1]))
        time.sleep(1)

        #步骤三：点击拖动按钮，弹出有缺口的图片
        button=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_slider_button')))
        button.click()
        time.sleep(1)

        #步骤四：拿到有缺口的图片
        image2=get_image(rate)
        logger.warning(">>>>>>>>>> 2. 有缺口的图片.size = " + str(image2.size[0]) + " * " + str(image2.size[1]))
        time.sleep(1)
        # print(image1.size, image2.size)

        # 步骤五：对比两张图片的所有RBG像素点，得到不一样像素点的x值，即要移动的距离
        gap = get_gap2(image1, image2, rate)
        logger.warning(">>>>>>>>>> 3. 缺口距离. gap = " + str(gap))

        #步骤六：模拟人的行为习惯（先匀加速拖动后匀减速拖动），把需要拖动的总距离分成一段一段小的轨迹
        tracks=slide_tracks(gap/rate)
        print(tracks)

        #步骤七：按照轨迹拖动，完全验证

        elements = driver.find_elements_by_class_name('geetest_result_title')
        for i in range(len(elements)):
            element = elements[i]
            print('##### ' + str(i)+ element.text)

        print('@@@ '+driver.find_element(By.ID,'getCode').get_attribute("value"))

        # print('1.'+driver.find_element(By.CLASS_NAME,'geetest_result_box').text)
        # print('2.'+driver.find_element(By.CLASS_NAME,'geetest_result_icon').text)
        # print('3.'+driver.find_element(By.CLASS_NAME,'geetest_result_title').text)
        # print('4.'+driver.find_element(By.CLASS_NAME,'geetest_result_content').text)
        # print('5.'+driver.find_element(By.CLASS_NAME,'geetest_slider').text)
        # print('6.'+driver.find_element(By.CLASS_NAME,'geetest_slider_button').text)
        # print('7.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_box').text)
        # print('8.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_title').text)
        # print('9.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_show').text)
        # print('10.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success').text)
        # print('11.'+driver.find_element(By.CLASS_NAME,'geetest_panel_success_correct').text)

        # print('a.' + str(wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_panel_success_title')))))
        # print('b.' + str(wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'geetest_panel_success_title')))))


        success = slide_button(tracks)
        logger.warning(">>>>>>>>>> 5. 滑块验证结果. " + str(success))

        if success:
            # 步骤八：滑块验证通过，短信登录
            suma_sms = suma.getVcodeAndHoldMobilenum(suma_phone)
            if suma_sms == '':
                button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1')))
                button.click()
                logger.warning(">>>>>>>>>> 8. 滑块验证成功，但未收到短信，重新验证. ")
                logger.warning("\n")
                geetest = False
            else:
                login_with_sms(suma_sms)
                logger.warning(">>>>>>>>>> 6. 滑块验证成功，短信登录. ")
                # 退出循环
                geetest = True
        else:
            # 刷新再试
            time.sleep(1)
            button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1')))
            button.click()
            logger.warning(">>>>>>>>>> 7. 滑块验证不成功，重新验证. ")
            logger.warning("\n")

except (ElementNotVisibleException, NoSuchElementException, TimeoutException)as e:
    print(e)
finally:
    driver.close()
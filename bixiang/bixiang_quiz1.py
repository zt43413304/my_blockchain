# coding=utf-8

import json
import logging
import random
import time
from io import StringIO

import requests
from appium import webdriver
from lxml import etree
from selenium.webdriver.support import expected_conditions as EC
# 第一步，创建一个logger,并设置级别
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger("bixiang_quiz.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/bixiang_quiz.log', mode='w')
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

# http://tui.yingshe.com/user/newtask?xxx=HK%3DXvJCHh66Wi68ZhJKI4
# <p id="xxx" style="display:none">hfoz9fZ1%3DfYz-fZ17goj-</p>

url = "http://tui.yingshe.com/user/newtask?xxx=BEMTZGKAkE87YHaEqD8PV"


def get_xxx():
    # global proxies

    headers = {
        'Host': "tui.yingshe.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/3.4.1",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    try:
        # logger.warning("********** quiz(), proxies = " + str(proxies))
        # response = requests.request("POST", url,  headers=headers, proxies=proxies)
        response = requests.request("GET", url, headers=headers)
        # time.sleep(random.randint(MIN_SEC, MAX_SEC))

        html = response.text

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)

        # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
        # print(result)

        xxx = tree.xpath('//*[@id="xxx"]')
        logger.warning(">>>>> xxx = " + xxx[0].text)
        return xxx[0].text

        # res = response.json()["status"]

        # if res == 1:
        #     logger.warning('********** Login success.')
        #     bixiang_userInfo(unique, uid)
        #     return 1
        # else:
        #     logger.warning('********** Login fail. uid:' + uid)
        #     return -1
    except Exception as e:
        print(e)
        # return -1


def quiz():
    xxx = get_xxx()
    # xxx = 'abbc'
    url_quiz = "http://tui.yingshe.com/user/taskCheck?xxx=" + xxx

    answer_list = '{"1": "A", "2": "D", "3": "D", "4": "C", "5": "A", "6": "D", "7": "B", "8": "A", "9": "A", "10": "D"}'
    answer_dict = json.loads(answer_list)
    # print(ans, type(ans))
    # print(ans[2])

    headers = {
        'Host': "tui.yingshe.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/3.4.1",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Referer': url
    }

    payload = "CNZZDATA1273207201=285046352-1527133912-%7C1527133912" + \
              "&CNZZDATA1273839213=2082437917-1527980171-%7C1527980171" + \
              "&CNZZDATA1272182233=572908881-1527138621-%7C1528033921" + \
              "&UM_distinctid=163909605f40-0a32cd23b-5d7e0559-47339-163909605f9ff"

    try:
        for i in range(1, 11):
            time.sleep(4)
            # index = "'"+i+"'"
            answer = answer_dict[str(i)]
            # print(answer)

            url_answer = url_quiz + "&task_id=" + str(i) + "&answer=" + answer
            print(url_answer)
            # logger.warning("********** quiz(), proxies = " + str(proxies))
            # response = requests.request("POST", url,  headers=headers, proxies=proxies)
            response = requests.request("POST", url_answer, headers=headers, data=payload)
            # time.sleep(random.randint(MIN_SEC, MAX_SEC))
            print(response.text.encode('utf-8').decode('unicode_escape'))
    except Exception as e:
        print(e)


def isElementExist_by_id(driver, id):
    try:
        driver.find_element_by_id(id)
        return True
    except Exception as e:
        print(e)
        return False


def get_html_driver():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '4.4.4'
    desired_caps['deviceName'] = 'emulator-5554'
    desired_caps['noReset'] = 'True'
    desired_caps['newCommandTimeout'] = '600'
    desired_caps['browserName'] = 'Chrome'
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    return driver


def quiz_html():
    quiz_url = input("********** Quiz url is: ")
    logger.warning('********** Your input is: ' + quiz_url)

    # quiz_url = "http://tui.yingshe.com/user/newtask?xxx=hfIf7fJt8gYv9ep15f4z4"

    try:
        driver = get_html_driver()

        logger.warning("********** quiz_by_html() ......")

        # /Users/Jackie.Liu/DevTools/Selenium/chromedriver

        # driver = webdriver.Chrome()
        # driver.maximize_window()
        # self.driver.set_window_size(600, 800)
        # self.driver.set_window_position(y=0, x=0)

        driver.get(quiz_url)
        wait = WebDriverWait(driver, 5)

        # 第1题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[1]/input[1]')))
        button.click()
        logger.warning(">>>>>>>>>> 1. 完成第1题 ......")
        time.sleep(random.randint(5, 7))

        # 第2题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[2]/input[4]')))
        button.click()
        logger.warning(">>>>>>>>>> 2. 完成第2题 ......")
        time.sleep(random.randint(5, 7))

        # 第3题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[3]/input[4]')))
        button.click()
        logger.warning(">>>>>>>>>> 3. 完成第3题 ......")
        time.sleep(random.randint(5, 7))

        # 第4题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[4]/input[3]')))
        button.click()
        logger.warning(">>>>>>>>>> 4. 完成第4题 ......")
        time.sleep(random.randint(5, 7))

        # 第5题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[5]/input[1]')))
        button.click()
        logger.warning(">>>>>>>>>> 5. 完成第5题 ......")
        time.sleep(random.randint(5, 7))

        # 第6题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[6]/input[4]')))
        button.click()
        logger.warning(">>>>>>>>>> 6. 完成第6题 ......")
        time.sleep(random.randint(5, 7))

        # 第7题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[7]/input[2]')))
        button.click()
        logger.warning(">>>>>>>>>> 7. 完成第7题 ......")
        time.sleep(random.randint(5, 7))

        # 第8题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[8]/input[1]')))
        button.click()
        logger.warning(">>>>>>>>>> 8. 完成第8题 ......")
        time.sleep(random.randint(5, 7))

        # 第9题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[9]/input[1]')))
        button.click()
        logger.warning(">>>>>>>>>> 9. 完成第9题 ......")
        time.sleep(random.randint(5, 7))

        # 第10题
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[10]/input[4]')))
        button.click()
        logger.warning(">>>>>>>>>> 10. 完成第10题 ......")
        time.sleep(random.randint(5, 7))

        logger.warning("********** quiz complete ......")

        if isElementExist_by_id(driver, "com.coinstation.bixiang:id/btn_back"):
            driver.find_element_by_id("com.coinstation.bixiang:id/btn_back").click()

        time.sleep(random.randint(1, 2))

        return 0

    except Exception as e:
        print(e)
        return -1
    # finally:
    #     self.driver.close()

# print(get_xxx())
# quiz()


# el1 = driver.find_element_by_accessibility_id("C.检查并核实绑定原来的手机号")
# el1.click()
# el2 = driver.find_element_by_accessibility_id("A.好友立即绑定手机号")
# el2.click()
# el3 = driver.find_element_by_accessibility_id("D.以上都对")
# el3.click()
# el4 = driver.find_element_by_accessibility_id("B.截图并在设置里反馈给官方")
# el4.click()
# el5 = driver.find_element_by_accessibility_id("A.币响号或者手机号")
# el5.click()
# el6 = driver.find_element_by_accessibility_id("A.使用产品能获得该产品股份分红福利等")
# el6.click()
# el7 = driver.find_element_by_accessibility_id("D.以上都是")
# el7.click()

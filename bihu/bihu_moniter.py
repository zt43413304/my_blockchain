# coding=utf-8

import configparser
import logging
import os
import re
import time

import requests

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# logging.basicConfig(level=logging.WARNING, filename='new.log', filemode='a',
#                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logfile = 'new.log'
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

ch.setFormatter(formatter)
logger.addHandler(ch)

# 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')

dictId = {}

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_RED = 0x0c  # red.


# get handle
# std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


# def set_cmd_text_color(color, handle=std_out_handle):
#     Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
#     return Bool
#
#
# # reset white
# def resetColor():
#     set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
#
#
# def printRed(mess):
#     set_cmd_text_color(FOREGROUND_RED)
#     sys.stdout.write(mess)
#     resetColor()


def getFollow():
    fp = open('Follow.txt', 'r')
    lines = fp.readlines()
    for line in lines:
        key = line.strip()
        # print key
        dictId[key] = 1
    fp.close()
    logging.warning('***** Get Follow.txt success ...')


def getUserArtList(userId):
    url_getUserArtList = 'https://be01.bihu.com/bihu-be/api/content/show/getUserArtList?queryUserId=' + userId + '&is_sort=true&page_size=20&pageNum=1'
    # print url_getUserArtList
    try:
        headers = {
            'device': 'android',
            'version': '1.0.2',
            'Content-Length': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'User-Agent': 'okhttp/3.4.'
        }

        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_getUserArtList, headers=headers, verify=False)  # headers=headers,
        # if bProxy == 0:
        #     r = requests.post(url_getUserArtList, headers=headers, verify=False) #headers=headers,
        # else:
        #     r = requests.post(url_getUserArtList, headers=headers, proxies=proxies, verify=False) #headers=headers,

        if r.status_code == 404:
            print('article page : 404...')
            return (-1, -1)
        if r.json()["res"] == 0:
            print(r.json()["resMsg"])
            # time_stamp = datetime.now()
            # print "time_stamp       " + time_stamp.strftime('%Y.%m.%d-%H:%M:%S')
            # print 'wait...'
            # time.sleep(30 * 60)
            # if flag % 2 == 0:
            #     bProxy = 1
            # else:
            #     bProxy = 0
            # flag = flag + 1
            return (-1, -1)

        contentlist = r.json()["data"]["list"][0]
        # print contentlist
        artid = contentlist['id']
        ups = contentlist['ups']
        return (artid, ups)
    except Exception as e:
        print(e)
        return (-1, -1)


def ups_art(userId, accessToken, artId, subjectUserId):
    url_ups = 'https://be01.bihu.com/bihu-be/api/content/upVote?userId=' + userId + '&accessToken=' + accessToken + '&artId=' + artId + '&commentId=&subjectUserId=' + subjectUserId
    try:
        headers = {
            'device': 'android',
            'version': '1.0.2',
            'Content-Length': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'User-Agent': 'okhttp/3.4.'
        }
        count = 0
        while (count < 100):
            # print 'try comment: ' + str(count)
            requests.packages.urllib3.disable_warnings()
            r = requests.post(url_ups, headers=headers, verify=False)  # headers=headers,
            # if bProxy == 0:
            #     r = requests.post(url_ups, headers=headers, verify=False) #headers=headers,
            # else:
            #     r = requests.post(url_ups, headers=headers, proxies=proxies, verify=False) #headers=headers,

            if r.json()['res'] == 1:
                ret = r.json()["resMsg"]
                logging.warn('>>>>> [+] up https://bihu.com/article/' + artId + ' ' + ret + '\n')
                break
            count = count + 1
    except Exception as e:
        print(e)
        return -1


def comment_art(userId, accessToken, artId, subjectUserId, content):
    url_comment = 'https://be01.bihu.com/bihu-be/api/content/createComment?userId=' + userId + '&accessToken=' + accessToken + '&artId=' + artId + '&subjectUserId=' + subjectUserId + '&content=' + content
    try:
        headers = {
            'device': 'android',
            'version': '1.0.2',
            'Content-Length': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'User-Agent': 'okhttp/3.4.'
        }

        count = 0
        while (count < 100):
            # print 'try comment: ' + str(count)
            requests.packages.urllib3.disable_warnings()
            r = requests.post(url_comment, headers=headers, verify=False)  # headers=headers,
            # if bProxy == 0:
            #     r = requests.post(url_comment, headers=headers, verify=False) #headers=headers,
            # else:
            #     r = requests.post(url_comment, headers=headers, proxies=proxies, verify=False) #headers=headers,

            if r.json()['res'] == 1:
                ret = r.json()["resMsg"]
                logging.warn('>>>>> [+] commet https://bihu.com/article/' + artId + ' ' + ret + '\n')
                break
            count = count + 1
    except:
        return -1


def loginGetAccessToken(phone, password):
    url_login = 'https://be01.bihu.com/bihu-be/api/user/loginViaPassword?phone=' + phone + '&password=' + password
    # print url_login
    try:
        headers = {
            'device': 'android',
            'version': '1.21.1',
            'Content-Length': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'User-Agent': 'okhttp/3.4.'
        }
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_login, headers=headers, verify=False)  # headers=headers,
        # if bProxy == 0:
        #     r = requests.post(url_login, headers=headers, verify=False) #headers=headers,
        # else:
        #     r = requests.post(url_login, headers=headers, proxies=proxies, verify=False) #headers=headers,

        ret = r.json()["resMsg"]
        if ret == 'success':
            accesstoken = r.json()["data"]['accessToken']
            userid = r.json()["data"]['userId']
            # print r.json()
            return (userid, accesstoken)
        else:
            return (-1, -1)
    except Exception as e:
        print(e)
        return (-1, -1)


def loop_check_article(userid, accesstoken):
    url_article = 'https://be01.bihu.com/bihu-be/api/content/show/getFollowArtList?userId=' + userid + '&accessToken=' + accesstoken + '&is_sort=true&page_size=20&pageNum=1'
    try:
        headers = {
            'device': 'android',
            'version': '1.21.1',
            'Content-Length': '0',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'User-Agent': 'okhttp/3.4.'
        }
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url_article, headers=headers, verify=False)

        ret = r.json()["resMsg"]
        if ret == 'success':
            artNum = 0
            while (artNum < 5):
                try:
                    logging.warn('***** 分析关注列表中第 ' + bytes(artNum) + ' 篇文章')

                    contentlist = r.json()['data']['artList']['list'][artNum]
                    # print contentlist
                    userName = contentlist['userName']
                    userId = contentlist['userId']
                    artid = contentlist['id']
                    ups = contentlist['ups']
                    up = contentlist['up']

                    # up等于0，没点过赞
                    if up == 0 and ups < 400:
                        logging.warning('>>>>>>>>>> A new article, up and comment...')
                        logging.warning(
                            '>>>>>>>>>> userName:' + userName + ', userId:' + bytes(userId) + ', artid:' + bytes(
                                artid) + ', Ups:' + bytes(ups))
                        ups_art(userid, accesstoken, str(artid), targetuserId)
                        time.sleep(2)
                        comment_art(userid, accesstoken, str(artid), targetuserId, content)

                    artNum = artNum + 1
                except Exception as e:
                    print(e)
                    continue
        else:
            return

    except Exception as e:
        print(e)
        return


def loop_get_firstups(userid, accesstoken):
    for targetuserId in dictId:

        try:
            # print key, dictId[key]
            count = 0
            while (count < 4):
                (artid, ups) = getUserArtList(targetuserId)
                if artid != -1:
                    break
                count = count + 1
            if artid == -1:
                continue

            logging.warning(
                '***** 1 Checked article ... UserID:' + targetuserId + ', ArtID:' + bytes(artid) + ', Ups:' + bytes(
                    ups))

            # first spider to get info
            if artid > dictId[targetuserId] and dictId[targetuserId] != 1 and ups < 400:

                dictId[targetuserId] = artid
                # print userid,accesstoken
                if bComment == '1':
                    # printRed('[*] a new article, start to up and comment...' + '\n')
                    logging.warning('>>>>>>>>>> a new article, up and comment...')
                    logging.warning('>>>>>>>>>> 2 Checked article ... UserID:' + targetuserId + ', ArtID:' + bytes(
                        artid) + ', Ups:' + bytes(ups))
                    ups_art(userid, accesstoken, str(artid), targetuserId)
                    time.sleep(2)
                    comment_art(userid, accesstoken, str(artid), targetuserId, content)

                else:
                    # printRed('[*] a new article, start to up...' + '\n')
                    logging.warning('>>>>>>>>>> a new article, start to up...')
                    logging.warning('>>>>>>>>>> Checked article ... UserID:' + targetuserId + ', ArtID:' + bytes(
                        artid) + ', Ups:' + bytes(ups))
                    ups_art(userid, accesstoken, str(artid), targetuserId)

            else:
                dictId[targetuserId] = artid
            # print rtime
            time.sleep(2)
        except:
            # print 'except in ' + artid
            continue


# start
# print 'Start...'
logging.warning('***** Start ...')
curpath = os.getcwd()
# get followings list
getFollow()
# get config information
content = open(curpath + '/config.ini').read()
content = re.sub(r"\xfe\xff", "", content)
content = re.sub(r"\xff\xfe", "", content)
content = re.sub(r"\xef\xbb\xbf", "", content)
open(curpath + '\config.ini', 'w').write(content)

cf = configparser.ConfigParser()
cf.read(curpath + '\config.ini')
username = cf.get('info', 'username').strip()
password = cf.get('info', 'password').strip()
bComment = cf.get('info', 'bComment').strip()
# content = cf.get('info', 'content').decode('utf-8').strip()
content = cf.get('info', 'content').strip()

refreshtime = int(cf.get('info', 'refreshtime'))

(userid, accesstoken) = loginGetAccessToken(username, password)
if accesstoken == -1:
    print('login error...')
    exit(-1)
else:
    # print userid,accesstoken
    # print 'login...'
    logging.warning('***** Login success ...')

while 1:
    # print 'refresh and moniter....'
    logging.warning('***** Refresh and moniter......')
    # time_stamp = datetime.datetime.now()
    # print "time_stamp       " + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') 
    # loop_get_firstups(userid, accesstoken)
    loop_check_article(userid, accesstoken)
    # print 'sleep & wait to refresh...'
    logging.warning('***** Sleep & wait to refresh......')
    logging.warning('***** ......')
    # time.sleep(random.randint(refreshtime - 60, refreshtime + 360))
    time.sleep(refreshtime)
# print 'End...'

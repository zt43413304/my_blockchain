#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import smtplib
import time
from email.mime.text import MIMEText

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("send_email.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/send_email.log', mode='w', encoding='UTF-8')
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

mailto_list = ['']  # 收件人(列表)
mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user = "newseeing"  # 用户名
mail_pass = "Liuxb0504$"  # 密码
mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com


def send_mail(to_list, sub, content):
    me = "newseeing@163.com"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_htmlmail(to_list, sub, content):
    me = "newseeing@163.com"
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_diwuqu_HtmlEmail(to_list, account_list):
    # logger.warning('********** send_diwuqu_HtmlEmail(), phone =' + str(phone))
    # logger.warning('********** send_diwuqu_HtmlEmail(), content_list length =' + str(len(account_list)))
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    head = '<!DOCTYPE HTML>' + \
           '<html id="pageLoading">' + \
           '<head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' + \
           '<title></title>' + \
           '<style type="text/css">' + \
           '/* Table Head */' + \
           '#table-7 thead th {' + \
           'background-color: RGB(255,94,102);' + \
           'color: #fff;' + \
           'border-bottom-width: 1;' + \
           '}' + \
           '/* Column Style */' + \
           '#table-7' + \
           'td {' + \
           'color: #000;' + \
           '}' + \
           '/* Heading and Column Style */' + \
           '#table-7 tr, #table-7 th {' + \
           'border-width: 1px;' + \
           'border-style: solid;' + \
           'border-color: rgb(0, 0, 0);' + \
           '}' + \
           '/* Padding and font style */' + \
           '#table-7 td, #table-7 th {' + \
           'padding: 5px 10px;' + \
           'font-size: 12px;' + \
           'font-family: Verdana;' + \
           'font-weight: bold;' + \
           '}' + \
           '</style>' + \
           '</head>' + \
           '<body>' + \
           '<p> ********** ' + datetime + ' ********** </p>' + \
           '<table border="1px" cellspacing="0px" style="border-collapse:collapse" id="table-7">' + \
           '<thead>' + \
           '<th align="center">No.</th>' + \
           '<th align="center">Name</th>' + \
           '<th align="center">Quantity</th>' + \
           '<th align="center">Price</th>' + \
           '<th align="center">Value</th>' + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    html_body = ''
    total_values_all = 0
    for m in range(len(account_list)):
        content_list = account_list[m]
        total_values = 0
        i = 0
        body = ''
        account_body = ''
        for item in content_list:
            i = i + 1
            phone = item.get('phone', 'NA')
            calculated = item.get('calculated', 'NA')
            name = item.get('name', 'NA')
            quantity = item.get('quantity', 'NA')
            price = item.get('price', 'NA')
            value = item.get('value', 'NA')
            total_values = total_values + value
            body = body + '<tr><td align="center">' + str(i) + \
                   '</td><td align="center">' + name + \
                   '</td><td align="center">' + str(round(quantity, 2)) + \
                   '</td><td align="right">' + str(round(price, 2)) + \
                   '</td><td align="right">' + str(round(value, 2)) + \
                   '</td></tr>'
        body_sum = '<tr><td colspan="4" align="center">' + str(phone) + ' (' + str(calculated) + ')' + '</td>' + \
                   '<td align="right">' + str(round(total_values, 2)) + '</td></tr>'

        total_values_all = total_values_all + total_values
        account_body = body + body_sum
        html_body = html_body + account_body
    mail_msg = head + html_body + end

    subject = "Diwuqu,[账号数:" + str(len(account_list)) + ", 总额:" + str(round(total_values_all, 2)) + "]"


    # logger.warning('********** send_diwuqu_HtmlEmail(), mail_msg =' + mail_msg)

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_diwuqu_HtmlEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_Bixiang_HtmlEmail(to_list, content_list, server):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    head = '<!DOCTYPE HTML>' + \
           '<html id="pageLoading">' + \
           '<head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' + \
           '<title></title>' + \
           '<style type="text/css">' + \
           '/* Table Head */' + \
           '#table-7 thead th {' + \
           'background-color: rgb(81, 130, 187);' + \
           'color: #fff;' + \
           'border-bottom-width: 1;' + \
           '}' + \
           '/* Column Style */' + \
           '#table-7' + \
           'td {' + \
           'color: #000;' + \
           '}' + \
           '/* Heading and Column Style */' + \
           '#table-7 tr, #table-7 th {' + \
           'border-width: 1px;' + \
           'border-style: solid;' + \
           'border-color: rgb(0, 0, 0);' + \
           '}' + \
           '/* Padding and font style */' + \
           '#table-7 td, #table-7 th {' + \
           'padding: 5px 10px;' + \
           'font-size: 12px;' + \
           'font-family: Verdana;' + \
           'font-weight: bold;' + \
           '}' + \
           '</style>' + \
           '</head>' + \
           '<body>' + \
           '<p> ********** ' + datetime + ' ********** </p>' + \
           '<table border="1px" cellspacing="0px" style="border-collapse:collapse" id="table-7">' + \
           '<thead>' + \
           '<th align="center">No.</th>' + \
           '<th align="center">Phone</th>' + \
           '<th align="center">nickname</th>' + \
           '<th align="center">uid</th>' + \
           '<th align="center">show_id</th>' + \
           '<th align="center">unique</th>' + \
           '<th align="center">BX总数</th>' + \
           '<th align="center">BX今日</th>' + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    body = ''
    total_bx_all = 0
    today_bx_all = 0
    i = 0
    for item in content_list:
        i = i + 1
        phone = item.get('phone', 'NA')
        nickname = item.get('nickname', 'NA')
        uid = item.get('uid', 'NA')
        show_id = item.get('show_id', 'NA')
        unique = item.get('unique', 'NA')
        total_bx = item.get('total_bx', 'NA')
        total_bx_all = total_bx_all + total_bx
        today_bx = item.get('today_bx', 'NA')
        today_bx_all = today_bx_all + today_bx
        body = body + '<tr><td align="center">' + str(i) + \
               '</td><td align="center">' + str(phone) + \
               '</td><td align="center">' + str(nickname) + \
               '</td><td align="center">' + str(uid) + \
               '</td><td align="center">' + str(show_id) + \
               '</td><td align="center">' + str(unique) + \
               '</td><td align="right">' + str(round(total_bx, 2)) + \
               '</td><td align="right">' + str(round(today_bx, 2)) + \
               '</td></tr>'

    sum = body + '<tr><td colspan="6" align="center">Sum:</td><td align="right">' + \
          str(round(total_bx_all, 2)) + '</td><td align="right">' + \
          str(round(today_bx_all, 2)) + '</td></tr>'
    mail_msg = head + sum + end

    subject = "Bixiang, "+server+" [BX总数:" + str(round(total_bx_all, 2)) + ", BX今日:" + str(
        round(today_bx_all, 2)) + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_Bixiang_HtmlEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_star163_HtmlEmail(to_list, subject, content):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    mail_msg = content

    subject = "Star163 [" + subject + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_HashWorld_LandEmail(to_list, content_list):
    logger.warning('********** send_HashWorld_LandEmail(), content_list length=' + str(len(content_list)))

    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    head = '<!DOCTYPE HTML>' + \
           '<html id="pageLoading">' + \
           '<head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' + \
           '<title></title>' + \
           '<style type="text/css">' + \
           '/* Table Head */' + \
           '#table-7 thead th {' + \
           'background-color: rgb(179, 103, 48);' + \
           'color: #fff;' + \
           'border-bottom-width: 1;' + \
           '}' + \
           '/* Column Style */' + \
           '#table-7' + \
           'td {' + \
           'color: #000;' + \
           '}' + \
           '/* Heading and Column Style */' + \
           '#table-7 tr, #table-7 th {' + \
           'border-width: 1px;' + \
           'border-style: solid;' + \
           'border-color: rgb(0, 0, 0);' + \
           '}' + \
           '/* Padding and font style */' + \
           '#table-7 td, #table-7 th {' + \
           'padding: 5px 10px;' + \
           'font-size: 12px;' + \
           'font-family: Verdana;' + \
           'font-weight: bold;' + \
           '}' + \
           '</style>' + \
           '</head>' + \
           '<body>' + \
           '<p> ********** ' + datetime + ' ********** </p>' + \
           '<table border="1px" cellspacing="0px" style="border-collapse:collapse" id="table-7">' + \
           '<thead>' + \
           '<th align="center">No.</th>' + \
           '<th align="center">Land_Num</th>' + \
           '<th align="center">Land_Name</th>' + \
           '<th align="center">Price</th>' + \
           '<th align="center">tradable_status</th>' + \
           '<th align="center">gen_time</th>' + \
           '<th align="center">nickname</th>' + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    body = ''

    i = 0
    for item in content_list:
        i = i + 1
        land_num = item.get('land_num', 'NA')
        land_name = item.get('land_name', 'NA')
        price = item.get('price', 'NA')
        tradable_status = item.get('tradable_status', 'NA')
        gen_time = item.get('gen_time', 'NA')
        nickname = item.get('nickname', 'NA')

        body = body + '<tr><td align="center">' + str(i) + \
               '</td><td align="center">' + str(land_num) + \
               '</td><td align="center">' + land_name + \
               '</td><td align="right">' + str(price) + \
               '</td><td align="center">' + tradable_status + \
               '</td><td align="center">' + str(gen_time) + \
               '</td><td align="center">' + nickname + \
               '</td></tr>'
    sum = body + '<tr><td colspan="2" align="center">Sum:</td><td align="right"></td><td></td><td></td><td></td><td></td></tr>'
    mail_msg = head + sum + end

    # subject = "HashWorld, [Value:" + str(round(value_total, 2)) + "]"
    subject = "HashWorld, [Total Land: " + str(i) + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_HashWorld_LandEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_HashWorld_HtmlEmail(to_list, content_list, server):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    head = '<!DOCTYPE HTML>' + \
           '<html id="pageLoading">' + \
           '<head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' + \
           '<title></title>' + \
           '<style type="text/css">' + \
           '/* Table Head */' + \
           '#table-7 thead th {' + \
           'background-color: rgb(81, 130, 187);' + \
           'color: #fff;' + \
           'border-bottom-width: 1;' + \
           '}' + \
           '/* Column Style */' + \
           '#table-7' + \
           'td {' + \
           'color: #000;' + \
           '}' + \
           '/* Heading and Column Style */' + \
           '#table-7 tr, #table-7 th {' + \
           'border-width: 1px;' + \
           'border-style: solid;' + \
           'border-color: rgb(0, 0, 0);' + \
           '}' + \
           '/* Padding and font style */' + \
           '#table-7 td, #table-7 th {' + \
           'padding: 5px 10px;' + \
           'font-size: 12px;' + \
           'font-family: Verdana;' + \
           'font-weight: bold;' + \
           '}' + \
           '</style>' + \
           '</head>' + \
           '<body>' + \
           '<p> ********** ' + datetime + ' ********** </p>' + \
           '<table border="1px" cellspacing="0px" style="border-collapse:collapse" id="table-7">' + \
           '<thead>' + \
           '<th align="center">No.</th>' + \
           '<th align="center">phone</th>' + \
           '<th align="center">value</th>' + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    body = ''
    value_total = 0
    i = 0
    for item in content_list:
        i = i + 1
        phone = item.get('phone', 'NA')
        value = item.get('value', 'NA')
        value_total = value_total + value

        body = body + '<tr><td align="center">' + str(i) + \
               '</td><td align="center">' + phone + \
               '</td><td align="right">' + str(round(value, 2)) + '</td></tr>'
    sum = body + '<tr><td colspan="2" align="center">Sum:</td><td align="right">' + \
          str(round(value_total, 2)) + '</td></tr>'
    mail_msg = head + sum + end
    # mail_msg = "hello, hashworld"

    subject = "哈希世界, "+server+" [Value:" + str(round(value_total, 2)) + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_HashWorld_HtmlEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_OneChain_HtmlEmail(to_list, content_list):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    content_data = content_list[0]
    keys = content_data.keys()
    th = ''
    for key in keys:
        th += '<th align="center">' + key + '</th>'

    head = '<!DOCTYPE HTML>' + \
           '<html id="pageLoading">' + \
           '<head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' + \
           '<title></title>' + \
           '<style type="text/css">' + \
           '/* Table Head */' + \
           '#table-7 thead th {' + \
           'background-color: rgb(81, 130, 187);' + \
           'color: #fff;' + \
           'border-bottom-width: 1;' + \
           '}' + \
           '/* Column Style */' + \
           '#table-7' + \
           'td {' + \
           'color: #000;' + \
           '}' + \
           '/* Heading and Column Style */' + \
           '#table-7 tr, #table-7 th {' + \
           'border-width: 1px;' + \
           'border-style: solid;' + \
           'border-color: rgb(0, 0, 0);' + \
           '}' + \
           '/* Padding and font style */' + \
           '#table-7 td, #table-7 th {' + \
           'padding: 5px 10px;' + \
           'font-size: 12px;' + \
           'font-family: Verdana;' + \
           'font-weight: bold;' + \
           '}' + \
           '</style>' + \
           '</head>' + \
           '<body>' + \
           '<p> ********** ' + datetime + ' ********** </p>' + \
           '<table border="1px" cellspacing="0px" style="border-collapse:collapse" id="table-7">' + \
           '<thead>' + \
           '<th align="center">No.</th>' + th + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    i = 0
    tr = ''
    for item in content_list:
        i = i + 1
        tr = tr + '<tr><td align="center">' + str(i) + '</td>'
        for key in keys:
            tr = tr + '<td align="center">' + str(item.get(key, 0)) + '</td>'
        tr = tr + '</tr>'

    mail_msg = head + tr
    subject = 'OneChain'

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_OneChain_HtmlEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_Elephant_htmlmail(to_list, subject, content_list):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    head = '<!DOCTYPE HTML>' + \
           '<html id="pageLoading">' + \
           '<head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' + \
           '<title></title>' + \
           '<style type="text/css">' + \
           '/* Table Head */' + \
           '#table-7 thead th {' + \
           'background-color: rgb(81, 130, 187);' + \
           'color: #fff;' + \
           'border-bottom-width: 1;' + \
           '}' + \
           '/* Column Style */' + \
           '#table-7' + \
           'td {' + \
           'color: #000;' + \
           '}' + \
           '/* Heading and Column Style */' + \
           '#table-7 tr, #table-7 th {' + \
           'border-width: 1px;' + \
           'border-style: solid;' + \
           'border-color: rgb(0, 0, 0);' + \
           '}' + \
           '/* Padding and font style */' + \
           '#table-7 td, #table-7 th {' + \
           'padding: 5px 10px;' + \
           'font-size: 12px;' + \
           'font-family: Verdana;' + \
           'font-weight: bold;' + \
           '}' + \
           '</style>' + \
           '</head>' + \
           '<body>' + \
           '<p> ********** ' + datetime + ' ********** </p>' + \
           '<table border="1px" cellspacing="0px" style="border-collapse:collapse" id="table-7">' + \
           '<thead>' + \
           '<th align="center">No.</th>' + \
           '<th align="center">Url</th>' + \
           '<th align="center">投入</th>' + \
           '<th align="center">泡泡</th>' + \
           '<th align="center">备注</th>' + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    body = ''
    for i in range(len(content_list)):
        try:
            item = content_list[i]
            url = item.get('url', 'NA')
            touru = item.get('touru', 'NA')
            pop = item.get('pop', 'NA')
            other = item.get('other', 'NA')

            body = body + '<tr><td align="center">' + str(i) + \
                   '</td><td align="left"><a href="' + url + '">' + url + '</a>' \
                                                                          '</td><td align="left">' + touru + \
                   '</td><td align="left">' + pop + \
                   '</td><td align="right">' + other + \
                   '</td></tr>'
        except Exception as e:
            continue

    sum = body + '<tr><td colspan="2" align="center">Sum:</td><td></td><td></td><td></td></tr>'
    mail_msg = head + sum + end

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_Elephant_htmlmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False

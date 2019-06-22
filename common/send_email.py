#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import email
import logging
import poplib
import time
from email.header import decode_header
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import parseaddr
from io import StringIO
from smtplib import SMTP_SSL

# 第一步，创建一个logger,并设置级别
from lxml import etree

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
# mail_pass = "Liuxb0504$"  # 密码
mail_pass = "epay1234"  # 密码
mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com


def get_email_epay(email, password):
    pop3_server = "pop.163.com"
    # 连接到POP3服务器:
    server = poplib.POP3(pop3_server)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))

    try:
        # 身份认证:
        server.user(email)
        server.pass_(password)
    except Exception as e:
        logger.warning('>>>>>>>>>> 登录邮箱失败，无授权码。账号：' + email)
        captcha = input(">>>>>>>>>> 手工输入captcha: ")
        return captcha

    captcha = 0

    try:

        # stat()返回邮件数量和占用空间:
        # print('Messages: %s. Size: %s' % server.stat())
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        # print(mails)

        # 获取最新一封邮件, 注意索引号从1开始:
        index = len(mails)
        resp, lines, octets = server.retr(index)

        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        # print(msg)
        # print("解码后的邮件信息:\r\n"+str(msg))

        html = get_mail_content(msg)
        # print(html)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)


        h2_code = tree.xpath('/html/body/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/h2')[0]
        # t = etree.tostring(h2_code[0], encoding="utf-8", pretty_print=True)
        # content = etree.tostring(h2_code, pretty_print=True, method='html')  # 转为字符串
        # print(content)
        t = str(h2_code.xpath('text()')[0])
        # print(t)

        captcha = t[-6:]

        # 可以根据邮件索引号直接从服务器删除邮件:
        server.dele(index)

    except Exception as e:
        print(e)


    # 关闭连接:
    server.quit()

    # logger.warning('********** get_email_epay(), capcha =' + str(captcha))
    return captcha


def get_mail_content(msg):
    if msg == None:
        return None
    for part in msg.walk():
        if not part.is_multipart():
            data = part.get_payload(decode=True)
            # print("emailcontent:\r\n"+data.decode())
    return data.decode()


# 解析subject对象
def parse_subject(msg):
    if msg != None:
        subject = msg.get('subject')
        # header = email.Header.Header(subject)
        # decode_h = email.Header.decode_header(header)
        # return decode_h[0][0]
    else:
        empty_obj()


# msg is empty
def empty_obj():
    print('msg is empty!')


# 获取发件人邮箱
def get_from(msg):
    if msg != None:
        return email.utils.parseaddr(msg.get("from"))[1]
    else:
        empty_obj()


# 获取收件人邮箱
def get_to(msg):
    if msg != None:
        return email.utils.parseaddr(msg.get('to'))[1]
    else:
        empty_obj()


# 获取邮件的生成时间
def get_date(msg):
    if msg != None:
        return email.utils.parseaddr(msg.get('date'))[1]
    else:
        empty_obj()


# 获取邮件的生成版本
def get_mime_version(msg):
    if msg != None:
        return email.utils.parseaddr(msg.get('mime-version'))[1]
    else:
        empty_obj()


# 获取邮件的文本类型
def get_content_type(msg):
    if msg != None:
        return email.utils.parseaddr(msg.get('content-type'))[1]
    else:
        empty_obj()


# 获取邮件的邮件的id
def get_message_id(msg):
    if msg != None:
        return email.utils.parseaddr(msg.get('message-id'))[1]
    else:
        empty_obj()


# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        # 输出From, To, Subject, Date头部及其信息
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()

        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            # 递归打印每一个子对象:
            print_info(part, indent + 1)
    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            # 不是文本,作为附件处理:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def send_mail(to_list, sub, content):
    me = "newseeing@163.com"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
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
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
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
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
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

    subject = "Bixiang, " + server + " [BX总数:" + str(round(total_bx_all, 2)) + ", BX今日:" + str(
        round(today_bx_all, 2)) + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_Bixiang_HtmlEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_Epay_HtmlEmail(to_list, content_list, server):
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
           '<th align="center">ID</th>' + \
           '<th align="center">静态收益(ET)</th>' + \
           '<th align="center">动态收益(ET)</th>' + \
           '<th align="center">社区奖励(ET)</th>' + \
           '<th align="center">拉新奖励(ET)</th>' + \
           '<th align="center">积分</th>' + \
           '<th align="center">日合计(ET)</th>' + \
           '<th align="center">投资总数(ET)</th>' + \
           '<th align="center">最早笔金额(ET)</th>' + \
           '<th align="center">已持续天数</th>' + \
           '<th align="center">Level</th>' + \
           '<th align="center">Team总人数</th>' + \
           '<th align="center">Team团队业绩($)</th>' + \
           '</thead>' + \
           '<tbody>'

    end = '</tbody>' + \
          '</table>' + \
          '</body>' + \
          ' </html>'

    body = ''
    total_income = 0
    total_commission = 0
    total_award = 0
    total_activity = 0
    total_score = 0
    total_et = 0
    total_invest = 0

    i = 0
    for item in content_list:
        i = i + 1
        account_id = item.get('account_id', 'NA')

        # 静态收益
        income = float(item.get('income', 'NA'))
        total_income = total_income + income

        # 动态收益
        commission = float(item.get('commission', 'NA'))
        total_commission = total_commission + commission

        # 社区奖励
        award = float(item.get('award', 'NA'))
        total_award = total_award + award

        # 拉新奖励
        activity = float(item.get('activity', 'NA'))
        total_activity = total_activity + activity

        # 积分
        score = float(item.get('score', 'NA'))
        total_score = total_score + score

        # ET总数(日)
        et = float(item.get('et', 'NA'))
        total_et = total_et + et

        investment_sum = float(item.get('investment_sum', 'NA'))
        total_invest = total_invest + investment_sum

        investment_earliest_amount = item.get('investment_earliest_amount', 'NA')

        investment_earliest_days = item.get('investment_earliest_days', 'NA')


        my_level = item.get('my_level', 'NA')
        team_member_count = item.get('team_member_count', 'NA')
        investment_sum_team = float(item.get('investment_sum_team', 'NA'))

        body = body + '<tr><td align="center">' + str(i) + \
               '</td><td align="center">' + str(account_id) + \
               '</td><td align="right">' + str(round(float(income), 2)) + \
               '</td><td align="right">' + str(round(float(commission), 2)) + \
               '</td><td align="right">' + str(round(float(award), 2)) + \
               '</td><td align="right">' + str(round(float(activity), 2)) + \
               '</td><td align="right">' + str(round(float(score), 2)) + \
               '</td><td align="right">' + str(round(et, 2)) + \
               '</td><td align="right">' + str(round(investment_sum, 2)) + \
               '</td><td align="right">' + str(investment_earliest_amount) + \
               '</td><td align="right">' + str(investment_earliest_days) + \
               '</td><td align="right">' + str(my_level) + \
               '</td><td align="right">' + str(team_member_count) + \
               '</td><td align="right">' + str(round(investment_sum_team, 2)) + \
               '</td></tr>'

    sum = body + '<tr><td colspan="2" align="center">Sum:</td>' \
                 '<td align="right">' + str(round(total_income, 2)) + '</td>' \
                 '<td align="right">' + str(round(total_commission, 2)) + '</td>' \
                 '<td align="right">' + str(round(total_award, 2)) + '</td>' \
                 '<td align="right">' + str(round(total_activity, 2)) + '</td>' \
                 '<td align="right">' + str(round(total_score, 2)) + '</td>' \
                 '<td align="right">' + str(round(total_et, 2)) + '</td>' \
                 '<td align="right">' + str(round(total_invest, 2)) + '</td>' \
                 '<td align="right"></td>' \
                 '<td align="right"></td>' \
                 '<td align="right"></td>' \
                 '<td align="right"></td>' \
                 '<td align="right"></td>' \
                 '</tr>'
    mail_msg = head + sum + end

    subject = "Epay "+server+" [ET总数:" + str(round(total_et, 2)) + ", Invest总数:" + str(
        round(total_invest, 2)) + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_Epay_HtmlEmail(), subject =' + subject)

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
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
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
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_HashWorld_LandEmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_HashWorld_HtmlEmail(to_list, all_coin_list, server):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    th = ''
    coin_list = all_coin_list[0]
    # phone = coin_list[0].get('phone', 'NA')
    th += '<th align="center">Phone</th>'
    for m in range(len(coin_list)):
        coin = coin_list[m]
        th += '<th colspan="3" align="center">' + coin.get('symbol', 'NA') + '</th>'

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

    body = ''
    value_total = 0
    i = 0
    for n in range(len(all_coin_list) - 1):
        i = i + 1
        phone = all_coin_list[n][0].get('phone', 'NA')
        body = body + '<tr><td align="center">' + str(i) + \
               '</td><td align="center">' + phone

        lists = all_coin_list[n]
        for p in range(len(lists)):
            item = lists[p]
            symbol = item.get('symbol', 'NA')
            market_price_cny = item.get('market_price_cny', 0)
            active_balance = item.get('active_balance', 0)
            value = item.get('value', 0)
            # value_total = value_total + value

            body = body + \
                   '</td><td align="right">' + str(round(market_price_cny, 2)) + '</td>' + \
                   '</td><td align="right">' + str(round(active_balance, 2)) + '</td>' + \
                   '</td><td align="right">' + str(round(value, 2)) + '</td>'
        body = body + '</tr>'

    length = len(all_coin_list)
    last = all_coin_list[length - 1]
    sum = '<tr><td colspan="2" align="center">Sum:</td>'
    for t in range(len(last)):
        item = last[t]
        active_balance = item.get('active_balance', 0)
        value = item.get('value', 0)
        sum = sum + \
              '</td><td align="right">  </td>' + \
              '</td><td align="right">' + str(round(active_balance, 2)) + '</td>' + \
              '</td><td align="right">' + str(round(value, 2)) + '</td>'
    sum = sum + '</tr>'

    mail_msg = head + body + sum + end
    # mail_msg = "hello, hashworld"

    subject = "哈希世界, " + server + " [Value:" + str(round(value_total, 2)) + "]"

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
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
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
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

    sum = body + '<tr><td colspan="2" align="center">Sum:</td><td></td><td></td><td></td></tr>'
    mail_msg = head + sum + end

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    me = "newseeing@163.com"
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = "newseeing@163.com"
    # msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        # server = smtplib.SMTP()
        server = SMTP_SSL("smtp.163.com")
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())

        logger.warning('********** send_Elephant_htmlmail(), subject =' + subject)

        server.close()
        return True
    except Exception as e:
        print(e)
        return False

# get_email_epay("chain7947@163.com", "epay1234")

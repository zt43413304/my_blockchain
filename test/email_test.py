# coding:utf8
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

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


send_mail('newseeing@163.com', 'Subject2', "Content")

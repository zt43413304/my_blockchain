# -*- coding: UTF-8 -*-
import urllib
from urllib import request

# if __name__ == "__main__":
#     #访问网址
#     # url = 'http://www.whatismyip.com.tw/'
#     url = 'http://www.baidu.com'
#     #这是代理IP
#     # proxy = "14.134.169.0:808"
#     proxy = {'http':'111.76.137.119:808'}
#     #创建ProxyHandler
#     # proxy_handler = request.ProxyHandler(
#     #     {
#     #         'http':'http://'+proxy,
#     #         'https':'https://'+proxy
#     #     }
#     # )
#
#     proxy_handler=request.ProxyHandler(proxy)
#
#     #创建Opener
#     opener = request.build_opener(proxy_handler)
#     #添加User Angent
#     opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
#     #安装OPener
#     request.install_opener(opener)
#     #使用自己安装好的Opener
#     response = request.urlopen(url)
#     #读取相应信息并解码
#     html = response.read().decode("utf-8")
#     #打印信息
#     print(html)
from urllib.request import urlopen

proxy_handler = urllib.request.ProxyHandler({'http': '111.76.137.119:808'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
page = urlopen('http://ip.chinaz.com/getip.aspx')
print(page.read().decode('utf-8'))
# {ip:'221.238.67.231',address:'天津市 电信'}

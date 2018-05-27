# -*- coding: UTF-8 -*-
from io import StringIO

import requests
from lxml import etree

headers = {
    'Host': "tui.yingshe.com",
    'Connection': "close",
    'Accept-Encoding': "gzip",
    'User-Agent': "okhttp/3.4.1",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}

# url = 'http://tui.yingshe.com/user/property?xxx=dMDuGOyXFhRuMLzuFOyDH'
url = 'http://tui.yingshe.com/user/property?xxx=P9VPpXlIkUGE5NmCTAGITgESjN3Fn91HoYFn6Szc3Nz5k%3DGDlUUrRMkAv'

try:
    response = requests.request("GET", url, headers=headers)
    html = response.text

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
    # print(result)

    result1 = tree.xpath('//*[@id="wallet"]/a[1]/li/span[2]/text()')
    print(result1[0])

    result2 = tree.xpath('//*[@id="wallet"]/a[1]/li/span[3]/span/text()')
    print(result2[0])

except Exception as e:
    print(e)

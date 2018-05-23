# coding=utf-8

import urllib.parse

url = 'http://tui.yingshe.com/user/property?xxx=vzlsIdmCYyW2Ji1CbiWsc'

parsed = urllib.parse.urlparse(url)
print(parsed)
print(parsed.query)

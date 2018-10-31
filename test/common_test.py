# coding=utf-8

url = 'http://tui.yingshe.com/user/property?xxx=vzlsIdmCYyW2Ji1CbiWsc'

# parsed = urllib.parse.urlparse(url)
# print(parsed)
# print(parsed.query)

# filename = "data_bixiang_Tokyo.json"
filename = "data_bixiang_Aliyun.json"
server = filename.split('.')[0][-5:]
print(server)
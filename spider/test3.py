import urllib.request
import ssl
import urllib.parse

name = urllib.parse.quote('你好')#转二进制编码
print(name)
date={'a' :'你好',
      'b':'他好'
    
    
}
print(urllib.parse.urlencode(date));
#urlencode

# 创建SSL上下文，不验证证书
# context = ssl.create_default_context()
# context.check_hostname = False
# context.verify_mode = ssl.CERT_NONE

headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
}

url="http://www.baidu.com"
request=urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
print(response.getcode())  # 使用getcode()获取状态码，而不是status
content = response.read().decode('utf-8')

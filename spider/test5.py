import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
url="https://movie.douban.com/subject/34780991/comments?percent_type=l&limit=20&status=P&sort=new_score"
headers={
   'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
}
request=urllib.request.Request(url=url,headers=headers)#打包

response=urllib.request.urlopen(request) #发送请求

content =response.read().decode('utf-8') #解码

print(content);
import re 
ret = re.findall(pattern="")
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    "User-Agent" :"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}

f =open(__file__.replace("南阳理工学院新闻爬虫.py","南阳理工新闻列表.txt"),"w")

for i in range(2,1,-1):
    url = f"https://www.nyist.edu.cn/xwdt/jxky/{i}.htm"
    request=urllib.request.Request(url=url,headers=headers)#打包

    response=urllib.request.urlopen(request) #发送请求

    content =response.read().decode('utf-8') #解码


    
    

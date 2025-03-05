import requests
from bs4 import BeautifulSoup
headers = {
    "User-Agent" :"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}

f =open(__file__.replace("南阳理工学院新闻爬虫.py","南阳理工新闻列表.txt"),"w")

for i in range(2,1,-1):
    s = f"https://www.nyist.edu.cn/xwdt/jxky/{i}.htm"
    request = requests.get(s,headers=headers)
    content = request.text ;
    soup = BeautifulSoup(content,"html.parser")
    for j in range(0,15):
        title =soup.findAll("li",attrs={"id":f"line_u9_{j}"})
        print(title)
      
    
    

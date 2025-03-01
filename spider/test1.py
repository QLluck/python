import requests
from bs4 import BeautifulSoup
s = "https://movie.douban.com/top250"
response = requests.get(s,headers=headers).text


f = open(__file__.replace("test1.py","test2.txt"),"w")

jiexi = BeautifulSoup(response,"html.parser")
obj = jiexi.find_all("span",class_="title")
for i in obj:
    f.write(i.get_text())
f.close();

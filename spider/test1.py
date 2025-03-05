import requests
from bs4 import BeautifulSoup
f = open(__file__.replace("test1.py","test2.txt"),"w")
f.close();
headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}
for start_num in range(0,250,25):
    s = f"https://movie.douban.com/top250?start={str(start_num)}&filter="


    html = requests.get(s,headers=headers).text



    f = open(__file__.replace("test1.py","test2.txt"),"a")
    soup=BeautifulSoup(html,"html.parser")
    all_title=soup.findAll("span",attrs={"class":"title"})
    all_rating = soup.findAll("span",attrs={"class":"rating_num","property":"v:average"})
    allChTitle = []
    for title in all_title:
        if "/" not in title.string :
            allChTitle.append(title.string);
    for i,j in zip(allChTitle,all_rating):
        f.write(i +" "+ j.string+'\n')
    f.close()
    

        
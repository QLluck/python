import requests
import os 
from bs4 import BeautifulSoup 
headers = {
    "User-Agent" :"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}
basename = os.path.basename(__file__)
f = open(__file__.replace(basename,"特效nb的网页源码.txt"),"w");
url = "https://noodlemagazine.com/new-video"
request = requests.get(url,headers=headers)
content = request.text;
soup = BeautifulSoup(content,"html.parser")
f.write(content)
f.close()
request.close()

 
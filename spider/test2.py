import urllib.request
url = "http://www.baidu.com";
response = urllib.request.urlopen(url);
#response 中有很多数据
content=response.read().decode("utf-8")
#read 方法返回的是字节形式的二进制数据
#二进制转字符串 又称为解码 
f=open(__file__.replace("test2.py","test2.txt"),'w')
f.write(content);
f.close()
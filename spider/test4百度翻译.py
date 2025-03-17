import urllib.request
import urllib.parse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
url ='https://fanyi.baidu.com/sug'

name =input("请输入要翻译的内容");

headers={
'cookie':
'__bid_n=1939171cbb72192ab0abb3; BAIDU_WISE_UID=wapp_1734161838260_726; ZFY=XcWJ:BCrRJ6HQh1Kv9uRaTa5qrmH2AwpsW2HMcP3LvtU:C; BIDUPSID=40D96119C95D94F86C052993031D0D2D; PSTM=1738388637; BAIDUID=C6337A7BA1299CD6C65187F04FA307DB:FG=1; BAIDUID_BFESS=C6337A7BA1299CD6C65187F04FA307DB:FG=1; H_PS_PSSID=61027_62133_62325_62343_62346_62329_62369_62373_62421_62422_62427_62439_62476_62493_62518; BA_HECTOR=2g05008124ah25a4a1050k802f52fo1jt2rq423; PSINO=1; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_OGJmN2EzYWRhMDAyMmM5Zjk0MzQzMTZiNjhhOTVlNzU5YmY4ZDMxMTk5YzVjOWYwNDQwODVkMDVkYmUxMDRlMTQ1N2MyNDllYWEzOTgxODMyN2E3MTU4MTFjMmI0YmUwMGJiNmMwMWVkYmRkYjdiYTQ1OTgxZTM4ZmRmMGQ5MzljNTA0NGI4ZWFmMDVkZDlkNmQ0ZDU1NTZhNTkzMzdjZQ==; RT="z=1&dm=baidu.com&si=7d13b9d0-23f7-404d-8798-e132748325f0&ss=m85vlji9&sl=3&tt=2j2&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1cqa"'}
#post 请求必须进行编码 而且不会拼接在url后面
data ={
    'kw':name
}
#data必须编码
data=urllib.parse.urlencode(data).encode('utf-8')
request=urllib.request.Request(url=url,data=data,headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
print(content)

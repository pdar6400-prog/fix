import os, asyncio, aiohttp
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

try: import m2
except: pass

FIXED_URL = "https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=c4b25be7c214&gw_sn=H1U320M001153&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.24&mac=d4:29:a7:47:b9:9b&slot_num=14&nasip=192.168.1.166&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C006&chap_challenge=%5C262%5C050%5C017%5C376%5C373%5C321%5C110%5C247%5C102%5C033%5C243%5C231%5C130%5C012%5C345%5C112"

async def main():
    print("[*] Detecting network...")
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=False) as r:
                if r.status in (301, 302):
                    q = parse_qs(urlparse(r.headers.get('Location', '')).query)
                    gw = (q.get('gw_address') or q.get('nasip'))[0]
                    mac = (q.get('mac') or q.get('umac') or q.get('usermac'))[0]
                    
                    p = parse_qs(urlparse(FIXED_URL).query)
                    p.update({'mac':[mac], 'gw_address':[gw], 'nasip':[gw]})
                    url = urlunparse(urlparse(FIXED_URL)._replace(query=urlencode({k:v[0] for k,v in p.items()})))
                    
                    print(f"[+] Found: MAC={mac}, GW={gw}")
                    os.system(f"termux-open-url '{url}'" if os.path.exists('/data/data/com.termux/files/usr/bin/termux-open-url') else f"xdg-open '{url}'")
                    print("[*] Portal opened in browser.")
                else: print("[!] No portal detected.")
        except Exception as e: print(f"[!] Error: {e}")

if __name__ == "__main__": asyncio.run(main())

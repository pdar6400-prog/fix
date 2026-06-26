import os
import asyncio
import aiohttp
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ===== အရောင်တွေအတွက် =====
w = "\033[1;00m"
g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
b = "\033[1;34m"
reset = "\033[0m"

# ===== ပုံသေ URL (Base URL) =====
FIXED_URL = "https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=c4b25be7c214&gw_sn=H1U320M001153&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.24&mac=d4:29:a7:47:b9:9b&slot_num=14&nasip=192.168.1.166&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C006&chap_challenge=%5C262%5C050%5C017%5C376%5C373%5C321%5C110%5C247%5C102%5C033%5C243%5C231%5C130%5C012%5C345%5C112"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def Line():
    try:
        print(f"{y}-\033[1;00m" * os.get_terminal_size().columns)
    except:
        print(f"{y}-{w}" * 40)

def Logo():
    clear()
    # 100.py မှ Logo ကို အသုံးပြုထားပါသည်
    logo = f"""{b}
  ______   ________  ______   _______   __       __  __    __  __    __ 
 /      \\ /        |/      \\ /       \\ /  \\     /  |/  |  /  |/  |  /  |
/$$$$$$  |$$$$$$$$//$$$$$$  |$$$$$$$  |$$  \\   /$$ |$$ |  $$ |$$ |  $$ |
$$ \\__$$/    $$ |  $$ |__$$ |$$ |__$$ |$$$  \\ /$$$ |$$ |  $$ |$$  \\/$$/ 
$$      \\    $$ |  $$    $$ |$$    $$< $$$$  /$$$$ |$$ |  $$ | $$  $$<  
 $$$$$$  |   $$ |  $$$$$$$$ |$$$$$$$  |$$ $$ $$/$$ |$$ |  $$ |  $$$$  \\ 
/  \\__$$ |   $$ |  $$ |  $$ |$$ |  $$ |$$ |$$$/ $$ |$$ \\__$$ | $$ /$$  |
$$    $$/    $$ |  $$ |  $$ |$$ |  $$ |$$ | $/  $$ |$$    $$/ $$ |  $$ |
 $$$$$$/     $$/   $$/   $$/ $$/   $$/ $$/      $$/  $$$$$$/  $$/   $$/ {w}
"""
    print(logo)
    Line()
    print(f"{w}      [*] This tool is only for Ruijie Network Router")
    Line()

async def auto_detect_network():
    """Network မှ MAC နဲ့ Gateway IP ကို auto ရှာဖွေခြင်း"""
    print(f"{b}[*] Detecting network parameters...{reset}")
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(test_url, headers=headers, timeout=5, allow_redirects=False) as resp:
                if resp.status in (301, 302):
                    location = resp.headers.get('Location', '')
                    parsed_url = urlparse(location)
                    query_params = parse_qs(parsed_url.query)
                    
                    gw_addr = query_params.get('gw_address') or query_params.get('nasip')
                    mac_addr = query_params.get('mac') or query_params.get('umac') or query_params.get('usermac')
                    
                    res_gw = gw_addr[0] if gw_addr else None
                    res_mac = mac_addr[0] if mac_addr else None
                    
                    return res_gw, res_mac
        except Exception:
            pass
    
    return None, None

def open_url_silently(gw_ip, mac_addr):
    """URL အား အပြင်သို့ ထုတ်မပြဘဲ Browser ဖွင့်ခြင်း"""
    parsed = urlparse(FIXED_URL)
    params = parse_qs(parsed.query)
    
    if mac_addr:
        params['mac'] = [mac_addr]
        print(f"{g}[+] MAC Detected: {mac_addr}{reset}")
    
    if gw_ip:
        params['gw_address'] = [gw_ip]
        params['nasip'] = [gw_ip]
        print(f"{g}[+] Gateway Detected: {gw_ip}{reset}")
    
    # Query string ပြန်တည်ဆောက်ခြင်း
    new_query = urlencode({k: v[0] for k, v in params.items()})
    final_url = urlunparse(parsed._replace(query=new_query))
    
    # URL ကို print မထုတ်တော့ပါ
    try:
        # Termux တွင် browser ဖွင့်ရန် termux-open-url သို့မဟုတ် xdg-open ကို အသုံးပြုနိုင်သည်
        if os.path.exists('/data/data/com.termux/files/usr/bin/termux-open-url'):
            os.system(f'termux-open-url "{final_url}"')
        else:
            os.system(f'xdg-open "{final_url}"')
        print(f"\n{g}[*] Opening portal in browser...{reset}")
        print(f"{g}[*] Done! Please enter your code in the browser.{reset}")
    except Exception as e:
        print(f"{r}[!] Failed to open browser: {e}{reset}")

async def main():
    Logo()
    
    gw_ip, mac_addr = await auto_detect_network()
    
    if not gw_ip or not mac_addr:
        print(f"{y}[!] Auto detection failed. Please enter manually.{reset}")
        mac_addr = input(f"{g}[?] Enter MAC address: {reset}").strip() or mac_addr
        gw_ip = input(f"{g}[?] Enter Gateway IP: {reset}").strip() or gw_ip
    
    if mac_addr and gw_ip:
        open_url_silently(gw_ip, mac_addr)
    else:
        print(f"{r}[!] Error: MAC and Gateway IP are missing.{reset}")
    
    print(f"\n{reset}Press Enter to exit...")
    input()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")

import os, asyncio, aiohttp, base64, re, time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin

try: import m2
except: pass

# Terminal Colors
bcyan = "\033[1;36m"
reset = "\033[0m"
white = "\033[0;37m"
bgreen = "\033[1;32m"
bred = "\033[1;31m"
yellow = "\033[0;33m"
magenta = "\033[1;35m"
g = "\033[1;32m"
r = "\033[1;31m"
b = "\033[1;34m"
y = "\033[1;33m"

# Encoded Portal URL
E = "aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/c3RhZ2U9cG9ydGFsJmd3X2lkPWM0YjI1YmU3YzIxNCZnd19zbj1IMVUzMjBNMDAxMTUzJmd3X2FkZHJlc3M9MTkyLjE2OC4xMTAuMSZnd19wb3J0PTIwNjAmaXA9MTkyLjE2OC4xMTAuMjQmbWFjPWQ0OjI5OmE3OjQ3OmI5OmdiJnNsb3RfbnVtPTE0Jm5hc2lwPTE5Mi4xNjguMS4xNjYmc3NpZD1WTEFOMjMzJnVzdGF0ZT0wJm1hY19yZXE9MSZ1cmw9aHR0cCUzQSUyRiUyRjE5Mi4xNjguMC4xJTJGJmNoYXBfaWQ9JTVDMDA2JmNoYXBfY2hhbGxlbmdlPSU1QzI2MiU1QzA1MCU1QzAxNyU1QzM3NiU1QzM3MyU1QzMyMSU1QzExMCU1QzI0NyU1QzEwMiU1QzAzMyU1QzI0MyU1QzIzMSU1QzEzMCU1QzAxMiU1QzM0NSU1QzExMg=="

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{b}  ______   ________  ______   _______   __       __  __    __  __    __ \n /      \\ /        |/      \\ /       \\ /  \\     /  |/  |  /  |/  |  /  |\n/$$$$$$  |$$$$$$$$//$$$$$$  |$$$$$$$  |$$  \\   /$$ |$$ |  $$ |$$ |  $$ |\n$$ \\__$$/    $$ |  $$ |__$$ |$$ |__$$ |$$$  \\ /$$$ |$$ |  $$ |$$  \\/$$/ \n$$      \\    $$ |  $$    $$ |$$    $$< $$$$  /$$$$ |$$ |  $$ | $$  $$<  \n $$$$$$  |   $$ |  $$$$$$$$ |$$$$$$$  |$$ $$ $$/$$ |$$ |  $$ |  $$$$  \\ \n/  \\__$$ |   $$ |  $$ |  $$ |$$ |  $$ |$$ |$$$/ $$ |$$ \\__$$ | $$ /$$  |\n$$    $$/    $$ |  $$ |  $$ |$$ |  $$ |$$ | $/  $$ |$$    $$/ $$ |  $$ |\n $$$$$$/     $$/   $$/   $$/ $$/   $$/ $$/      $$/  $$$$$$/  $$/   $$/ {reset}")
    print(f"{y}" + "-" * 60 + f"{reset}")
    print(f"      [*] This tool is only for Ruijie Network Router")
    print(f"{y}" + "-" * 60 + f"{reset}")

class RuijieLoginManager:
    def __init__(self):
        self.ip = None
        self.mac = None
        self.load_saved_ip()
        self.load_saved_mac()

    def load_saved_ip(self):
        if os.path.exists(".ip"):
            try:
                with open(".ip", "r") as f: self.ip = f.read().strip()
            except: self.ip = None

    def load_saved_mac(self):
        if os.path.exists(".mac"):
            try:
                with open(".mac", "r") as f: self.mac = f.read().strip()
            except: self.mac = None

    async def auto_detect_gateway(self, session):
        print(f"{b}[*] Detecting network parameters...{reset}")
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile'}
        
        try:
            async with session.get(test_url, headers=headers, timeout=5, allow_redirects=False) as resp:
                if resp.status in (301, 302):
                    location = resp.headers.get('Location', '')
                    parsed_url = urlparse(location)
                    query_params = parse_qs(parsed_url.query)
                    
                    gw_addr_list = query_params.get('gw_address') or query_params.get('nasip')
                    if gw_addr_list:
                        self.ip = gw_addr_list[0]
                        with open(".ip", "w") as f: f.write(self.ip)
                        print(f"{g}[+] Gateway Detected: {self.ip}{reset}")

                    mac_list = query_params.get('mac') or query_params.get('umac') or query_params.get('usermac')
                    if mac_list:
                        self.mac = mac_list[0]
                        with open(".mac", "w") as f: f.write(self.mac)
                        print(f"{g}[+] MAC Detected: {self.mac}{reset}")
                    return True
                else:
                    if self.ip and self.mac:
                        print(f"{g}[+] Using Cached Data: MAC={self.mac}, GW={self.ip}{reset}")
                        return True
        except:
            if self.ip and self.mac:
                print(f"{g}[+] Using Cached Connection: MAC={self.mac}, GW={self.ip}{reset}")
                return True
        return False

async def main():
    show_banner()
    manager = RuijieLoginManager()
    
    async with aiohttp.ClientSession() as session:
        detected = await manager.auto_detect_gateway(session)
        
        if not detected or not manager.mac or not manager.ip:
            if not manager.mac:
                print(f"{r}[-] MAC detection failed.{reset}")
                manager.mac = input(f"{g}[?] Enter MAC address: {reset}").strip()
            if not manager.ip:
                print(f"{r}[-] Gateway detection failed.{reset}")
                manager.ip = input(f"{g}[?] Enter Gateway IP: {reset}").strip()

        if manager.mac and manager.ip:
            print(f"\n{g}[*] Opening portal in browser...{reset}")
            U = base64.b64decode(E).decode()
            p = parse_qs(urlparse(U).query)
            p.update({'mac':[manager.mac], 'gw_address':[manager.ip], 'nasip':[manager.ip]})
            f = urlunparse(urlparse(U)._replace(query=urlencode({k:v[0] for k,v in p.items()})))
            
            os.system(f"termux-open-url '{f}'" if os.path.exists('/data/data/com.termux/files/usr/bin/termux-open-url') else f"xdg-open '{f}'")
            print(f"{g}[*] Done! Please enter your code in the browser.{reset}")
            
            # Run M2 Core if exists
            try:
                if 'm2' in globals() or 'm2' in locals():
                    if hasattr(m2, 'run'): m2.run()
                    elif hasattr(m2, 'main'): m2.main()
            except: pass
        else:
            print(f"{r}[!] Error: MAC and Gateway IP are required.{reset}")

    print(f"\n{white}Press Enter to exit...{reset}")
    input()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")

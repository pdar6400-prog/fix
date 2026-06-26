import os, asyncio, aiohttp, base64
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

try: import m2
except: pass

E = "aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/c3RhZ2U9cG9ydGFsJmd3X2lkPWM0YjI1YmU3YzIxNCZnd19zbj1IMVUzMjBNMDAxMTUzJmd3X2FkZHJlc3M9MTkyLjE2OC4xMTAuMSZnd19wb3J0PTIwNjAmaXA9MTkyLjE2OC4xMTAuMjQmbWFjPWQ0OjI5OmE3OjQ3OmI5OmdiJnNsb3RfbnVtPTE0Jm5hc2lwPTE5Mi4xNjguMS4xNjYmc3NpZD1WTEFOMjMzJnVzdGF0ZT0wJm1hY19yZXE9MSZ1cmw9aHR0cCUzQSUyRiUyRjE5Mi4xNjguMC4xJTJGJmNoYXBfaWQ9JTVDMDA2JmNoYXBfY2hhbGxlbmdlPSU1QzI2MiU1QzA1MCU1QzAxNyU1QzM3NiU1QzM3MyU1QzMyMSU1QzExMCU1QzI0NyU1QzEwMiU1QzAzMyU1QzI0MyU1QzIzMSU1QzEzMCU1QzAxMiU1QzM0NSU1QzExMg=="

def logo():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;34m  ______   ________  ______   _______   __       __  __    __  __    __ \n /      \\ /        |/      \\ /       \\ /  \\     /  |/  |  /  |/  |  /  |\n/$$$$$$  |$$$$$$$$//$$$$$$  |$$$$$$$  |$$  \\   /$$ |$$ |  $$ |$$ |  $$ |\n$$ \\__$$/    $$ |  $$ |__$$ |$$ |__$$ |$$$  \\ /$$$ |$$ |  $$ |$$  \\/$$/ \n$$      \\    $$ |  $$    $$ |$$    $$< $$$$  /$$$$ |$$ |  $$ | $$  $$<  \n $$$$$$  |   $$ |  $$$$$$$$ |$$$$$$$  |$$ $$ $$/$$ |$$ |  $$ |  $$$$  \\ \n/  \\__$$ |   $$ |  $$ |  $$ |$$ |  $$ |$$ |$$$/ $$ |$$ \\__$$ | $$ /$$  |\n$$    $$/    $$ |  $$ |  $$ |$$ |  $$ |$$ | $/  $$ |$$    $$/ $$ |  $$ |\n $$$$$$/     $$/   $$/   $$/ $$/   $$/ $$/      $$/  $$$$$$/  $$/   $$/ \033[0m")
    print("\033[1;33m" + "-" * 60 + "\033[0m")
    print("      [*] This tool is only for Ruijie Network Router")
    print("\033[1;33m" + "-" * 60 + "\033[0m")

async def main():
    logo()
    U = base64.b64decode(E).decode()
    gw, mac = "192.168.110.1", "d4:29:a7:47:b9:9b"
    
    print("\033[1;34m[*] Detecting network parameters...\033[0m")
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=False, timeout=3) as r:
                if r.status in (301, 302):
                    q = parse_qs(urlparse(r.headers.get('Location', '')).query)
                    gw = (q.get('gw_address') or q.get('nasip') or [gw])[0]
                    mac = (q.get('mac') or q.get('umac') or q.get('usermac') or [mac])[0]
        except: pass
    
    print(f"\033[1;32m[+] MAC Detected: {mac}\033[0m")
    print(f"\033[1;32m[+] Gateway Detected: {gw}\033[0m\n")
    
    print("\033[1;32m[*] Opening portal in browser...\033[0m")
    
    p = parse_qs(urlparse(U).query)
    p.update({'mac':[mac], 'gw_address':[gw], 'nasip':[gw]})
    f = urlunparse(urlparse(U)._replace(query=urlencode({k:v[0] for k,v in p.items()})))
    
    os.system(f"termux-open-url '{f}'" if os.path.exists('/data/data/com.termux/files/usr/bin/termux-open-url') else f"xdg-open '{f}'")
    
    print("\033[1;32m[*] Done! Please enter your code in the browser.\033[0m")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")

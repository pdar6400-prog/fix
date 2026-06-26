import os, asyncio, aiohttp, base64
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
try: import m2
except: pass
# URL ကို base64 နဲ့ encode လုပ်ထားပါတယ်
E = "aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/c3RhZ2U9cG9ydGFsJmd3X2lkPWM0YjI1YmU3YzIxNCZnd19zbj1IMVUzMjBNMDAxMTUzJmd3X2FkZHJlc3M9MTkyLjE2OC4xMTAuMSZnd19wb3J0PTIwNjAmaXA9MTkyLjE2OC4xMTAuMjQmbWFjPWQ0OjI5OmE3OjQ3OmI5OmdiJnNsb3RfbnVtPTE0Jm5hc2lwPTE5Mi4xNjguMS4xNjYmc3NpZD1WTEFOMjMzJnVzdGF0ZT0wJm1hY19yZXE9MSZ1cmw9aHR0cCUzQSUyRiUyRjE5Mi4xNjguMC4xJTJGJmNoYXBfaWQ9JTVDMDA2JmNoYXBfY2hhbGxlbmdlPSU1QzI2MiU1QzA1MCU1QzAxNyU1QzM3NiU1QzM3MyU1QzMyMSU1QzExMCU1QzI0NyU1QzEwMiU1QzAzMyU1QzI0MyU1QzIzMSU1QzEzMCU1QzAxMiU1QzM0NSU1QzExMg=="
async def main():
    U = base64.b64decode(E).decode()
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=False) as r:
                if r.status in (301, 302):
                    q = parse_qs(urlparse(r.headers.get('Location', '')).query)
                    gw, mac = (q.get('gw_address') or q.get('nasip'))[0], (q.get('mac') or q.get('umac') or q.get('usermac'))[0]
                    p = parse_qs(urlparse(U).query)
                    p.update({'mac':[mac], 'gw_address':[gw], 'nasip':[gw]})
                    f = urlunparse(urlparse(U)._replace(query=urlencode({k:v[0] for k,v in p.items()})))
                    os.system(f"termux-open-url '{f}'" if os.path.exists('/data/data/com.termux/files/usr/bin/termux-open-url') else f"xdg-open '{f}'")
                    print("[+] Portal Opened.")
                else: print("[-] No Portal.")
        except: print("[!] Error.")
if __name__ == "__main__": asyncio.run(main())

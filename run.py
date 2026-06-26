import sys
import os

# ANSI color codes
g = "\033[32m"
w = "\033[37m"
r = "\033[31m"

def mock_logo():
    # 100.py မှ Logo ကို အသုံးပြုထားပါသည်
    logo_text = f"""\033[1;34m
  ______   ________  ______   _______   __       __  __    __  __    __ 
 /      \\ /        |/      \\ /       \\ /  \\     /  |/  |  /  |/  |  /  |
/$$$$$$  |$$$$$$$$//$$$$$$  |$$$$$$$  |$$  \\   /$$ |$$ |  $$ |$$ |  $$ |
$$ \\__$$/    $$ |  $$ |__$$ |$$ |__$$ |$$$  \\ /$$$ |$$ |  $$ |$$  \\/$$/ 
$$      \\    $$ |  $$    $$ |$$    $$< $$$$  /$$$$ |$$ |  $$ | $$  $$<  
 $$$$$$  |   $$ |  $$$$$$$$ |$$$$$$$  |$$ $$ $$/$$ |$$ |  $$ |  $$$$  \\ 
/  \\__$$ |   $$ |  $$ |  $$ |$$ |  $$ |$$ |$$$/ $$ |$$ \\__$$ | $$ /$$  |
$$    $$/    $$ |  $$ |  $$ |$$ |  $$ |$$ | $/  $$ |$$    $$/ $$ |  $$ |
 $$$$$$/     $$/   $$/   $$/ $$/   $$/ $$/      $$/  $$$$$$/  $$/   $$/ \033[0m
"""
    print(logo_text)
    print("\033[1;33m" + "-" * 60 + "\033[0m")
    print("      [*] This tool is only for Ruijie Network Router")
    print("\033[1;33m" + "-" * 60 + "\033[0m")

def mock_run_session(encrypted_str, new_mac):
    print(f"{g}[+] Processing encrypted string: {encrypted_str}")
    print(f"{g}[+] Using MAC address: {new_mac}")
    print(f"{r}[!] Note: The actual processing logic is in a compiled .so file.")

try:
    import m2
except ImportError:
    # m2 module ကို import မရခဲ့ရင် mock function တွေသုံးမယ်
    m2 = type('Mock', (), {'Logo': mock_logo, 'run_session': mock_run_session})

if __name__ == "__main__":
    # m2 module ထဲက Logo function ကို ခေါ်ဖို့ ကြိုးစားမယ်
    if hasattr(m2, 'Logo'):
        m2.Logo()
    else:
        mock_logo()

    try:
        user_input = input(f"{g}[?] Enter the encrypted string: {w}")
        mac_input = input(f"{g}[?] Enter MAC address (e.g. 24:06:aa:4d:3f:13): {w}")
        
        if hasattr(m2, 'run_session'):
            m2.run_session(encrypted_str=user_input, new_mac=mac_input)
        else:
            mock_run_session(user_input, mac_input)
            
    except KeyboardInterrupt:
        print(f"\n{r}[!] Exiting...")

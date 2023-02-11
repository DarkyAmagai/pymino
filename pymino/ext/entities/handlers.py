from re import search
from sys import platform
from datetime import datetime
from os import system, environ
from contextlib import suppress
from colorama import Fore, Style

def check_debugger() -> bool:
    with suppress(Exception):
        return any([
            search("vscode", environ.get("TERM_PROGRAM")),
            search("pycharm", environ.get("TERM_PROGRAM"))
            ])
    
def orjson_exists() -> bool:
    if is_android(): return False

    try:
        from orjson import dumps as dumps
        return True
    except ImportError:
        system("pip install orjson")
        system("cls") if platform == "win32" else system("clear")
        return True
    
def is_android() -> bool:
    return any(key in environ for key in ("ANDROID_ROOT", "ANDROID_DATA"))

def is_repl() -> bool:
    return any(key for key in environ if key.lower().startswith("repl"))

def notify() -> None:
    print(f"\n{Fore.MAGENTA}[PYMINO] | {Fore.GREEN}BOT STATUS: {Fore.YELLOW}ONLINE | {Style.RESET_ALL}{datetime.now().strftime('%H:%M:%S')}\n")
    print(f"{Fore.RED}[!] {Fore.YELLOW}If you see this message, you can safely ignore it. The bot is still running and will continue to run until you stop it.{Style.RESET_ALL}\n")
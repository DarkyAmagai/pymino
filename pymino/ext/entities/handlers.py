from base64 import urlsafe_b64decode
from diskcache import Cache
from json import loads
from re import search
from .messages import Message
from datetime import datetime
from os import system, environ
from pip import main as pipmain
from contextlib import suppress

from colorama import Fore, Style

def check_debugger() -> bool:
    """
    Checks if the program is being run in a debugger.
    """
    with suppress(Exception):
        return any([
            search("vscode", environ.get("TERM_PROGRAM")),
            search("pycharm", environ.get("TERM_PROGRAM")),
            is_repl(), is_android()
            ])
    
def orjson_exists() -> bool:
    """
    Checks if orjson is installed. If it isn't, it will install it.
    """
    if is_android(): return False

    try:
        from orjson import dumps as dumps
        return True
    except ImportError:
        pipmain(["install", "orjson"])
        system("cls || clear")
        return True
    
def is_android() -> bool:
    """
    Checks if the program is running on an Android device.
    """
    return any(key in environ for key in ("ANDROID_ROOT", "ANDROID_DATA"))

def is_repl() -> bool:
    """
    Checks if the program is running on a repl.it instance.
    """
    return any(key for key in environ if key.lower().startswith("repl"))

def notify() -> None:
    """
    Notifies the user that the bot is online.
    """
    print(f"\n{Fore.MAGENTA}[PYMINO] | {Fore.GREEN}BOT STATUS: {Fore.YELLOW}ONLINE | {Style.RESET_ALL}{datetime.now().strftime('%H:%M:%S')}\n")
    print(f"{Fore.RED}[!] {Fore.YELLOW}If you see this message, you can safely ignore it. The bot is still running and will continue to run until you stop it.{Style.RESET_ALL}\n")

def parse_auid(sid: str) -> str:
    """Parses the user ID from a session ID."""
    decoded_sid = urlsafe_b64decode(f"{sid}==")
    decoded_json: dict = loads(decoded_sid[1:-20].decode())
    return decoded_json["2"]

def cache_login(email: str, device: str, sid: str):
    """Cache the login credentials for the current user."""
    with suppress(Exception):
        cache = Cache("cache")
        cache[email] = {"device": device, "sid": sid}

def fetch_cache(email: str) -> tuple:
    """Fetch the login credentials for the current user."""
    with suppress(Exception):
        cache = Cache("cache")
        return cache[email]["sid"], cache[email]["device"]

def cache_exists(email: str) -> bool:
    """Check if the cache exists for the current user."""
    with suppress(Exception):
        cache = Cache("cache")
        return email in cache
from base64 import urlsafe_b64decode
from random import randint
from time import time, sleep
from diskcache import Cache
from json import loads
from re import search
from asyncio import sleep as asleep
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

def install_wsaccel() -> None:
    """
    Try to install wsaccel if it isn't installed.
    """
    with Cache("cache") as cache:
        if cache.get("wsaccel"):
            return None

        try:
            from wsaccel import __version__
            cache.set("wsaccel", True)
            return True
        except ImportError:
            pipmain(["install", "wsaccel"])
            cache.set("wsaccel", True)
            system("cls || clear")
            return None

def orjson_exists() -> bool:
    """
    Checks if orjson is installed. If it isn't, it will install it.
    """
    if is_android(): return False

    install_wsaccel()
    with Cache("cache") as cache:
        if cache.get("orjson"):
            return True

        try:
            from orjson import dumps as dumps
            cache.set("orjson", True)
            return True
        except ImportError:
            pipmain(["install", "orjson"])
            cache.set("orjson", True)
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
    
async def alive_loop(ws) -> None:
    run_check = any([is_android(), is_repl()])

    start_time          = time()
    last_activity_time  = start_time
    last_message_time   = start_time
    while True:
        current_time = time()
        notify() if run_check else None

        with suppress(Exception):

            if await ws._is_interval_elapsed(
                last_time=ws._last_pinged,
                interval=15
            ) and not ws.reconnecting:
                await ws.reconnect()
                
            if await ws._is_interval_elapsed(
                last_time=last_message_time,
                interval=10
                ):
                last_message_time = current_time
                ws.loop.create_task(ws._send_message())

            if current_time - start_time >= 86400:
                start_time = current_time

            if all([await ws._is_interval_elapsed(
                last_time=last_activity_time,
                interval=300
                ),
                current_time - start_time <= 36000
                ]):
                ws.loop.create_task(ws._activity_status())
                last_activity_time = current_time

            await asleep(0)


def run_alive_loop(ws) -> None:
    run_check = False if ws.console_enabled else any([is_android(), is_repl()])
    
    start_time          = time()
    last_activity_time  = start_time
    last_message_time   = start_time

    while True:
        current_time = time()

        notify() if run_check else None

        with suppress(Exception):

            if ws._last_message(last_message_time):
                ws._send_message()
                last_message_time = current_time

            if current_time - start_time >= 86400:
                start_time = current_time

            if all([ws._last_active(last_activity_time), current_time - start_time <= 36000]):
                ws._activity_status()
                last_activity_time = current_time

            sleep(randint(25, 50))
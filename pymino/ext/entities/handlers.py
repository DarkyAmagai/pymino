import base64
import contextlib
import os
import random
import re
import time
import urllib.request
from typing import BinaryIO, Optional, Union

import colorama
import diskcache
import ujson

from pymino.ext import entities, socket

__all__ = (
    "Media",
    "cache",
    "cache_exists",
    "cache_login",
    "check_debugger",
    "fetch_cache",
    "is_android",
    "is_repl",
    "notify",
    "parse_auid",
    "read_media",
    "run_alive_loop",
)

colorama.init()

RUNNING_MSG = (
    f"{colorama.Fore.RED}[!] {colorama.Fore.YELLOW}"
    "If you see this message, you can safely ignore it. "
    "The bot is still running and will continue to run until you stop it.\n"
    f"{colorama.Fore.RED}[!] {colorama.Fore.YELLOW}"
    f"Press {colorama.Fore.RED}CTRL+C {colorama.Fore.YELLOW}to stop the bot."
    f"{colorama.Style.RESET_ALL}\n"
)

cache = diskcache.Cache("cache")

Media = Union[BinaryIO, bytes, str]


def check_debugger() -> bool:
    """Checks if the program is being run in a debugger."""
    ide_term = os.environ.get("TERM_PROGRAM", "").lower()
    return bool(
        re.search("vscode", ide_term) or
        re.search("pycharm", ide_term) or
        is_repl() or
        is_android()
    )


def is_android() -> bool:
    """Checks if the program is running on an Android device."""
    return any(key in os.environ for key in ("ANDROID_ROOT", "ANDROID_DATA"))


def is_repl() -> bool:
    """Checks if the program is running on a repl.it instance."""
    return any(key for key in os.environ if key.lower().startswith("repl"))


def notify() -> None:
    """Notifies the user that the bot is online."""
    time.sleep(0.1)
    print(RUNNING_MSG)


def parse_auid(sid: str) -> str:
    """Parses the user ID from a session ID."""
    decoded_sid = base64.urlsafe_b64decode(f"{sid}==")
    decoded_json = ujson.loads(decoded_sid[1:-20].decode())
    return decoded_json["2"]


def cache_login(email: str, device: str, sid: str) -> None:
    """Cache the login credentials for the current user."""
    with contextlib.suppress(Exception), cache:
        cache.set(email, {"device": device, "sid": sid}, expire=86400)


def fetch_cache(email: str) -> Optional[tuple[str, str]]:
    """Fetch the login credentials for the current user."""
    with contextlib.suppress(Exception), cache:
        cache.expire()
        data = cache[email]
        return (data["sid"], data["device"])


def cache_exists(email: str) -> bool:
    """Check if the cache exists for the current user."""
    with contextlib.suppress(Exception), cache:
        return email in cache
    return False


def run_alive_loop(ws: socket.WSClient) -> None:
    start_time = time.time()
    last_activity_time = start_time
    last_message_time = start_time

    notify()
    while True:
        current_time = time.time()
        with contextlib.suppress(Exception):
            if time.time() - last_message_time >= 30:
                ws._send_ping()  # pyright: ignore[reportPrivateUsage]
                last_message_time = current_time

            if current_time - start_time >= 86400:
                start_time = current_time

            if all(
                [
                    time.time() - last_activity_time >= 300,
                    current_time - start_time <= 36000,
                ]
            ):
                ws._activity_status()  # pyright: ignore[reportPrivateUsage]
                last_activity_time = current_time
            time.sleep(random.randint(25, 50))


def read_media(media: Media) -> bytes:
    if isinstance(media, str):
        if media.startswith("http") and "://" in media:
            try:
                with urllib.request.urlopen(media) as response:
                    data = response.read()
            except Exception as exc:
                raise entities.InvalidImage from exc
        elif os.path.exists(media) and os.path.isfile(media):
            with open(media, "rb") as f:
                data = f.read()
        else:
            raise entities.InvalidImage from None
    elif isinstance(media, BinaryIO):
        data = media.read()
    elif isinstance(media, bytes):  # pyright: ignore[reportUnnecessaryIsInstance]
        data = media
    else:
        raise entities.InvalidImage from None
    return data

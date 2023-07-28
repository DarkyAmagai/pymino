from typing import List
from requests import get
from colorama import Fore, Style

__title__ = 'pymino'
__author__ = 'cynical'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Cynical'
__version__ = '1.2.4.6'
__description__ = 'A Python wrapper for the aminoapps.com API'

from .bot import Bot
from .async_bot import AsyncBot
from .client import Client
from .async_client import AsyncClient

__all__: List[str] = [
    'Bot',
    'AsyncBot',
    'Client',
    'AsyncClient',
]

print("Join the pymino discord server: https://discord.gg/RuRzyya55Z")

try:
    latest_version = get("https://pypi.org/pypi/pymino/json").json()["info"]["version"]
except Exception as e:
    print(f"Failed to check the latest version: {e}")
else:
    if __version__ != latest_version:
        print(f"{Fore.RED}WARNING:{Style.RESET_ALL} You are using an outdated version of pymino ({__version__}). The latest version is {latest_version}.")
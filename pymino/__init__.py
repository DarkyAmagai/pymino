from typing import List
from requests import get
from colorama import Fore, Style

__title__ = 'pymino'
__author__ = 'cynical'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Cynical'
__version__ = '1.3.0.1'
__description__ = 'A Python wrapper for the aminoapps.com API'

from .bot import Bot
from .client import Client

__all__: List[str] = [
    'Bot',
    'Client',
]

print("Join the pymino discord server: https://discord.gg/3HRdkVNets.")

try:
    latest_version = get("https://pypi.org/pypi/pymino/json").json()["info"]["version"]
except Exception as e:
    print(f"Failed to check the latest version: {e}")
else:
    if __version__ != latest_version:
        print(f"{Fore.RED}WARNING:{Style.RESET_ALL} You are using an outdated version of pymino ({__version__}). The latest version is {latest_version}.")
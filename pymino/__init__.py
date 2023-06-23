__title__ = 'pymino'
__author__ = 'cynical'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Cynical'
__version__ = '1.2.1.9'
__description__ = 'A Python wrapper for the aminoapps.com API'

from .bot import Bot as Bot
from .async_bot import AsyncBot as AsyncBot
from .client import Client as Client

from requests import get
from colorama import Fore, Style

print("Join the pymino discord server: https://discord.gg/RuRzyya55Z")

latestVersion = get("https://pypi.org/pypi/pymino/json").json()["info"]["version"]

if __version__ != latestVersion:
    print(f"{Fore.RED}WARNING:{Style.RESET_ALL} You are using an outdated version of pymino ({__version__}). The latest version is {latestVersion}.")

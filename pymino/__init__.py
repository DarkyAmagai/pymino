from typing import TYPE_CHECKING

from pymino.bot import *
from pymino.client import *

__all__ = (
    "Bot",
    "Client",
)

__title__ = "pymino"
__author__ = "cynical"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Cynical"
__version__ = "1.3.4.9"
__description__ = "A Python wrapper for the aminoapps.com API"

print("Join the pymino Discord server: https://discord.gg/3HRdkVNets")

if not TYPE_CHECKING:
    import requests
    import colorama

    try:
        latest_version = requests.get(
            "https://api.github.com/repos/DarkyAmagai/pymino/releases?per_page=1",
            timeout=5,
        ).json()[0]["name"]
    except (requests.ConnectionError, requests.Timeout):
        print("Could not fetch version info from PyPI.")
    else:
        if __version__ != latest_version:
            print(
                f"{colorama.Fore.RED}WARNING:{colorama.Style.RESET_ALL} "
                f"You are using an outdated version of pymino ({__version__}). "
                f"The latest version is {latest_version}."
            )
        del latest_version
    del requests, colorama

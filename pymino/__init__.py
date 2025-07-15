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
__version__ = "1.3.4.6"
__description__ = "A Python wrapper for the aminoapps.com API"

print("Join the pymino discord server: https://discord.gg/3HRdkVNets.")

if not TYPE_CHECKING:
    import requests
    import colorama

    try:
        latest_version = requests.get("https://pypi.org/pypi/pymino/json").json()[
            "info"
        ]["version"]
    except Exception as e:
        print(f"Failed to check the latest version: {e}")
    else:
        if __version__ != latest_version:
            print(
                f"{colorama.Fore.RED}WARNING:{colorama.Style.RESET_ALL} "
                f"You are using an outdated version of pymino ({__version__}). "
                f"The latest version is {latest_version}."
            )
        del latest_version

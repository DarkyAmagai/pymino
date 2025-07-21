from typing import TYPE_CHECKING

from pymino.bot import Bot
from pymino.client import Client

__title__ = "pymino"
__author__ = "cynical"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Cynical"
__version__ = "1.3.4.9"
__description__ = "A Python wrapper for the aminoapps.com API"

__all__ = ("Bot", "Client")

print("Join the pymino Discord server: https://discord.gg/3HRdkVNets")

if not TYPE_CHECKING:
    import requests
    import colorama

    colorama.init(autoreset=True)

    get_latest_version = lambda: (
        requests.get("https://pypi.org/pypi/pymino/json", timeout=5)
        if requests.get("https://pypi.org/pypi/pymino/json", timeout=5).ok
        else None
    )

    compare_versions = lambda current, latest: current != latest

    response = get_latest_version()
    latest = response.json().get("info", {}).get("version") if response else None

    if latest:
        if compare_versions(__version__, latest):
            print("{}WARNING:{} You are using pymino version {} but the latest is {}. Run 'pip install --upgrade pymino'.".format(
                colorama.Fore.YELLOW, colorama.Style.RESET_ALL, __version__, latest
            ))
        else:
            print("{}pymino is up to date (version {}).{}".format(
                colorama.Fore.GREEN, __version__, colorama.Style.RESET_ALL
            ))
    else:
        print("Could not fetch version info from PyPI.")
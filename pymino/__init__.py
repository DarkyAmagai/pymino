__title__ = 'pymino'
__author__ = 'cynical'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Cynical'
__version__ = '0.5.0'
__description__ = 'A Python wrapper for the aminoapps.com API'

from .bot import Bot

print("Join the pymino discord server: https://discord.gg/gwGjWwsEVA")

from requests import get
latestVersion = get("https://pypi.org/pypi/pymino/json").json()["info"]["version"]

if __version__ != latestVersion:
    print(f"WARNING: You are using an outdated version of pymino. The latest version is {latestVersion}.")

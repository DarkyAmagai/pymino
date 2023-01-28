############################################################################################################
#                
#                      Helper Functions                                                     #
from sys import platform
from os import system, environ
from contextlib import suppress
from re import search

def check_debugger() -> bool:
    with suppress(Exception):
        return any([search("vsc", environ.get("TERM_PROGRAM")), search("pycharm", environ.get("TERM_PROGRAM"))])

def orjson_exists() -> bool:
    if platform != "win32": return False

    try:
        from orjson import dumps
        return True
    except ImportError:
        system("pip install orjson")
        system("cls") if platform == "win32" else system("clear")
        return True

############################################################################################################

############################################################################################################
#                                     Helper Functions                                                     #
from os import environ
from contextlib import suppress
from re import search

def check_debugger() -> bool:
    with suppress(Exception):
        return any([search("vsc", environ.get("TERM_PROGRAM")), search("pycharm", environ.get("TERM_PROGRAM"))])

############################################################################################################

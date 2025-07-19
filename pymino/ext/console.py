import os
import textwrap
import time
from typing import Literal

import colorama

from pymino.ext import entities, utilities
from pymino import bot

__all__ = ("Console",)


class Console:
    """
    The Console class is responsible for the overall operation of the terminal application.

    :param bot: An instance of the bot which will interact with the Amino API.
    :type bot: Bot
    """

    def __init__(self, bot: "bot.Bot") -> None:
        self.bot = bot
        self.indent_size = self.fetch_indent_size()
        self.menu = utilities.Menu(self)
        self.community_console = utilities.CommunityConsole(self)
        self.profile_console = utilities.ProfileConsole(self)
        self.chat_console = utilities.ChatConsole(self)

    def fetch_indent_size(self) -> Literal[0, 20]:
        """
        Checks if the application is running on an Android device or a REPL environment and sets the appropriate
        indentation size.
        """
        return 0 if entities.is_android() or entities.is_repl() else 20

    def print(self, text: str = "") -> None:
        """
        Prints a string with a specified indentation.

        :param text: The string to be printed.
        :type text: str
        :param amount: The number of spaces to indent.
        :type amount: int
        """
        print(textwrap.indent(text, ' ' * self.indent_size))

    def error_print(self, text: str = "") -> None:
        """
        Prints a string with a specified indentation and a red color.

        :param text: The string to be printed.
        :type text: str
        """
        print(colorama.Fore.RED + textwrap.indent(text, ' ' * self.indent_size) + colorama.Style.RESET_ALL)

    def on_error(self, error: str) -> None:
        """
        Displays an error message to the user and prompts them to press enter to return to the main menu.
        """
        self.error_print(error)
        input(f"{' ' * self.indent_size}Press enter to return to the main menu.")

    def sleep(self, seconds: float) -> None:
        """
        Sleeps for a specified number of seconds.

        :param seconds: The number of seconds to sleep.
        :type seconds: int
        """
        time.sleep(seconds)

    def clear(self) -> None:
        """
        Clears the console screen irrespective of the platform (Windows/Linux).
        """
        os.system("cls || clear")

    def input(self, text: str) -> str:
        """
        Accepts user input prefixed with a fixed number of spaces for consistent look and feel.

        :param text: The prompt to be displayed to the user.
        :type text: str
        :return: User input as a string.
        """
        return input(" " * self.indent_size + text)

    def fetch_menu(self) -> None:
        """
        Displays the main menu of the application to the user and processes their input.
        """
        while True:
            self.menu.display()

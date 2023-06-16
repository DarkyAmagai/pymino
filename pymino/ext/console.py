import textwrap

from os import system
from time import sleep
from .utilities.menu import Menu
from .entities.handlers import is_android, is_repl
from .utilities.community_console import CommunityConsole
from .utilities.profile_console import ProfileConsole
from .utilities.chat_console import ChatConsole
from colorama import Fore, Style

class Console:
    def __init__(self, bot):
        """
        The Console class is responsible for the overall operation of the terminal application.

        :param bot: An instance of the bot which will interact with the Amino API.
        :type bot: Bot
        """
        self.bot = bot
        self.indent_size = self.fetch_indent_size()
        self.menu = Menu(self)
        self.community_console = CommunityConsole(self)
        self.profile_console = ProfileConsole(self)
        self.chat_console = ChatConsole(self)

    
    def fetch_indent_size(self):
        """
        Checks if the application is running on an Android device or a REPL environment and sets the appropriate
        indentation size.
        """
        return 0 if is_android() or is_repl() else 20

    def print(self, text=""):
        """
        Prints a string with a specified indentation.

        :param text: The string to be printed.
        :type text: str
        :param amount: The number of spaces to indent.
        :type amount: int
        """
        print(textwrap.indent(text, ' ' * self.indent_size))

    def error_print(self, text=""):
        """
        Prints a string with a specified indentation and a red color.

        :param text: The string to be printed.
        :type text: str
        """
        print(Fore.RED + textwrap.indent(text, ' ' * self.indent_size) + Style.RESET_ALL)

    def on_error(self, error):
        """
        Displays an error message to the user and prompts them to press enter to return to the main menu.
        """
        self.error_print(error)
        input(f"{' ' * self.indent_size}Press enter to return to the main menu.")
        self.fetch_menu()

    def sleep(self, seconds):
        """
        Sleeps for a specified number of seconds.

        :param seconds: The number of seconds to sleep.
        :type seconds: int
        """
        sleep(seconds)

    def clear(self):
        """
        Clears the console screen irrespective of the platform (Windows/Linux).
        """
        clear_command = "cls || clear"
        system(clear_command)

    def input(self, text):
        """
        Accepts user input prefixed with a fixed number of spaces for consistent look and feel.

        :param text: The prompt to be displayed to the user.
        :type text: str
        :return: User input as a string.
        """
        return input(" " * self.indent_size + text)

    def fetch_menu(self):
        """
        Displays the main menu of the application to the user and processes their input.
        """
        self.menu.display()

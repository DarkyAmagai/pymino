import colorama

from pymino.ext import console

__all__ = ("Menu",)

MENU_LOGO = """
██████╗ ██╗   ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ 
██╔══██╗╚██╗ ██╔╝████╗ ████║██║████╗  ██║██╔═══██╗
██████╔╝ ╚████╔╝ ██╔████╔██║██║██╔██╗ ██║██║   ██║
██╔═══╝   ╚██╔╝  ██║╚██╔╝██║██║██║╚██╗██║██║   ██║
██║        ██║   ██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝
╚═╝        ╚═╝   ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
"""


class Menu:
    def __init__(self, console: console.Console) -> None:
        self.console = console
        self.menu_logo = colorama.Fore.MAGENTA + MENU_LOGO + colorama.Style.RESET_ALL
        self.author = (
            colorama.Fore.LIGHTYELLOW_EX + "CONSOLE v0.1                    by @forevercynical" + colorama.Style.RESET_ALL)
        self.menu_logo += self.author

    def display(self) -> None:
        """Displays the main menu options to the user and processes their input."""
        self.console.clear()
        self.console.print(self.menu_logo)
        self.console.print(self.welcome_screen())
        self.console.print("""
    1. Select Community
    2. Edit Profile
    3. Join Public Chat
    4. My Chats
    """)
        choice = self.console.input(">>> ")
        print()
        menu = {
            "1": self.console.community_console.select_community,
            "2": self.console.profile_console.edit_profile,
            "3": self.console.chat_console.join_public_chat,
            "4": self.console.chat_console.my_chats
        }
        if choice in menu:
            self.console.clear()
            try:
                menu[choice]()
            except Exception as exc:
                self.console.on_error(repr(exc))
        else:
            self.console.print("Invalid option. Please try again.")

    def welcome_screen(self) -> str:
        """Returns a string containing the welcome message for the user.

        :return: A string containing the welcome message for the user.
        :rtype: str
        """
        profile = self.console.bot.profile
        userId = profile.userId
        aminoId = profile.aminoId
        username = profile.nickname
        selected_community = self.console.bot.community_id

        return f"""
    Welcome, {username}({aminoId})!
    User ID: {userId}
    Selected Community: {selected_community}
    """

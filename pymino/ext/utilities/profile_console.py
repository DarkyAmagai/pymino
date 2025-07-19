import contextlib
from typing import Any

from pymino.ext import console

__all__ = ("ProfileConsole",)


class ProfileConsole:
    """
    The ProfileConsole class handles user profile related operations in the application.

    :param console: An instance of the Console class for inter-component communication.
    :type console: Console
    """

    def __init__(self, console: console.Console) -> None:
        self.console = console

    def edit_profile(self) -> None:
        """
        Handles editing of user profile.
        """
        if not self.console.bot.community_id:
            self.console.on_error("You must select a community first.")
            return
        self.console.print("Edit Profile")
        self.console.print("""
    1. Change Username
    2. Change Bio
    3. Change Profile Picture
    4. Change Background Picture
    5. Back
    """)
        back_option, choice = 5, 0
        while choice not in range(1, back_option+1):
            with contextlib.suppress(ValueError):
                choice = int(self.console.input(">>> "))
        if choice == back_option:
            return
        field_name = None
        new_value = None
        while not (field_name and new_value is not None):
            if choice == 1:
                field_name = "nickname"
                new_value = self.console.input("Enter new username: ")
            elif choice == 2:
                field_name = "content"
                new_value = self.console.input("Enter new bio: ")
            elif choice == 3:
                field_name = "icon"
                new_value = self.console.input("Enter new profile picture URL: ")
            else:
                field_name = "backgroundImage"
                new_value = self.console.input("Enter new background picture URL: ")
            if not new_value:
                self.console.print("Invalid value. Please try again.")
        if not new_value:
            self.edit_profile()
            return
        try:
            kwargs: dict[str, Any] = {field_name: new_value}
            self.console.bot.community.edit_profile(**kwargs)
            self.console.print(f"{field_name.capitalize()} changed successfully to {new_value}.")
        except Exception as e:
            self.console.print(f"Error: {e}")
        self.console.sleep(2)

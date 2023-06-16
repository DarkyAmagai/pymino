class ProfileConsole:
    def __init__(self, console):
        """
        The ProfileConsole class handles user profile related operations in the application.

        :param console: An instance of the Console class for inter-component communication.
        :type console: Console
        """
        self.console = console

    def edit_profile(self):
        """
        Handles editing of user profile.
        """
        if not self.console.bot.community_id:
            return self.console.on_error("You must select a community first.")
        
        self.console.print("Edit Profile")
        self.console.print("""
    1. Change Username
    2. Change Bio
    3. Change Profile Picture
    4. Change Background Picture
    5. Back
    """)
        choice = self.console.input(">>> ")

        try:
            if choice == "5":
                return self.console.menu.display()

            field_name = None
            new_value = None

            if choice == "1":
                field_name = "nickname"
                new_value = self.console.input("Enter new username: ")
            elif choice == "2":
                field_name = "content"
                new_value = self.console.input("Enter new bio: ")
            elif choice == "3":
                field_name = "icon"
                new_value = self.console.input("Enter new profile picture URL: ")
            elif choice == "4":
                field_name = "backgroundImage"
                new_value = self.console.input("Enter new background picture URL: ")
            else:
                self.console.print("Invalid option. Please try again.")
                return self.edit_profile()

            self.console.bot.community.edit_profile(**{field_name: new_value})
            self.console.print(f"{field_name.capitalize()} changed successfully to {new_value}.")
            self.console.sleep(2)

        except Exception as e:
            self.console.print(f"Error: {e}")
            self.console.sleep(2)

        return self.console.menu.display()

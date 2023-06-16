from time import sleep

class CommunityConsole:
    def __init__(self, console):
        """
        CommunityConsole handles interactions related to communities.

        :param console: An instance of the Console class for inter-component communication.
        :type console: Console
        """
        self.console = console

    def print_communities(self, communities):
        """
        Prints a list of communities the user has joined.

        :param communities: A list of communities.
        :type communities: list of Community objects
        """
        if not communities.comId:
            self.console.print("You are not in any communities.")
            sleep(2)
            return self.console.menu.display()

        for index, (community_id, community_name) in enumerate(zip(communities.comId, communities.name), start=1):
            try:
                self.console.print(f"{index}. {community_name}({community_id})")
            except Exception:
                self.console.print("Error occurred while fetching communities.")
                sleep(2)

    def select_community(self):
        """
        Prompts the user to select a community and sets the bot's community accordingly.
        """
        communities = self.console.bot.community.joined_communities()
        self.console.print("\nSelect a community:\n")
        self.print_communities(communities)
        self.console.print(f"{len(communities.comId)+1}. Back\n")
        choice = self.console.input(">>> ")
        print()

        if choice == str(len(communities.comId)+1):
            return self.console.menu.display()
        
        try:
            choice = int(choice)
            if not (1 <= choice <= len(communities.comId)):
                raise ValueError
        except ValueError:
            self.console.print("Invalid option. Please try again.")
            return self.select_community()

        self.console.bot.set_community_id(communities.comId[choice-1])
        return self.console.menu.display()

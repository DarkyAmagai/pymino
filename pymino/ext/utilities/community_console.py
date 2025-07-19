import contextlib
import time

from pymino.ext import console

__all__ = ("CommunityConsole",)


class CommunityConsole:
    """
    CommunityConsole handles interactions related to communities.

    :param console: An instance of the Console class for inter-component communication.
    :type console: Console
    """

    def __init__(self, console: console.Console) -> None:
        self.console = console

    def select_community(self) -> None:
        """
        Prompts the user to select a community and sets the bot's community accordingly.
        """
        communities = self.console.bot.community.joined_communities()
        if not communities.comId:
            self.console.print("You are not in any communities.")
            time.sleep(2)
            return
        back_option = len(communities.comId) + 1
        self.console.print("\nSelect a community:\n")
        for index, (community_id, community_name) in enumerate(zip(communities.comId, communities.name), start=1):
            self.console.print(f"{index}. {community_name}({community_id})")
        self.console.print(f"{back_option}. Back\n")
        choice = 0
        while choice not in range(1, back_option+1):
            with contextlib.suppress(ValueError):
                choice = int(self.console.input(">>> "))
        if choice == back_option:
            return
        self.console.bot.set_community_id(communities.comId[choice-1])

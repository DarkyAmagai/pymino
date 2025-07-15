import time
from collections.abc import Sequence
from typing import Any, Callable, Dict, List, Optional

__all__ = ("CommandCallback", "Command", "Commands")


CommandCallback = Callable[..., Any]


class Command:
    """
    `Command` - The main command class.

    `**Parameters**`
    - `func` - The function to run when the command is called.
    - `name` - The name of the command.
    - `description` - The description of the command. `Defaults` to `None`.
    - `usage` - The usage of the command. `Defaults` to `None`.
    - `aliases` - The aliases of the command. `Defaults` to `None`.
    - `cooldown` - The cooldown of the command. `Defaults` to `0`.

    """

    def __init__(
        self,
        func: CommandCallback,
        name: str,
        description: Optional[str] = None,
        usage: Optional[str] = None,
        aliases: Optional["Sequence[str]"] = None,
        cooldown: float = 0.0,
    ) -> None:
        self.func = func
        self.name = name
        self.description = description
        self.usage = usage
        self.aliases = list(aliases or [])
        self.cooldown = cooldown


class Commands:
    def __init__(self) -> None:
        self.commands: Dict[str, Command] = {}
        self.cooldowns: Dict[str, Dict[str, float]] = {}

    def add_command(self, command: Command) -> Command:
        """
        Adds a command to the command list.

        `**Parameters**`
        - `command` - The command to add.

        `**Returns**`
        - `Command` - The command that was added.

        """
        self.commands[command.name] = command
        return command

    def fetch_command(self, command_name: str) -> Optional[Command]:
        """
        Fetches a command from the command list.

        `**Parameters**`
        - `command_name` - The name of the command to fetch.

        `**Returns**`
        - `Command` - The command that was fetched.

        """
        if command_name in self.commands:
            return self.commands[command_name]
        for command in self.commands.values():
            if command_name in command.aliases:
                return command
        return None

    def fetch_commands(self) -> List[Command]:
        """
        Fetches all commands from the command list.

        `**Returns**`
        - `list[Command]` - The commands that were fetched.

        """
        return list(self.commands.values())

    def __command_functions__(self) -> Dict[str, CommandCallback]:
        """
        Fetches all command functions from the command list.

        `**Returns**`
        - `dict[str, Callable]` - The command functions that were fetched.

        """
        return {command.name: command.func for command in self.commands.values()}

    def __command_names__(self) -> List[str]:
        """
        Fetches all command names from the command list.

        `**Returns**`
        - `list[str]` - The command names that were fetched.

        """
        return [command.name for command in self.commands.values()]

    def __command_aliases__(self) -> Dict[str, str]:
        """
        Fetches all command aliases from the command list.

        `**Returns**`
        - `dict[str, str]` - The command aliases that were fetched.

        """
        aliases: Dict[str, str] = {}
        for command in self.commands.values():
            for alias in command.aliases:
                aliases[alias] = command.name
        return aliases

    def __command_descriptions__(self) -> Dict[str, Optional[str]]:
        """
        Fetches all command descriptions from the command list.

        `**Returns**`
        - `dict[str, str | None]` - The command descriptions that were fetched.

        """
        return {command.name: command.description for command in self.commands.values()}

    def __command_usages__(self) -> Dict[str, Optional[str]]:
        """
        Fetches all command usages from the command list.

        `**Returns**`
        - `dict[str, str | None]` - The command usages that were fetched.

        """
        return {command.name: command.usage for command in self.commands.values()}

    def __command_cooldowns__(self) -> Dict[str, float]:
        """
        Fetches all command cooldowns from the command list.

        `**Returns**`
        - `dict[str, float]` - The command cooldowns that were fetched.

        """
        return {command.name: command.cooldown for command in self.commands.values()}

    def set_cooldown(self, command_name: str, cooldown: float, userId: str) -> None:
        """
        Sets the cooldown of a command for a user.

        `**Parameters**`
        - `command_name` - The name of the command to set the cooldown for.
        - `cooldown` - The cooldown to set.
        - `userId` - The user to set the cooldown for.

        """
        self.cooldowns[command_name][userId] = time.time() + cooldown

    def fetch_cooldown(self, command_name: str, userId: str) -> float:
        """
        Fetches the cooldown of a command for a user.

        `**Parameters**`
        - `command_name` - The name of the command to fetch the cooldown for.
        - `userId` - The user to fetch the cooldown for.

        `**Returns**`
        - `float` - The cooldown that was fetched.

        """
        self.cooldowns[command_name].setdefault(userId, 0.0)
        return self.cooldowns[command_name][userId]

    def __help__(self) -> str:
        """
        Generates a help message for the bot.

        `**Returns**`
        - `str` - The help message that was generated.

        """
        help_message = "[bcu]Commands\n\n[ic]This is a list of all the commands available on this bot.\n"

        for command in self.commands.values():
            help_message += f"\n[uc]{command.name}\n[ic]{command.description}\n[uc]Usage: {command.usage}\n"
        help_message += "\n\n[ic]This message was generated automatically. If you have any questions, please contact the bot owner."
        return help_message

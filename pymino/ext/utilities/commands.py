from time import time
from typing import Callable
from collections import defaultdict


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
    def __init__(self, func: Callable, name: str, description: str=None, usage: str=None, aliases: list=None, cooldown: int=0):
        self.func:           Callable = func
        self.name:           str = name
        self.description:    str = description
        self.usage:          str = usage
        self.aliases:        list = [] if aliases is None else aliases
        self.cooldown:       int = cooldown


class Commands:
    def __init__(self):
        self.commands: dict[str, Command] = {}
        self.cooldowns: defaultdict[dict] = defaultdict(dict)


    def add_command(self, command: Command) -> Command:
        """
        `add_command` - Adds a command to the command list.
        
        `**Parameters**`
        - `command` - The command to add.
        
        `**Returns**`
        - `Command` - The command that was added.
        
        """
        self.commands[command.name] = command
        return command


    def fetch_command(self, command_name: str) -> Command:
        """
        `fetch_command` - Fetches a command from the command list.
        
        `**Parameters**`
        - `command_name` - The name of the command to fetch.
        
        `**Returns**`
        - `Command` - The command that was fetched.
        
        """
        return self.commands.get(command_name) or next(
            (command for command in self.commands.values() if command_name in command.aliases), None
        )


    def fetch_commands(self) -> Command:
        """
        `fetch_commands` - Fetches all commands from the command list.
        
        `**Returns**`
        - `list[Command]` - The commands that were fetched.
        
        """
        return list(self.commands.values())


    def __command_functions__(self) -> list:
        """
        `__command_functions__` - Fetches all command functions from the command list.
        
        `**Returns**`
        - `list[Callable]` - The command functions that were fetched.
        
        """
        return {command.name: command.func for command in self.commands}


    def __command_names__(self) -> list:
        """
        `__command_names__` - Fetches all command names from the command list.
        
        `**Returns**`
        - `list[str]` - The command names that were fetched.
        
        """
        return [command.name for command in self.commands.values()]


    def __command_aliases__(self) -> list:
        """
        `__command_aliases__` - Fetches all command aliases from the command list.
        
        `**Returns**`
        - `list[str]` - The command aliases that were fetched.
        
        """
        aliases = {}
        for command in self.commands.values():
            for alias in command.aliases:
                aliases[alias] = command.name
        return aliases


    def __command_descriptions__(self) -> list:
        """
        `__command_descriptions__` - Fetches all command descriptions from the command list.
        
        `**Returns**`
        - `list[str]` - The command descriptions that were fetched.
        
        """
        return {command.name: command.description for command in self.commands}


    def __command_usages__(self) -> list:
        """
        `__command_usages__` - Fetches all command usages from the command list.
        
        `**Returns**`
        - `list[str]` - The command usages that were fetched.
        
        """
        return {command.name: command.usage for command in self.commands}


    def __command_cooldowns__(self) -> list:
        """
        `__command_cooldowns__` - Fetches all command cooldowns from the command list.
        
        `**Returns**`
        - `list[int]` - The command cooldowns that were fetched.
        
        """
        return {command.name: command.cooldown for command in self.commands}


    def set_cooldown(self, command_name: str, cooldown: int, userId: str) -> None:
        """
        `set_cooldown` - Sets the cooldown of a command for a user.
        
        `**Parameters**`
        - `command_name` - The name of the command to set the cooldown for.
        - `cooldown` - The cooldown to set.
        - `userId` - The user to set the cooldown for.
        
        `**Returns**`
        - `None` - Nothing.

        """
        self.cooldowns[command_name][userId] = time() + cooldown


    def fetch_cooldown(self, command_name: str, userId: str) -> int:
        """
        `fetch_cooldown` - Fetches the cooldown of a command for a user.
        
        `**Parameters**`
        - `command_name` - The name of the command to fetch the cooldown for.
        - `userId` - The user to fetch the cooldown for.
        
        `**Returns**`
        - `int` - The cooldown that was fetched.
        
        """
        self.cooldowns[command_name].setdefault(userId, 0)
        return self.cooldowns[command_name][userId]


    def __help__(self):
        """
        `__help__` - Generates a help message for the bot.
        
        `**Returns**`
        - `str` - The help message that was generated.
        
        """
        help_message = "[bcu]Commands\n" + "\n[ic]This is a list of all the commands available on this bot.\n"

        for command in self.commands.values():
            help_message += f"\n[uc]{command.name}\n[ic]{command.description}\n[uc]Usage: {command.usage}\n"
        help_message += "\n\n[ic]This message was generated automatically. If you have any questions, please contact the bot owner."
        return help_message
from time import time
from typing import Callable

class Command:
    """
    `Command` - The main command class.
    
    `**Parameters**`
    - `func` - The function to run when the command is called.
    - `command_name` - The name of the command.
    - `command_description` - The description of the command. `Defaults` to `None`.
    - `aliases` - The aliases of the command. `Defaults` to `None`.
    - `cooldown` - The cooldown of the command. `Defaults` to `0`.
    
    """
    def __init__(self, func: Callable, command_name: str, command_description: str=None, aliases: list = None, cooldown: int=0):
        if aliases is None:
            aliases = []
        self.func:           Callable = func
        self.name:           str = command_name
        self.description:    str = command_description
        self.aliases:        list = aliases
        self.cooldown:       int = cooldown

class Commands:
    def __init__(self):
        self.commands: list[Command] = []
        self.cooldowns: dict = {}

    def add_command(self, command: Command) -> Command:
        """
        `add_command` - Adds a command to the command list.
        
        `**Parameters**`
        - `command` - The command to add.
        
        `**Returns**`
        - `Command` - The command that was added.
        
        """
        self.commands.append(command)
        return command

    def fetch_command(self, command_name: str) -> Command:
        """
        `fetch_command` - Fetches a command from the command list.
        
        `**Parameters**`
        - `command_name` - The name of the command to fetch.
        
        `**Returns**`
        - `Command` - The command that was fetched.
        
        """
        return next((command for command in self.commands if command.name == command_name or command_name in command.aliases), None)

    def fetch_commands(self) -> Command:
        """
        `fetch_commands` - Fetches all commands from the command list.
        
        `**Returns**`
        - `list[Command]` - The commands that were fetched.
        
        """
        return self.commands

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
        return [command.name for command in self.commands]

    def __command_aliases__(self) -> list:
        """
        `__command_aliases__` - Fetches all command aliases from the command list.
        
        `**Returns**`
        - `list[str]` - The command aliases that were fetched.
        
        """
        aliases = {}
        for command in self.commands:
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
        if command_name not in self.cooldowns:
            self.cooldowns[command_name] = {}
        if userId not in self.cooldowns[command_name]:
            self.cooldowns[command_name][userId] = 0
        return self.cooldowns[command_name][userId]

    def __help__(self):
        """
        `__help__` - Generates a help message for the bot.
        
        `**Returns**`
        - `str` - The help message that was generated.
        
        """
        help_message = "[bcu]Commands\n" + "\n[ic]This is a list of all the commands available on this bot.\n"

        for command in self.commands:
            help_message += f"\n[uc]{command.name}\n[ic]{command.description}"
        help_message += "\n\n[ic]This message was generated automatically. If you have any questions, please contact the bot owner."
        return help_message

    def __repr__(self):
        """`__repr__` - Generates a string representation of the commands."""
        return f"Commands({self.commands})"
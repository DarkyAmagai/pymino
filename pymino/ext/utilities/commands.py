from .generate import *

class Command:
    def __init__(self, func: Callable, command_name: str, command_description: str=None, aliases: list=[], cooldown: int=0):
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
        self.commands.append(command)
        return command

    def fetch_command(self, command_name: str) -> Command:
        for command in self.commands:
            if command.name == command_name or command_name in command.aliases:
                return command
        return None

    def fetch_commands(self) -> Command:
        return self.commands

    def __command_functions__(self) -> list:
        functions = {}
        for command in self.commands:
            functions[command.name] = command.func
        return functions

    def __command_names__(self) -> list:
        return [command.name for command in self.commands]

    def __command_aliases__(self) -> list:
        aliases = {}
        for command in self.commands:
            for alias in command.aliases:
                aliases[alias] = command.name
        return aliases

    def __command_descriptions__(self) -> list:
        descriptions = {}
        for command in self.commands:
            descriptions[command.name] = command.description
        return descriptions

    def __command_cooldowns__(self) -> list:
        cooldowns = {}
        for command in self.commands:
            cooldowns[command.name] = command.cooldown
        return cooldowns

    def set_cooldown(self, command_name: str, cooldown: int, userId: str):
        self.cooldowns[command_name][userId] = time() + cooldown

    def fetch_cooldown(self, command_name: str, userId: str) -> int:
        if command_name not in self.cooldowns:
            self.cooldowns[command_name] = {}
        if userId not in self.cooldowns[command_name]:
            self.cooldowns[command_name][userId] = 0
        return self.cooldowns[command_name][userId]

    def __help__(self):
        help_message = "[bcu]Commands\n"
        help_message += "\n[ic]This is a list of all the commands available on this bot.\n"
        for command in self.commands:
            help_message += f"\n[uc]{command.name}\n[ic]{command.description}"
        help_message += "\n\n[ic]This message was generated automatically. If you have any questions, please contact the bot owner."
        return help_message

    def __repr__(self):
        return f"Commands({self.commands})"
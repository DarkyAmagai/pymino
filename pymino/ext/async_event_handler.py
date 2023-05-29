import asyncio
from requests import get
from diskcache import Cache
from threading import Thread
from base64 import b64encode
from contextlib import suppress
from colorama import Fore, Style
from time import sleep as delay, time
from inspect import signature as inspect_signature
from typing import BinaryIO, Callable, List, Union
from asyncio import AbstractEventLoop

from .entities.general import ApiResponse
from .entities.userprofile import OnlineMembers
from .utilities.commands import Command, Commands
from .entities.exceptions import InvalidImage, MustRunInContext
from .entities.messages import (
    CMessage, Message, MessageAuthor, PrepareMessage, NNotification
    )

from .async_context import AsyncContext

class AsyncEventHandler:
    """
    `EventHandler` - AKA where all the events are handled.

    `**Parameters**``
    - `session` - The session we are using.

    """
    def __init__(self):
        self.command_prefix:    str = self.command_prefix
        self._events:           dict = {}
        self._wait_for:         Cache = Cache("cache")
        self._commands:         Commands = Commands()
        self.context:           AsyncContext = AsyncContext


    async def _handle_task(self, func: Callable, interval: int):
        """
        `_handle_task` - This handles the task.
        
        `**Parameters**``
        - `func` - The function.
        - `interval` - The interval in seconds.
        
        `**Returns**`` - None
        """
        while True:
            if len(inspect_signature(func).parameters) == 0:
                await func()
            else:
                await func(self.community)

            await asyncio.sleep(interval)


    def task(self, interval: int = 10):
        async def decorator(func: Callable) -> Callable:
            async def wrapper(interval: int):
                await self._handle_task(func, interval)
            self.loop.create_task(wrapper(interval=interval))
        return decorator


    async def _set_parameters(self, context: AsyncContext, func: Callable, message: str = None) -> list:
        try:
            message = message if isinstance(message, str) else context.message.content
        except AttributeError:
            message = None

        try:
            username = context.author.username
        except AttributeError:
            username = None

        try:
            userId = context.author.userId
        except AttributeError:
            userId = None

        potential_parameters = {
            "ctx": context,
            "message": message,
            "username": username,
            "userId": userId
        }

        return [
            potential_parameters.get(parameter)
            for parameter in inspect_signature(func).parameters
        ]


    async def emit(self, name: str, *args) -> None:
        """`emit` is a function that emits an event."""
        await self._events[name](*args) if name in self._events else None


    def command(
        self,
        name: str=None,
        description: str=None,
        usage: str=None,
        aliases: list=[],
        cooldown: int=0,
        **kwargs
    ) -> Callable:
        """
        `command` - This creates a command.
        
        `**Command Parameters**``
        - `command_name` - The name of the command.
        - `command_description` - The description of the command.
        - `aliases` - The other names the command can be called by.
        - `cooldown` - The cooldown of the command in seconds.

        `**Function Parameters**``
        - `ctx` - The context of the command.
        - `message` - The message that called the command.
        - `username` - The username of the person who called the command.
        - `userId` - The userId of the person who called the command.

        Do I need a `command_description`?
            - No, you don't need a command description however it is recommended.
            - If you don't supply a command description the command will not show up in the help command.

        What are `aliases`?
            - The command can be called by the command name, aliases, or both.

        Is `cooldown` required?
            - No, you don't need a cooldown however it is recommended to avoid spam.

        What is the difference between `message` and `ctx.message.content`?
            - `ctx.message.content` contains the entire message.        
            - `message` contains the message without the command prefix.

        Do I need to supply all the parameters?
            - No, you only need to supply the parameters you want to use however `ctx` is required.
        
        `**Example**``
        ```py
        @bot.command(command_name="ping") # Command parameters.
        def ping(ctx: AsyncContext, message: str, username: str, userId: str): # Function parameters.
            print(f"{username}({userId}): {message}") # OUTPUT: "JohnDoe(0000-0000-0000-0000): !ping"
            return ctx.send(content="Pong!")

        @bot.command(command_name="ping", aliases=["alive", "test"]) # Command parameters.
        def ping(ctx: AsyncContext): # Function parameters.
            # This command can be called by "ping", "alive", and "test".
            return ctx.send(content="Pong!")

        @bot.command(command_name="ping", cooldown=5) # Command parameters.
        def ping(ctx: AsyncContext): # Function parameters.
            # This command can only be called every 5 seconds.
            return ctx.send(content="Pong!")

        @bot.command(command_name="say", command_description="This is a command that says something.") # Command parameters.
        def say(ctx: AsyncContext, message: str, username: str, userId: str): # Function parameters.
            bot.community.delete_message(chatId=ctx.chatId, messageId=ctx.message.chatId, comId=ctx.comId)
            return ctx.send(content=message)
        ```
        """
        
        if "command_name" in kwargs:
            self._is_deprecated("command_name", "name")
            name = kwargs["command_name"]

        elif name is None:
            raise ValueError("Please supply a name for the command. Example: @bot.command(name='ping')")

        if "command_description" in kwargs:
            self._is_deprecated("command_description", "description")
            description = kwargs["command_description"]

        async def decorator(func: Callable) -> Callable:
            self._commands.add_command(
                Command(
                    func=func,
                    name=name,
                    description=description,
                    usage=usage,
                    aliases=aliases,
                    cooldown=cooldown
                ))
            return await func
        return decorator


    def _is_deprecated(self, parameter: str, new_parameter: str):
        print(f"{Style.BRIGHT}{Fore.RED}WARNING:{Style.RESET_ALL} '{parameter}' is deprecated. Please use '{new_parameter}' instead.")


    def command_exists(self, command_name: str) -> bool:
        return any([
            command_name in self._commands.__command_names__(),
            command_name in self._commands.__command_aliases__()
            ])


    def fetch_command(self, command_name: str) -> Command:
        return self._commands.fetch_command(command_name)

    async def _handle_command(self, data: Message, context: AsyncContext):
        """Handles commands."""
        command_name = data.content[len(self.command_prefix):].split(" ")[0]

        if (not self.command_exists(command_name) or
                self.command_prefix != data.content[:len(self.command_prefix)]):

            if (command_name == "help" and
                    data.content == f"{self.command_prefix}help"):
                return await context.reply(self._commands.__help__())

            elif "text_message" in self._events:
                return await self._handle_all_events(event="text_message", data=data, context=context)

            else:
                return None

        if data.content[:len(self.command_prefix)] != self.command_prefix:
            return None

        message = data.content[len(self.command_prefix) + len(command_name) + 1:]
        command_name = dict(self._commands.__command_aliases__().copy()).get(command_name, command_name)
        
        await self._check_cooldown(command_name, data, context)
        func = self._commands.fetch_command(command_name).func
        return await func(*await self._set_parameters(context=context, func=func, message=message))

        
    async def _check_cooldown(self, command_name: str, data: Message, context: AsyncContext) -> None:
        """`_check_cooldown` is a function that checks if a command is on cooldown."""
        if self._commands.fetch_command(command_name).cooldown > 0:
            if self._commands.fetch_cooldown(command_name, data.author.userId) > time():

                return context.reply(
                    content=f"You are on cooldown for {int(self._commands.fetch_cooldown(command_name, data.author.userId) - time())} seconds."
                    )
            
            self._commands.set_cooldown(
                command_name=command_name,
                cooldown=self._commands.fetch_command(command_name).cooldown,
                userId=data.author.userId
                )

        return None


    def on_error(self):
        async def decorator(func: Callable) -> Callable:
            self._events["error"] = func
            return await func
        return decorator


    def on_ready(self):
        async def decorator(func: Callable) -> Callable:
            self._events["ready"] = func
            return await func
        return decorator


    def on_text_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["text_message"] = func
            return await func
        return decorator


    def _add_cache(self, chatId: str, userId: str, content: str):
        if self._wait_for.get(f"{chatId}_{userId}") is not None:
            self._wait_for.clear(f"{chatId}_{userId}")
            print("Cleared cache.")

        self._wait_for.add(
            key=f"{chatId}_{userId}",
            value=content,
            expire=90
            )
        print("Added cache.")


    def on_image_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["image_message"] = func
            return await func
        return decorator


    def on_youtube_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["youtube_message"] = func
            return await func
        return decorator


    def on_strike_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["strike_message"] = func
            return await func
        return decorator


    def on_voice_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["voice_message"] = func
            return await func
        return decorator


    def on_sticker_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["sticker_message"] = func
            return await func
        return decorator


    def on_vc_not_answered(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_not_answered"] = func
            return await func
        return decorator


    def on_vc_not_cancelled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_not_cancelled"] = func
            return await func
        return decorator


    def on_vc_not_declined(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_not_declined"] = func
            return await func
        return decorator


    def on_video_chat_not_answered(self):
        async def decorator(func: Callable) -> Callable:
            self._events["video_chat_not_answered"] = func
            return await func
        return decorator


    def on_video_chat_not_cancelled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["video_chat_not_cancelled"] = func
            return await func
        return decorator


    def on_video_chat_not_declined(self):
        async def decorator(func: Callable) -> Callable:
            self._events["video_chat_not_declined"] = func
            return await func
        return decorator


    def on_avatar_chat_not_answered(self):
        async def decorator(func: Callable) -> Callable:
            self._events["avatar_chat_not_answered"] = func
            return await func
        return decorator


    def on_avatar_chat_not_cancelled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["avatar_chat_not_cancelled"] = func
            return await func
        return decorator


    def on_avatar_chat_not_declined(self):
        async def decorator(func: Callable) -> Callable:
            self._events["avatar_chat_not_declined"] = func
            return await func
        return decorator


    def on_delete_message(self):
        async def decorator(func: Callable) -> Callable:
            def wrapper(ctx: AsyncContext):
                func(*self._set_parameters(ctx, func))
            self._events["delete_message"] = wrapper
            return await func
        return decorator


    def on_member_join(self):
        async def decorator(func: Callable) -> Callable:
            self._events["member_join"] = func
            return await func
        return decorator


    def on_member_leave(self):
        async def decorator(func: Callable) -> Callable:
            self._events["member_leave"] = func
            return await func
        return decorator


    def on_chat_invite(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_invite"] = func
            return await func
        return decorator


    def on_chat_background_changed(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_background_changed"] = func
            return await func
        return decorator


    def on_chat_title_changed(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_title_changed"] = func
            return await func
        return decorator


    def on_chat_icon_changed(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_icon_changed"] = func
            return await func
        return decorator


    def on_vc_start(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_start"] = func
            return await func
        return decorator


    def on_video_chat_start(self):
        async def decorator(func: Callable) -> Callable:
            self._events["video_chat_start"] = func
            return await func
        return decorator


    def on_avatar_chat_start(self):
        async def decorator(func: Callable) -> Callable:
            self._events["avatar_chat_start"] = func
            return await func
        return decorator


    def on_vc_end(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_end"] = func
            return await func
        return decorator


    def on_video_chat_end(self):
        async def decorator(func: Callable) -> Callable:
            self._events["video_chat_end"] = func
            return await func
        return decorator


    def on_avatar_chat_end(self):
        async def decorator(func: Callable) -> Callable:
            self._events["avatar_chat_end"] = func
            return await func
        return decorator


    def on_chat_content_changed(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_content_changed"] = func
            return await func
        return decorator


    def on_screen_room_start(self):
        async def decorator(func: Callable) -> Callable:
            self._events["screen_room_start"] = func
            return await func
        return decorator


    def on_screen_room_end(self):
        async def decorator(func: Callable) -> Callable:
            self._events["screen_room_end"] = func
            return await func
        return decorator


    def on_chat_host_transfered(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_host_transfered"] = func
            return await func
        return decorator


    def on_text_message_force_removed(self):
        async def decorator(func: Callable) -> Callable:
            self._events["text_message_force_removed"] = func
            return await func
        return decorator


    def on_chat_removed_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_removed_message"] = func
            return await func
        return decorator


    def on_mod_deleted_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["mod_deleted_message"] = func
            return await func
        return decorator


    def on_chat_tip(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_tip"] = func
            return await func
        return decorator


    def on_chat_pin_announcement(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_pin_announcement"] = func
            return await func
        return decorator


    def on_vc_permission_open_to_everyone(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_permission_open_to_everyone"] = func
            return await func
        return decorator


    def on_vc_permission_invited_and_requested(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_permission_invited_and_requested"] = func
            return await func
        return decorator


    def on_vc_permission_invite_only(self):
        async def decorator(func: Callable) -> Callable:
            self._events["vc_permission_invite_only"] = func
            return await func
        return decorator


    def on_chat_view_only_enabled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_view_only_enabled"] = func
            return await func
        return decorator


    def on_chat_view_only_disabled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_view_only_disabled"] = func
            return await func
        return decorator


    def on_chat_unpin_announcement(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_unpin_announcement"] = func
            return await func
        return decorator


    def on_chat_tipping_enabled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_tipping_enabled"] = func
            return await func
        return decorator


    def on_chat_tipping_disabled(self):
        async def decorator(func: Callable) -> Callable:
            self._events["chat_tipping_disabled"] = func
            return await func
        return decorator


    def on_timestamp_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["timestamp_message"] = func
            return await func
        return decorator


    def on_welcome_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["welcome_message"] = func
            return await func
        return decorator


    def on_share_exurl_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["share_exurl_message"] = func
            return await func
        return decorator
    

    def on_invite_message(self):
        async def decorator(func: Callable) -> Callable:
            self._events["invite_message"] = func
            return await func
        return decorator


    def on_user_online(self):
        async def decorator(func: Callable) -> Callable:
            self._events["user_online"] = func
            return await func
        return decorator


    def on_member_set_you_host(self):
        """
        `on_member_set_you_host` - This is an event that is called when you are set as host.

        `**Example**``
        ```py
        from pymino.ext import *
        chatId = "0000-0000-0000-0000"

        @bot.on_member_set_you_host()
        def member_set_you_host(notification: NNotification):
            if notification.chatId == chatId:
                print("You are now host")
                bot.community.send_message(chatId=chatId, content="I am now host", comId=notification.comId)
        ```
        """
        async def decorator(func: Callable) -> Callable:
            self._events["member_set_you_host"] = func
            return await func
        return decorator


    def on_member_set_you_cohost(self):
        """
        `on_member_set_you_cohost` - This is an event that is called when you are set as cohost.
        
        `**Example**``
        ```py
        from pymino.ext import *
        chatId = "0000-0000-0000-0000"
        
        @bot.on_member_set_you_cohost()
        def member_set_you_cohost(notification: NNotification):
            if notification.chatId == chatId:
                print("You are now cohost")
                bot.community.send_message(chatId=chatId, content="I am now cohost", comId=notification.comId)
        ```
        """
        async def decorator(func: Callable) -> Callable:
            self._events["member_set_you_cohost"] = func
            return await func
        return decorator


    def on_member_remove_your_cohost(self):
        """
        `on_member_remove_your_cohost` - This is an event that is called when you are removed as cohost.
        
        `**Example**``
        ```py
        from pymino.ext import *
        chatId = "0000-0000-0000-0000"
        
        @bot.on_member_remove_your_cohost()
        def member_remove_your_cohost(notification: NNotification):
            if notification.chatId == chatId:
                print("You are no longer cohost")
                bot.community.send_message(chatId=chatId, content="I am no longer cohost", comId=notification.comId)
        ```
        """
        async def decorator(func: Callable) -> Callable:
            self._events["member_remove_your_cohost"] = func
            return await func
        return decorator


    async def _handle_all_events(self, event: str, data: Message, context: AsyncContext) -> None:
        func = self._events[event]
        return await func(* await self._set_parameters(context, func, data))


    async def _handle_event(
        self,
        event: str,
        data: Union[Message, OnlineMembers, NNotification, AsyncContext]
        ) -> Union[AsyncContext, None]:
        """
        `_handle_event` is a function that handles events.
        """
        with suppress(KeyError):
            context = self.context(data, self.loop, self.request)

            if event == "text_message":
                if not self.command_exists(
                    command_name=data.content[len(self.command_prefix):].split(" ")[0]
                    ):
                    self._add_cache(data.chatId, data.author.userId, data.content)

                return await self._handle_command(data=data, context=context)


            if event in self._events:
                if event in {
                    "user_online",
                    "member_set_you_host",
                    "member_set_you_cohost",
                    "member_remove_your_cohost",
                }:
                    return await self._events[event](data)
                else:
                    return await self._handle_all_events(event=event, data=data, context=context)
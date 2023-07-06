import asyncio
from time import time
from diskcache import Cache
from functools import wraps
from contextlib import suppress
from colorama import Fore, Style
from typing import Callable, Union
from inspect import signature as inspect_signature


from .entities import *
from .async_context import AsyncContext
from .utilities.commands import Command, Commands


def event_handler(event_name):
    event_name = event_name.lower()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


class AsyncEventHandler:
    """
    `EventHandler` - AKA where all the events are handled.

    `**Parameters**``
    - `session` - The session we are using.

    """
    def __init__(self):
        self.command_prefix:    str = self.command_prefix
        self._events:           dict = {}
        self._commands:         Commands = Commands()
        self.context:           AsyncContext = AsyncContext


    def register_event(self, event_name: str) -> Callable:
        def decorator(event_handler: Callable) -> Callable:
            self._events[event_name] = event_handler
            return event_handler
        return decorator


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
        def decorator(func: Callable) -> Callable:
            async def wrapper():
                await self._handle_task(func, interval)
            self.loop.create_task(wrapper())
            return func
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
            "member": Member(context.author.json()),
            "message": message,
            "username": username,
            "userId": userId
        }

        return (
            potential_parameters.get(parameter)
            for parameter in inspect_signature(func).parameters
        )


    async def emit(self, name: str, *args) -> None:
        """`emit` is a function that emits an event."""
        self._events[name](*args) if name in self._events else None


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

        def decorator(func: Callable) -> Callable:
            self._commands.add_command(
                Command(
                    func=func,
                    name=name,
                    description=description,
                    usage=usage,
                    aliases=aliases,
                    cooldown=cooldown
                ))
            return func
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
        command_name = next(iter(data.content[len(self.command_prefix):].split(" ")))
        
        message = data.content[len(self.command_prefix) + len(command_name) + 1:]
        command = self._commands.fetch_command(command_name)

        if command is None:
            if command_name == "help" and data.content == f"{self.command_prefix}help":
                cooldown_message = self._cooldown_message or self._commands.__help__()
                return context.reply(content=cooldown_message)
            
            if self._events.get("text_message"):
                return await self._handle_all_events(event="text_message", data=data, context=context)

        if data.content[:len(self.command_prefix)] != self.command_prefix:
            return None

        response = await self._check_cooldown(command.name, data, context)

        if response != 403:
            func = command.func
            return await func(*await self._set_parameters(context=context, func=func, message=message))

        return None


    async def _check_cooldown(self, command_name: str, data: Message, context: AsyncContext) -> None:
        """`_check_cooldown` is a function that checks if a command is on cooldown."""
        if self._commands.fetch_command(command_name).cooldown > 0:
            if self._commands.fetch_cooldown(command_name, data.author.userId) > time():

                await context.reply(
                    content=f"You are on cooldown for {int(self._commands.fetch_cooldown(command_name, data.author.userId) - time())} seconds."
                    )
                return 403
            
            self._commands.set_cooldown(
                command_name=command_name,
                cooldown=self._commands.fetch_command(command_name).cooldown,
                userId=data.author.userId
                )

        return 200


    def _add_cache(self, chatId: str, userId: str, content: str):
        with self.cache as cache:
            if cache.get(f"{chatId}_{userId}") is not None:
                self.cache.pop(f"{chatId}_{userId}")

            cache.add(
                key=f"{chatId}_{userId}",
                value=content,
                expire=90
                )


    def on_error(self):
        """
        `on_error` - This is an event that is called when an error occurs.
        """
        return self.register_event("error")


    def on_ready(self):
        """
        `on_ready` - This is an event that is called when the bot is ready to start handling events.
        """
        return self.register_event("ready")


    def on_text_message(self):
        """
        `on_text_message` - This is an event that is called when a text message is received in the chat.
        """
        return self.register_event("text_message")


    def _console_on_text_message(self):
        """
        `_console_on_text_message` - This is an event that is called when a text message is received in the console.
        """
        return self.register_event("_console_text_message")


    def on_image_message(self):
        """
        `on_image_message` - This is an event that is called when an image message is received in the chat.
        """
        return self.register_event("image_message")
        

    def on_youtube_message(self):
        """
        `on_youtube_message` - This is an event that is called when a YouTube message is received in the chat.
        """
        return self.register_event("youtube_message")


    def on_strike_message(self):
        """
        `on_strike_message` - This is an event that is called when a strike message is received in the chat.
        """
        return self.register_event("strike_message")


    def on_voice_message(self):
        """
        `on_voice_message` - This is an event that is called when a voice message is received in the chat.
        """
        return self.register_event("voice_message")


    def on_sticker_message(self):
        """
        `on_sticker_message` - This is an event that is called when a sticker message is received in the chat.
        """
        return self.register_event("sticker_message")


    def on_vc_not_answered(self):
        """
        `on_vc_not_answered` - This is an event that is called when a voice chat request is not answered.
        """
        return self.register_event("vc_not_answered")


    def on_vc_not_cancelled(self):
        """
        `on_vc_not_cancelled` - This is an event that is called when a voice chat request is not cancelled.
        """
        return self.register_event("vc_not_cancelled")



    def on_vc_not_declined(self):
        """
        `on_vc_not_declined` - This is an event that is called when a voice chat request is not declined.
        """
        return self.register_event("vc_not_declined")


    def on_video_chat_not_answered(self):
        """
        `on_video_chat_not_answered` - This is an event that is called when a video chat request is not answered.
        """
        return self.register_event("video_chat_not_answered")


    def on_video_chat_not_cancelled(self):
        """
        `on_video_chat_not_cancelled` - This is an event that is called when a video chat request is not cancelled.
        """
        return self.register_event("video_chat_not_cancelled")


    def on_video_chat_not_declined(self):
        """
        `on_video_chat_not_declined` - This is an event that is called when a video chat request is not declined.
        """
        return self.register_event("video_chat_not_declined")


    def on_avatar_chat_not_answered(self):
        """
        `on_avatar_chat_not_answered` - This is an event that is called when an avatar chat request is not answered.
        """
        return self.register_event("avatar_chat_not_answered")


    def on_avatar_chat_not_cancelled(self):
        """
        `on_avatar_chat_not_cancelled` - This is an event that is called when an avatar chat request is not cancelled.
        """
        return self.register_event("avatar_chat_not_cancelled")


    def on_avatar_chat_not_declined(self):
        """
        `on_avatar_chat_not_declined` - This is an event that is called when an avatar chat request is not declined.
        """
        return self.register_event("avatar_chat_not_declined")


    def on_delete_message(self):
        """
        `on_delete_message` - This is an event that is called when a message is deleted in the chat.
        """
        return self.register_event("delete_message")


    def on_member_join(self):
        """
        `on_member_join` - This is an event that is called when a member joins the chat.
        """
        return self.register_event("member_join")


    def on_member_leave(self):
        """
        `on_member_leave` - This is an event that is called when a member leaves the chat.
        """
        return self.register_event("member_leave")


    def on_chat_invite(self):
        """
        `on_chat_invite` - This is an event that is called when an invite is sent to the chat.
        """
        return self.register_event("chat_invite")


    def on_chat_background_changed(self):
        """
        `on_chat_background_changed` - This is an event that is called when the chat background is changed.
        """
        return self.register_event("chat_background_changed")


    def on_chat_title_changed(self):
        """
        `on_chat_title_changed` - This is an event that is called when the chat title is changed.
        """
        return self.register_event("chat_title_changed")


    def on_chat_icon_changed(self):
        """
        `on_chat_icon_changed` - This is an event that is called when the chat icon is changed.
        """
        return self.register_event("chat_icon_changed")


    def on_vc_start(self):
        """
        `on_vc_start` - This is an event that is called when a voice chat starts.
        """
        return self.register_event("vc_start")


    def on_video_chat_start(self):
        """
        `on_video_chat_start` - This is an event that is called when a video chat starts.
        """
        return self.register_event("video_chat_start")


    def on_avatar_chat_start(self):
        """
        `on_avatar_chat_start` - This is an event that is called when an avatar chat starts.
        """
        return self.register_event("avatar_chat_start")


    def on_vc_end(self):
        """
        `on_vc_end` - This is an event that is called when a voice chat ends.
        """
        return self.register_event("vc_end")


    def on_video_chat_end(self):
        """
        `on_video_chat_end` - This is an event that is called when a video chat ends.
        """
        return self.register_event("video_chat_end")


    def on_avatar_chat_end(self):
        """
        `on_avatar_chat_end` - This is an event that is called when an avatar chat ends.
        """
        return self.register_event("avatar_chat_end")


    def on_chat_content_changed(self):
        """
        `on_chat_content_changed` - This is an event that is called when the chat content is changed.
        """
        return self.register_event("chat_content_changed")


    def on_screen_room_start(self):
        """
        `on_screen_room_start` - This is an event that is called when a screen room starts.
        """
        return self.register_event("screen_room_start")


    def on_screen_room_end(self):
        """
        `on_screen_room_end` - This is an event that is called when a screen room ends.
        """
        return self.register_event("screen_room_end")


    def on_chat_host_transfered(self):
        """
        `on_chat_host_transfered` - This is an event that is called when the chat host is transferred.
        """
        return self.register_event("chat_host_transfered")


    def on_text_message_force_removed(self):
        """
        `on_text_message_force_removed` - This is an event that is called when a text message is forcefully removed.
        """
        return self.register_event("text_message_force_removed")


    def on_chat_removed_message(self):
        """
        `on_chat_removed_message` - This is an event that is called when a chat message is removed.
        """
        return self.register_event("chat_removed_message")


    def on_mod_deleted_message(self):
        """
        `on_mod_deleted_message` - This is an event that is called when a moderator deletes a message.
        """
        return self.register_event("mod_deleted_message")


    def on_chat_tip(self):
        """
        `on_chat_tip` - This is an event that is called when a tip is received in the chat.
        """
        return self.register_event("chat_tip")


    def on_chat_pin_announcement(self):
        """
        `on_chat_pin_announcement` - This is an event that is called when an announcement is pinned in the chat.
        """
        return self.register_event("chat_pin_announcement")


    def on_vc_permission_open_to_everyone(self):
        """
        `on_vc_permission_open_to_everyone` - This is an event that is called when voice chat permissions are set to open to everyone.
        """
        return self.register_event("vc_permission_open_to_everyone")


    def on_vc_permission_invited_and_requested(self):
        """
        `on_vc_permission_invited_and_requested` - This is an event that is called when voice chat permissions are set to invited and requested.
        """
        return self.register_event("vc_permission_invited_and_requested")


    def on_vc_permission_invite_only(self):
        """
        `on_vc_permission_invite_only` - This is an event that is called when voice chat permissions are set to invite only.
        """
        return self.register_event("vc_permission_invite_only")


    def on_chat_view_only_enabled(self):
        """
        `on_chat_view_only_enabled` - This is an event that is called when chat view only mode is enabled.
        """
        return self.register_event("chat_view_only_enabled")


    def on_chat_view_only_disabled(self):
        """
        `on_chat_view_only_disabled` - This is an event that is called when chat view only mode is disabled.
        """
        return self.register_event("chat_view_only_disabled")


    def on_chat_unpin_announcement(self):
        """
        `on_chat_unpin_announcement` - This is an event that is called when an announcement is unpinned in the chat.
        """
        return self.register_event("chat_unpin_announcement")


    def on_chat_tipping_enabled(self):
        """
        `on_chat_tipping_enabled` - This is an event that is called when chat tipping is enabled.
        """
        return self.register_event("chat_tipping_enabled")


    def on_chat_tipping_disabled(self):
        """
        `on_chat_tipping_disabled` - This is an event that is called when chat tipping is disabled.
        """
        return self.register_event("chat_tipping_disabled")


    def on_timestamp_message(self):
        """
        `on_timestamp_message` - This is an event that is called when a timestamp message is received in the chat.
        """
        return self.register_event("timestamp_message")


    def on_welcome_message(self):
        """
        `on_welcome_message` - This is an event that is called when a welcome message is received in the chat.
        """
        return self.register_event("welcome_message")


    def on_share_exurl_message(self):
        """
        `on_share_exurl_message` - This is an event that is called when a shared external URL message is received in the chat.
        """
        return self.register_event("share_exurl_message")


    def on_invite_message(self):
        """
        `on_invite_message` - This is an event that is called when an invite message is received in the chat.
        """
        return self.register_event("invite_message")


    def on_user_online(self):
        """
        `on_user_online` - This is an event that is called when a user comes online.
        """
        return self.register_event("user_online")


    def on_member_set_you_host(self):
        """
        `on_member_set_you_host` - This is an event that is called when you are set as the host of the chat.

        **Example:**
        ```python
        from pymino.ext import *
        chatId = "0000-0000-0000-0000"

        @bot.on_member_set_you_host()
        def member_set_you_host(notification: Notification):
            if notification.chatId == chatId:
                print("You are now the host")
                bot.community.send_message(chatId=chatId, content="I am now the host", comId=notification.comId)
        ```
        """
        return self.register_event("member_set_you_host")


    def on_member_set_you_cohost(self):
        """
        `on_member_set_you_cohost` - This is an event that is called when you are set as a cohost of the chat.
        
        **Example:**
        ```python
        from pymino.ext import *
        chatId = "0000-0000-0000-0000"
        
        @bot.on_member_set_you_cohost()
        def member_set_you_cohost(notification: Notification):
            if notification.chatId == chatId:
                print("You are now a cohost")
                bot.community.send_message(chatId=chatId, content="I am now a cohost", comId=notification.comId)
        ```
        """
        return self.register_event("member_set_you_cohost")


    def on_member_remove_your_cohost(self):
        """
        `on_member_remove_your_cohost` - This is an event that is called when you are removed as a cohost of the chat.
        
        **Example:**
        ```python
        from pymino.ext import *
        chatId = "0000-0000-0000-0000"
        
        @bot.on_member_remove_your_cohost()
        def member_remove_your_cohost(notification: Notification):
            if notification.chatId == chatId:
                print("You are no longer a cohost")
                bot.community.send_message(chatId=chatId, content="I am no longer a cohost", comId=notification.comId)
        ```
        """
        return self.register_event("member_remove_your_cohost")


    async def _handle_all_events(self, event: str, data: Message, context: AsyncContext) -> None:
        func = self._events[event]
        return await func(* await self._set_parameters(context, func, data))


    async def _handle_event(
        self,
        event: str,
        data: Union[Message, OnlineMembers, Notification, AsyncContext]
        ) -> Union[AsyncContext, None]:
        """
        `_handle_event` is a function that handles events.
        """      
        with suppress(KeyError):

            if event == "text_message":
                context = self.context(data, self)
                if all([self.intents, not self.command_exists(
                    command_name=data.content[len(self.command_prefix):].split(" ")[0]
                    )]):
                        self._add_cache(data.chatId, data.author.userId, data.content)

                return await self._handle_command(data=data, context=context)
            
            if event in self._events:
                context = self.context(data, self)

                if event in {
                    "user_online",
                    "member_set_you_host",
                    "member_set_you_cohost",
                    "member_remove_your_cohost",
                }:
                    return self._events[event](data)

                else:
                    return await self._handle_all_events(event=event, data=data, context=context)
                
            return None
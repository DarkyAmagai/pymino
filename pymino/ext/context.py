import abc
import base64
import contextlib
import functools
import inspect
import logging
import random
import threading
import time
from collections.abc import Callable, Iterator, Sequence
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import colorama
from typing_extensions import ParamSpec, Concatenate

from pymino.ext import community, entities, utilities
from pymino import bot

__all__ = (
    "Context",
    "EventHandler",
    "WaitForMessage",
)

P = ParamSpec("P")
R = TypeVar("R")
CallableT = TypeVar("CallableT", bound="Callable[..., Any]")
CommandCallbackT = TypeVar("CommandCallbackT", bound=utilities.CommandCallback)
TaskT = TypeVar("TaskT", bound="Task")

Task = Union[
    "Callable[[], Any]",
    "Callable[[community.Community], Any]",
]

logger = logging.getLogger("pymino")


def with_typing(
    func: "Callable[Concatenate[Context, P], R]",
) -> "Callable[Concatenate[Context, P], R]":
    @functools.wraps(func)
    def wrapper(self: "Context", *args: P.args, **kwargs: P.kwargs) -> R:
        with self.typing():
            return func(self, *args, **kwargs)

    return wrapper


class WaitForMessage:
    __slots__ = (
        "status_code",
        "_incorrect_message",
        "_message_found",
        "_message_not_found",
        "_message_timeout",
    )

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        self._message_timeout = False
        self._incorrect_message = None
        self._message_found = False
        self._message_not_found = False
        self.__set_status_code__()

    @property
    def message_timeout(self) -> bool:
        """Whether or not the timeout was reached."""
        return self._message_timeout

    @message_timeout.setter
    def message_timeout(self, value: bool) -> None:
        self._message_timeout = value

    @property
    def message_not_found(self) -> bool:
        """Whether or not the message was not found."""
        return self._message_not_found

    @message_not_found.setter
    def message_not_found(self, value: bool) -> None:
        self._message_not_found = value

    @property
    def message_found(self) -> bool:
        """Whether or not the message was found."""
        return self._message_found

    @message_found.setter
    def message_found(self, value: bool) -> None:
        self._message_found = value

    def __set_status_code__(self) -> None:
        if self.status_code == 200:
            self.message_found = True
            self.message_not_found = False
            self.message_timeout = False
        elif self.status_code == 404:
            self.message_found = False
            self.message_not_found = True
            self.message_timeout = False
        elif self.status_code == 500:
            self.message_found = False
            self.message_not_found = False
            self.message_timeout = True

    def __repr__(self) -> str:
        return f"<WaitForMessage status_code={self.status_code} message_timeout={self.message_timeout} message_not_found={self.message_not_found} message_found={self.message_found}>"


class Context:
    """
    Context class that handles context.

    This class is used to handle context for commands.

    Attributes:
    message : Message
        The message object.
    bot : Bot
        The bot object.
    request : RequestHandler
        The request handler object.
    userId : str
        The user ID.
    intents : bool
        Whether or not intents are enabled.

    """

    __slots__ = (
        "message",
        "bot",
    )

    def __init__(self, message: "entities.Message", bot: "bot.Bot") -> None:
        self.message = message
        self.bot = bot

    @property
    def request(self) -> utilities.RequestHandler:
        return self.bot.request

    @property
    def intents(self) -> bool:
        return self.bot.intents

    @property
    def userId(self) -> str:
        return cast(str, self.bot.userId)

    @property
    def author(self) -> "entities.MessageAuthor":
        """The author of the message."""
        return self.message.author

    @property
    def communityId(self) -> str:
        """Sets the url to community/global."""
        return "g" if self.message.comId == 0 else f"x{self.message.comId}"

    @property
    def comId(self) -> int:
        """The community ID."""
        return self.message.comId

    @property
    def chatId(self) -> str:
        """The chat ID."""
        return self.message.chatId

    @property
    def api(self) -> str:
        """The API url."""
        return "https://service.aminoapps.com/api/v1/"

    @property
    def __message_endpoint__(self) -> str:
        """The message endpoint."""
        return f"/{self.communityId}/s/chat/thread/{self.message.chatId}/message"

    __typing__ = staticmethod(with_typing)

    def __purge__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in data.items() if v is not None}

    def __prepare_message__(self, **kwargs: Any) -> Dict[str, Any]:
        return self.__purge__(self.__parse_kwargs__(**kwargs))

    def __parse_kwargs__(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            "content": kwargs.get("content"),
            "type": kwargs.get("type"),
            "mediaType": kwargs.get("mediaType"),
            "mediaValue": kwargs.get("mediaValue"),
            "mediaUploadValue": kwargs.get("mediaUploadValue"),
            "stickerId": kwargs.get("stickerId"),
            "attachedObject": kwargs.get("attachedObject"),
            "uid": self.userId,
        }

    def __message__(self, **kwargs: Any) -> Dict[str, Any]:
        return entities.PrepareMessage(**kwargs).json()

    def __send_message__(self, **kwargs: Any) -> "entities.CMessage":
        return entities.CMessage(
            self.request.handler(
                "POST",
                self.__message_endpoint__,
                data=self.__message__(**kwargs),
            )
        )

    @contextlib.contextmanager
    def typing(self) -> "Iterator[None]":
        payload: Dict[str, Any] = {
            "actions": ["Typing"],
            "target": f"ndc://x{self.comId}/chat-thread/{self.chatId}",
            "ndcId": self.comId,
            "params": {
                "topicIds": [],
                "threadType": 2,
            },
            "id": time.monotonic() + random.randint(0, 100),
        }
        start = time.time()
        try:
            self.bot.send_websocket_message({"o": payload, "t": 304})
            yield None
        finally:
            payload["params"]["duration"] = int(time.time() - start)
            self.bot.send_websocket_message({"o": payload, "t": 306})

    def _delete(
        self,
        message: "entities.CMessage",
        delete_after: float = 5.0,
    ) -> entities.ApiResponse:
        """Deletes a message.

        `**Parameters**`
        - `message` - The message to delete.
        - `delete_after` - The time to delay before deleting the message.

        """
        time.sleep(delete_after)
        return entities.ApiResponse(
            self.request.handler(
                "DELETE",
                f"/{self.communityId}/s/chat/thread/{message.chatId}/message/{message.messageId}",
            )
        )

    def wait_for_message(self, message: str, timeout: float = 10.0) -> WaitForMessage:
        """This waits for a specific message within a certain timeout period.

        `**Parameters**`
        - `message` : str
            The specific message to wait for in the cache.
        - `timeout` : int, optional
            The maximum time to wait for the message in seconds. Default is 10.

        `**Returns**`
        - `WaitForMessage`: The WaitForMessage object.

            - `MESSAGE_TIMEOUT` : bool
                - Whether or not the timeout was reached.
            - `MESSAGE_NOT_FOUND` : bool
                - Whether or not the message was not found.
            - `MESSAGE_FOUND` : bool
                - Whether or not the message was found.

        `**Example**`
        ```py
        @bot.on_member_join()
        def on_member_join(ctx: Context):
            if ctx.comId != bot.community.community_id:
                return

            TIMEOUT = 15

            ctx.send(content="Welcome to the chat! Please verify yourself by typing `$verify` in the chat.", delete_after=TIMEOUT)

            response = ctx.wait_for_message(message="$verify", timeout=15)

            if response.MESSAGE_TIMEOUT:
                ctx.send(content="You took too long to verify yourself. You have been kicked from the chat.", delete_after=TIMEOUT)
                return bot.community.kick(userId=ctx.author.userId, chatId=ctx.chatId, allowRejoin=True, comId=ctx.comId)

            elif response.MESSAGE_NOT_FOUND:
                ctx.send(content="Invalid verification code. You have been kicked from the chat.", delete_after=TIMEOUT)

            elif response.MESSAGE_FOUND:
                ctx.send(content="You have been verified!", delete_after=TIMEOUT)
        ```
        """
        if not self.intents:
            raise entities.IntentsNotEnabled
        start = time.time()
        with entities.cache as cache:
            key = f"{self.message.chatId}_{self.message.author.userId}"
            while (time.time() - start) < timeout:
                cached_message = cache.get(key)

                if cached_message == message:
                    cache.pop(key)
                    return WaitForMessage(status_code=200)
                if all([cached_message is not None, cached_message != message]):
                    cache.pop(key)
                    return WaitForMessage(status_code=404)
            cache.pop(key)
            return WaitForMessage(status_code=500)

    @with_typing
    def send(
        self,
        content: str,
        delete_after: Optional[float] = None,
        mentioned: Optional[Union["Sequence[str]", str]] = None,
    ) -> "entities.CMessage":
        """This sends a message.

        `**Parameters**``
        - `content` - The message you want to send.
        - `delete_after` - The time in seconds before the message is deleted. [Optional]
        - `mentioned` - The user(s) you want to mention. [Optional]

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send(content="Hello World!", delete_after=None)
        ```
        """
        if isinstance(mentioned, str):
            mentioned = [mentioned]
        message = self.__send_message__(
            content=content,
            extensions={
                "mentionedArray": (
                    [{"uid": user} for user in mentioned] if mentioned else None
                )
            },
        )
        if delete_after:
            threading.Thread(target=self._delete, args=(message, delete_after)).start()
        return message

    @with_typing
    def reply(
        self,
        content: str,
        delete_after: Optional[float] = None,
        mentioned: Optional[Union["Sequence[str]", str]] = None,
    ) -> "entities.CMessage":
        """This replies to the message.

        `**Parameters**``
        - `content` - The message you want to send.
        - `delete_after` - The time in seconds before the message is deleted. [Optional]
        - `mentioned` - The user(s) you want to mention. [Optional]

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.reply(content = "Hello World!", delete_after = None)
        ```
        """
        if isinstance(mentioned, str):
            mentioned = [mentioned]
        message = self.__send_message__(
            content=content,
            replyMessageId=self.message.messageId,
            extensions={
                "mentionedArray": (
                    [{"uid": user} for user in mentioned] if mentioned else None
                )
            },
        )

        if delete_after:
            threading.Thread(target=self._delete, args=(message, delete_after)).start()

        return message

    def prepare_mentions(self, mentioned: "Sequence[str]") -> List[str]:
        """This prepares the mentions for the message.

        `**Parameters**``
        - `mentioned` - `ctx.message.mentioned_user_names`.

        `**Returns**``
        - `list[str]` - The list of usernames to use as your `message`

        `**Example**``
        ```py
        @bot.command("mention")
        def mention(ctx: Context):
            mentioned_users = ctx.message.mentioned_user_names
            if not mentioned_users:
                return ctx.reply("You didn't mention anyone!")

            mentioned = ctx.prepare_mentions(mentioned_users)
            return ctx.reply(
                "Mentioned: " + ", ".join(mentioned), mentioned=list(mentioned_users)
            )
        """
        return [f"\u200e\u200f@{username}\u202c\u202d" for username in mentioned]

    @with_typing
    def send_link_snippet(
        self,
        image: "entities.Media",
        message: str = "[c]",
        link: str = "ndc://user-me",
        mentioned: Optional[Union["Sequence[str]", str]] = None,
    ) -> "entities.CMessage":
        """This sends a link snippet.

        `**Parameters**``
        - `image` - The image you want to send. Recommended size: 807x216
        - `message` - The message you want to send.
        - `link` - The link you want to send. [Optional]

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.command("linksnippet")
        def linksnippet(ctx: Context):
            return ctx.send_link_snippet(
                image = "https://i.imgur.com/8ZQZ9Zm.png",
                message = "Hello World!",
                link = "https://www.google.com"
            )
        ```
        """
        if isinstance(mentioned, str):
            mentioned = [mentioned]
        return self.__send_message__(
            content=message,
            extensions={
                "linkSnippetList": [
                    {
                        "mediaType": 100,
                        "mediaUploadValue": self.__handle_media__(image),
                        "mediaUploadValueContentType": "image/png",
                        "link": link,
                    }
                ],
                "mentionedArray": (
                    [{"uid": uid} for uid in mentioned] if mentioned else None
                ),
            },
        )

    @with_typing
    def send_embed(
        self,
        message: str,
        title: str,
        content: str,
        image: str,
        link: str = "ndc://user-me",
        mentioned: Optional[Union["Sequence[str]", str]] = None,
    ) -> "entities.CMessage":
        """This sends an embed.

        `**Parameters**``
        - `message` - The message you want to send.
        - `title` - The title of the embed.
        - `content` - The content of the embed.
        - `image` - The image you want to send. Recommended size: 807x216
        - `link` - The link you want to send. [Optional]

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.command("embed")
        def embed(ctx: Context):
            return ctx.send_embed(
                message = "[c]",
                title = "Hello World!",
                content = "This is an embed.",
                image = "https://i.imgur.com/8ZQZ9Zm.png",
                link = "https://www.google.com"
            )
        ```
        """
        if isinstance(mentioned, str):
            mentioned = [mentioned]
        return self.__send_message__(
            content=message,
            attachedObject={
                "title": title,
                "content": content,
                "mediaList": [[100, self.__handle_media__(image, "image/jpg"), None]],
                "link": link,
            },
            extensions={
                "mentionedArray": (
                    [{"uid": user} for user in mentioned] if mentioned else None
                )
            },
        )

    def __handle_media__(
        self,
        media: "entities.Media",
        content_type: Optional[str] = None,
    ) -> str:
        media = entities.read_media(media)
        if content_type:
            return self.upload_media(media, content_type)

        return base64.b64encode(media).decode()

    def upload_media(
        self,
        media: "entities.Media",
        content_type: str = "image/jpg",
    ) -> str:
        return self.bot.upload_media(media, content_type)

    @with_typing
    def send_sticker(self, sticker_id: str) -> "entities.CMessage":
        """This sends a sticker.

        `**Parameters**``
        - `sticker_id` - The sticker ID you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_sticker(sticker_id="sticker_id")
        ```
        """
        sticker_id = sticker_id.removeprefix("ndcsticker://")
        return self.__send_message__(
            type=3,
            stickerId=sticker_id,
            mediaValue=f"ndcsticker://{sticker_id}",
        )

    def send_image(self, image: "entities.Media") -> "entities.CMessage":
        """This sends an image.

        `**Parameters**``
        - `image` - The image link or file you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_image(image="https://i.imgur.com/image.jpg")
        ```
        """
        return self.__send_message__(
            mediaType=100,
            mediaUploadValue=self.__handle_media__(image),
        )

    def send_gif(self, gif: "entities.Media") -> "entities.CMessage":
        """This sends a gif.

        `**Parameters**``
        - `gif` - The gif link or file you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_gif(gif="https://i.imgur.com/image.gif")
        ```
        """
        return self.__send_message__(
            mediaType=100,
            mediaUploadValueContentType="image/gif",
            mediaUploadValue=self.__handle_media__(gif),
        )

    def send_audio(self, audio: str) -> "entities.CMessage":
        """This sends an audio file.

        `**Parameters**``
        - `audio` - The audio link or file you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_audio(audio="output.mp3")
        ```
        """
        return self.__send_message__(
            type=2,
            mediaType=110,
            mediaUploadValue=self.__handle_media__(audio),
        )

    def join_chat(self, chatId: Optional[str] = None) -> entities.ApiResponse:
        """This joins a chat.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.join_chat(chatId="0000-0000-0000-0000")
        ```
        """
        if not chatId:
            chatId = self.chatId
        return entities.ApiResponse(
            self.request.handler(
                "POST",
                f"/{self.communityId}/s/chat/thread/{chatId}/member/{self.userId}",
            ),
        )

    def leave_chat(self, chatId: Optional[str] = None) -> entities.ApiResponse:
        """This leaves a chat.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.leave_chat(chatId="0000-0000-0000-0000")
        ```
        """
        if not chatId:
            chatId = self.chatId
        return entities.ApiResponse(
            self.request.handler(
                "DELETE",
                f"/{self.communityId}/s/chat/thread/{chatId}/member/{self.userId}",
            ),
        )


class EventHandler(abc.ABC):
    """AKA where all the events are handled."""

    @property
    @abc.abstractmethod
    def community(self) -> community.Community: ...

    @property
    @abc.abstractmethod
    def intents(self) -> bool: ...

    @property
    @abc.abstractmethod
    def command_prefix(self) -> str: ...

    def __init__(self) -> None:
        self._events: Dict[str, Callable[..., Any]] = {}
        self._commands = utilities.Commands()
        self._tasks: List[Tuple[Task, float]] = []
        self._cooldown_message: Optional[str] = None

    def register_event(self, event_name: str) -> "Callable[[CallableT], CallableT]":
        def decorator(event_handler: CallableT) -> CallableT:
            self._events[event_name] = event_handler
            return event_handler

        return decorator

    def _handle_task(self, callback: Task, interval: float) -> None:
        """
        This handles the task.

        `**Parameters**``
        - `func` - The function.
        - `interval` - The interval in seconds.

        `**Returns**`` - None
        """
        community_required = len(inspect.signature(callback).parameters) != 0
        while True:
            args = [self.community] if community_required else []
            try:
                callback(*args)
            except Exception as e:
                logger.debug(f"Task error: {e}")
            finally:
                time.sleep(interval)

    def task(self, interval: float = 10.0) -> "Callable[[TaskT], TaskT]":
        """
        This creates a task.

        `**Parameters**``
        - `interval` - The interval in seconds.

        `**Example**``
        ```py
        # This will print "Hello World!" every 10 seconds.
        @bot.task(interval=10)
        def task():
            print("Hello World!")

        # This will send a message to a chat every 120 seconds.
        @bot.task(interval=120)
        def task(community: Community):
            community.send_message(chatId=0000-0000-0000-0000, content="Hello World!")
        ```
        """

        def decorator(callback: TaskT) -> TaskT:
            self._tasks.append((callback, interval))
            return callback

        return decorator

    def _set_parameters(
        self,
        context: Context,
        func: utilities.CommandCallback,
        message: Optional[str] = None,
    ) -> List[Any]:
        potential_parameters = {
            "ctx": context,
            "member": entities.Member(context.author.json()),
            "message": message if isinstance(message, str) else context.message.content,
            "username": context.author.username,
            "userId": context.author.userId,
        }

        return [
            potential_parameters.get(parameter)
            for parameter in inspect.signature(func).parameters
        ]

    def emit(self, name: str, *args: Any) -> None:
        """`emit` is a function that emits an event."""
        if name in self._events:
            self._events[name](*args)

    def command(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        usage: Optional[str] = None,
        aliases: Optional["Sequence[str]"] = None,
        cooldown: float = 0.0,
        **kwargs: Any,
    ) -> "Callable[[CommandCallbackT], CommandCallbackT]":
        """This creates a command.

        `**Command Parameters**``
        - `command_name` - The name of the command.
        - `command_description` - The description of the command.
        - `aliases` - The other names the command can be called by.
        - `cooldown` - The cooldown of the command in seconds.

        `**Function Parameters**``
        - `ctx` - The context of the command.
        - `member` - The Member(member) who called the command.
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
        def ping(ctx: Context, message: str, username: str, userId: str): # Function parameters.
            print(f"{username}({userId}): {message}") # OUTPUT: "JohnDoe(0000-0000-0000-0000): !ping"
            return ctx.send(content="Pong!")

        @bot.command(command_name="ping", aliases=["alive", "test"]) # Command parameters.
        def ping(ctx: Context): # Function parameters.
            # This command can be called by "ping", "alive", and "test".
            return ctx.send(content="Pong!")

        @bot.command(command_name="ping", cooldown=5) # Command parameters.
        def ping(ctx: Context): # Function parameters.
            # This command can only be called every 5 seconds.
            return ctx.send(content="Pong!")

        @bot.command(command_name="say", command_description="This is a command that says something.") # Command parameters.
        def say(ctx: Context, message: str, username: str, userId: str): # Function parameters.
            bot.community.delete_message(chatId=ctx.chatId, messageId=ctx.message.chatId, comId=ctx.comId)
            return ctx.send(content=message)
        ```
        """
        if "command_name" in kwargs:
            self._is_deprecated("command_name", "name")
            name = kwargs["command_name"]
        if name is None:
            raise ValueError(
                "Please supply a name for the command. Example: @bot.command(name='ping')"
            )
        if "command_description" in kwargs:
            self._is_deprecated("command_description", "description")
            description = kwargs["command_description"]

        def decorator(func: CommandCallbackT) -> CommandCallbackT:
            self._commands.add_command(
                utilities.Command(
                    func=func,
                    name=name,
                    description=description,
                    usage=usage,
                    aliases=aliases,
                    cooldown=cooldown,
                )
            )
            return func

        return decorator

    def _is_deprecated(self, parameter: str, new_parameter: str) -> None:
        print(
            f"{colorama.Style.BRIGHT}{colorama.Fore.RED}"
            f"WARNING:{colorama.Style.RESET_ALL} '{parameter}' is deprecated. "
            f"Please use '{new_parameter}' instead."
        )

    def command_exists(self, command_name: str) -> bool:
        return any(
            [
                command_name in self._commands.__command_names__(),
                command_name in self._commands.__command_aliases__(),
            ]
        )

    def fetch_command(self, command_name: str) -> Optional[utilities.Command]:
        return self._commands.fetch_command(command_name)

    def _handle_command(self, data: "entities.Message", context: Context):
        """Handles commands.

        Args:
            self: The instance of the class.
            data (Message): The message data containing the command.
            context (Context): The context of the command.

        Returns:
            None or the response from the command function.

        Examples:
            This function is internally called and does not have direct usage examples.
        """
        if not data.content.startswith(self.command_prefix):
            if self._events.get("text_message"):
                self._handle_all_events(
                    event="text_message", data=data, context=context
                )
            return
        command_name, *_ = data.content[len(self.command_prefix) :].split()
        command = self._commands.fetch_command(command_name)
        if command is None:
            if command_name == "help" and data.content.startswith(
                f"{self.command_prefix}help"
            ):
                context.reply(content=self._commands.__help__())
            return None
        message = data.content[len(self.command_prefix) + len(command_name) + 1 :]
        if self._check_cooldown(command.name, data, context):
            return None

        args = self._set_parameters(context=context, func=command.func, message=message)
        command.func(*args)

    def _check_cooldown(
        self,
        command_name: str,
        data: "entities.Message",
        context: Context,
    ) -> bool:
        """A function that checks if a command is on cooldown."""
        command = self._commands.fetch_command(command_name)
        if command and command.cooldown:
            cooldown_time = int(
                self._commands.fetch_cooldown(command_name, data.author.userId)
                - time.time()
            )
            if (
                self._commands.fetch_cooldown(command_name, data.author.userId)
                > time.time()
            ):
                default_message = f"You are on cooldown for {cooldown_time} seconds."
                context.reply(content=self._cooldown_message or default_message)
                return True
            self._commands.set_cooldown(
                command_name=command_name,
                cooldown=command.cooldown,
                userId=data.author.userId,
            )
        return False

    def _add_cache(self, chatId: str, userId: str, content: str) -> None:
        key = f"{chatId}_{userId}"
        with entities.cache as cache:
            if cache.get(key) is not None:
                cache.pop(key)
            cache.add(key, content, expire=90)

    def on_error(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an error occurs."""
        return self.register_event("error")

    def on_ready(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when the bot is ready to start handling events."""
        return self.register_event("ready")

    def on_text_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a text message is received in the chat."""
        return self.register_event("text_message")

    def _console_on_text_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a text message is received in the console."""
        return self.register_event("_console_text_message")

    def on_image_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an image message is received in the chat."""
        return self.register_event("image_message")

    def on_youtube_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a YouTube message is received in the chat."""
        return self.register_event("youtube_message")

    def on_strike_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a strike message is received in the chat."""
        return self.register_event("strike_message")

    def on_voice_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a voice message is received in the chat."""
        return self.register_event("voice_message")

    def on_sticker_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a sticker message is received in the chat."""
        return self.register_event("sticker_message")

    def on_vc_not_answered(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a voice chat request is not answered."""
        return self.register_event("vc_not_answered")

    def on_vc_not_cancelled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a voice chat request is not cancelled."""
        return self.register_event("vc_not_cancelled")

    def on_vc_not_declined(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a voice chat request is not declined."""
        return self.register_event("vc_not_declined")

    def on_video_chat_not_answered(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a video chat request is not answered."""
        return self.register_event("video_chat_not_answered")

    def on_video_chat_not_cancelled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a video chat request is not cancelled."""
        return self.register_event("video_chat_not_cancelled")

    def on_video_chat_not_declined(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a video chat request is not declined."""
        return self.register_event("video_chat_not_declined")

    def on_avatar_chat_not_answered(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an avatar chat request is not answered."""
        return self.register_event("avatar_chat_not_answered")

    def on_avatar_chat_not_cancelled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an avatar chat request is not cancelled."""
        return self.register_event("avatar_chat_not_cancelled")

    def on_avatar_chat_not_declined(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an avatar chat request is not declined."""
        return self.register_event("avatar_chat_not_declined")

    def on_delete_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a message is deleted in the chat."""
        return self.register_event("delete_message")

    def on_member_join(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a member joins the chat."""
        return self.register_event("member_join")

    def on_member_leave(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a member leaves the chat."""
        return self.register_event("member_leave")

    def on_chat_invite(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an invite is sent to the chat."""
        return self.register_event("chat_invite")

    def on_chat_background_changed(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when the chat background is changed."""
        return self.register_event("chat_background_changed")

    def on_chat_title_changed(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when the chat title is changed."""
        return self.register_event("chat_title_changed")

    def on_chat_icon_changed(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when the chat icon is changed."""
        return self.register_event("chat_icon_changed")

    def on_vc_start(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a voice chat starts."""
        return self.register_event("vc_start")

    def on_video_chat_start(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a video chat starts."""
        return self.register_event("video_chat_start")

    def on_avatar_chat_start(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an avatar chat starts."""
        return self.register_event("avatar_chat_start")

    def on_vc_end(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a voice chat ends."""
        return self.register_event("vc_end")

    def on_video_chat_end(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a video chat ends."""
        return self.register_event("video_chat_end")

    def on_avatar_chat_end(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an avatar chat ends."""
        return self.register_event("avatar_chat_end")

    def on_chat_content_changed(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when the chat content is changed."""
        return self.register_event("chat_content_changed")

    def on_screen_room_start(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a screen room starts."""
        return self.register_event("screen_room_start")

    def on_screen_room_end(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a screen room ends."""
        return self.register_event("screen_room_end")

    def on_chat_host_transfered(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when the chat host is transferred."""
        return self.register_event("chat_host_transfered")

    def on_text_message_force_removed(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a text message is forcefully removed."""
        return self.register_event("text_message_force_removed")

    def on_chat_removed_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a chat message is removed."""
        return self.register_event("chat_removed_message")

    def on_mod_deleted_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a moderator deletes a message."""
        return self.register_event("mod_deleted_message")

    def on_chat_tip(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a tip is received in the chat."""
        return self.register_event("chat_tip")

    def on_chat_pin_announcement(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an announcement is pinned in the chat."""
        return self.register_event("chat_pin_announcement")

    def on_vc_permission_open_to_everyone(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when voice chat permissions are set to open to everyone."""
        return self.register_event("vc_permission_open_to_everyone")

    def on_vc_permission_invited_and_requested(
        self,
    ) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when voice chat permissions are set to invited and requested."""
        return self.register_event("vc_permission_invited_and_requested")

    def on_vc_permission_invite_only(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when voice chat permissions are set to invite only."""
        return self.register_event("vc_permission_invite_only")

    def on_chat_view_only_enabled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when chat view only mode is enabled."""
        return self.register_event("chat_view_only_enabled")

    def on_chat_view_only_disabled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when chat view only mode is disabled."""
        return self.register_event("chat_view_only_disabled")

    def on_chat_unpin_announcement(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an announcement is unpinned in the chat."""
        return self.register_event("chat_unpin_announcement")

    def on_chat_tipping_enabled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when chat tipping is enabled."""
        return self.register_event("chat_tipping_enabled")

    def on_chat_tipping_disabled(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when chat tipping is disabled."""
        return self.register_event("chat_tipping_disabled")

    def on_timestamp_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a timestamp message is received in the chat."""
        return self.register_event("timestamp_message")

    def on_welcome_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a welcome message is received in the chat."""
        return self.register_event("welcome_message")

    def on_share_exurl_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a shared external URL message is received in the chat."""
        return self.register_event("share_exurl_message")

    def on_invite_message(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when an invite message is received in the chat."""
        return self.register_event("invite_message")

    def on_user_online(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when a user comes online."""
        return self.register_event("user_online")

    def on_member_set_you_host(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when you are set as the host of the chat.

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

    def on_member_set_you_cohost(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when you are set as a cohost of the chat.

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

    def on_member_remove_your_cohost(self) -> "Callable[[CallableT], CallableT]":
        """This is an event that is called when you are removed as a cohost of the chat.

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

    def _handle_all_events(
        self,
        event: str,
        data: Union[
            "entities.Message", "entities.OnlineMembers", entities.Notification, Context
        ],
        context: Optional[Context],
    ) -> None:
        callback = self._events.get(event)
        if not callback:
            return
        args: List[Any] = []
        if context:
            args.extend(self._set_parameters(context, callback))
        else:
            args.append(data)
        callback(*args)

    def _handle_event(
        self,
        event: str,
        data: Union[
            "entities.Message", "entities.OnlineMembers", entities.Notification, Context
        ],
    ) -> None:
        """Is a function that handles events."""
        context: Optional[Context] = None
        if isinstance(data, entities.Message):
            context = Context(data, cast(bot.Bot, self))
        elif isinstance(data, Context):
            context = data
        if event == "text_message" and isinstance(data, entities.Message):
            command_name = data.content[len(self.command_prefix) :].split(" ")[0]
            if self.intents and not self.command_exists(command_name):
                self._add_cache(data.chatId, data.author.userId, data.content)
            if context:
                self._handle_command(data=data, context=context)
                return None
        if event in self._events:
            self._handle_all_events(event=event, data=data, context=context)

        return None

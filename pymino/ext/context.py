from requests import get
from functools import wraps
from diskcache import Cache
from threading import Thread
from base64 import b64encode
from contextlib import suppress
from colorama import Fore, Style
from time import sleep as delay, time
from inspect import signature as inspect_signature
from typing import BinaryIO, Callable, List, Union

from .entities import *
from .utilities.commands import Command, Commands

__all__ = (
    "Context",
    "EventHandler",
    "WaitForMessage",
    )

class WaitForMessage:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        self._MESSAGE_TIMEOUT = None
        self._INCORRECT_MESSAGE = None
        self._MESSAGE_FOUND = None

        self.__set_status_code__()

    @property
    def MESSAGE_TIMEOUT(self) -> bool:
        """Whether or not the timeout was reached."""
        return self._MESSAGE_TIMEOUT
    
    @MESSAGE_TIMEOUT.setter
    def MESSAGE_TIMEOUT(self, value: bool) -> None:
        self._MESSAGE_TIMEOUT = value

    @property
    def MESSAGE_NOT_FOUND(self) -> bool:
        """Whether or not the message was not found."""
        return self._MESSAGE_NOT_FOUND
    
    @MESSAGE_NOT_FOUND.setter
    def MESSAGE_NOT_FOUND(self, value: bool) -> None:
        self._MESSAGE_NOT_FOUND = value

    @property
    def MESSAGE_FOUND(self) -> bool:
        """Whether or not the message was found."""
        return self._MESSAGE_FOUND
    
    @MESSAGE_FOUND.setter
    def MESSAGE_FOUND(self, value: bool) -> None:
        self._MESSAGE_FOUND = value
    
    def __set_status_code__(self):
        if self.status_code == 200:
            self.MESSAGE_FOUND = True
            self.MESSAGE_NOT_FOUND = False
            self.MESSAGE_TIMEOUT = False

        elif self.status_code == 404:
            self.MESSAGE_FOUND = False
            self.MESSAGE_NOT_FOUND = True
            self.MESSAGE_TIMEOUT = False

        elif self.status_code == 500:
            self.MESSAGE_FOUND = False
            self.MESSAGE_NOT_FOUND = False
            self.MESSAGE_TIMEOUT = True

    def __repr__(self) -> str:
        return f"<WaitForMessage status_code={self.status_code} MESSAGE_TIMEOUT={self.MESSAGE_TIMEOUT} MESSAGE_NOT_FOUND={self.MESSAGE_NOT_FOUND} MESSAGE_FOUND={self.MESSAGE_FOUND}>"

class Context:
    """
    Context class that handles context.

    This class is used to handle context for commands.

    Special Attributes:
    __slots__ : tuple
        A tuple containing a fixed set of attributes to optimize memory usage.

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
        "request",
        "userId",
        "intents"
    )
    def __init__(self, message: Message, bot):
        self.message:   Message = message 
        self.bot        = bot
        self.request    = self.bot.request
        self.userId:    str = self.request.userId
        self.intents:   bool = self.bot.intents


    @property
    def author(self) -> MessageAuthor:
        """The author of the message."""
        with suppress(AttributeError):
            return self.message.author

    @property
    def communityId(self) -> str:
        """Sets the url to community/global."""
        return {True: "g", False: f"x{self.message.comId}"}[self.message.comId == 0]

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
        return "http://service.aminoapps.com/api/v1"
    
    @property
    def cache(self) -> Cache:
        """The cache."""
        return Cache("cache")

    @property
    def __message_endpoint__(self) -> str:
        """The message endpoint."""
        return f"/{self.communityId}/s/chat/thread/{self.message.chatId}/message"


    def __typing__(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            Thread(target=args[0].__rt__, args=(args[0].comId, args[0].chatId)).start()
            return func(*args, **kwargs)
        return wrapper


    def _run(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
                if isinstance(args[0], Context):
                    return func(*args, **kwargs)
                else:
                    raise MustRunInContext
        return wrapper


    def __purge__(self, data: dict) -> dict:
        return {k: v for k, v in data.items() if v is not None}


    def __prepare_message__(self, **kwargs) -> dict:
        return self.__purge__(self.__parse_kwargs__(**kwargs))    


    def __read_image__(self, image: Union[str, BinaryIO]) -> BinaryIO:
        try:
            return get(image).content if image.startswith("http") else open(image, "rb").read()
        except InvalidImage as e:
            raise InvalidImage from e


    def __parse_kwargs__(self, **kwargs) -> dict:
        return {
            "content": kwargs.get("content"),
            "type": kwargs.get("type"),
            "mediaType": kwargs.get("mediaType"),
            "mediaValue": kwargs.get("mediaValue"),
            "mediaUploadValue": kwargs.get("mediaUploadValue"),
            "stickerId": kwargs.get("stickerId"),
            "attachedObject": kwargs.get("attachedObject"),
            "uid": self.userId
            } 


    def __message__(self, **kwargs) -> dict:
        return PrepareMessage(**kwargs).json()


    def __send_message__(self, **kwargs) -> CMessage:
        return CMessage(self.request.handler(
            method = "POST",
            url = self.__message_endpoint__,
            data = self.__message__(**kwargs)
            ))


    def __st__(self, comId: str, chatId: str):
        return self.bot.send_websocket_message({
            "o":{
                "actions":["Typing"],
                "target":f"ndc://x{comId}/chat-thread/{chatId}",
                "ndcId":comId,
                "params":{"topicIds":[],"threadType":2},
                "id":randint(0, 100)},
                "t":304
                })


    def __et__(self, comId: str, chatId: str):
        def wrapper():
            return self.bot.send_websocket_message({
                "o":{
                    "actions":["Typing"],
                    "target":f"ndc://x{comId}/chat-thread/{chatId}",
                    "ndcId":comId,
                    "params":{"duration":0,"topicIds":[],"threadType":2},
                    "id":randint(0, 100)},
                    "t":306
                    })
        delay(2.5)
        return wrapper()


    def __rt__(self, comId: str, chatId: str):
        self.__st__(comId, chatId)
        self.__et__(comId, chatId)


    def _delete(self, delete_message: CMessage, delete_after: int = 5) -> ApiResponse:
        """
        `delete` - Deletes a message.
        
        `**Parameters**`
        - `delete_message` - The message to delete.
        - `delete_after` - The time to delay before deleting the message.
        
        """
        delay(delete_after)
        return ApiResponse(self.request.handler(
            method = "DELETE",
            url = f"/{self.communityId}/s/chat/thread/{self.message.chatId}/message/{delete_message.messageId}"
            ))
    
    def wait_for_message(self, message: str, timeout: int = 10) -> WaitForMessage:
        """
        `wait_for_message` - This waits for a specific message within a certain timeout period. 
        
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
            raise IntentsNotEnabled

        start = time()

        with self.bot.cache as cache:
            while time() - start < timeout:
                cached_message = cache.get(f"{self.message.chatId}_{self.message.author.userId}")

                if cached_message == message:
                    cache.pop(f"{self.message.chatId}_{self.message.author.userId}")
                    return WaitForMessage(status_code=200)

                if all([cached_message is not None, cached_message != message]):
                    cache.pop(f"{self.message.chatId}_{self.message.author.userId}")
                    return WaitForMessage(status_code=404)

            cache.pop(f"{self.message.chatId}_{self.message.author.userId}")
            return WaitForMessage(status_code=500)

    @_run
    @__typing__
    def send(self, content: str, delete_after: int= None, mentioned: Union[str, List[str]]= None) -> CMessage:
        """
        `send` - This sends a message.

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
        message: CMessage = self.__send_message__(
            content=content,
            extensions = {
            "mentionedArray": [{"uid": user} for user in mentioned] if mentioned else None
            })

        Thread(target=self._delete, args=(message, delete_after)).start() if delete_after else None

        return message


    @_run
    @__typing__
    def reply(self, content: str, delete_after: int= None, mentioned: Union[str, List[str]]= None) -> CMessage:
        """
        `reply` - This replies to the message.

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
        message: CMessage = self.__send_message__(
            content=content,
            replyMessageId=self.message.messageId,
            extensions = {
            "mentionedArray": [{"uid": user} for user in mentioned] if mentioned else None
            })
        
        Thread(target=self._delete, args=(message, delete_after)).start() if delete_after else None
        
        return message


    def prepare_mentions(self, mentioned: list) -> list:
        """
        `prepare_mentions` - This prepares the mentions for the message.
        
        `**Parameters**``
        - `mentioned` - `ctx.message.mentioned_user_names`.
        
        `**Returns**``
        - `list` - The list of mentions to use as your `message`

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


    @_run
    @__typing__
    def send_link_snippet(self, image: str, message: str = "[c]", link: str = "ndc://user-me", mentioned: list = None) -> CMessage:
        """
        `send_link_snippet` - This sends a link snippet.

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
        if mentioned is None: mentioned = []

        message: CMessage = self.__send_message__(
            content=message,
            extensions = {
                "linkSnippetList": [{
                "mediaType": 100,
                "mediaUploadValue": self.encode_media(
                    self.__handle_media__(media=image, content_type="image/jpg", media_value=False)
                ),
                "mediaUploadValueContentType": "image/png",
                "link": link
                }],
            "mentionedArray": [{"uid": user} for user in mentioned] if mentioned else None
            })

        return message


    @_run
    @__typing__
    def send_embed(
        self,
        message: str,
        title: str,
        content: str,
        image: str,
        link: str = "ndc://user-me",
        mentioned: Union[str, List[str]]= None
        ) -> CMessage:
        """
        `send_embed` - This sends an embed.

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
        message: CMessage = self.__send_message__(
            content=message,
            attachedObject = {
                "title": title,
                "content": content,
                "mediaList": [[100, self.__handle_media__(media=image, media_value=True), None]],
                "link": link
                },
            extensions = {
                "mentionedArray": [{"uid": user} for user in mentioned] if mentioned else None
            })
        
        return message


    def __handle_media__(self, media: str, content_type: str = "image/jpg", media_value: bool = False) -> str:
        response = None
        
        try:
            if media.startswith("http"):
                response = get(media)
                response.raise_for_status()
                media = response.content
            else:
                media = open(media, "rb").read()
        except Exception as e:
            raise InvalidImage from e
        
        if content_type == "audio/aac":
            return self.encode_media(media)

        if media_value:
            return self.upload_media(media=media, content_type=content_type)

        if response and not response.headers.get("content-type").startswith("image"):
            raise InvalidImage

        return media
    

    def encode_media(self, file: bytes) -> str:
        return b64encode(file).decode()


    def upload_media(self, media: Union[str, BinaryIO], content_type: str = "image/jpg") -> str:
        return ApiResponse(self.request.handler(
            method = "POST",
            url = "/g/s/media/upload",
            data = media,
            content_type = content_type
            )).mediaValue


    @_run
    @__typing__
    def send_sticker(self, sticker_id: str) -> CMessage:
        """
        `send_sticker` - This sends a sticker.

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
        sticker_id = sticker_id.replace("ndcsticker://", "") if sticker_id.startswith("ndcsticker://") else sticker_id
        message: CMessage = self.__send_message__(
            type=3,
            stickerId=sticker_id,
            mediaValue=f"ndcsticker://{sticker_id}"
            )
        
        return message


    @_run
    def send_image(self, image: str) -> CMessage:
        """
        `send_image` - This sends an image.

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
        message: CMessage = self.__send_message__(
            mediaType=100,
            mediaUploadValue=self.encode_media(
                self.__handle_media__(
                    media=image,
                    content_type="image/jpg",
                    media_value=False
            )))

        return message


    @_run
    def send_gif(self, gif: str) -> CMessage:
        """
        `send_gif` - This sends a gif.

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
        message: CMessage = self.__send_message__(
            mediaType=100,
            mediaUploadValueContentType="image/gif",
            mediaUploadValue=self.encode_media(
                self.__handle_media__(
                    media=gif,
                    content_type="image/gif",
                    media_value=False
            )))
        
        return message


    @_run
    def send_audio(self, audio: str) -> CMessage:
        """
        `send_audio` - This sends an audio file.
        
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
        message: CMessage = self.__send_message__(
            type=2,
            mediaType=110,
            mediaUploadValue=self.__handle_media__(
                    media=audio,
                    content_type="audio/aac",
                    media_value=False
            ))
        
        return message


    @_run
    def join_chat(self, chatId: str=None) -> ApiResponse:
        """
        `join_chat` - This joins a chat.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.join_chat(chatId="0000-0000-0000-0000")
        ```
        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/{self.communityId}/s/chat/thread/{chatId or self.chatId}/member/{self.userId}"
            ))


    @_run
    def leave_chat(self, chatId: str=None) -> ApiResponse:
        """
        `leave_chat` - This leaves a chat.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.leave_chat(chatId="0000-0000-0000-0000")
        ```
        """
        return ApiResponse(self.request.handler(
            method="DELETE",
            url=f"/{self.communityId}/s/chat/thread/{chatId or self.chatId}/member/{self.userId}"
            ))


class EventHandler:
    """
    `EventHandler` - AKA where all the events are handled.

    `**Parameters**``
    - `session` - The session we are using.

    """
    def __init__(self):
        self.command_prefix:    str = self.command_prefix
        self._events:           dict = {}
        self._commands:         Commands = Commands()
        self.context:           Context = Context


    def register_event(self, event_name: str) -> Callable:
        def decorator(event_handler: Callable) -> Callable:
            self._events[event_name] = event_handler
            return event_handler
        return decorator


    def start_task(self, func):
        """`start_task` - This starts a task."""
        Thread(target=func).start()


    def _handle_task(self, func, interval):
        """
        `_handle_task` - This handles the task.
        
        `**Parameters**``
        - `func` - The function.
        - `interval` - The interval in seconds.
        
        `**Returns**`` - None
        """
        while True:
            if len(inspect_signature(func).parameters) == 0:
                func()
            else:
                func(self.community)
            delay(interval)


    def task(self, interval: int = 10):
        """
        `task` - This creates a task.

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

        def decorator(func):
            def wrapper():
                self._handle_task(func, interval)
            self.start_task(wrapper)
        return decorator


    def _set_parameters(self, context: Context, func: Callable, message: str = None) -> list:
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


    def emit(self, name: str, *args) -> None:
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

    def _handle_command(self, data: Message, context: Context):
        """
        Handles commands.

        Args:
            self: The instance of the class.
            data (Message): The message data containing the command.
            context (Context): The context of the command.

        Returns:
            None or the response from the command function.

        Raises:
            None

        Examples:
            This function is internally called and does not have direct usage examples.
        """
        command_name = next(iter(data.content[len(self.command_prefix):].split(" ")))

        message = data.content[len(self.command_prefix) + len(command_name) + 1:]
        command = self._commands.fetch_command(command_name)
    
        if command is None:
            if command_name == "help" and data.content == f"{self.command_prefix}help":
                return context.reply(content=self._commands.__help__())
            
            if self._events.get("text_message"):
                return self._handle_all_events(event="text_message", data=data, context=context)

        if data.content[:len(self.command_prefix)] != self.command_prefix:
            return None

        try:
            response = self._check_cooldown(command.name, data, context)
        except AttributeError:
            return None

        if response != 403:
            func = command.func
            return func(*self._set_parameters(context=context, func=func, message=message))

        return None


    def _check_cooldown(self, command_name: str, data: Message, context: Context) -> None:
        """`_check_cooldown` is a function that checks if a command is on cooldown."""
        if self._commands.fetch_command(command_name).cooldown > 0:
            if self._commands.fetch_cooldown(command_name, data.author.userId) > time():
                context.reply(content=self._cooldown_message or f"You are on cooldown for {int(self._commands.fetch_cooldown(command_name, data.author.userId) - time())} seconds.")
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


    def _handle_all_events(self, event: str, data: Message, context: Context) -> None:
        func = self._events[event]
        return func(*self._set_parameters(context, func, data))


    def _handle_event(
        self,
        event: str,
        data: Union[Message, OnlineMembers, Notification, Context]
        ) -> Union[Context, None]:
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

                return self._handle_command(data=data, context=context)
            
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
                    return self._handle_all_events(event=event, data=data, context=context)
                
            return None
import asyncio
from functools import wraps
import aiohttp
from diskcache import Cache
from base64 import b64encode
from contextlib import suppress
from time import sleep as delay, time
from asyncio import AbstractEventLoop
from typing import BinaryIO, Callable, List, Union

from .entities import *

class AsyncContext:
    """
    `Context` - This handles the event context.

    `**Parameters**``
    - `message` - The message which triggered the event.
    - `session` - The session we will use to send requests.

    """
    def __init__(self, message: Message, bot):
        self.bot = bot
        self.message:   Message = message
        self.loop:      AbstractEventLoop = self.bot.loop
        self.intents:   bool = self.bot.intents
        self.request    = self.bot.request
        self.userId:    str = self.request.userId


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
    def comId(self) -> str:
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
            args[0].loop.create_task(args[0].__rt__(args[0].comId, args[0].chatId))
            return func(*args, **kwargs)
        return wrapper


    def _run(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
                if isinstance(args[0], AsyncContext):
                    return await func(*args, **kwargs)
                else:
                    raise MustRunInContext
        return wrapper


    async def __purge__(self, data: dict) -> dict:
        return {k: v for k, v in data.items() if v is not None}


    async def __prepare_message__(self, **kwargs) -> dict:
        return await self.__purge__(await self.__parse_kwargs__(**kwargs))    


    async def __read_image__(self, image: Union[str, BinaryIO]) -> BinaryIO:
        try:
            if not image.startswith("http"):
                return open(image, "rb").read()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(image) as resp:
                    return await resp.read()

        except FileNotFoundError as e:
            raise FileNotFoundError from e

        except InvalidImage as e:
            raise InvalidImage from e


    async def __parse_kwargs__(self, **kwargs) -> dict:
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


    async def __message__(self, **kwargs) -> dict:
        return PrepareMessage(**kwargs).json()


    async def __send_message__(self, **kwargs) -> CMessage:
        return CMessage(
            await self.request.handler(
                method = "POST",
                url = self.__message_endpoint__,
                data = await self.__message__(**kwargs)
            ))


    async def __st__(self, comId: str, chatId: str):
        return await self.bot.send_websocket_message({
            "o":{
                "actions":["Typing"],
                "target":f"ndc://x{comId}/chat-thread/{chatId}",
                "ndcId":comId,
                "params":{"topicIds":[],"threadType":2},
                "id":randint(0, 100)},
                "t":304
                })


    async def __et__(self, comId: str, chatId: str):
        async def wrapper():
            return await self.bot.send_websocket_message({
                "o":{
                    "actions":["Typing"],
                    "target":f"ndc://x{comId}/chat-thread/{chatId}",
                    "ndcId":comId,
                    "params":{"duration":0,"topicIds":[],"threadType":2},
                    "id":randint(0, 100)},
                    "t":306
                    })
        await asyncio.sleep(2.5)
        return await wrapper()


    async def __rt__(self, comId: str, chatId: str):
        await self.__st__(comId, chatId)
        await self.__et__(comId, chatId)


    async def _delete(self, delete_message: CMessage, delete_after: int = 5) -> ApiResponse:
        delay(delete_after)
        return ApiResponse(
            await self.request.handler(
                method = "DELETE",
                url = f"/{self.communityId}/s/chat/thread/{self.message.chatId}/message/{delete_message.messageId}"
            ))


    async def wait_for_message(self, message: str, timeout: int = 10) -> int:
        """
        `wait_for_message` - This waits for a specific message within a certain timeout period. 
        
        `**Parameters**`
        - `message` : str
            The specific message to wait for in the cache.
        - `timeout` : int, optional
            The maximum time to wait for the message in seconds. Default is 10.
        
        `**Returns**`
        - `int` 
            The method returns a status code indicating the result of the operation:
            200 - If the desired message is found within the timeout.
            404 - If a different message is found within the timeout.
            500 - If the timeout is reached without finding the desired message.
        
        `**Example**`
        ```py
        @bot.on_member_join()
        async def on_member_join(ctx: Context):
            if ctx.comId != bot.community.community_id:
                return
                
            TIMEOUT = 15

            await ctx.send(content="Welcome to the chat! Please verify yourself by typing `$verify` in the chat.", delete_after=TIMEOUT)

            response = await ctx.wait_for_message(message="$verify", timeout=15)

            if response == 500:
                await ctx.send(content="You took too long to verify yourself. You have been kicked from the chat.", delete_after=TIMEOUT)
                return await bot.community.kick(userId=ctx.author.userId, chatId=ctx.chatId, allowRejoin=True, comId=ctx.comId)

            elif response == 404:
                return await ctx.send(content="Invalid verification code. You have been kicked from the chat.", delete_after=TIMEOUT)

            else:
                return await ctx.send(content="You have been verified!", delete_after=TIMEOUT)
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
                    return 200

                if all([cached_message is not None, cached_message != message]):
                    cache.pop(f"{self.message.chatId}_{self.message.author.userId}")
                    return 404

                await asyncio.sleep(0.1)

            cache.pop(f"{self.message.chatId}_{self.message.author.userId}")
            return 500


    @_run
    @__typing__
    async def send(self, content: str, delete_after: int= None, mentioned: Union[str, List[str]]= None) -> CMessage:
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
        async def on_text_message(ctx: Context):
            ctx.send(content="Hello World!", delete_after=None)
        ```
        """
        message: CMessage = await self.__send_message__(
            content=content,
            extensions = {
            "mentionedArray": [
            {"uid": self.message.author.userId}
            ] if isinstance(mentioned, str) else [{"uid": i} for i in mentioned
            ] if isinstance(mentioned, list) else None
            })

        self.loop.create_task(self._delete(message, delete_after)) if delete_after else None

        return message


    @_run
    @__typing__
    async def reply(self, content: str, delete_after: int= None, mentioned: Union[str, List[str]]= None) -> CMessage:
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
        async def on_text_message(ctx: Context):
            ctx.reply(content = "Hello World!", delete_after = None)
        ```
        """
        message: CMessage = await self.__send_message__(
            content=content,
            replyMessageId=self.message.messageId,
            extensions = {
                "mentionedArray": [{
                    "uid": self.message.author.userId}] if isinstance(mentioned, str) else [{"uid": i} for i in mentioned] if isinstance(mentioned, list) else None
                    })
        
        self.loop.create_task(self._delete(message, delete_after)) if delete_after else None

        return message


    async def prepare_mentions(self, mentioned: dict) -> list:
        """
        `prepare_mentions` - This prepares the mentions for the message.
        
        `**Parameters**``
        - `mentioned` - `ctx.message.mentioned_dictionary`.
        
        `**Returns**``
        - `list` - The list of mentions to use as your `message`

        `**Example**``
        ```py
        @bot.command("mention")
        async def mention(ctx: Context):
            mentioned_users = ctx.message.mentioned_dictionary
            if not mentioned_users:
                return ctx.reply("You didn't mention anyone!")

            mentioned = ctx.prepare_mentions(mentioned_users)
            return ctx.reply(
                "Mentioned: " + ", ".join(mentioned), mentioned=list(mentioned_users)
            )
        """
        return [f"\u200e\u200f@{mentioned[user_id]}\u202c\u202d" for user_id in mentioned]


    @_run
    @__typing__
    async def send_link_snippet(self, image: str, message: str = "[c]", link: str = "ndc://user-me", mentioned: list = None) -> CMessage:
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
        async def linksnippet(ctx: Context):
            return ctx.send_link_snippet(
                image = "https://i.imgur.com/8ZQZ9Zm.png",
                message = "Hello World!",
                link = "https://www.google.com"
            )
        ```
        """
        mentioned = mentioned or []

        message: CMessage = await self.__send_message__(
            content=message,
            extensions = {
                "linkSnippetList": [{
                "mediaType": 100,
                "mediaUploadValue": await self.encode_media(
                    await self.__handle_media__(media=image, content_type="image/jpg", media_value=False)
                ),
                "mediaUploadValueContentType": "image/png",
                "link": link
                }],
            "mentionedArray": [
            {"uid": self.message.author.userId}
            ] if isinstance(mentioned, str) else [{"uid": i} for i in mentioned
            ] if isinstance(mentioned, list) else None
            })

        return message


    @_run
    @__typing__
    async def send_embed(
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
        async def embed(ctx: Context):
            return ctx.send_embed(
                message = "[c]",
                title = "Hello World!",
                content = "This is an embed.",
                image = "https://i.imgur.com/8ZQZ9Zm.png",
                link = "https://www.google.com"
            )
        ```
        """
        message: CMessage = await self.__send_message__(
            content=message,
            attachedObject = {
                "title": title,
                "content": content,
                "mediaList": [[100, await self.__handle_media__(media=image, media_value=True), None]],
                "link": link
                },
            extensions = {
                "mentionedArray": [
                {"uid": self.message.author.userId}
                ] if isinstance(mentioned, str) else [{"uid": i} for i in mentioned
                ] if isinstance(mentioned, list) else None
            })
        
        return message


    async def __handle_media__(self, media: str, content_type: str = "image/jpg", media_value: bool = False) -> str:
        
        try:
            if media.startswith("http"):
                async with aiohttp.ClientSession() as session:
                    async with session.get(media) as response:
                        media = await response.read()

            else:
                media = open(media, "rb").read()
        except Exception as e:
            raise InvalidImage from e
        
        if content_type == "audio/aac":
            return await self.encode_media(media)

        if media_value:
            return await self.upload_media(media=media, content_type=content_type)

        return media
    

    async def encode_media(self, file: bytes) -> str:
        return b64encode(file).decode()


    async def upload_media(self, media: Union[str, BinaryIO], content_type: str = "image/jpg") -> str:
        return ApiResponse(
            await self.request.handler(
                method = "POST",
                url = "/g/s/media/upload",
                data = media,
                content_type = content_type
            )).mediaValue


    @_run
    @__typing__
    async def send_sticker(self, sticker_id: str) -> CMessage:
        """
        `send_sticker` - This sends a sticker.

        `**Parameters**``
        - `sticker_id` - The sticker ID you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.send_sticker(sticker_id="sticker_id")
        ```
        """
        sticker_id = sticker_id.replace("ndcsticker://", "") if sticker_id.startswith("ndcsticker://") else sticker_id
        message: CMessage = await self.__send_message__(
            type=3,
            stickerId=sticker_id,
            mediaValue=f"ndcsticker://{sticker_id}"
            )
        
        return message


    @_run
    async def send_image(self, image: str) -> CMessage:
        """
        `send_image` - This sends an image.

        `**Parameters**``
        - `image` - The image link or file you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.send_image(image="https://i.imgur.com/image.jpg")
        ```
        """
        message: CMessage = await self.__send_message__(
            mediaType=100,
            mediaUploadValue=await self.encode_media(
                await self.__handle_media__(
                    media=image,
                    content_type="image/jpg",
                    media_value=False
            )))

        return message


    @_run
    async def send_gif(self, gif: str) -> CMessage:
        """
        `send_gif` - This sends a gif.

        `**Parameters**``
        - `gif` - The gif link or file you want to send.

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.send_gif(gif="https://i.imgur.com/image.gif")
        ```
        """
        message: CMessage = await self.__send_message__(
            mediaType=100,
            mediaUploadValueContentType="image/gif",
            mediaUploadValue=await self.encode_media(
                await self.__handle_media__(
                    media=gif,
                    content_type="image/gif",
                    media_value=False
            )))
        
        return message


    @_run
    async def send_audio(self, audio: str) -> CMessage:
        """
        `send_audio` - This sends an audio file.
        
        `**Parameters**``
        - `audio` - The audio link or file you want to send.
        
        `**Returns**`` - CMessage object.
        
        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.send_audio(audio="output.mp3")
        ```
        """
        message: CMessage = await self.__send_message__(
            type=2,
            mediaType=110,
            mediaUploadValue= await self.__handle_media__(
                media=audio,
                content_type="audio/aac",
                media_value=False
            ))

        return message


    @_run
    async def join_chat(self, chatId: str=None) -> ApiResponse:
        """
        `join_chat` - This joins a chat.

        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.join_chat(chatId="0000-0000-0000-0000")
        ```
        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/{self.communityId}/s/chat/thread/{chatId or self.chatId}/member/{self.userId}"
            ))


    @_run
    async def leave_chat(self, chatId: str=None) -> ApiResponse:
        """
        `leave_chat` - This leaves a chat.

        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.leave_chat(chatId="0000-0000-0000-0000")
        ```
        """
        return ApiResponse(self.request.handler(
            method="DELETE",
            url=f"/{self.communityId}/s/chat/thread/{chatId or self.chatId}/member/{self.userId}"
            ))


    @_run
    async def kick(self, userId: str, chatId: str=None) -> ApiResponse:
        """
        `kick` - This kicks a user.

        `**Parameters**``
        - `userId` - The user ID you want to kick.
        - `chatId` - The chat ID you want to kick the user from.

        `**Example**``
        ```py
        @bot.on_text_message()
        async def on_text_message(ctx: Context):
            ctx.kick(userId="0000-0000-0000-0000", chatId="0000-0000-0000-0000")
        ```
        """
        return ApiResponse(await self.request.handler(
            method="DELETE",
            url=f"/{self.communityId}/s/chat/thread/{chatId or self.chatId}/member/{userId}"
            ))
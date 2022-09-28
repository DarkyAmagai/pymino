
from time import time
from typing import Optional
from .objects import Message, User
from .http_client import *

class Context():
    """
    This is an objects class for Context

    `**Example**`
    ```python
    from pymino import Client

    bot = Client("email", "password")

    @bot.command("ping")
    def ping(ctx):
        ctx.send("pong")
    ```
     """
    def __init__(self, message: Message):
        self.sid: Optional[str] = None
        self._message = message


    @property
    def message(self) -> Message:
        """
        `message` is a property that returns the message.

        `**Example**` `>>> Context.message`

        """
        return self._message

    @property
    def author(self) -> User:
        """
        `author` is a property that returns the author.

        `**Example**` `>>> Context.author`

        """
        return self._message.author

    def send(self, content: str)-> Message:
        """
        `send` is a function that sends a message.

        `**Example**` `>>> Context.send()`

        `**Parameters**`
        - `content` - The content to send.

        """

        return Message(httpx_handler().handler(
            method="POST", endpoint=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = {
                "content": content,
                "timestamp": int(time() * 1000),
                "type": 0
            }))


    def reply(self, content: str) -> Message:
        """
        `reply` is a function that replies to a message.

        `**Example**` `>>> Context.reply()`

        `**Parameters**`
        - `content` - The content to send.

        """
        return Message(httpx_handler().handler(
            method="POST", endpoint=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = {
                "content": content,
                "timestamp": int(time() * 1000),
                "type": 0,
                "replyMessageId": self._message.messageId
            }))


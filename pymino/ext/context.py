from .generate import *

class Context():
    """
    `Context` handles messages sent from bot to user.

    `**Object Attributes**`

    - `message` - The message that triggered the command.

    - `author` - The author of the message that triggered the command.

    `**Object Methods**`

    - `reply` - Replies to the message that triggered the command.

    - `send` - Sends a message to the chat that triggered the command.

    - `send_embed` - Sends an embed to the chat that triggered the command.

    """
    def __init__(self, message: Message, session):
        self._message = message
        self._session = session

    @property
    def message(self) -> Message:
        return self._message

    @property
    def author(self) -> User:
        return self._message.author

    def attribute_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AttributeError:
                raise AttributeError(f"Make sure you're using the {func.__name__} method in a command!")
        return wrapper

    @attribute_error
    def reply(self, content: str, delete_after: int= None):
        """
        `**reply**` replies to the message that triggered the command.

        `**Parameters**`

        - `content` - The message to send.

        - `delete_after` - The time in seconds to wait before deleting the message.
        
        `**Example**`

        ```py
        @bot.command("ping")
        def ping(ctx: Context):
            ctx.reply("Pong!")
        ```
        """
        message = Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = {
                "content": content,
                "timestamp": int(time() * 1000),
                "type": 0,
                "replyMessageId": self._message.messageId
            }))
        if delete_after:
            Thread(target=self._delete, args=(message, delete_after)).start()

        return message

    @attribute_error
    def _delete(self, message: Message, delete_after: int = 5):
        if delete_after != 0:
            sleep(delete_after)
        return self._session.handler(
            method="DELETE", url=f"/x{message.comId}/s/chat/thread/{message.chatId}/message/{message.messageId}")

    @attribute_error
    def send(self, content: str, delete_after: int= None):
        """
        `**send**` sends a message to the chat that triggered the command.

        `**Parameters**`

        - `content` - The message to send.

        - `delete_after` - The time in seconds to wait before deleting the message.
        
        `**Example**`

        ```py
        @bot.command("ping")
        def ping(ctx: Context):
            ctx.send("Pong!")
        ```
        """
        message =  Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = {
                "content": content,
                "timestamp": int(time() * 1000),
                "type": 0
            }))
        if delete_after:
            Thread(target=self._delete, args=(message, delete_after)).start()

        return message

    @attribute_error
    def send_embed(self, title: str, content: str, image: str = None, link: Optional[str]=None, delete_after: int= None) -> Message:
        """
        `**send_embed**` sends an embed to the chat that triggered the command.

        `**Parameters**`

        - `title` is the title of the embed.

        - `content` is the message in the embed.

        - `image` must be a url or a path to a file.

        - `link` is the link of the embed.

        - `delete_after` is the time in seconds to wait before deleting the message.

        `**Example**`

        ```py
        @bot.on_member_join()
        def member_join(ctx: Context):
            ctx.send_embed(title="This is a test embed/", content=f"Welcome to the chat {ctx.author.username}!", image="icon.jpg")
        ```
        """
        image = self._prep_image(image)
        message = Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = {
                "type": 0,
                "content": "[c]",
                "clientRefId": int(time() / 10 % 1000000000),
                "attachedObject": {
                    "link": link,
                    "title": title,
                    "content": content,
                    "mediaList": [[100, self.upload_image(image), None]] if image else None
                },
                "extensions": {},
                "timestamp": int(time() * 1000)
                }))
                
        if delete_after:
            Thread(target=self._delete, args=(message, delete_after)).start()

        return message

    @attribute_error
    def upload_image(self, image: Union[str, BinaryIO]) -> str:
        """
        `upload_image` is a function that uploads an image to the server and returns it's link.

        `**Parameters**`

        - `image` - The image to upload.
        """
        image = open(image, "rb") if isinstance(image, str) else image
        return SResponse(self._session.handler(method="POST", url=f"/g/s/media/upload",
            data=image.read(), content_type="image/jpg")).mediaValue

    @attribute_error
    def _prep_image(self, image: str) -> BinaryIO:
        """
        `_prep_image` is a function that prepares an image to be sent.
        
        `**Parameters**`

        - `image` - The image to prepare.
        """
        
        if image.startswith("http"):
            [open("temp.png", "wb").write(get(image).content), image := open("temp.png", "rb")]
        else:
            image = open(image, "rb")

        return image

class EventHandler(Context):
    """
    `EventHandler` is a class that handles events and commands.
    
    `**Example**`
    ```py
    bot = Bot()
    
    @bot.event
    def on_text_message(ctx: Context):
        ctx.reply("Hello World!")
    
    bot.run(email="email", password="password") or bot.run(sid="sid")
        """
    def __init__(self):
        super().__init__(self, self.request)
        self.context = Context
        self._events = {}
        self._commands = {}

    def start_task(self, func):
        """
        `start_task` is a function that starts a task.
        """
        Thread(target=func).start()

    def task(self, interval: int = 10):
        """
        `task` is a function that starts a task.

        The task will be executed every `interval` seconds.
        
        `**Example**`
        ```python
        @bot.task(interval=10)
        def task():
            print("Hello World!")

        #Community task
        @bot.task(interval=10)
        def task2(community: Community):
            send_message(chatId, "Hello World!")
        ```
        """
        def decorator(func):
            def wrapper():
                while True:
                    if len(inspect_signature(func).parameters) == 0:
                        func()
                    else:
                        func(self.community)
                    sleep(interval)
            self.start_task(wrapper)
            return func
        return decorator
        
    def emit(self, name: str, *args):
        """`emit` is a function that emits an event."""
        if name in self._events:
            self._events[name](*args) 
                       
    def command(self, name: str):
        """
        `command` is a function that registers a command.
        
        `**Example**`
        ```python
        @bot.command("hello")
        def hello(ctx: Context):
            ctx.reply("Hello World!")
        ```"""
        def decorator(func):
            self._commands[name] = func
            return func
        return decorator

    def _handle_command(self, data: dict):
        """
        `_handle_command` is a function that handles commands.
        """
        message: Message = Message(data)

        command = message.content.split(" ")[0][len(self.command_prefix):]
        command_length = len(self.command_prefix + message.content.split(" ")[0][1:]) + 1
        arg = message.content[command_length - 1:]

        if command in self._commands:
            if len(inspect_signature(self._commands[command]).parameters) == 1:
                self._commands[command](self.context(message, self.request))
            else:
                self._commands[command](self.context(message, self.request), arg)

    def on_error(self):
        """
        `on_error` is a function that handles errors.
        
        `**Example**`
        ```python
        
        @bot.on_error()`
        def error_handler(error: Exception):`
            print(error)`
        ```
        It is recommended to use this function to handle errors to prevent the bot from crashing.
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["error"] = func
            return func
        return decorator

    def on_ready(self):
        """
        `on_ready` is a function that lets you know when the bot is ready.
        
        `**Example**`
        ```python
        @bot.on_ready()`
        def ready_handler():`
            print("Bot is ready!")`
        ```
        It is useful if you want to know when the bot is ready.
        ```
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["ready"] = func
            return func
        return decorator

    def on_text_message(self):
        """
        `on_text_message` is a function that handles text messages.
        
        `**Example**`
        ```python
        @bot.on_text_message()`
        def text_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["text_message"] = func
            return func
        return decorator

    def on_image_message(self):
        """
        `on_image_message` is a function that handles image messages.
        
        `**Example**`
        ```python
        @bot.on_image_message()`
        def image_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["image_message"] = func
            return func
        return decorator

    def on_youtube_message(self):
        """
        `on_youtube_message` is a function that handles youtube messages.
        
        `**Example**`
        ```python
        @bot.on_youtube_message()`
        def youtube_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["youtube_message"] = func
            return func
        return decorator

    def on_strike_message(self):
        """
        `on_strike_message` is a function that handles strike messages.
        
        `**Example**`
        ```python
        @bot.on_strike_message()`
        def strike_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["strike_message"] = func
            return func
        return decorator

    def on_voice_message(self):
        """
        `on_voice_message` is a function that handles voice messages.
        
        `**Example**`
        ```python
        @bot.on_voice_message()`
        def voice_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["voice_message"] = func
            return func
        return decorator

    def on_sticker_message(self):
        """
        `on_sticker_message` is a function that handles sticker messages.
        
        `**Example**`
        ```python
        @bot.on_sticker_message()`
        def sticker_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["sticker_message"] = func
            return func
        return decorator

    def on_vc_not_answered(self):
        """
        `on_vc_not_answered` is a function that handles voice chat not answered messages.
        
        `**Example**`
        ```python
        @bot.on_vc_not_answered()`
        def vc_not_answered_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_not_answered"] = func
            return func
        return decorator

    def on_vc_not_cancelled(self):
        """
        `on_vc_not_cancelled` is a function that handles voice chat not cancelled messages.
        
        `**Example**`
        ```python
        @bot.on_vc_not_cancelled()`
        def vc_not_cancelled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_not_cancelled"] = func
            return func
        return decorator

    def on_vc_not_declined(self):
        """
        `on_vc_not_declined` is a function that handles voice chat not declined messages.
        
        `**Example**`
        ```python
        @bot.on_vc_not_declined()`
        def vc_not_declined_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_not_declined"] = func
            return func
        return decorator

    def on_video_chat_not_answered(self):
        """
        `on_video_chat_not_answered` is a function that handles video chat not answered messages.
        
        `**Example**`
        ```python
        @bot.on_video_chat_not_answered()`
        def video_chat_not_answered_handler(ctx: Context):`
            print(ctx.message.json)`"""
        def decorator(func):
            self._events["video_chat_not_answered"] = func
            return func
        return decorator

    def on_video_chat_not_cancelled(self):
        """
        `on_video_chat_not_cancelled` is a function that handles video chat not cancelled messages.
        
        `**Example**`
        ```python
        @bot.on_video_chat_not_cancelled()`
        def video_chat_not_cancelled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["video_chat_not_cancelled"] = func
            return func
        return decorator

    def on_video_chat_not_declined(self):
        """
        `on_video_chat_not_declined` is a function that handles video chat not declined messages.
            
        `**Example**`
        ```python
        @bot.on_video_chat_not_declined()`
        def video_chat_not_declined_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["video_chat_not_declined"] = func
            return func
        return decorator

    def on_avatar_chat_not_answered(self):
        """
        `on_avatar_chat_not_answered` is a function that handles avatar chat not answered messages.
        
        `**Example**`
        ```python
        @bot.on_avatar_chat_not_answered()`
        def avatar_chat_not_answered_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["avatar_chat_not_answered"] = func
            return func
        return decorator

    def on_avatar_chat_not_cancelled(self):
        """"
        `on_avatar_chat_not_cancelled` is a function that handles avatar chat not cancelled messages.
        
        `**Example**`
        ```python
        @bot.on_avatar_chat_not_cancelled()`
        def avatar_chat_not_cancelled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["avatar_chat_not_cancelled"] = func
            return func
        return decorator

    def on_avatar_chat_not_declined(self):
        """
        `on_avatar_chat_not_declined` is a function that handles avatar chat not declined messages.
        
        `**Example**`
        ```python
        @bot.on_avatar_chat_not_declined()`
        def avatar_chat_not_declined_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["avatar_chat_not_declined"] = func
            return func
        return decorator

    def on_delete_message(self):
        """
        `on_delete_message` is a function that handles delete messages.
        
        `**Example**`
        ```python
        @bot.on_delete_message()`
        def delete_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["delete_message"] = func
            return func
        return decorator

    def on_member_join(self):
        """
        `on_member_join` is a function that handles member join messages.
        
        `**Example**`
        ```python
        @bot.on_member_join()`
        def member_join_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["member_join"] = func
            return func
        return decorator

    def on_member_leave(self):
        """
        `on_member_leave` is a function that handles member leave messages.
        
        `**Example**`
        ```python
        @bot.on_member_leave()`
        def member_leave_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["member_leave"] = func
            return func
        return decorator

    def on_chat_invite(self):
        """
        `on_chat_invite` is a function that handles chat invite messages.
        
        `**Example**`
        ```python
        @bot.on_chat_invite()`
        def chat_invite_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_invite"] = func
            return func
        return decorator

    def on_chat_background_changed(self):
        """
        `on_chat_background_changed` is a function that handles chat background changed messages.
        
        `**Example**`
        ```python
        @bot.on_chat_background_changed()`
        def chat_background_changed_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_background_changed"] = func
            return func
        return decorator

    def on_chat_title_changed(self):
        """
        `on_chat_title_changed` is a function that handles chat title changed messages.
        
        `**Example**`
        ```python
        @bot.on_chat_title_changed()`
        def chat_title_changed_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_title_changed"] = func
            return func
        return decorator

    def on_chat_icon_changed(self):
        """
        `on_chat_icon_changed` is a function that handles chat icon changed messages.
        
        `**Example**`
        ```python
        @bot.on_chat_icon_changed()`
        def chat_icon_changed_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_icon_changed"] = func
            return func
        return decorator

    def on_vc_start(self):
        """
        `on_vc_start` is a function that handles vc start messages.
        
        `**Example**`
        ```python
        @bot.on_vc_start()`
        def vc_start_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_start"] = func
            return func
        return decorator

    def on_video_chat_start(self):
        """
        `on_video_chat_start` is a function that handles video chat start messages.
        
        `**Example**`
        ```python
        @bot.on_video_chat_start()`
        def video_chat_start_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["video_chat_start"] = func
            return func
        return decorator

    def on_avatar_chat_start(self):
        """
        `on_avatar_chat_start` is a function that handles avatar chat start messages.
        
        `**Example**`
        ```python
        @bot.on_avatar_chat_start()`
        def avatar_chat_start_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["avatar_chat_start"] = func
            return func
        return decorator

    def on_vc_end(self):
        """
        `on_vc_end` is a function that handles vc end messages.
        
        `**Example**`
        ```python
        @bot.on_vc_end()`
        def vc_end_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_end"] = func
            return func
        return decorator

    def on_video_chat_end(self):
        """
        `on_video_chat_end` is a function that handles video chat end messages.
        
        `**Example**`
        ```python
        @bot.on_video_chat_end()`
        def video_chat_end_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["video_chat_end"] = func
            return func
        return decorator

    def on_avatar_chat_end(self):
        """
        `on_avatar_chat_end` is a function that handles avatar chat end messages.
        
        `**Example**`
        ```python
        @bot.on_avatar_chat_end()`
        def avatar_chat_end_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["avatar_chat_end"] = func
            return func
        return decorator

    def on_chat_content_changed(self):
        """
        `on_chat_content_changed` is a function that handles chat content changed messages.
        
        `**Example**`
        ```python
        @bot.on_chat_content_changed()`
        def chat_content_changed_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_content_changed"] = func
            return func
        return decorator

    def on_screen_room_start(self):
        """
        `on_screen_room_start` is a function that handles screen room start messages.
        
        `**Example**`
        ```python
        @bot.on_screen_room_start()`
        def screen_room_start_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["screen_room_start"] = func
            return func
        return decorator

    def on_screen_room_end(self):
        """
        `on_screen_room_end` is a function that handles screen room end messages.
        
        `**Example**`
        ```python
        @bot.on_screen_room_end()`
        def screen_room_end_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["screen_room_end"] = func
            return func
        return decorator

    def on_chat_host_transfered(self):
        """
        `on_chat_host_transfered` is a function that handles chat host transfered messages.
        
        `**Example**`
        ```python
        @bot.on_chat_host_transfered()`
        def chat_host_transfered_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_host_transfered"] = func
            return func
        return decorator

    def on_text_message_force_removed(self):
        """
        `on_text_message_force_removed` is a function that handles text message force removed messages.
        
        `**Example**`
        ```python
        @bot.on_text_message_force_removed()`
        def text_message_force_removed_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["text_message_force_removed"] = func
            return func
        return decorator

    def on_chat_removed_message(self):
        """
        `on_chat_removed_message` is a function that handles chat removed messages.
        
        `**Example**`
        ```python
        @bot.on_chat_removed_message()`
        def chat_removed_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_removed_message"] = func
            return func
        return decorator

    def on_mod_deleted_message(self):
        """
        `on_mod_deleted_message` is a function that handles mod deleted messages.
        
        `**Example**`
        ```python
        @bot.on_mod_deleted_message()`
        def mod_deleted_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["mod_deleted_message"] = func
            return func
        return decorator

    def on_chat_tip(self):
        """
        `on_chat_tip` is a function that handles chat tip messages.
        
        `**Example**`
        ```python
        @bot.on_chat_tip()`
        def chat_tip_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_tip"] = func
            return func
        return decorator

    def on_chat_pin_announcement(self):
        """
        `on_chat_pin_announcement` is a function that handles chat pin announcement messages.
            
        `**Example**`
        ```python
        @bot.on_chat_pin_announcement()`
        def chat_pin_announcement_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_pin_announcement"] = func
            return func
        return decorator

    def on_vc_permission_open_to_everyone(self):
        """
        `on_vc_permission_open_to_everyone` is a function that handles vc permission open to everyone messages.
        
        `**Example**`
        ```python
        @bot.on_vc_permission_open_to_everyone()`
        def vc_permission_open_to_everyone_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_permission_open_to_everyone"] = func
            return func
        return decorator

    def on_vc_permission_invited_and_requested(self):
        """
        `on_vc_permission_invited_and_requested` is a function that handles vc permission invited and requested messages.
        
        `**Example**`
        ```python
        @bot.on_vc_permission_invited_and_requested()`
        def vc_permission_invited_and_requested_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_permission_invited_and_requested"] = func
            return func
        return decorator

    def on_vc_permission_invite_only(self):
        """
        `on_vc_permission_invite_only` is a function that handles vc permission invite only messages.
        
        `**Example**`
        ```python
        @bot.on_vc_permission_invite_only()`
        def vc_permission_invite_only_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["vc_permission_invite_only"] = func
            return func
        return decorator

    def on_chat_view_only_enabled(self):
        """
        `on_chat_view_only_enabled` is a function that handles chat view only enabled messages.
        
        `**Example**`
        ```python
        @bot.on_chat_view_only_enabled()`
        def chat_view_only_enabled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_view_only_enabled"] = func
            return func
        return decorator

    def on_chat_view_only_disabled(self):
        """
        `on_chat_view_only_disabled` is a function that handles chat view only disabled messages.
        
        `**Example**`
        ```python
        @bot.on_chat_view_only_disabled()`
        def chat_view_only_disabled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_view_only_disabled"] = func
            return func
        return decorator

    def on_chat_unpin_announcement(self):
        """
        `on_chat_unpin_announcement` is a function that handles chat unpin announcement messages.
        
        `**Example**`
        ```python
        @bot.on_chat_unpin_announcement()`
        def chat_unpin_announcement_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_unpin_announcement"] = func
            return func
        return decorator

    def on_chat_tipping_enabled(self):
        """
        `on_chat_tipping_enabled` is a function that handles chat tipping enabled messages.
        
        `**Example**`
        ```python
        @bot.on_chat_tipping_enabled()`
        def chat_tipping_enabled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_tipping_enabled"] = func
            return func
        return decorator

    def on_chat_tipping_disabled(self):
        """
        `on_chat_tipping_disabled` is a function that handles chat tipping disabled messages.
        
        `**Example**`
        ```python
        @bot.on_chat_tipping_disabled()`
        def chat_tipping_disabled_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["chat_tipping_disabled"] = func
            return func
        return decorator

    def on_timestamp_message(self):
        """
        `on_timestamp_message` is a function that handles timestamp messages.
        
        `**Example**`
        ```python
        @bot.on_timestamp_message()`
        def timestamp_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["timestamp_message"] = func
            return func
        return decorator

    def on_welcome_message(self):
        """
        `on_welcome_message` is a function that handles welcome messages.
        
        `**Example**`
        ```python
        @bot.on_welcome_message()`
        def welcome_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["welcome_message"] = func
            return func
        return decorator

    def on_invite_message(self):
        """
        `on_invite_message` is a function that handles invite messages.
        
        `**Example**`
        ```python
        @bot.on_invite_message()`
        def invite_message_handler(ctx: Context):`
            print(ctx.message.json)`
        ```

        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        """
        def decorator(func):
            self._events["invite_message"] = func
            return func
        return decorator

    def on_user_online(self):
        """
        `on_user_online` is a function that notifies when a user goes online in the specified community.

        `**Example**`
        ```python
        @bot.on_user_online()
        def user_online_handler(ctx: Context):
            print(ctx.message.json)
        ```
        `**Returns**`
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.
        """
        def decorator(func):
            self._events["user_online"] = func
            return func
        return decorator

    def key_error(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except KeyError:
                return None
        return wrapper
        
    @key_error
    def _handle_event(self, event: str, data: dict):
        """
        `_handle_event` is a function that handles events.
        
        `**Example**`
        ```python
        @bot._handle_event("text_message")
        def text_message_handler(ctx: Context):
            print(ctx.message.json)
        ```"""
        if event == "text_message":
            self._events["text_message"](self.context(data, self.request))
        elif event == "image_message":
            self._events["image_message"](self.context(data, self.request))
        elif event == "youtube_message":
            self._events["youtube_message"](self.context(data, self.request))
        elif event == "strike_message":
            self._events["strike_message"](self.context(data, self.request))
        elif event == "voice_message":
            self._events["voice_message"](self.context(data, self.request))
        elif event == "sticker_message":
            self._events["sticker_message"](self.context(data, self.request))
        elif event == "vc_not_answered":
            self._events["vc_not_answered"](self.context(data, self.request))
        elif event == "vc_not_cancelled":
            self._events["vc_not_cancelled"](self.context(data, self.request))
        elif event == "vc_not_declined":
            self._events["vc_not_declined"](self.context(data, self.request))
        elif event == "video_chat_not_answered":
            self._events["video_chat_not_answered"](self.context(data, self.request))
        elif event == "video_chat_not_cancelled":
            self._events["video_chat_not_cancelled"](self.context(data, self.request))
        elif event == "video_chat_not_declined":
            self._events["video_chat_not_declined"](self.context(data, self.request))
        elif event == "avatar_chat_not_answered":
            self._events["avatar_chat_not_answered"](self.context(data, self.request))
        elif event == "avatar_chat_not_cancelled":
            self._events["avatar_chat_not_cancelled"](self.context(data, self.request))
        elif event == "avatar_chat_not_declined":
            self._events["avatar_chat_not_declined"](self.context(data, self.request))
        elif event == "delete_message":
            self._events["delete_message"](self.context(data, self.request))
        elif event == "member_join":
            self._events["member_join"](self.context(data, self.request))
        elif event == "member_leave":
            self._events["member_leave"](self.context(data, self.request))
        elif event == "chat_invite":
            self._events["chat_invite"](self.context(data, self.request))
        elif event == "chat_background_changed":
            self._events["chat_background_changed"](self.context(data, self.request))
        elif event == "chat_title_changed":
            self._events["chat_title_changed"](self.context(data, self.request))
        elif event == "chat_icon_changed":
            self._events["chat_icon_changed"](self.context(data, self.request))
        elif event == "vc_start":
            self._events["vc_start"](self.context(data, self.request))
        elif event == "video_chat_start":
            self._events["video_chat_start"](self.context(data, self.request))
        elif event == "avatar_chat_start":
            self._events["avatar_chat_start"](self.context(data, self.request))
        elif event == "vc_end":
            self._events["vc_end"](self.context(data, self.request))
        elif event == "video_chat_end":
            self._events["video_chat_end"](self.context(data, self.request))
        elif event == "avatar_chat_end":
            self._events["avatar_chat_end"](self.context(data, self.request))
        elif event == "chat_content_changed":
            self._events["chat_content_changed"](self.context(data, self.request))
        elif event == "screen_room_start":
            self._events["screen_room_start"](self.context(data, self.request))
        elif event == "screen_room_end":
            self._events["screen_room_end"](self.context(data, self.request))
        elif event == "chat_host_transfered":
            self._events["chat_host_transfered"](self.context(data, self.request))
        elif event == "text_message_force_removed":
            self._events["text_message_force_removed"](self.context(data, self.request))
        elif event == "chat_removed_message":
            self._events["chat_removed_message"](self.context(data, self.request))
        elif event == "mod_deleted_message":
            self._events["mod_deleted_message"](self.context(data, self.request))
        elif event == "chat_tip":
            self._events["chat_tip"](self.context(data, self.request))
        elif event == "chat_pin_announcement":
            self._events["chat_pin_announcement"](self.context(data, self.request))
        elif event == "vc_permission_open_to_everyone":
            self._events["vc_permission_open_to_everyone"](self.context(data, self.request))
        elif event == "vc_permission_invited_and_requested":
            self._events["vc_permission_invited_and_requested"](self.context(data, self.request))
        elif event == "vc_permission_invite_only":
            self._events["vc_permission_invite_only"](self.context(data, self.request))
        elif event == "chat_view_only_enabled":
            self._events["chat_view_only_enabled"](self.context(data, self.request))
        elif event == "chat_view_only_disabled":
            self._events["chat_view_only_disabled"](self.context(data, self.request))
        elif event == "chat_unpin_announcement":
            self._events["chat_unpin_announcement"](self.context(data, self.request))
        elif event == "chat_tipping_enabled":
            self._events["chat_tipping_enabled"](self.context(data, self.request))
        elif event == "chat_tipping_disabled":
            self._events["chat_tipping_disabled"](self.context(data, self.request))
        elif event == "timestamp_message":
            self._events["timestamp_message"](self.context(data, self.request))
        elif event == "welcome_message":
            self._events["welcome_message"](self.context(data, self.request))
        elif event == "invite_message":
            self._events["invite_message"](self.context(data, self.request))
        elif event == "user_online":
            self._events["user_online"](User(data))
        


        

    




    
from .utilities.generate import *

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

    def run(func):
        def wrapper(*args, **kwargs):
            try:

                if args[0].__class__.__name__ != "Context":
                    raise Exception(
                        f"You must use this method as ctx.{func.__name__} not bot.{func.__name__}"
                        )
                else:
                    return Thread(target=func, args=args, kwargs=kwargs).start()

            except (AttributeError, TypeError):
                raise Exception(f"Make sure you're using the {func.__name__} method in a command!")

        return wrapper

    def _delete(self, message: Message, delete_after: int = 5):
        if delete_after != 0:
            wait(delete_after)
        return self._session.handler(
            method="DELETE", url=f"/x{message.comId}/s/chat/thread/{message.chatId}/message/{message.messageId}")

    def upload_image(self, image: Union[str, BinaryIO]) -> str:
        """
        `upload_image` is a function that uploads an image to the server and returns it's link.

        `**Parameters**`

        - `image` - The image to upload.
        """
        image = open(image, "rb") if isinstance(image, str) else image
        return SResponse(self._session.handler(method="POST", url=f"/g/s/media/upload",
            data=image.read(), content_type="image/jpg")).mediaValue

    def _prep_file(self, file: str, mediaValue: bool=True) -> BinaryIO:
        """
        `_prep_file` is a function that prepares an file to be sent.
        
        `**Parameters**`

        - `file` - The file to prepare.
        """
        if file.startswith("http"):
            file = BytesIO(get(file).content)
        else:
            file = open(file, "rb")

        if not mediaValue: return file

        file = self.upload_image(file)
        
        return file

    @run
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
            data = PrepareMessage(content=content, replyMessageId=self.message.messageId).reply_message
            ))

        if delete_after:
            Thread(target=self._delete, args=(message, delete_after)).start()

        return message

    @run
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
            data = PrepareMessage(content=content).base_message))

        if delete_after:
            Thread(target=self._delete, args=(message, delete_after)).start()

        return message

    @run
    def send_embed(self, title: str, content: str, image: str, link: Optional[str]=None) -> Message:
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
        return Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = PrepareMessage(content="[c]",
            attachedObject={
                "title": title,
                "content": content,
                "mediaList": [[100, self._prep_file(image), None]],
                "link": link
                }).embed_message))

    @run
    def send_image(self, image: str):
        """
        `**send_image**` sends an image to the chat that triggered the command.
        
        `**Parameters**`
        
        - `image` must be a url or a path to a file.
        
        `**Example**`
        
        ```py
        @bot.command("image")
        def image(ctx: Context):
            ctx.send_image("image.jpg")
        ```
        """
        return Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = PrepareMessage(image=b64encode((self._prep_file(image, False)).read()).decode()).image_message))

    @run
    def send_gif(self, gif: str):
        """
        `**send_gif**` sends a gif to the chat that triggered the command.
        
        `**Parameters**`
        
        - `gif` must be a url or a path to a file.
        
        `**Example**`
        
        ```py
        @bot.command("gif")
        def gif(ctx: Context):
            ctx.send_gif("jiffyyyy.gif")
        ```
        """
        return Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = PrepareMessage(gif=b64encode((self._prep_file(gif, False)).read()).decode()).gif_message))

    @run
    def send_audio(self, audio: str) -> Message: #NOTE: Not sure how long the audio can be.
        """
        `**send_audio**` sends an audio file to the chat that triggered the command.
        
        `**Parameters**`
        
        - `audio` must be a url or a path to a file.
        
        `**Example**`
        
        ```py
        @bot.command("audio")
        def audio(ctx: Context):
            ctx.send_audio("audio.mp3")
        ```
        """
        return Message(self._session.handler(
            method="POST", url=f"/x{self._message.comId}/s/chat/thread/{self._message.chatId}/message",
            data = PrepareMessage(audio=b64encode((self._prep_file(audio, False)).read()).decode()).audio_message))


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
                    wait(interval)
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
        
        `**Parameters**`
        
        - `name` is the name of the command.
        
        `**Example**`
        ```py
        # Simple no parameter function
        @bot.command("hello")
        def hello(ctx: Context):
            ctx.reply("Hello World!")
        
        # Function with parameters
        @bot.command("hello")
        def hello(ctx: Context, message: str, username: str, userId: str):
            ctx.reply(f"Hello {username}! You said {message}!")
        ```
        """
        def decorator(func):
            self._commands[name] = func
            return func
        return decorator

    def _handle_command(self, data: dict):
        """`_handle_command` is a function that handles commands."""
        message: Message = Message(data)
        potential_parameters = {
            "ctx": self.context(message, self.request),
            "message": message.content[2:],
            "username": message.author.username,
            "userId": message.author.userId
        }
        command_name = message.content[len(self.command_prefix):].split(" ")[0]
        if command_name in self._commands:
            command = self._commands[command_name]
            parameters = []
            for parameter in inspect_signature(command).parameters:
                if parameter in potential_parameters:
                    parameters.append(potential_parameters[parameter])

            return command(*parameters)

        return self.emit("text_message", self.context(message, self.request))

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
        `on_text_message` is a function that handles all chat messages the bot receives while connected to the websocket.
        
        `**Parameters**`
        
        - `ctx` - The context of the message.

        `**ctx attributes**`
        - `ctx.message` - The message.
        - `ctx.author` - The author of the message.

        `print(ctx.message.json)` to see the raw message.

        `**Example**`
        ```python
        # Simple no parameter function
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.reply("Hello World!")

        # Function with parameters
        @bot.on_text_message()
        def on_text_message(ctx: Context, message: str, username: str, userId: str):
            ctx.reply(f"Hello {username}! You said {message}!")
            print(userId)
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                if any([ctx.message.content.startswith(x) for x in self.command_prefix]):
                    command_name = ctx.message.content.split(" ")[0][len(self.command_prefix):]
                else:
                    command_name = None
                
                potential_parameters = {
                    "ctx": ctx,
                    "message": ctx.message.content[len(command_name) + len(self.command_prefix) + 1:] if command_name else ctx.message.content,
                    "username": ctx.author.username,
                    "userId": ctx.author.userId
                }
                parameters = []
                for parameter in inspect_signature(func).parameters:
                    parameters.append(potential_parameters.get(parameter, None))
                func(*parameters)
            self._events["text_message"] = wrapper
            return func
        return decorator

    def on_image_message(self):
        """
        `on_image_message` is a function that handles all image messages the bot receives while connected to the websocket.

        `**Parameters**`

        - `ctx` allows you to access the message content and take actions on it.

            - `ctx.message` is a `Message` object.

            - `ctx.author` is a `User` object.

        - `image` is the link of the image.

        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_image_message()
        def on_image_message(ctx: Context):
            ctx.reply("Received image!")

        # Function with parameters
        @bot.on_image_message()
        def on_image_message(ctx: Context, image: str):
            print(image) # Prints the image link to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                potential_parameters = {
                    "ctx": ctx,
                    "image": ctx.message.mediaValue
                }
                parameters = []
                for parameter in inspect_signature(func).parameters:
                    parameters.append(potential_parameters.get(parameter, None))
                func(*parameters)
            self._events["image_message"] = wrapper
            return func
        return decorator

    def on_youtube_message(self):
        """
        `on_youtube_message` is a function that handles all youtube messages the bot receives while connected to the websocket.

        `**Parameters**`

        - `ctx` allows you to access the message content and take actions on it.

            - `ctx.message` is a `Message` object.

            - `ctx.author` is a `User` object.

        - `title` is the title of the youtube video.

        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_youtube_message()
        def on_youtube_message(ctx: Context):
            ctx.reply("Received youtube video!")

        # Function with parameters
        @bot.on_youtube_message()
        def on_youtube_message(ctx: Context, title: str):
            print(title) # Prints the youtube video title to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                potential_parameters = {
                    "ctx": ctx,
                    "title": ctx.message.content
                }
                parameters = []
                for parameter in inspect_signature(func).parameters:
                    parameters.append(potential_parameters.get(parameter, None))
                func(*parameters)
            self._events["youtube_message"] = wrapper
            return func

    def on_strike_message(self):
        """
        `on_strike_message` is a function that handles all strike messages the bot receives while connected to the websocket.
        """
        def decorator(func):
            self._events["strike_message"] = func
            return func
        return decorator

    def on_voice_message(self):
        """
        `on_voice_message` is a function that handles all voice messages the bot receives while connected to the websocket.
        
        `**Parameters**`
        
        - `ctx` allows you to access the message content and take actions on it.
        
            - `ctx.message` is a `Message` object.
            
            - `ctx.author` is a `User` object.
            
            - `voice` is the link of the voice message.
            
        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_voice_message()
        def on_voice_message(ctx: Context):
            ctx.reply("Received voice message!")

        # Function with parameters
        @bot.on_voice_message()
        def on_voice_message(ctx: Context, voice: str):
            print(voice) # Prints the voice message link to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                inspect = len(inspect_signature(func).parameters)
                if inspect > 2:
                    return None
                elif inspect > 1:
                    func(ctx, ctx.message.mediaValue)
                else:
                    func(ctx)
            self._events["voice_message"] = wrapper
            return func
        return decorator

    def on_sticker_message(self):
        """
        `on_sticker_message` is a function that handles all sticker messages the bot receives while connected to the websocket.

        `**Parameters**`

        - `ctx` allows you to access the message content and take actions on it.

            - `ctx.message` is a `Message` object.

            - `ctx.author` is a `User` object.

        - `sticker` is the id of the sticker.

        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_sticker_message()
        def on_sticker_message(ctx: Context):
            ctx.reply("Received sticker!")

        # Function with parameters
        @bot.on_sticker_message()
        def on_sticker_message(ctx: Context, sticker: str):
            print(sticker) # Prints the sticker id to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                inspect = len(inspect_signature(func).parameters)
                if inspect > 2:
                    return None
                elif inspect > 1:
                    func(ctx, ctx.message.mediaValue.split("://")[1])
                else:
                    func(ctx)
            self._events["sticker_message"] = wrapper
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
        `on_delete_message` is a function that handles all deleted messages the bot receives while connected to the websocket.

        `**Parameters**`

        - `ctx` allows you to access the message content and take actions on it.

            - `ctx.message` is a `Message` object.

            - `ctx.author` is a `User` object.

        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_delete_message()
        def on_delete_message(ctx: Context):
            ctx.reply("Message deleted!")

        # Function with parameters
        @bot.on_delete_message()
        def on_delete_message(ctx: Context, messageId: str):
            print(messageId) # Prints the message id to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                inspect = len(inspect_signature(func).parameters)
                if inspect > 2:
                    return None
                elif inspect > 1:
                    func(ctx, ctx.message.messageId)
                else:
                    func(ctx)
            self._events["delete_message"] = wrapper
            return func
        return decorator

    def on_member_join(self):
        """
        `on_member_join` is a function that handles all member join messages the bot receives while connected to the websocket.

        `**Parameters**`

        - `ctx` allows you to access the message content and take actions on it.
        
            - `ctx.message` is a `Message` object.

            - `ctx.author` is a `User` object.

        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_member_join()
        def on_member_join(ctx: Context):
            ctx.send("Welcome to the chat {ctx.author.username}!")

        # Function with parameters
        @bot.on_member_join()
        def on_member_join(ctx: Context, username: str, userId: str):
            print(username) # Prints the username to the console.
            print(userId) # Prints the user id to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                potential_parameters = {
                    "ctx": ctx,
                    "username": ctx.author.username,
                    "userId": ctx.author.userId
                }
                parameters = []
                for parameter in inspect_signature(func).parameters:
                    parameters.append(potential_parameters.get(parameter, None))
                func(*parameters)
            self._events["member_join"] = wrapper
            return func
        return decorator

    def on_member_leave(self):
        """
        `on_member_leave` is a function that handles all member leave messages the bot receives while connected to the websocket.

        `**Parameters**`

        - `ctx` allows you to access the message content and take actions on it.

            - `ctx.message` is a `Message` object.

            - `ctx.author` is a `User` object.

        `**Example**`
        ```py
        # Simple no parameter function
        @bot.on_member_leave()
        def on_member_leave(ctx: Context):
            ctx.send("Goodbye {ctx.author.username}!")

        # Function with parameters
        @bot.on_member_leave()
        def on_member_leave(ctx: Context, username: str, userId: str):
            print(username) # Prints the username to the console.
            print(userId) # Prints the user id to the console.
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                potential_parameters = {
                    "ctx": ctx,
                    "username": ctx.author.username,
                    "userId": ctx.author.userId
                }
                parameters = []
                for parameter in inspect_signature(func).parameters:
                    parameters.append(potential_parameters.get(parameter, None))
                func(*parameters)
            self._events["member_leave"] = wrapper
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
            if not data.content.startswith(self.command_prefix):
                return self._events["text_message"](self.context(data, self.request))
            return self._handle_command(data.json)
        elif event == "image_message":
            return self._events["image_message"](self.context(data, self.request))
        elif event == "youtube_message":
            return self._events["youtube_message"](self.context(data, self.request))
        elif event == "strike_message":
            return self._events["strike_message"](self.context(data, self.request))
        elif event == "voice_message":
            return self._events["voice_message"](self.context(data, self.request))
        elif event == "sticker_message":
            return self._events["sticker_message"](self.context(data, self.request))
        elif event == "vc_not_answered":
            return self._events["vc_not_answered"](self.context(data, self.request))
        elif event == "vc_not_cancelled":
            return self._events["vc_not_cancelled"](self.context(data, self.request))
        elif event == "vc_not_declined":
            return self._events["vc_not_declined"](self.context(data, self.request))
        elif event == "video_chat_not_answered":
            return self._events["video_chat_not_answered"](self.context(data, self.request))
        elif event == "video_chat_not_cancelled":
            return self._events["video_chat_not_cancelled"](self.context(data, self.request))
        elif event == "video_chat_not_declined":
            return self._events["video_chat_not_declined"](self.context(data, self.request))
        elif event == "avatar_chat_not_answered":
            return self._events["avatar_chat_not_answered"](self.context(data, self.request))
        elif event == "avatar_chat_not_cancelled":
            return self._events["avatar_chat_not_cancelled"](self.context(data, self.request))
        elif event == "avatar_chat_not_declined":
            return self._events["avatar_chat_not_declined"](self.context(data, self.request))
        elif event == "delete_message":
            return self._events["delete_message"](self.context(data, self.request))
        elif event == "member_join":
            return self._events["member_join"](self.context(data, self.request))
        elif event == "member_leave":
            return self._events["member_leave"](self.context(data, self.request))
        elif event == "chat_invite":
            return self._events["chat_invite"](self.context(data, self.request))
        elif event == "chat_background_changed":
            return self._events["chat_background_changed"](self.context(data, self.request))
        elif event == "chat_title_changed":
            return self._events["chat_title_changed"](self.context(data, self.request))
        elif event == "chat_icon_changed":
            return self._events["chat_icon_changed"](self.context(data, self.request))
        elif event == "vc_start":
            return self._events["vc_start"](self.context(data, self.request))
        elif event == "video_chat_start":
            return self._events["video_chat_start"](self.context(data, self.request))
        elif event == "avatar_chat_start":
            return self._events["avatar_chat_start"](self.context(data, self.request))
        elif event == "vc_end":
            return self._events["vc_end"](self.context(data, self.request))
        elif event == "video_chat_end":
            return self._events["video_chat_end"](self.context(data, self.request))
        elif event == "avatar_chat_end":
            return self._events["avatar_chat_end"](self.context(data, self.request))
        elif event == "chat_content_changed":
            return self._events["chat_content_changed"](self.context(data, self.request))
        elif event == "screen_room_start":
            return self._events["screen_room_start"](self.context(data, self.request))
        elif event == "screen_room_end":
            return self._events["screen_room_end"](self.context(data, self.request))
        elif event == "chat_host_transfered":
            return self._events["chat_host_transfered"](self.context(data, self.request))
        elif event == "text_message_force_removed":
            return self._events["text_message_force_removed"](self.context(data, self.request))
        elif event == "chat_removed_message":
            return self._events["chat_removed_message"](self.context(data, self.request))
        elif event == "mod_deleted_message":
            return self._events["mod_deleted_message"](self.context(data, self.request))
        elif event == "chat_tip":
            return self._events["chat_tip"](self.context(data, self.request))
        elif event == "chat_pin_announcement":
            return self._events["chat_pin_announcement"](self.context(data, self.request))
        elif event == "vc_permission_open_to_everyone":
            return self._events["vc_permission_open_to_everyone"](self.context(data, self.request))
        elif event == "vc_permission_invited_and_requested":
            return self._events["vc_permission_invited_and_requested"](self.context(data, self.request))
        elif event == "vc_permission_invite_only":
            return self._events["vc_permission_invite_only"](self.context(data, self.request))
        elif event == "chat_view_only_enabled":
            return self._events["chat_view_only_enabled"](self.context(data, self.request))
        elif event == "chat_view_only_disabled":
            return self._events["chat_view_only_disabled"](self.context(data, self.request))
        elif event == "chat_unpin_announcement":
            return self._events["chat_unpin_announcement"](self.context(data, self.request))
        elif event == "chat_tipping_enabled":
            return self._events["chat_tipping_enabled"](self.context(data, self.request))
        elif event == "chat_tipping_disabled":
            return self._events["chat_tipping_disabled"](self.context(data, self.request))
        elif event == "timestamp_message":
            return self._events["timestamp_message"](self.context(data, self.request))
        elif event == "welcome_message":
            return self._events["welcome_message"](self.context(data, self.request))
        elif event == "invite_message":
            return self._events["invite_message"](self.context(data, self.request))
        elif event == "user_online":
            return self._events["user_online"](User(data))
        


        

    




    
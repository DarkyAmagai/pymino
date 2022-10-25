from .utilities.generate import *

class Context():
    """
    `Context` - This handles the event context.

    `**Parameters**``
    - `message` - The message which triggered the event.
    - `session` - The session we will use to send requests.

    """
    def __init__(self, message: Message, session):
        self.message: Message = message
        self._session = session
    
    @property
    def author(self) -> MessageAuthor:
        """The author of the message."""
        return self.message.author
    
    def _run(func):
        def wrapper(*args, **kwargs):
                if isinstance(args[0], Context):
                    with suppress(Exception): return func(*args, **kwargs)
        return wrapper

    def _delete(self, delete_message: CMessage, delete_after: int = 5):
        """
        `delete` - Deletes a message.
        
        `**Parameters**`
        - `delete_message` - The message to delete.
        - `delete_after` - The time to wait before deleting the message.
        
        """
        wait(delete_after)
        return self._session.handler(
            method = "DELETE",
            url = f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message/{delete_message.messageId}",
            wait = False)

    def _upload_image(self, image: Union[str, BinaryIO]) -> str:
        """
        `upload_image` - Uploads an image to the server.
        
        `**Parameters**`
        - `image` - The image to upload.
        
        `**Returns**`
        - `str` - The image URL.
        """
        return ApiResponse(self._session.handler(
            method = "POST",
            url = f"/g/s/media/upload",
            data = (open(image, "rb") if isinstance(image, str) else image).read(),
            content_type = "image/jpg"
            )).mediaValue

    def _prep_file(self, file: str, mediaValue: bool=True) -> BinaryIO:
        """
        `prep_file` - Prepares a file to be uploaded.
        
        `**Parameters**`
        - `file` - The file to prepare.
        - `mediaValue` - Whether to upload file and fetch mediaValue.

        `**Returns**`
        - `BinaryIO` - The binary file.
        """
        file = BytesIO(get(file).content) if file.startswith("http") else open(file, "rb")
        return self._upload_image(file) if mediaValue else file

    @_run
    def reply(self, content: str, delete_after: int= None) -> None:
        """
        `reply` - This replies to the message.

        `**Parameters**``
        - `content` - The message you want to send.
        - `delete_after` - The time in seconds before the message is deleted. [Optional]

        `**Returns**`` - None

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.reply(content = "Hello World!", delete_after = None)
        ```
        """
        message = self._session.handler(
            method="POST",
            url=f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message",
            data = PrepareMessage(content=content, replyMessageId=self.message.messageId).json(), 
            wait = True if delete_after else False)

        return self._delete(CMessage(message), delete_after) if delete_after else None

    @_run
    def send(self, content: str, delete_after: int= None) -> None:
        """
        `send` - This sends a message.

        `**Parameters**``
        - `content` - The message you want to send.
        - `delete_after` - The time in seconds before the message is deleted. [Optional]

        `**Returns**`` - None

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send(content="Hello World!", delete_after=None)
        ```
        """
        message =  self._session.handler(
            method="POST",
            url=f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message",
            data = PrepareMessage(content=content).json(),
            wait = True if delete_after is not None else False)

        return self._delete(CMessage(message), delete_after) if delete_after else None

    @_run
    def send_embed(self, message: str, embed_title: str, embed_content: str, embed_image: str, embed_link: Optional[str]=None) -> None:
        """
        `send_embed` - This sends an embed.

        `**Parameters**``
        - `message` - The message you want to send.
        - `embed_title` - The title of the embed.
        - `embed_content` - The content of the embed.
        - `embed_image` - The image link or image file.
        - `embed_link` - The link of the embed. [Optional]

        `**Returns**`` - None

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_embed(
                message="This is an embed!",
                embed_title="Embed Title",
                embed_content="Embed Content",
                embed_image="https://i.imgur.com/image.png",
                embed_link="ndc://user-me"
                )
        ```
        """
        return self._session.handler(
            method = "POST", url = f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message",
            data = PrepareMessage(content = message, attachedObject = {
                "title": embed_title,
                "content": embed_content,
                "mediaList": [[100, self._prep_file(embed_image), None]],
                "link": embed_link}).json(), wait = False)

    @_run
    def send_image(self, image: str) -> None:
        """
        `send_image` - This sends an image.

        `**Parameters**``
        - `image` - The image link or file you want to send.

        `**Returns**`` - None

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_image(image="https://i.imgur.com/image.jpg")
        ```
        """
        return self._session.handler(
            method = "POST",
            url = f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message",
            data = PrepareMessage(
                mediaType = 100,
                mediaUploadValue=b64encode((self._prep_file(image, False)).read()).decode(),
                mediaUploadValueContentType = "image/jpg",
                mediaUhqEnabled = True).json(), wait=False)

    @_run
    def send_gif(self, gif: str) -> None:
        """
        `send_gif` - This sends a gif.

        `**Parameters**``
        - `gif` - The gif link or file you want to send.

        `**Returns**`` - None

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_gif(gif="https://i.imgur.com/image.gif")
        ```
        """
        return self._session.handler(
            method="POST",
            url=f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message",
            data = PrepareMessage(
                mediaType = 100,
                mediaUploadValue=b64encode((self._prep_file(gif, False)).read()).decode(),
                mediaUploadValueContentType = "image/gif",
                mediaUhqEnabled = True).json(), wait=False)

    @_run
    def send_audio(self, audio: str) -> None:
        """
        `send_audio` - This sends an audio file.
        
        `**Parameters**``
        - `audio` - The audio link or file you want to send.
        
        `**Returns**`` - None
        
        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send_audio(audio="output.mp3")
        ```
        """
        return self._session.handler(
            method="POST",
            url=f"/x{self.message.comId}/s/chat/thread/{self.message.chatId}/message",
            data = PrepareMessage(type=2, mediaType=110, mediaUploadValue=b64encode((self._prep_file(audio, False)).read()).decode()).json(), wait=False)

class EventHandler(Context):
    """
    `EventHandler` - AKA where all the events are handled.

    `**Parameters**``
    - `session` - The session we are using.

    """
    def __init__(self):
        super().__init__(self, self.request)
        self.command_prefix:    str = self.command_prefix
        self.context:           Context = Context
        self._events:           dict = {}
        self._commands:         dict = {}

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
            else: func(self.community)
            wait(interval)
            
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
                
    def emit(self, name: str, *args):
        """`emit` is a function that emits an event."""
        if name in self._events:
            self._events[name](*args) 
                       
    def command(self, command_name: str):
        """
        `command` - This creates a command.
        
        `**Parameters**``
        - `command_name` - The name of the command.
        
        `**Example**``
        ```py
        @bot.command(command_name="ping")
        def ping(ctx: Context):
            ctx.send(content="Pong!")
        ```
        """
        def decorator(func):
            self._commands[command_name] = func
            return func
        return decorator

    def _handle_command(self, data: Message):
        """`_handle_command` is a function that handles commands."""
        command_name = data.content[len(self.command_prefix):].split(" ")[0]
        parameters = []
        pparameters = {
            "ctx": self.context(data, self.request),
            "message": data.content[len(self.command_prefix) + len(command_name) + 1:],
            "username": data.author.username,
            "userId": data.author.userId
        }
        if command_name in self._commands:
            command = self._commands[command_name]
            
            for parameter in inspect_signature(command).parameters:
                if parameter in pparameters:
                    parameters.append(pparameters[parameter])

            return command(*parameters)

        return self._handle_text_message(data)

    def on_error(self):
        """
        `on_error` - This is an event that handles errors to prevent the bot from crashing.
        
        `**Example**``
        ```py
        @bot.on_error()
        def on_error(error: Exception):
            print(error)
        ```
        """
        def decorator(func):
            self._events["error"] = func
            return func
        return decorator

    def on_ready(self):
        """
        `on_ready` - This is an event that is called when the bot is ready.

        `**Example**``
        ```py
        @bot.on_ready()
        def on_ready():
            print(f"Logged in as {bot.profile.username}")
        ```
        """
        def decorator(func):
            self._events["ready"] = func
            return func
        return decorator

    def on_text_message(self):
        """
        `on_text_message` - This is an event that is called when a text message is received.

        `**Example**``
        ```py
        # Basic usage.
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send(content="Hello World!")

        # Parameter usage.
        @bot.on_text_message()
        def on_text_message(ctx: Context, message: str, username: str, userId: str):
            ctx.send(content=f"{username} said {message}")
            print(userId)
        ```
        """
        def decorator(func):
            self._events["text_message"] = func
            return func
        return decorator

    def _handle_text_message(self, data: Message):
        """`_handle_text_message` is a function that handles text messages."""

        ctx: Context = self.context(data, self.request)
        if data.content.startswith(self.command_prefix):
            command_name = data.content.split(" ")[0][len(self.command_prefix):]
        else: command_name = None

        parameters = []
        pparameters = {
            "ctx": ctx,
            "command": self.command_prefix + command_name if command_name != None else "Command not found",
            "message": ctx.message.content[len(command_name) + len(self.command_prefix) + 1:] if command_name else ctx.message.content,
            "username": ctx.author.username,
            "userId": ctx.author.userId
        }
        
        for parameter in inspect_signature(self._events["text_message"]).parameters:
            if parameter in pparameters:
                parameters.append(pparameters[parameter])

        return self._events["text_message"](*parameters)

    def on_image_message(self):
        """
        `on_image_message` - This is an event that is called when an image message is received.
        
        `**Example**``
        ```py
        # This will send the image back to the chat.
        @bot.on_image_message()
        def on_image_message(ctx: Context, image: str):
            ctx.send_image(image=image)
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                parameters = []
                pparameters = {"ctx": ctx, "image": ctx.message.mediaValue}
                for parameter in inspect_signature(func).parameters:
                    parameters.append(pparameters.get(parameter, None))
                func(*parameters)
            self._events["image_message"] = wrapper
            return func
        return decorator
        
    def on_youtube_message(self):
        """
        `on_youtube_message` - This is an event that is called when a YouTube video message is received.

        `**Example**``
        ```py
        # This will print the youtube title in the console.
        @bot.on_youtube_message()
        def on_youtube_message(ctx: Context, title: str):
            print(title)
        ```
        """
        def decorator(func):
            def wrapper(ctx: Context):
                parameters = []
                pparameters = {"ctx": ctx, "title": ctx.message.content}
                for parameter in inspect_signature(func).parameters:
                    parameters.append(pparameters.get(parameter, None))
                func(*parameters)
            self._events["youtube_message"] = wrapper
            return func
        return decorator

    def on_strike_message(self):
        def decorator(func):
            self._events["strike_message"] = func
            return func
        return decorator

    def on_voice_message(self):
        """
        `on_voice_message` - This is an event that is called when a voice message is received.
        
        `**Example**``
        ```py
        # This will send the audio message back to the chat.
        @bot.on_voice_message()
        def on_voice_message(ctx: Context, audio: str):
            ctx.send_audio(audio=audio)
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
        def decorator(func):
            self._events["vc_not_answered"] = func
            return func
        return decorator

    def on_vc_not_cancelled(self):
        def decorator(func):
            self._events["vc_not_cancelled"] = func
            return func
        return decorator

    def on_vc_not_declined(self):
        def decorator(func):
            self._events["vc_not_declined"] = func
            return func
        return decorator

    def on_video_chat_not_answered(self):
        def decorator(func):
            self._events["video_chat_not_answered"] = func
            return func
        return decorator

    def on_video_chat_not_cancelled(self):
        def decorator(func):
            self._events["video_chat_not_cancelled"] = func
            return func
        return decorator

    def on_video_chat_not_declined(self):
        def decorator(func):
            self._events["video_chat_not_declined"] = func
            return func
        return decorator

    def on_avatar_chat_not_answered(self):
        def decorator(func):
            self._events["avatar_chat_not_answered"] = func
            return func
        return decorator

    def on_avatar_chat_not_cancelled(self):
        def decorator(func):
            self._events["avatar_chat_not_cancelled"] = func
            return func
        return decorator

    def on_avatar_chat_not_declined(self):
        def decorator(func):
            self._events["avatar_chat_not_declined"] = func
            return func
        return decorator

    def on_delete_message(self):
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
        def decorator(func):
            self._events["chat_invite"] = func
            return func
        return decorator

    def on_chat_background_changed(self):
        def decorator(func):
            self._events["chat_background_changed"] = func
            return func
        return decorator

    def on_chat_title_changed(self):
        def decorator(func):
            self._events["chat_title_changed"] = func
            return func
        return decorator

    def on_chat_icon_changed(self):
        def decorator(func):
            self._events["chat_icon_changed"] = func
            return func
        return decorator

    def on_vc_start(self):
        def decorator(func):
            self._events["vc_start"] = func
            return func
        return decorator

    def on_video_chat_start(self):
        def decorator(func):
            self._events["video_chat_start"] = func
            return func
        return decorator

    def on_avatar_chat_start(self):
        def decorator(func):
            self._events["avatar_chat_start"] = func
            return func
        return decorator

    def on_vc_end(self):
        def decorator(func):
            self._events["vc_end"] = func
            return func
        return decorator

    def on_video_chat_end(self):
        def decorator(func):
            self._events["video_chat_end"] = func
            return func
        return decorator

    def on_avatar_chat_end(self):
        def decorator(func):
            self._events["avatar_chat_end"] = func
            return func
        return decorator

    def on_chat_content_changed(self):
        def decorator(func):
            self._events["chat_content_changed"] = func
            return func
        return decorator

    def on_screen_room_start(self):
        def decorator(func):
            self._events["screen_room_start"] = func
            return func
        return decorator

    def on_screen_room_end(self):
        def decorator(func):
            self._events["screen_room_end"] = func
            return func
        return decorator

    def on_chat_host_transfered(self):
        def decorator(func):
            self._events["chat_host_transfered"] = func
            return func
        return decorator

    def on_text_message_force_removed(self):
        def decorator(func):
            self._events["text_message_force_removed"] = func
            return func
        return decorator

    def on_chat_removed_message(self):
        def decorator(func):
            self._events["chat_removed_message"] = func
            return func
        return decorator

    def on_mod_deleted_message(self):
        def decorator(func):
            self._events["mod_deleted_message"] = func
            return func
        return decorator

    def on_chat_tip(self):
        def decorator(func):
            self._events["chat_tip"] = func
            return func
        return decorator

    def on_chat_pin_announcement(self):
        def decorator(func):
            self._events["chat_pin_announcement"] = func
            return func
        return decorator

    def on_vc_permission_open_to_everyone(self):
        def decorator(func):
            self._events["vc_permission_open_to_everyone"] = func
            return func
        return decorator

    def on_vc_permission_invited_and_requested(self):
        def decorator(func):
            self._events["vc_permission_invited_and_requested"] = func
            return func
        return decorator

    def on_vc_permission_invite_only(self):
        def decorator(func):
            self._events["vc_permission_invite_only"] = func
            return func
        return decorator

    def on_chat_view_only_enabled(self):
        def decorator(func):
            self._events["chat_view_only_enabled"] = func
            return func
        return decorator

    def on_chat_view_only_disabled(self):
        def decorator(func):
            self._events["chat_view_only_disabled"] = func
            return func
        return decorator

    def on_chat_unpin_announcement(self):
        def decorator(func):
            self._events["chat_unpin_announcement"] = func
            return func
        return decorator

    def on_chat_tipping_enabled(self):
        def decorator(func):
            self._events["chat_tipping_enabled"] = func
            return func
        return decorator

    def on_chat_tipping_disabled(self):
        def decorator(func):
            self._events["chat_tipping_disabled"] = func
            return func
        return decorator

    def on_timestamp_message(self):
        def decorator(func):
            self._events["timestamp_message"] = func
            return func
        return decorator

    def on_welcome_message(self):
        def decorator(func):
            self._events["welcome_message"] = func
            return func
        return decorator

    def on_invite_message(self):
        def decorator(func):
            self._events["invite_message"] = func
            return func
        return decorator

    def on_user_online(self):
        def decorator(func):
            self._events["user_online"] = func
            return func
        return decorator

    def _handle_event(self, event: str, data: Message):
        if event == "text_message":
            return self._handle_command(data)

        elif event == "user_online":
            return self._events["user_online"](OnlineMembers(data.json()))

        elif any([event != "text_message", event != "user_online"]):
            with suppress(KeyError):
                return self._events[event](self.context(data, self.request))
        

from .utilities.generate import *
from .utilities.commands import *

class Context():
    """
    `Context` - This handles the event context.

    `**Parameters**``
    - `message` - The message which triggered the event.
    - `session` - The session we will use to send requests.

    """
    def __init__(self, message: Message, session, session_login: bool=False):
        self.message:       Message = message
        self.userId:        str = session.userId
        self.request        = session
        self.session_login: bool = session_login

    @property
    def author(self) -> MessageAuthor:
        """The author of the message."""
        with suppress(AttributeError): return self.message.author

    @property
    def communityId(self) -> str:
        """Sets the url to community/global."""
        if all([self.message.comId == 0, not self.session_login]): return "g"
        return f"x{self.message.comId}"

    @property
    def chatId(self) -> str:
        """The chat ID."""
        return self.message.chatId

    @property
    def default(self) -> str:
        return "https://aminoapps.com/api"

    @property
    def service(self) -> str:
        return "https://service.aminoapps.com/api/v1"

    @property
    def api(self) -> str:
        return self.default if self.session_login else self.service

    @property
    def __message_endpoint__(self) -> str:
        return f"{self.api}/add-chat-message" if self.session_login else f"/{self.communityId}/s/chat/thread/{self.message.chatId}/message"

    def _run(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
                if isinstance(args[0], Context):
                    with suppress(Exception): return func(*args, **kwargs)
        return wrapper

    def __purge__(self, data: dict) -> dict:
        return {k: v for k, v in data.items() if v is not None}

    def __prepare_message__(self, **kwargs) -> dict:
        return self.__purge__(self.__parse_kwargs__(**kwargs))    
    
    def __read_image__(self, image: Union[str, BinaryIO]) -> BinaryIO:
        return open(image, "rb").read() if isinstance(image, str) else image.read()

    def __parse_kwargs__(self, **kwargs) -> dict:
        return {
            "content": kwargs.get("content"),
            "type": kwargs.get("type"),
            "mediaType": kwargs.get("mediaType"),
            "mediaValue": kwargs.get("mediaValue"),
            "mediaUploadValue": kwargs.get("mediaUploadValue"),
            "stickerId": kwargs.get("stickerId"),
            "attachedObject": kwargs.get("attachedObject"),
            "uid": self.userId,
            "sendFailed": False if self.session_login else None
            } 

    def __message__(self, **kwargs) -> dict:
        return {
            "ndcId": self.communityId,
            "threadId": self.message.chatId,
            "message": PrepareMessage(**kwargs).json()
            } if self.session_login else PrepareMessage(**kwargs).json()

    def __send_message__(self, **kwargs) -> CMessage:
        return CMessage(self.request.handler(
            method = "POST",
            url = self.__message_endpoint__,
            data = self.__message__(**kwargs)
            ))

    def _delete(
        self,
        delete_message: CMessage,
        delete_after: int = 5
        ) -> ApiResponse:
        """
        `delete` - Deletes a message.
        
        `**Parameters**`
        - `delete_message` - The message to delete.
        - `delete_after` - The time to wait before deleting the message.
        
        """
        wait(delete_after)
        return ApiResponse(self.request.handler(
            method = "DELETE",
            url = f"/{self.communityId}/s/chat/thread/{self.message.chatId}/message/{delete_message.messageId}"
            ))

    def __prep_file__(
        self,
        file: str,
        mediaValue: bool=True,
        content_type: str="image/jpg"
        ) -> BinaryIO:
        if all([mediaValue, file.startswith("http://pm1.narvii.com")]): return file
        file = BytesIO(get(file).content) if file.startswith("http") else open(file, "rb")
        return self.upload_image(file, content_type) if mediaValue else file

    def upload_image(
        self,
        image: Union[str, BinaryIO],
        content_type: str="image/jpg"
        ) -> str:
        """
        `upload_image` - Uploads an image to the server.
        
        `**Parameters**`
        - `image` - The image to upload.
        
        `**Returns**`
        - `str` - The image URL.
        """
        return ApiResponse(self.request.handler(
            method = "POST",
            url = f"{self.default}/upload-image" if self.session_login else "/g/s/media/upload",
            data = self.__read_image__(image),
            content_type = "multipart/form-data" if self.session_login else content_type
            )).mediaValue

    @_run
    def send(
        self,
        content: str,
        delete_after: int= None
        ) -> CMessage:
        """
        `send` - This sends a message.

        `**Parameters**``
        - `content` - The message you want to send.
        - `delete_after` - The time in seconds before the message is deleted. [Optional]

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.send(content="Hello World!", delete_after=None)
        ```
        """
        message: CMessage = self.__send_message__(content=content)
        if delete_after: self._delete(message, delete_after)
        return message

    @_run
    def reply(
        self,
        content: str,
        delete_after: int= None
        ) -> CMessage:
        """
        `reply` - This replies to the message.

        `**Parameters**``
        - `content` - The message you want to send.
        - `delete_after` - The time in seconds before the message is deleted. [Optional]

        `**Returns**`` - CMessage object.

        `**Example**``
        ```py
        @bot.on_text_message()
        def on_text_message(ctx: Context):
            ctx.reply(content = "Hello World!", delete_after = None)
        ```
        """
        message: CMessage = self.__send_message__(content=content, replyMessageId=self.message.messageId)
        if delete_after: self._delete(message, delete_after)
        return message

    @_run
    def send_embed(
        self,
        message: str,
        embed_title: str,
        embed_content: str,
        embed_image: str,
        embed_link: Optional[str]=None
        ) -> CMessage:
        """
        `send_embed` - This sends an embed.

        `**Parameters**``
        - `message` - The message you want to send.
        - `embed_title` - The title of the embed.
        - `embed_content` - The content of the embed.
        - `embed_image` - The image link or image file.
        - `embed_link` - The link of the embed. [Optional]

        `**Returns**`` - CMessage object.

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
        return CMessage(
            self.__send_message__(
                content=message,
                attachedObject={
                    "title": embed_title,
                    "content": embed_content,
                    "mediaList": [[100, self.__prep_file__(embed_image), None]],
                    "link": embed_link
                    }
                ))

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
        return CMessage(
            self.__send_message__(mediaType=100, mediaUploadValue=b64encode((self.__prep_file__(image, False)).read()).decode()))

    @_run
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
        sticker_link = f"ndcsticker://{sticker_id}"
        return CMessage(self.__send_message__(type=3, stickerId=sticker_id, mediaValue=sticker_link))

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
        return CMessage(self.__send_message__(mediaType=100, mediaValue=self.__prep_file__(gif, content_type="image/gif")))

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
        return CMessage(self.__send_message__(type=2, mediaType=110, mediaUploadValue=b64encode((self.__prep_file__(audio, False)).read()).decode()))

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
        chatId = chatId or self.chatId
        if self.session_login:
            url = f"{self.api}/join-thread"
            data={"ndcId": self.communityId, "threadId": chatId}
        else:
            url = f"/{self.communityId}/s/chat/thread/{chatId}/member/{self.userId}"
            data=None

        return ApiResponse(self.request.handler(
            method="POST",
            url=url,
            data=data
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
        chatId = chatId or self.chatId
        if self.session_login:
            method = "POST"
            url = f"{self.api}/leave-thread"
            data={"ndcId": self.communityId, "threadId": chatId}
        else:
            method="DELETE"
            url = f"/{self.communityId}/s/chat/thread/{chatId}/member/{self.userId}"
            data=None

        return ApiResponse(self.request.handler(
            method=method,
            url=url,
            data=data
            ))

class EventHandler(Context):
    """
    `EventHandler` - AKA where all the events are handled.

    `**Parameters**``
    - `session` - The session we are using.

    """
    def __init__(self):
        self.command_prefix:    str = self.command_prefix
        self._events:           dict = {}
        self._commands:         Commands = Commands()
        super().__init__(self, self.request, self.session_login)

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

    def command(self, command_name: str, command_description: str=None, aliases: list=[], cooldown: int=0) -> Callable:
        """
        `command` - This creates a command.
        
        `**Parameters**``
        - `command_name` - The name of the command.
        - `command_description` - The description of the command.
        - `aliases` - The other names the command can be called by.
        - `cooldown` - The cooldown of the command in seconds.
        
        `**Example**``
        ```py
        @bot.command(command_name="ping")
        def ping(ctx: Context):
            ctx.send(content="Pong!")

        @bot.command(command_name="ping", aliases=["alive", "test"])
        def ping(ctx: Context):
            # This command can be called by "ping", "alive", and "test".
            ctx.send(content="Pong!")

        @bot.command(command_name="ping", cooldown=5)
        def ping(ctx: Context):
            # This command can only be called every 5 seconds.
            ctx.send(content="Pong!")
        ```
        """
        def decorator(func: Callable) -> Callable:
            self._commands.add_command(Command(func, command_name, command_description=command_description, aliases=aliases, cooldown=cooldown))
            return func
        return decorator

    def command_exists(self, command_name: str) -> bool:
        """
        `command_exists` - This checks if a command exists.
        
        `**Parameters**``
        - `command_name` - The name of the command.
        
        `**Returns**`` - bool
        """
        return any([
            command_name in self._commands.__command_names__(),
            command_name in self._commands.__command_aliases__()
            ])

    def fetch_command(self, command_name: str) -> Command:
        """
        `fetch_command` - This fetches a command.
        
        `**Parameters**``
        - `command_name` - The name of the command.
        
        `**Returns**`` - Command
        """
        return self._commands.fetch_command(command_name)

    def _handle_command(self, data: Message):
        """`_handle_command` is a function that handles commands."""
        command_name = data.content[len(self.command_prefix):].split(" ")[0]

        if self.command_exists(command_name) != True:
            if command_name == "help":
                return Context(data, self.request, self.session_login).reply(self._commands.__help__())
            elif "text_message" in self._events:
                return self._handle_text_message(data)
            else:
                return None

        parameters = [{
            "ctx": Context(data, self.request, self.session_login),
            "message": data.content[len(self.command_prefix) + len(command_name) + 1:],
            "username": data.author.username,
            "userId": data.author.userId
        }.get(i) for i in inspect_signature(self.fetch_command(command_name).func).parameters]

        command_name = dict(self._commands.__command_aliases__().copy()).get(command_name, command_name)  

        if self._commands.fetch_command(command_name).cooldown > 0:
            if self._commands.fetch_cooldown(command_name, data.author.userId) > time():
                return Context(data, self.request, self.session_login).reply(f"You are on cooldown for {int(self._commands.fetch_cooldown(command_name, data.author.userId) - time())} seconds.")
            self._commands.set_cooldown(command_name, self._commands.fetch_command(command_name).cooldown, data.author.userId)

        return self._commands.fetch_command(command_name).func(*parameters)
        
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

        ctx: Context = Context(data, self.request, self.session_login)
        
        if data.content.startswith(self.command_prefix):
            command_name = data.content.split(" ")[0][len(self.command_prefix):]
        else:
            command_name = None

        parameters = [{
            "ctx": ctx,
            "command": self.command_prefix + command_name if command_name != None else "Command not found",
            "message": ctx.message.content[len(command_name) + len(self.command_prefix) + 1:] if command_name else ctx.message.content,
            "username": ctx.author.username,
            "userId": ctx.author.userId
        }.get(i) for i in inspect_signature(self._events["text_message"]).parameters]

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
            self._events["member_leave"] = func
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
                return self._events[event](Context(data, self.request, self.session_login))
        
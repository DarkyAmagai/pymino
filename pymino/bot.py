from time import time
from ujson import loads
from base64 import b64decode
from functools import reduce
from colorama import Fore, Style
from typing import Optional, Union

from .ext.socket import WSClient
from .ext.account import Account
from .ext.community import Community
from .ext.utilities.generate import device_id
from .ext.entities.userprofile import UserProfile
from .ext.entities.handlers import check_debugger
from .ext.utilities.request_handler import RequestHandler
from .ext.entities.general import ApiResponse, CCommunity
from .ext.entities.exceptions import (
    LoginFailed, MissingEmailPasswordOrSid, VerifyCommunityIdIsCorrect
    )

class Bot(WSClient):
    """
    `Bot` - This is the main client.

    `**Parameters**``
    - `command_prefix` - The prefix to use for commands. `Defaults` to `!`.
    - `community_id` - The community id to use for the bot. `Defaults` to `None`.
    - `**kwargs` - Any other parameters to use for the bot.

        - `device_id` - The device id to use for the bot.

        - `proxy` - The proxy to use for the bot. `proxy` must be `str`.

        - `disable_socket` - Whether to disable the socket.

    ----------------------------
    When should I use `Bot` instead of `Client`?

    - If you want to create a bot that responds to commands or events.
    - `Client` does not respond to commands or events.

    ----------------------------

    How do I login to my bot account?

    - You can login to your bot account by using the `run` method.

    ----------------------------

    How do I use the `run` method?
    
    - It's simple! Just use the `run` method like this:

        ```py
        bot = Bot()
        #NOTE: Keep in mind bot.run() should be the last line of your code.
        bot.run(email="email", password="password")
        ```

    ----------------------------
    How do I login to my bot account with a proxy?

    - It's as easy as adding a `proxy` parameter to the `bot` class.

        ```py
        bot = Bot(proxy="http://username:password@ip:port")

        bot.run(email="email", password="password")
        ```
    ----------------------------
    How do I know if my bot is ready?

    - You can check if your bot is ready by using the `is_ready` attribute.
    - `is_ready` is a `bool` that is `True` if the bot is ready and `False` if the bot is not ready.
    - Alternatively, you can use the `on_ready` event.
    - `on_ready` is an event that is called when the bot is ready.

    ----------------------------
    How do I use the `on_ready` event?

    - You can use the `ready` event like this:

        ```py
        bot = Bot()

        @bot.on("on_ready")
        def on_ready():
            print(f"Logged in as {bot.profile.username}(bot.profile.userId)")

        bot.run(email="email", password="password")
        ```
    ----------------------------
    How do I use the is_ready attribute?

    - You can use the `is_ready` attribute like this:

        ```py
        bot = Bot()

        bot.run(email="email", password="password")

        if bot.is_ready:
            print(f"Logged in as {bot.profile.username}(bot.profile.userId)")

        ```
    ----------------------------
    How do I set the community id for my bot?

    - If you know the community id, you can use the `set_community_id` method to set the community id for your bot.
    - Alternatively, if you do not know the community id, you can use the `fetch_community_id` method to get the community id from the community's link.

    ----------------------------
    How do I use the `set_community_id` method?

    - You can use the `set_community_id` method like this:

        ```py
        bot = Bot()

        bot.run(email="email", password="password")
        bot.set_community_id(community_id=123456789)
        ```
    ----------------------------
    How do I use the `fetch_community_id` method?

    - You can use the `fetch_community_id` method like this:

        ```py
        bot = Bot()

        bot.run(email="email", password="password")
        bot.fetch_community_id(community_link="https://aminoapps.com/c/OnePiece")
        ```
    ----------------------------
    Ok, I'm ready to make my first bot! What do I do now?
    - You can start by making a `command`.
    - They are functions that are called when a user sends a message that starts with the `command_prefix`.
    - You can make a command like this:

        ```py
        from pymino import Bot
        from pymino.ext import *

        bot = Bot()

        @bot.command(command_name="ping")
        def ping_command(ctx: Context):
            ctx.send("Pong!")

        bot.run(email="email", password="password")
        ```
    ----------------------------
    What is my command prefix?
    - Your command prefix by default is `!`.
    - You can change your command prefix by using the `command_prefix` parameter in the `Bot` class.
    - You can change your command prefix like this:

        ```py
        bot = Bot(command_prefix=".")
        # Now your command prefix is "." instead of "!".
        ```
    ----------------------------
    Can I use multiple names for my command?
    - Yes! You can use multiple names for your command by using the `aliases` parameter in the `command` decorator.
    - You can use multiple names for your command like this:

        ```py
        from pymino import Bot
        from pymino.ext import *

        bot = Bot()
        #NOTE: This will register the command as "ping", "p", and "pong".
        # Meaning the command will be called if the message starts with "!ping", "!p", or "!pong".
        @bot.command(command_name="ping", aliases=["p", "pong"])
        def ping_command(ctx: Context):
            ctx.send("Pong!")

        bot.run(email="email", password="password")
        ```
    ----------------------------
    How about cooldowns? Can I use them?
    - Yes! You can use cooldowns for your commands by using the `cooldown` parameter in the `command` decorator.
    - You can use cooldowns like this:

        ```py
        from pymino import Bot
        from pymino.ext import *

        bot = Bot()
        #NOTE: This will set the cooldown for the command to 5 seconds.
        # The cooldown is user based, meaning that each user will have their own cooldown.
        @bot.command(command_name="ping", cooldown=5)
        def ping_command(ctx: Context):
            ctx.send("Pong!")

        bot.run(email="email", password="password")
        ```
    ----------------------------
    Is there a help command built in?
    - Yes! There is a built in help command that you can use.
    - It will return a list of all the commands that the bot has and their descriptions.
    
    How do I set the description for my command?
    - You can set the description for your command by using the `command_description` parameter in the `command` decorator.
    - You can set the description for your command like this:

        ```py
        from pymino import Bot
        from pymino.ext import *

        bot = Bot()
        # This way when the user uses the help command, it will return the description for the command.
        @bot.command(command_name="ping", command_description="This command will return pong.")
        def ping_command(ctx: Context):
            ctx.send("Pong!")

        bot.run(email="email", password="password")
        ```
    """
    def __init__(self, command_prefix: Optional[str] = "!", community_id: Union[str, int] = None, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.debug:             bool = check_debugger()
        self.is_ready:          bool = False
        self.userId:            str = None
        self.command_prefix:    Optional[str] = command_prefix
        self.community_id:      Union[str, int] = community_id
        self.device_id:         Optional[str] = kwargs.get("device_id") or device_id()
        self.request:           RequestHandler = RequestHandler(
                                bot = self,
                                proxy=kwargs.get("proxy")
                                )
        self.community:         Community = Community(
                                bot = self,
                                session=self.request,
                                community_id=self.community_id
                                )
        self.account:           Account = Account(
                                session=self.request
                                )

        if self.community_id:   self.set_community_id(community_id)

        WSClient.__init__(self, bot=self)


    def authenticate(self, email: str, password: str, device_id: str = None) -> dict:
        """
        `authenticate` - authenticates the bot.

        [This is used internally.]

        `**Parameters**`
        - `email` - The email to use to login.
        - `password` - The password to use to login.
        - `device_id` - The device id to use to login. `Defaults` to `None`.

        """
        return ApiResponse(self.request.handler(
            method="POST",
            url = "/g/s/auth/login",
            data = {
                "secret": f"0 {password}",
                "clientType": 100,
                "systemPushEnabled": 0,
                "timestamp": int(time() * 1000),
                "locale": "en_US",
                "action": "normal",
                "bundleID": "com.narvii.master",
                "timezone": -480,
                "deviceID": device_id or self.device_id,
                "email": email,
                "v": 2,
                "clientCallbackURL": "narviiapp://default"
                }
            )).json()

    def fetch_account(self) -> dict:
        """
        `fetch_account` - fetches the account of the bot to verify the sid is valid.

        [This is used internally.]

        `**Parameters**`
        - `None`

        `**Returns**`
        - `dict` - The response from the request.

        """
        self.profile: UserProfile = UserProfile(self.request.handler(method="GET", url=f"/g/s/user-profile/{self.userId}"))
        return ApiResponse(self.request.handler(method="GET", url="/g/s/account")).json()

    def run(self, email: str=None, password: str=None, sid: str=None, device_id: str=None) -> None:
        """
        `run` - runs the bot.

        `**Parameters**`
        - `email` - The email to use to login. Defaults to `None`.
        - `password` - The password to use to login. Defaults to `None`.
        - `sid` - The sid to use to login. Defaults to `None`.
        - `device_id` - The device id to use to login. Defaults to `None`.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()

        bot.run(email="email", password="password")
        ```
        """
        if email and password:

            for key, value in {"email": email, "password": password}.items():
                setattr(self.request, key, value)

            response: dict = self.authenticate(email=email, password=password, device_id=device_id)

        elif sid:
            self.sid:               str = sid
            self.request.sid:       str = self.sid
            self.userId:            str = loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())["2"]
            response:               dict = self.fetch_account()

        else:
            raise MissingEmailPasswordOrSid

        if response:
            return self.__run__(response, sid)
        else:
            raise LoginFailed

    def __run__(self, response: dict, sid: str) -> Union[None, Exception]:
        if response["api:statuscode"] != 0: input(response), exit()

        if not hasattr(self, "profile"): 
            self.profile:       UserProfile = UserProfile(response)

        self.sid:               str = sid or response['sid']
        self.userId:            str = self.profile.userId
        self.community.userId:  str = self.userId
        self.request.sid:       str = self.sid
        self.request.userId:    str = self.userId

        if all([not self.is_ready, not hasattr(self, "disable_socket") or not self.disable_socket]):
            self.is_ready = True
            self.connect()

        if self.debug:
            print(f"{Fore.MAGENTA}Logged in as {self.profile.username} ({self.profile.userId}){Style.RESET_ALL}")

        return response

    def fetch_community_id(self, community_link: str, set_community_id: Optional[bool] = True) -> int:
        """
        `fetch_community_id` - fetches the community id from a community link.

        `**Parameters**`
        - `community_link` - The community link to fetch the community id from.
        - `set_community_id` - Whether or not to set the community id. Defaults to `True`.

        `**Returns**`
        - `int` - The community id.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()

        bot.fetch_community_id("https://aminoapps.com/c/CommunityName")
        ```
        """
        community_id = CCommunity(self.request.handler(
            method="GET", url=f"/g/s/link-resolution?q={community_link}")
            ).comId

        if set_community_id:
            self.set_community_id(community_id)

        return community_id

    def set_community_id(self, community_id: Union[str, int]) -> int:
        """
        `set_community_id` - sets the community id.

        `**Parameters**`
        - `community_id` - The community id to set.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()

        bot.set_community_id(123456789)
        ```
        """
        try:
            if community_id is not None and not isinstance(community_id, int):
                community_id = int(community_id)
        except VerifyCommunityIdIsCorrect as e:
            raise VerifyCommunityIdIsCorrect from e

        self.community_id = community_id
        self.community.community_id = community_id

        return community_id
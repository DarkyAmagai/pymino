from time import time
from base64 import b64decode
from functools import reduce
from colorama import Fore, Style
from typing import Optional, Union
from requests import Session as HTTPClient

from .ext.entities import *
from .ext.utilities import *
from .ext.socket import WSClient
from .ext import Community, RequestHandler, Account

if orjson_exists():
    from orjson import loads
else:
    from json import loads

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

    `**Example**``
    ```python
    from pymino import Bot

    bot = Bot(
        command_prefix="!",
        community_id="1234567890"
        )

    bot.run(sid="sid")
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
        self.session:           HTTPClient = HTTPClient()
        self.request:           RequestHandler = RequestHandler(
                                bot = self,
                                session=self.session,
                                proxy=kwargs.get("proxy", None)
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


    def authenticate(self, email: str, password: str) -> dict:
        """
        `authenticate` - authenticates the bot.

        [This is used internally.]

        `**Parameters**`
        - `email` - The email to use to login.
        - `password` - The password to use to login.
        """
        return ApiResponse(self.request.handler(
            method="POST", url = "/g/s/auth/login",
            data = {
                "email": email,
                "v": 2,
                "secret": f"0 {password}",
                "deviceID": self.device_id,
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
            })).json()

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

    def run(self, email: str=None, password: str=None, sid: str=None) -> None:
        """
        `run` - runs the bot.

        `**Parameters**`
        - `email` - The email to use to login. Defaults to `None`.
        - `password` - The password to use to login. Defaults to `None`.
        - `sid` - The sid to use to login. Defaults to `None`.

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

            response: dict = self.authenticate(email, password)

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
    
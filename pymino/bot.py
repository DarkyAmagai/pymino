from .ext.utilities.generate import *
from .ext import Community, RequestHandler, Account, Global
from .ext.socket import WSClient

class Bot(WSClient):
    """
    `Bot` - This is the main client.

    `**Parameters**``
    - `command_prefix` - The prefix to use for commands. Defaults to `!`.
    - `community_id` - The community id to use for the bot. Defaults to `None`.
    - `**kwargs` - Any other parameters to use for the bot.

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
        self.is_ready:          bool = False
        self.command_prefix:    Optional[str] = command_prefix
        self.community_id:      Union[str, int] = community_id
        self.device_id:         Optional[str] = kwargs.get("device_id", None)
        self.session:           ClientSession = ClientSession(
                                headers={
                                "NDCLANG": "en",
                                "ACCEPT-LANGUAGE": "en-US",
                                "CONTENT-TYPE": "application/json; charset=utf-8",
                                "USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/LYZ28N; com.narvii.amino.master/3.5.34654)",
                                "HOST": "service.aminoapps.com",
                                "CONNECTION": "Keep-Alive",
                                "ACCEPT-ENCODING": "gzip"
                                })
        self.request:           RequestHandler = RequestHandler(
                                bot = self,
                                session=self.session,
                                proxy=kwargs.get("proxy", None),
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

        WSClient.__init__(self, client=self)


    def authenticate(self, email: str, password: str):
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
                "secret": "0 {}".format(password),
                "deviceID": self.device_id if self.device_id else device_id(),
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
            })).json()

    def fetch_account(self):
        """
        `fetch_account` - fetches the account of the bot to verify the sid is valid.

        [This is used internally.]

        `**Parameters**`
        - `None`

        `**Returns**`
        - `dict` - The response from the request.

        """
        return ApiResponse(self.request.handler(method="GET", url="/g/s/account")).json()

    def run(self, email: str=None, password: str=None, sid: str=None):
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

            response = self.authenticate(email, password)

        elif sid:
            self.session.headers.update({"NDCAUTH": f"sid={sid}"})
            response = self.fetch_account()
        else:
            raise Exception("You're missing either an email and password or a sid.")

        if response:
            if response['api:statuscode'] != 0: input(response), exit()
            
            self.profile:           UserProfile = UserProfile(response)

            self.sid:               str = sid if sid else response['sid']
            self.userId:            str = response["account"]['uid']
            self.community.userId:  str = self.userId
            self.session.headers.update({"NDCAUTH": f"sid={self.sid}", "AUID": self.userId})

            if not self.is_ready:
                self.is_ready = True
            if not hasattr(self, "disable_socket") or not self.disable_socket:
                self.connect()

            return response
        else:
            raise Exception("Failed to authenticate.")

    def fetch_community_id(self, community_link: str, set_community_id: Optional[bool] = True):
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
        community_id = LinkInfo(self.request.handler(
            method="GET", url=f"/g/s/link-resolution?q={community_link}")
            ).comId

        if set_community_id:
            self.set_community_id(community_id)

        return community_id

    def set_community_id(self, community_id: Union[str, int]) -> None:
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
        except ValueError:
            raise Exception(
                "Check your community id! It should be an integer.\nIf you're using a community link, use `fetch_community_id` instead."
                )

        self.community_id = community_id
        self.community.community_id = community_id

        return None
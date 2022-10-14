from .ext.utilities.generate import *
from .ext import Community, RequestHandler, Account, Global
from .ext.socket import WSClient as Socket

class Bot(Socket):
    """
    `Bot` is the main class that handles the bot.

    `**Parameters**`

    - `command_prefix` - The prefix to use for commands. Defaults to `!`.

    - `community_id` - The community id to use. Defaults to `None`.

    - `debug` - Whether to print debug messages or not. Defaults to `False`.

    - `**kwargs` - Any other keyword arguments to pass to the bot. These will be set as attributes.

    `**Example**`

    ```python
    from pymino import Bot

    bot = Bot(
        command_prefix="!",
        community_id="1234567890",
        debug=True
    )
    ```
    """
    def __init__(self, command_prefix: Optional[str] = "!", community_id: Union[str, int] = None, debug: Optional[bool] = False, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)

        self.command_prefix:    Optional[str] = command_prefix
        self.community_id:      Union[str, int] = community_id
        self.debug:             Optional[bool] = debug
        self.is_ready:          Optional[bool] = False

        self.session = Session(
            proxies=self.proxies if hasattr(self, "proxies") else None,
            headers={
            "NDCLANG": "en",
            "ACCEPT-LANGUAGE": "en-US",
            "CONTENT-TYPE": "application/json; charset=utf-8",
            "USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/LYZ28N; com.narvii.amino.master/3.5.34654)",
            "HOST": "service.aminoapps.com",
            "CONNECTION": "Keep-Alive",
            "ACCEPT-ENCODING": "gzip"
            })
        self.request: RequestHandler = RequestHandler(
            bot=self,
            session=self.session,
            debug=self.debug
            )
        self.community: Community = Community(
            session=self.request,
            community_id=self.community_id,
            debug=self.debug
            )
        #self.global: Global = Global(
        #    session=self.request,
        #    debug=self.debug
        #    )
        self.account: Account = Account(
            session=self.request,
            debug=self.debug
            )
            
        if self.community_id: self.set_community_id(community_id)

        Socket.__init__(self, client=self, debug=debug)


    def authenticate(self, email: str, password: str):
        """
        `authenticate` authenticates the bot. [This is used internally.]
        
        `**Parameters**`
        
        - `email` - The email to use to login.
        
        - `password` - The password to use to login.
        """
        return SResponse(self.request.handler(
            method="POST", url = "https://service.aminoapps.com/api/v1/g/s/auth/login",
            data={
                "email": email,
                "v": 2,
                "secret": "0 {}".format(password),
                "deviceID": self.deviceId if hasattr(self, "deviceId") else device_id(),
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
            })).json

    def fetch_account(self):
        """
        `fetch_account` fetches the account of the bot to verify the sid is valid.

        [This is used internally.]
        """
        return SResponse(self.request.handler(method="GET", url="https://service.aminoapps.com/api/v1/g/s/account"))

    def run(self, email: str=None, password: str=None, sid: str=None):
        """
        `run` runs the bot.
        
        `**Parameters**`
        
        - `email` - The email to use to login. Defaults to `None`.
        
        - `password` - The password to use to login. Defaults to `None`.
        
        - `sid` - The sid to use to login. Defaults to `None`.
        
        `**Example**`
        
        ```python
        
        from pymino import Bot
        
        bot = Bot()
        
        bot.run(
            email="email@email.com",
            password="password"
            )
        ```
        """
        if email and password:
            for key, value in {"email": email, "password": password}.items():
                setattr(self.request, key, value)
            response = self.authenticate(email, password)

        elif sid:
            self.session.headers.update({"NDCAUTH": f"sid={sid}"})
            response = self.fetch_account().json
        else:
            raise Exception("You're missing either an email and password or a sid.")

        if response:
            if response['api:statuscode'] != 0: input(response), exit()

            self.profile: User = User(response)

            self.sid:               str = sid if sid else response['sid']
            self.userId:            str = response["account"]['uid']
            self.community.userId:  str = self.userId
            self.session.headers.update({"NDCAUTH": f"sid={self.sid}", "AUID": self.userId})

            if self.debug: print(f"sid={self.sid}")

            if not self.is_ready:
                self.is_ready = True
                self.connect()

            return response
        else:
            raise Exception("Failed to authenticate.")

    def fetch_community_id(self, community_link: str, set_community_id: Optional[bool] = True):
        """
        `fetch_community_id` fetches the community id from a community link and sets it to `self.community_id` if `set_community_id` is `True`.
        
        `**Parameters**`
        - `community_link` - The community link to fetch the community id from.

        - `set_community_id` - Whether to set the community id to the fetched community id or not. Defaults to `True`.
        
        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        
        community_id = bot.fetch_community_id(
            community_link="https://aminoapps.com/c/your-community",
            set_community_id=True
        )
        ```
        """
        community_id = linkInfoV2(self.request.handler(
            method="GET", url=f"https://service.aminoapps.com/api/v1/g/s/link-resolution?q={community_link}")
            ).comId

        if set_community_id:
            self.set_community_id(community_id)

        return community_id

    def set_community_id(self, community_id: Union[str, int]) -> None:
        """
        `set_community_id` sets the community id to `self.community_id` and `self.community.community_id`.
        
        `**Parameters**`
        
        - `community_id` - The community id to set.
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
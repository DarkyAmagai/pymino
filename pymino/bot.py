from .ext.generate import *
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
        self.command_prefix = command_prefix
        self.community_id = community_id
        try:
            if self.community_id is not None and not isinstance(community_id, int):
                self.community_id = int(community_id)
        except ValueError:
            raise Exception("Check your community id! It should be an integer.\nIf you're using a community link, use `fetch_community_id` instead.")
        self.debug = debug
        self.is_ready = False
        self.session = Session(
            proxies=self.proxies if hasattr(self, "proxies") else None
            )
        self.session.headers = {
        "USER-AGENT": "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        "ACCEPT-LANGUAGE": "en-US",
        "CONTENT-TYPE": "application/json; charset=utf-8",
        "HOST": "service.aminoapps.com",
        "ACCEPT-ENCODING": "gzip",
        "CONNECTION": "Upgrade"
        }
        self.request = RequestHandler(self.session, debug)
        self.community = Community(self.request, community_id, debug)
        #self.global = Global(self.request, debug) #NOTE: This is not implemented yet.
        self.account = Account(self.request, debug)

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
            }))

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
            response = self.authenticate(email, password).json

        elif sid:
            self.session.headers.update({"NDCAUTH": f"sid={sid}"})
            response = self.fetch_account().json
        else:
            raise Exception("You're missing either an email and password or a sid.")

        if response:
            if response['api:statuscode'] != 0:
                input(response), exit()

            self.profile: User = User(response)
            [self.sid, self.userId] = [sid if sid else response['sid'], response["account"]['uid']]
            [self.community.userId, self.is_ready] = [self.userId, True]
            self.session.headers.update({"NDCAUTH": f"sid={self.sid}"})
            self.session.headers.update({"AUID": self.userId})
            if self.debug: print(f"sid={self.sid}")

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
            self.community_id = community_id
            self.community.community_id = community_id

        return community_id
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

    `**Example**`
    ```python
    from pymino import Bot

    bot = Bot(
        command_prefix="!",
        community_id="1234567890",
        debug=True
    )
    """
    def __init__(self, command_prefix: Optional[str] = "!", community_id: Optional[str] = None, debug: Optional[bool] = False):
        self.command_prefix = command_prefix
        self.community_id = community_id
        self.debug = debug
        self.is_ready = False
        self.session = Session()
        self.session.headers = {
        "USER-AGENT": "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        "ACCEPT-LANGUAGE": "en-US",
        "CONTENT-TYPE": "application/json; charset=utf-8",
        "HOST": "service.narvii.com",
        "ACCEPT-ENCODING": "gzip",
        "CONNECTION": "Upgrade"
        }
        self.request = RequestHandler(self.session, debug)
        self.community = Community(self.request, community_id, debug)
        #self.global = Global(self.request, debug) #NOTE: This is not implemented yet.
        self.account = Account(self.request, debug)

        Socket.__init__(self, client=self, debug=debug)


    def authenticate(self, email: str, password: str):
        return SResponse(self.request.handler(
            method="POST", url = "https://service.narvii.com/api/v1/g/s/auth/login",
            data={
                "email": email,
                "v": 2,
                "secret": "0 {}".format(password),
                "deviceID": device_id(),
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
            }))

    def fetch_account(self):
        return SResponse(self.request.handler(method="GET", url="https://service.narvii.com/api/v1/g/s/account"))

    def run(self, email: str=None, password: str=None, sid: str=None):
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

            Thread(self.connect())
            return response
        else:
            raise Exception("Failed to authenticate.")
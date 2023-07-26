from threading import Thread
from typing import Optional, Union
from time import perf_counter, time
from logging import FileHandler, Logger, getLogger, Formatter, DEBUG

from .ext.console import *
from .ext.entities import *
from .ext.account import Account
from .ext.socket import WSClient
from .ext.community import Community
from .ext.global_client import Global
from .ext.utilities.generate import Generator
from .ext.utilities.request_handler import RequestHandler

__all__ = (
    'Bot',
)


class Bot(WSClient, Global):
    """
    Bot class that interacts with aminoapps API.

    This class extends `WSClient` and `Global` classes, allowing the bot to use WebSocket functionality and global client features.

    Special Attributes:
    __slots__ : tuple
        A tuple containing a fixed set of attributes to optimize memory usage.

    Attributes:
    _debug : bool
        Whether or not debug mode is enabled.
    _console_enabled : bool
        Whether or not the CONSOLE is enabled.
    _cooldown_message : str
        The default cooldown message used when a command is on cooldown.
    _intents : bool
        Whether or not intents are enabled.
    _is_ready : bool
        Whether the bot is ready after successful login.
    _userId : str
        The ID of the user associated with the bot.
    _sid : str
        The session ID of the client.
    _cached : bool
        Whether the login credentials are cached.
    logger : Logger
        The logger object.
    cache : Cache
        An instance of the Cache class for caching data.
    command_prefix : Optional[str]
        The prefix used for bot commands.
    community_id : Union[str, int]
        The ID of the community associated with the bot.
    generate : Generator
        An instance of the Generator class for generating data.
    online_status : bool
        Whether the bot's online status is enabled.
    device_id : Optional[str]
        The device ID used for logging in. If not provided, it will be generated using the Generator class.
    _is_authenticated : bool
        Whether the bot is authenticated.
    request : RequestHandler
        An instance of the RequestHandler class for handling API requests.
    community : Community
        An instance of the Community class for community-related actions.
    account : Account
        An instance of the Account class for account-related actions.
    profile : UserProfile
        An instance of the UserProfile class representing the bot's user profile.
    """
    __slots__ = (
        '_debug',
        '_console_enabled',
        '_cooldown_message',
        '_intents',
        '_is_ready',
        '_userId',
        '_sid',
        '_cached',
        'cache',
        'logger',
        'command_prefix',
        'community_id',
        'generate',
        'online_status',
        'device_id',
        '_is_authenticated'
        'request',
        'community',
        'account',
        'profile',
    )
    def __init__(
        self,
        command_prefix: Optional[str] = "!",
        community_id: Union[str, int] = None,
        console_enabled: bool = False,
        device_id: str = None,
        intents: bool = False,
        online_status: bool = False,
        proxy: str = None,
        hash_prefix: Union[str, int] = 19,
        device_key: str = "E7309ECC0953C6FA60005B2765F99DBBC965C8E9",
        signature_key: str  = "DFA5ED192DDA6E88A12FE12130DC6206B1251E44"
        ) -> None:
        """
        `Bot` - This is the main client.

        `**Parameters**``
        - `command_prefix` - The prefix to use for commands. `Defaults` to `!`.
        - `community_id` - The community id to use for the bot. `Defaults` to `None`.
        - `console_enabled` - Whether to enable the console. `Defaults` to `True`.
        - `device_id` - The device id to use for the bot. `Defaults` to `None`.
        - `intents` - Avoids receiving events that you do not need. `Defaults` to `False`.
        - `online_status` - Whether to set the bot's online status to `online`. `Defaults` to `True`.
        - `proxy` - The proxy to use for the bot. `Defaults` to `None`.
        - `hash_prefix` - The hash prefix to use for the bot. `Defaults` to `19`.
        - `device_key` - The device key to use for the bot. `Defaults` to `E7309ECC0953C6FA60005B2765F99DBBC965C8E9`.
        - `signature_key` - The signature key to use for the bot. `Defaults` to `DFA5ED192DDA6E88A12FE12130DC6206B1251E44`.

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
        self._debug:            bool = check_debugger()
        self._console_enabled:  bool = console_enabled
        self._cooldown_message: Optional[str] = None
        self._is_authenticated: bool = False
        self._intents:          bool = intents
        self._is_ready:         bool = False
        self._userId:           str = None
        self._sid:              str = None
        self._cached:           bool = False
        self.cache:             Cache = Cache("cache")

        self.command_prefix:    Optional[str] = command_prefix
        if self.command_prefix == "":
            raise InvalidCommandPrefix()
        
        self.logger:            Optional[Logger] = self._create_logger()
        self.community_id:      Union[str, int] = community_id
        self.generate:          Generator = Generator(hash_prefix, device_key, signature_key)
        self.online_status:     bool = online_status
        self.device_id:         Optional[str] = device_id or self.generate.device_id()
        self.request:           RequestHandler = RequestHandler(
                                bot = self,
                                proxy=proxy,
                                generator=self.generate
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

        super().__init__()

    def __repr__(self):
        """
        Returns a string representation of the Bot object.

        :return: A string representation of the Bot object.
        :rtype: str
        """
        return f"Bot(command_prefix='{self.command_prefix}', community_id={self.community_id}, device_id='{self.device_id}')"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Bot object.

        :return: A user-friendly string representation of the Bot object.
        :rtype: str
        """
        return f"Bot: Prefix='{self.command_prefix}', Community ID={self.community_id}, Device ID='{self.device_id}'"

    def __iter__(self) -> iter:
        """
        Allows iteration over the Bot object.

        :return: An iterator for the Bot object.
        :rtype: iter
        """
        return iter(self.__slots__)

    @property
    def debug(self) -> bool:
        """
        Whether or not debug mode is enabled.

        :return: True if debug mode is enabled, False otherwise.
        :rtype: bool

        This property returns whether or not debug mode is enabled. Debug mode can be used to enable additional logging and
        debug information during development.

        **Note:** This property only returns the debug mode state and cannot be used to set the debug mode state. To set the
        debug mode state, use the `self._debug` attribute directly.
        """
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        """
        Sets the debug mode state.

        :param value: True to enable debug mode, False to disable it.
        :type value: bool
        :return: None

        This setter sets the debug mode state. Debug mode can be used to enable additional logging and debug information
        during development.

        **Note:** This setter only sets the debug mode state and cannot be used to retrieve the debug mode state. To retrieve
        the debug mode state, use the `self.debug` property.
        """
        self._debug = value

    @property
    def console_enabled(self) -> bool:
        """
        Whether or not the CONSOLE is enabled.

        :return: True if the CONSOLE is enabled, False otherwise.
        :rtype: bool

        This property returns whether or not the CONSOLE is enabled. The CONSOLE can be used to interact with the bot and access
        additional features such as the console.

        **Note:** This property only returns the CONSOLE state and cannot be used to set the CONSOLE state. To set the CONSOLE state, use
        the `self._console_enabled` attribute directly.
        """
        return self._console_enabled

    @console_enabled.setter
    def console_enabled(self, value: bool) -> None:
        """
        Sets the CONSOLE state.

        :param value: True to enable the CONSOLE, False to disable it.
        :type value: bool
        :return: None

        This setter sets the CONSOLE state. The CONSOLE can be used to interact with the bot and access additional features such as
        the console.

        **Note:** This setter only sets the CONSOLE state and cannot be used to retrieve the CONSOLE state. To retrieve the CONSOLE state,
        use the `self.console_enabled` property.
        """
        self._console_enabled = value

    @property
    def intents(self) -> bool:
        """
        Whether or not intents are enabled.

        :return: True if intents are enabled, False otherwise.
        :rtype: bool

        This property returns whether or not intents are enabled. Intents allow the bot to use additional features such as
        `ctx.wait_for_message()`.

        **Note:** This property only returns the intents state and cannot be used to set the intents state. To set the intents
        state, use the `self._intents` attribute directly.
        """
        return self._intents

    @intents.setter
    def intents(self, value: bool) -> None:
        """
        Sets the intents state.

        :param value: True to enable intents, False to disable them.
        :type value: bool
        :return: None

        This setter sets the intents state. Intents allow the bot to use additional features such as `ctx.wait_for_message()`.

        **Note:** This setter only sets the intents state and cannot be used to retrieve the intents state. To retrieve the
        intents state, use the `self.intents` property.
        """
        self._intents = value

    @property
    def is_ready(self) -> bool:
        """
        Whether or not the bot is ready.

        :return: True if the bot is ready, False otherwise.
        :rtype: bool

        This property returns whether or not the bot is ready. The bot is ready after logging in to
        Amino and receiving a valid session ID.

        **Note:** This property only returns the authentication state and cannot be used to set the authentication state. To
        set the authentication state, use the `self._is_ready` attribute directly.
        """
        return self._is_ready

    @is_ready.setter
    def is_ready(self, value: bool) -> None:
        """
        Sets the `is_ready` state of the client.

        :param value: True to set the client as ready, False to set it as not ready.
        :type value: bool
        :return: None

        This setter sets the `is_ready` state of the bot client. The bot `is_ready` after logging in to Amino and
        receiving a valid session ID.

        **Note:** This setter only sets the authentication state and cannot be used to retrieve the authentication state. To
        retrieve the authentication state, use the `self.is_ready` property.
        """
        self._is_ready = value

    @property
    def userId(self) -> str:
        """
        The ID of the user associated with the client.

        :return: The ID of the user.
        :rtype: str

        This property returns the ID of the user associated with the client. The user ID is set when the client logs in to
        Amino, and can be used to make API calls related to the user, such as retrieving the user's profile or posts.

        **Note:** This property only returns the user ID and cannot be used to set the user ID. To set the user ID, use the
        `self._userId` attribute directly.
        """
        return self._userId

    @userId.setter
    def userId(self, value: str) -> None: # Human is gay.
        """
        Sets the ID of the user associated with the client.

        :param value: The ID of the user to set.
        :type value: str
        :return: None

        This setter sets the ID of the user associated with the client. The user ID is used to make API calls related to the
        user, such as retrieving the user's profile or posts.

        **Note:** This setter only sets the user ID and cannot be used to retrieve the user ID. To retrieve the user ID, use
        the `self.userId` property.
        """
        self._userId = value

    @property
    def sid(self) -> str:
        """
        The session ID of the client.

        :return: The session ID.
        :rtype: str

        This property returns the session ID of the client. The session ID is set when the client logs in to Amino, and is
        used to make authenticated API calls, such as posting messages or retrieving user information.

        **Note:** This property only returns the session ID and cannot be used to set the session ID. To set the session ID,
        use the `self._sid` attribute directly.
        """
        return self._sid

    @sid.setter
    def sid(self, value: str) -> None:
        """
        Sets the session ID of the client.

        :param value: The session ID to set.
        :type value: str
        :return: None

        This setter sets the session ID of the client. The session ID is used to make authenticated API calls, such as
        posting messages or retrieving user information.

        **Note:** This setter only sets the session ID and cannot be used to retrieve the session ID. To retrieve the session
        ID, use the `self.sid` property.
        """
        self._sid = value

    def set_cooldown_message(self, message: str) -> None:
        """
        Changes the default cooldown message.
        
        :param message: The message to set as the default cooldown message.
        :type message: str
        :return: None
        
        This method changes the default cooldown message. The default cooldown message is used when a command is on cooldown
        
        **Note:** This method only sets the default cooldown message and cannot be used to retrieve the default cooldown message.
        """
        self._cooldown_message = message

    @property
    def is_authenticated(self) -> bool:
        """
        Whether or not the client is authenticated.

        :return: True if the client is authenticated, False otherwise.
        :rtype: bool

        This property returns whether or not the client is authenticated. The client is authenticated after logging in to
        Amino and receiving a valid session ID.

        **Note:** This property only returns the authentication state and cannot be used to set the authentication state. To
        set the authentication state, use the `self._is_authenticated` attribute directly.
        """
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value: bool) -> None:
        """
        Sets the authentication state of the client.

        :param value: True to authenticate the client, False to deauthenticate it.
        :type value: bool
        :return: None

        This setter sets the authentication state of the client. The client is authenticated after logging in to Amino and
        receiving a valid session ID.

        **Note:** This setter only sets the authentication state and cannot be used to retrieve the authentication state. To
        retrieve the authentication state, use the `self.is_authenticated` property.
        """
        self._is_authenticated = value

    def _create_logger(self) -> Logger:
        """
        Creates a logger object.
        
        :return: A logger object.
        :rtype: Logger
        
        This method creates a logger object. The logger object is used to log debug information to debug.log.
        """
        logger = getLogger("pymino")
        logger.setLevel(DEBUG)

        file_handler = FileHandler("debug.log")
        file_handler.setLevel(DEBUG)

        formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def authenticate(self, email: str, password: str, device_id: str=None) -> dict:
        """
        Authenticates the bot with the provided email and password.

        :param email: The email to use to log in.
        :type email: str
        :param password: The password to use to log in.
        :type password: str
        :param device_id: The device id to use to log in. Defaults to None.
        :type device_id: Optional[str]
        :return: A dictionary representing the server response.
        :rtype: dict
        :raises: `APIError` if the API response code is not 200.
        """
        if device_id:
            self.device_id = device_id

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
                "deviceID": self.device_id,
                "email": email,
                "v": 2,
                "clientCallbackURL": "narviiapp://default"
                }
            )).json()

    def _login_handler(self, email: str, password: str, device_id: str=None, use_cache: bool=True) -> dict:
        """
        Authenticates the user with the provided email and password.

        :param email: The email address associated with the account.
        :type email: str
        :param password: The password for the account.
        :type password: str
        :param device_id: The device ID associated with the account. Defaults to None.
        :type device_id: Optional[str]
        :param use_cache: Whether or not to use cached login credentials. Defaults to True.
        :type use_cache: bool
        :return: A dictionary containing the login response from the server.
        :rtype: dict
        
        The function first checks if cached login credentials are available for the provided email. If so, it uses the cached
        session ID and device ID to fetch the account details from the server. If the server returns an exception, it falls
        back to authenticating with the provided email and password, and the device ID from the cache.

        If no cached credentials are available, the function authenticates with the provided email and password, and the
        provided or default device ID.

        Finally, the function sets the email and password on the request object for future API calls.

        **Note:** This function should not be called directly. Instead, use the `login` function to authenticate the user.
        """
        if use_cache and cache_exists(email=email):
            cached = fetch_cache(email=email)

            self.sid: str = cached[0]
            self.request.sid: str = cached[0]
            self.userId: str = parse_auid(cached[0])

            try:
                response: dict = self.fetch_account()
            except Exception:
                response: dict = self.authenticate(
                    email=email,
                    password=password,
                    device_id=cached[1]
                    )

        else:
            self.sid = None
            self._cached = True
            response: dict = self.authenticate(
                email=email,
                password=password,
                device_id=device_id
                )

        for key, value in {"email": email, "password": password}.items():
            setattr(self.request, key, value)            

        return response

    def run(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        sid: Optional[str] = None,
        device_id: Optional[str] = None,
        use_cache: bool = True
    ) -> None:
        """
        Logs in to the client and starts running it. 

        If authentication is successful, the bot will be logged in and the client will be ready to use.

        :param email: The email to use to log in. Defaults to None.
        :type email: str, optional
        :param password: The password to use to log in. Defaults to None.
        :type password: str, optional
        :param sid: The sid to use to log in. Defaults to None.
        :type sid: str, optional
        :param device_id: The device id to use to log in. Defaults to None.
        :type device_id: str, optional
        :param use_cache: Whether to use the cache to retrieve the sid. Defaults to True.
        :type use_cache: bool, optional
        :raises MissingEmailPasswordOrSid: If email, password, or sid is missing.
        :raises LoginFailed: If authentication failed.
        :return: None.
        :rtype: None

        **Example usage:**

        >>> client = Client()
        >>> client.run(email="example@example.com", password="password")
        """
        if not sid and not email and not password:
            raise MissingEmailPasswordOrSid

        if sid:
            self.sid = sid
            self.request.sid = sid
            self.userId = parse_auid(sid)
            response = self.fetch_account()
        else:
            response = self._login_handler(
                email=email,
                password=password,
                device_id=device_id,
                use_cache=use_cache
                )

        if not response:
            raise LoginFailed

        return self._run(response)

    def _run(self, response: dict) -> dict:
        """
        Processes the response from a successful login attempt and sets up the authenticated client.

        :param response: The response from the login attempt.
        :type response: dict
        :return: The response from the login attempt.
        :rtype: dict

        This method is called internally by the `login` and `run` methods after a successful login attempt.
        It sets up the authenticated client by parsing the response, initializing some client properties,
        and caching the login credentials if applicable.

        If the `debug` property of the client instance is `True`, this method prints a message to the console
        confirming that the client is now authenticated.

        **Example usage:**

        >>> client = Client()
        >>> response = client.authenticate(email="example@example.com", password="password")
        >>> client.__run__(response)
        """
        if response["api:statuscode"] != 0:
            input(response), exit()

        if not hasattr(self, "profile"): 
            self.profile: UserProfile = UserProfile(response)

        if not self.sid:
            self.sid: str = response["sid"]

        self.userId: str = self.profile.userId
        self.community.userId: str = self.userId
        self.request.sid: str = self.sid
        self.request.userId: str = self.userId
        
        if hasattr(self.request, "email") and self._cached:
            cache_login(email=self.request.email, device=self.device_id, sid=self.sid)

        if not self.is_ready:
            self._is_ready = True
            self._is_authenticated = True
            self._log(f"Logged in as {self.profile.username} ({self.profile.userId})")
            self.connect()
        else:
            self._log(f"Reconnected as {self.profile.username} ({self.profile.userId})")

        if self.debug:
            print(f"{Fore.MAGENTA}Logged in as {self.profile.username} ({self.profile.userId}){Style.RESET_ALL}")

        Thread(target=self.__run_console__).start()
        return response

    def __run_console__(self) -> None:
        if self.console_enabled:
            self._debug = False
            Console(self).fetch_menu()

    def fetch_account(self) -> dict:
        """
        Fetches the account information for the authenticated user.

        :return: A dictionary containing the user's account information.
        :rtype: dict

        This method fetches the account information for the authenticated user. The account information includes
        the user's username, email address, and other relevant details. The method calls the `UserProfile` object's
        `handler` method with the `method` parameter set to `GET` and the `url` parameter set to the user profile endpoint.
        The result is an `ApiResponse` object that contains the user's profile information.

        The method then calls the `handler` method of the `request` object with the `method` parameter set to `GET`
        and the `url` parameter set to the account endpoint. The result is an `ApiResponse` object that contains the
        user's account information in JSON format.

        The method returns a dictionary containing the user's account information.
        """
        self.profile: UserProfile = UserProfile(
            self.request.handler(
                method="GET",
                url=f"/g/s/user-profile/{self.userId}"
                ))
        
        return ApiResponse(self.request.handler(method="GET", url="/g/s/account")).json()

    def fetch_community_id(self, community_link: str, set_community_id: Optional[bool] = True) -> int:
        """
        Fetches the community ID associated with the provided community link.

        :param community_link: The community link for which to fetch the ID.
        :type community_link: str
        :param set_community_id: Whether or not to set the fetched community ID on the client instance. Defaults to True.
        :type set_community_id: Optional[bool]
        :return: The community ID associated with the provided community link.
        :rtype: int

        The function first checks if the community ID for the provided community link is already present in the cache.
        If not, it fetches the community ID from the server using the provided community link. It then stores the community
        ID in the cache for future use.

        If the `set_community_id` parameter is set to True, the function also sets the community ID on the client instance
        for future API calls.

        If the provided community link is not found on the server, the function raises a CommunityNotFound exception.

        **Note:** The community ID is required for making API calls related to a specific community, such as posting or
        retrieving posts. It is recommended to use this function if you do not already know the community ID.
        """
        KEY = str((community_link, "comId"))
        if not self.cache.get(KEY):
            self.cache.set(KEY, CCommunity(self.request.handler(
                method="GET", url=f"/g/s/link-resolution?q={community_link}")
                ).comId)
            
        community_id = self.cache.get(KEY)

        if set_community_id:
            self.set_community_id(community_id)

        return community_id

    def set_community_id(self, community_id: Union[str, int]) -> int:
        """
        Sets the community ID on the client instance and the Community object.

        :param community_id: The community ID to set.
        :type community_id: Union[str, int]
        :return: The community ID that was set.
        :rtype: int

        The function first checks if the provided community ID is not None and not already an integer. If it is a string,
        it converts it to an integer.

        If the community ID cannot be verified, the function raises a VerifyCommunityIdIsCorrect exception.

        The function then sets the community ID on the client instance and the Community object for future API calls.

        **Note:** The community ID is required for making API calls related to a specific community, such as posting or
        retrieving posts. It is recommended to use the `fetch_community_id` function if you do not already know the
        community ID.
        """
        try:
            if community_id is not None and not isinstance(community_id, int):
                community_id = int(community_id)
        except VerifyCommunityIdIsCorrect as e:
            raise VerifyCommunityIdIsCorrect from e

        self.community_id = community_id
        self.community.community_id = community_id

        return community_id

    def ping(self) -> float:
        """
        Pings the server and returns the elapsed time in milliseconds.
        
        :return: The elapsed time in milliseconds.
        :rtype: float
        
        This method pings the server by sending a GET request to the account endpoint. It then calculates the elapsed
        time in milliseconds and returns it.
        
        If the ping fails, the method raises a PingFailed exception.
        
        **Note:** This method is not recommended for production use. It is intended for testing purposes only.
        
        **Example usage:**
        
        ```python
        bot = Bot()
        @bot.command("ping")
        def ping_command(ctx: Context):
            ping = bot.ping()
            ctx.reply(f"Pong! {ping}ms")
        ```
        """
        try:
            start = perf_counter()
            self.request.handler(method="GET", url="/g/s/account")
            end = perf_counter()
            elapsed_time_ms = (end - start) * 1000
            return round(elapsed_time_ms, 2)
        except Exception as e:
            raise PingFailed from e
import logging
import os
import threading
import time
from collections.abc import Iterator
from typing import Any, Optional

import diskcache

from pymino.ext import (
    account,
    community,
    console,
    entities,
    global_client,
    socket,
    utilities,
)

__all__ = ("Bot",)

logger = logging.getLogger("pymino")
local_cache = diskcache.Cache(f"{os.path.dirname(os.path.realpath(__file__))}/cache")


class Bot(socket.WSClient, global_client.Global):
    """
    Bot class that interacts with aminoapps API.

    This class extends `WSClient` and `Global` classes, allowing the bot to use WebSocket functionality and global client features.

    Attributes:
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
        "__hash_prefix__",
        "__device_key__",
        "__signature_key__",
        "__service_key__",
        "_cached",
        "_command_prefix",
        "_community_id",
        "_console_enabled",
        "_debug",
        "_device_id",
        "_generate",
        "_intents",
        "_is_ready",
        "_proxy",
        "_request",
        "_sid",
        "_userId",
        "account",
        "cooldown_message",
        "online_status",
    )

    def __init__(
        self,
        command_prefix: str = "!",
        community_id: Optional[int] = None,
        console_enabled: bool = False,
        debug_log: bool = False,
        device_id: Optional[str] = None,
        intents: bool = False,
        online_status: bool = False,
        proxy: Optional[str] = None,
        hash_prefix: str = "52",
        device_key: str = "AE49550458D8E7C51D566916B04888BFB8B3CA7D",
        signature_key: str = "EAB4F1B9E3340CD1631EDE3B587CC3EBEDF1AFA9",
        service_key: Optional[str] = None,
    ) -> None:
        """
        `Bot` - This is the main client.

        `**Parameters**``
        - `command_prefix` - The prefix to use for commands. `Defaults` to `!`.
        - `community_id` - The community id to use for the bot. `Defaults` to `None`.
        - `console_enabled` - Whether to enable the console. `Defaults` to `True`.
        - `debug_log` - Whether to enable logging to file. `Defaults` to `False`.
        - `device_id` - The device id to use for the bot. `Defaults` to `None`.
        - `intents` - Avoids receiving events that you do not need. `Defaults` to `False`.
        - `online_status` - Whether to set the bot's online status to `online`. `Defaults` to `True`.
        - `proxy` - The proxy to use for the bot. `Defaults` to `None`.
        - `hash_prefix` - The hash prefix to use for the bot. `Defaults` to `19`.
        - `device_key` - The device key to use for the bot.
        - `signature_key` - The signature key to use for the bot.

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
        hash_prefix = local_cache.get("hash_prefix", hash_prefix)
        device_key = local_cache.get("device_key", device_key)
        signature_key = local_cache.get("signature_key", signature_key)
        service_key = local_cache.get("service_key", service_key)
        if hash_prefix and device_key and signature_key:
            self.__hash_prefix__ = hash_prefix
            self.__device_key__ = device_key
            self.__signature_key__ = signature_key
        else:
            raise entities.MissingDeviceKeyOrSignatureKey
        if service_key:
            self.__service_key__ = service_key
        else:
            raise entities.MissingServiceKey
        self.debug = entities.check_debugger()
        self.console_enabled = console_enabled
        self.cooldown_message = None
        self.intents = intents
        self.is_ready = False
        self.userId = None
        self.sid = None
        self._cached: bool = False
        self.command_prefix = command_prefix
        self.community_id = community_id
        self.proxy = proxy
        self.generate = utilities.Generator(
            self.__hash_prefix__,
            self.__device_key__,
            self.__signature_key__,
            self.__service_key__,
        )
        self.online_status = online_status
        self.device_id = device_id or self.generate.device_id()
        self.request = utilities.RequestHandler(self, self.generate)
        self.account = account.Account(session=self.request)
        if debug_log:
            utilities.enable_file_logging()
        super().__init__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Bot object.

        :return: A string representation of the Bot object.
        :rtype: str
        """
        return f"Bot(command_prefix='{self.command_prefix}', community_id={self.community_id}, device_id='{self.device_id}')"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the Bot object.

        :return: A user-friendly string representation of the Bot object.
        :rtype: str
        """
        return f"Bot: Prefix='{self.command_prefix}', Community ID={self.community_id}, Device ID='{self.device_id}'"

    def __iter__(self) -> Iterator[str]:
        """
        Allows iteration over the Bot object.

        :return: An iterator for the Bot object.
        :rtype: iter
        """
        return iter(self.__slots__)

    @property
    def community(self) -> community.Community:
        if not self.userId:
            raise entities.NotLoggedIn()
        return community.Community(self)

    @property
    def community_id(self) -> Optional[int]:
        return self._community_id

    @community_id.setter
    def community_id(self, value: Optional[int]) -> None:
        self._community_id = value

    @property
    def command_prefix(self) -> str:
        return self._command_prefix

    @command_prefix.setter
    def command_prefix(self, value: str) -> None:
        if not value:
            raise entities.InvalidCommandPrefix()
        self._command_prefix = value

    @property
    def proxy(self) -> Optional[str]:
        return self._proxy

    @proxy.setter
    def proxy(self, value: Optional[str]) -> None:
        self._proxy = value

    @property
    def generate(self) -> utilities.Generator:
        return self._generate

    @generate.setter
    def generate(self, value: utilities.Generator) -> None:
        self._generate = value

    @property
    def request(self) -> utilities.RequestHandler:
        return self._request

    @request.setter
    def request(self, value: utilities.RequestHandler) -> None:
        self._request = value

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
    def userId(self) -> Optional[str]:
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
    def userId(self, value: Optional[str]) -> None:  # Human is gay.
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
    def device_id(self) -> str:
        """
        The Device ID associated with the client.

        :return: The ID of the device.
        :rtype: str

        This property returns the ID of the device associated with the client. The device ID is set when the client creation.
        """
        return self._device_id

    @device_id.setter
    def device_id(self, value: str) -> None:
        """
        Sets the ID of the device associated with the client.

        :param value: The ID of the device to set.
        :type value: str
        :return: None

        This setter sets the ID of the device associated with the client.
        """
        self._device_id = value

    @property
    def sid(self) -> Optional[str]:
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
    def sid(self, value: Optional[str]) -> None:
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

    @property
    def secret(self) -> Optional[str]:
        """
        The secret of the client.

        :return: The secret.
        :rtype: str

        This property returns the secret of the client. The secret is set when the client logs in to Amino, and is used to
        make authenticated API calls, such as posting messages or retrieving user information.

        **Note:** This property only returns the secret and cannot be used to set the secret. To set the secret, use the
        `self._secret` attribute directly.
        """
        return self._secret

    @secret.setter
    def secret(self, value: Optional[str]) -> None:
        """
        Sets the secret of the client.

        :param value: The secret to set.
        :type value: str
        :return: None

        This setter sets the secret of the client. The secret is used to make authenticated API calls, such as posting
        messages or retrieving user information.

        **Note:** This setter only sets the secret and cannot be used to retrieve the secret. To retrieve the secret, use
        the `self.secret` property.
        """
        self._secret = value

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
        """
        return bool(self.sid and self.userId)

    def authenticate(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        secret: Optional[str] = None,
        device_id: Optional[str] = None,
    ) -> dict[str, Any]:
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
        response = self.request.handler(
            method="POST",
            url="/g/s/auth/login",
            data={
                "secret": secret or f"0 {password}",
                "clientType": 100,
                "systemPushEnabled": 0,
                "timestamp": int(time.time() * 1000),
                "locale": "en_US",
                "action": "normal",
                "bundleID": "com.narvii.master",
                "timezone": -480,
                "deviceID": self.device_id,
                "email": email,
                "v": 2,
                "clientCallbackURL": "narviiapp://default",
            },
        )
        if not response.get("sid"):
            raise entities.AccountLoginRatelimited()
        return response

    def _login_handler(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        secret: Optional[str] = None,
        device_id: Optional[str] = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """
        Authenticates the user with the provided email and password.

        :param email: The email address associated with the account.
        :type email: str
        :param password: The password for the account.
        :type password: str
        :param secret: The secret for the account. Defaults to None.
        :type secret: Optional[str]
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
        if use_cache and email and entities.cache_exists(email=email):
            cached = entities.fetch_cache(email=email)
            assert cached  # cast for type checking
            self.device_id = cached[1]
            self.sid = cached[0]
            self.userId = entities.parse_auid(cached[0])
            try:
                response = self.fetch_account()
            except Exception:
                response = self.authenticate(
                    email=email,
                    password=password,
                    device_id=self.device_id,
                )
        else:
            self.sid = None
            self._cached = True
            response = self.authenticate(
                email=email,
                password=password,
                secret=secret,
                device_id=device_id,
            )
        self.request.email = email
        self.request.password = password
        return response

    def call_amino_certificate(self) -> None:
        response = self.request.http_handler.get(
            "https://app.pymino.site/amino_certificate",
            params={
                "key": self.__service_key__,
                "user_id": self.userId,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = self.request.handler(
            "POST",
            "/g/s/security/public_key",
            data=response.json(),
        )
        if response.get("api:statuscode") != 0:
            raise Exception(str(response))

    def run(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        secret: Optional[str] = None,
        sid: Optional[str] = None,
        device_id: Optional[str] = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """
        Logs in to the client using the provided credentials.

        :param email: The email address associated with the account. Defaults to None.
        :type email: Optional[str]
        :param password: The password for the account. Defaults to None.
        :type password: Optional[str]
        :param secret: The secret for the account. Defaults to None.
        :type secret: Optional[str]
        :param sid: The session ID for the account. Defaults to None.
        :type sid: Optional[str]
        :param device_id: The device ID associated with the account. Defaults to None.
        :type device_id: Optional[str]
        :param use_cache: Whether or not to use cached login credentials. Defaults to True.
        :type use_cache: bool
        :raises MissingEmailPasswordOrSid: If no email, password or sid is provided.
        :raises LoginFailed: If login failed.
        :return: None
        :rtype: None

        **Example usage:**

        >>> client = Client()
        >>> client.login(email="example@example.com", password="password")
        """

        if not any([email, password, sid, secret]):
            raise entities.MissingEmailPasswordOrSid

        if sid:
            self.sid = sid
            self.userId = entities.parse_auid(sid)
            response = self.fetch_account()
        else:
            response = self._login_handler(
                email=email,
                password=password,
                secret=secret,
                device_id=device_id,
                use_cache=use_cache,
            )
        if not response:
            raise entities.LoginFailed
        return self._run(response)

    def _run(self, response: dict[str, Any]) -> dict[str, Any]:
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
        if response.get("api:statuscode") != 0:
            input(response)
            exit()
        if not hasattr(self, "profile"):
            self.profile = entities.UserProfile(response)
        if not self.sid:
            self.sid = response.get("sid")
        self.userId = self.profile.userId
        self.secret = response.get("secret")

        if self.request.email and self.sid and self._cached:
            entities.cache_login(
                email=self.request.email, device=self.device_id, sid=self.sid
            )

        if not self.is_ready:
            self.is_ready = True
            logger.debug(
                f"Logged in as {self.profile.username} ({self.profile.userId})"
            )
            self.connect()
        else:
            logger.debug(
                f"Reconnected as {self.profile.username} ({self.profile.userId})"
            )

        threading.Thread(target=self.__run_console__).start()
        with entities.cache as cache:
            cache.set(key=f"{self.userId}-account", value=response, expire=43200)

        self.__set_keys__()
        self.call_amino_certificate()
        return response

    def __set_keys__(self):
        """
        Sets the device key and signature key on the client instance.

        :return: None
        :rtype: None

        This method is called internally by the `login` and `run` methods after a successful login attempt.
        It sets the device key and signature key on the client instance.
        """
        with local_cache:
            for key, value in (
                ("device_key", self.__device_key__),
                ("signature_key", self.__signature_key__),
            ):
                if local_cache.get(key) != value:
                    local_cache.set(key=key, value=value)

    def reset_keys(self) -> None:
        """
        Resets the device key and signature key on the client instance.

        :return: None
        :rtype: None

        This method resets the device key and signature key on the client instance.
        """
        with local_cache:
            for key in ["device_key", "signature_key"]:
                local_cache.delete(key)
        raise entities.MissingDeviceKeyOrSignatureKey

    def __run_console__(self) -> None:
        if self.console_enabled:
            self._debug = False
            console.Console(self).fetch_menu()

    def fetch_account(self) -> dict[str, Any]:
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
        with entities.cache as cache:
            if cached_info := cache.get(f"{self.userId}-account"):
                return cached_info
            profile = self.request.handler(
                method="GET", url=f"/g/s/user-profile/{self.userId}"
            )
            self.profile = entities.UserProfile(profile)
            account = self.request.handler(method="GET", url="/g/s/account")

            account.update(profile)
            cache.set(key=f"{self.userId}-account", value=account, expire=43200)
        return account

    def fetch_community_id(
        self,
        community_link: str,
        set_community_id: Optional[bool] = True,
    ) -> int:
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
        key = str((community_link, "comId"))
        with entities.cache as cache:
            if not cache.get(key):
                cache.set(
                    key,
                    entities.CCommunity(
                        self.request.handler(
                            method="GET", url=f"/g/s/link-resolution?q={community_link}"
                        )
                    ).comId,
                )
            community_id = cache.get(key)
        if set_community_id:
            self.set_community_id(community_id)
        return community_id

    def set_community_id(self, community_id: int) -> int:
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
        self.community_id = community_id
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
        start = time.perf_counter()
        try:
            self.request.handler(method="GET", url="/g/s/account")
        except Exception as e:
            raise entities.PingFailed from e
        end = time.perf_counter()
        elapsed_time_ms = (end - start) * 1000
        return round(elapsed_time_ms, 2)

    def fetch_wallet(self) -> entities.Wallet:
        """
        Fetches the wallet information for the authenticated user.

        :return: A `Wallet` object containing the user's wallet information.
        :rtype: Wallet

        This method fetches the wallet information for the authenticated user. The wallet information includes the user's
        total number of coins, the number of business coins, and other relevant details. The method calls the `fetch_wallet`
        method of the `account` object. The result is a `Wallet` object that contains the user's wallet information.

        The method returns a `Wallet` object containing the user's wallet information.
        """
        return self.account.fetch_wallet()

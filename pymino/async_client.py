import asyncio
from time import time
from typing import Any, Callable, Optional, TypeVar, Union

from .ext.entities import *
from .ext.async_global_client import AsyncGlobal
from .ext.utilities.generate import Generator
from .ext import AsyncRequestHandler, AsyncAccount, AsyncCommunity


F = TypeVar("F", bound=Callable[..., Any])

class AsyncClient(AsyncGlobal):
    """
    `Client` - This is the main client.

    `**Parameters**``
    - `**kwargs` - any other parameters to use for the client.
    - `device_id` - device id to use for the client.
    - `proxy` - proxy string to use for the client.
    - `hash_prefix` - The hash prefix to use for the bot. `Defaults` to `19`.
    - `device_key` - The device key to use for the bot. `Defaults` to `E7309ECC0953C6FA60005B2765F99DBBC965C8E9`.
    - `signature_key` - The signature key to use for the bot. `Defaults` to `DFA5ED192DDA6E88A12FE12130DC6206B1251E44`.
    
    
    ----------------------------
    Why use `Client` over `Bot`?

    - Used for scripts rather than bots.
    - Lightweight, does not utilize websocket.

    ----------------------------
    Do I have to be logged in to use `Client`?

    - No, you do not have to be logged in to use `Client`.
    - However, you will not be able to use any methods that require authentication.

    `**NON-AUTH EXAMPLE**`
    ```python
    # This method does not require authentication, so it will work without logging in.    

    from pymino import Client

    client = Client()

    print(f"Logged in: {client.is_authenticated}")

    chat_id = client.community.fetch_object_id(link="https://aminoapps.com/p/123456789")

    print(f"Chat ID: {chat_id}")
    ```
    ----------------------------

    How do I login with `Client`?
        - You can login with `Client` by using the `login` method.
        
    `**Login Example**`

    ```python
    from pymino import Client

    client = Client()

    client.login(email="email", password="password")

    print(f"Logged in: {client.is_authenticated}")

    # Output: Logged in: True
    ```
    ----------------------------
    How can I utilize community methods with `Client`?
        - First, you must set the community id.
        - You can set the community id by using the `set_community_id` method
        - Or the `fetch_community_id` method if you do not know the community id.

    `**Community Example**`
    ```python
    from pymino import Client

    client = Client()

    client.login(email="email", password="password")

    print(f"Logged in: {client.is_authenticated}")

    client.fetch_community_id("http://aminoapps.com/c/CommunityName")
    # Or
    client.set_community_id(123456789)

    print(f"Community ID has been set: {client.community_id}")
    ```
    ----------------------------
    `**Community Methods**`
    ```python
    from pymino import Client

    client = Client()

    client.login(email="email", password="password")

    client.fetch_community_id("http://aminoapps.com/c/CommunityName")

    client.community.send_message(
        chatId = "000000-0000-0000-0000-000000",
        content = "Hello, world!"
    ) # This will send in the community you set the community id for.

    #Alternatively, you can use the community id as a parameter.
    comId = client.fetch_community_id("http://aminoapps.com/c/CommunityName")
    client.community.send_message(
        chatId = "000000-0000-0000-0000-000000",
        content = "Hello, world!",
        comId = comId
    )
    ```

    """
    def __init__(
        self,
        community_id: Optional[Union[str, int]] = None,
        hash_prefix: Union[str, int] = 19,
        device_key: str = "E7309ECC0953C6FA60005B2765F99DBBC965C8E9",
        signature_key: str  = "DFA5ED192DDA6E88A12FE12130DC6206B1251E44",
        **kwargs
        ) -> None:
        self._debug:            bool = check_debugger()
        self.loop:              asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._is_authenticated: bool = False
        self._userId:           str = None
        self._sid:              str = None
        self._cached:           bool = False
        self.cache:             Cache = Cache("cache")
        self.community_id:      Optional[str] = community_id or kwargs.get("comId")
        self.generate:          Generator = Generator(
                                prefix=hash_prefix,
                                device_key=device_key,
                                signature_key=signature_key
                                )
        self.device_id:         Optional[str] = kwargs.get("device_id") or self.generate.device_id()
        self.request:           AsyncRequestHandler = AsyncRequestHandler(
                                bot=self,
                                loop = self.loop,
                                proxy = kwargs.get("proxy"),
                                generator=self.generate
                                )
        self.account:           AsyncAccount = AsyncAccount(
                                session=self.request
                                )
        self.community:         AsyncCommunity = AsyncCommunity(
                                bot=self,
                                session=self.request,
                                community_id=self.community_id
                                )
        
        super().__init__()


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
    def userId(self, value: str) -> None:
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
        self._userId = value # Human is gay.

        
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


    def authenticated(func: F) -> F:
        """
        A decorator that ensures the user is authenticated before running the decorated function.

        :param func: The function to be decorated.
        :type func: Callable
        :raises LoginRequired: If the user is not authenticated.
        :return: The result of calling the decorated function.
        :rtype: Any

        **Example usage:**

        >>> client = Client()
        >>> client.login(email="example@example.com", password="password")

        >>> @authenticated
        >>> def my_function(self):
        >>>     # Function code
        """
        async def wrapper(*args, **kwargs) -> Any:
            try:
                if not args[0].is_authenticated:
                    raise LoginRequired
                return await func(*args, **kwargs)
            except AttributeError:
                raise LoginRequired
        return wrapper


    async def fetch_community_id(self, community_link: str, set_community_id: Optional[bool] = True) -> int:
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
            self.cache.set(KEY, CCommunity(await self.request.handler(
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


    async def authenticate(self, email: str, password: str, device_id: str=None) -> dict:
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

        return ApiResponse(await self.request.handler(
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


    async def _login_handler(self, email: str, password: str, device_id: str=None, use_cache: bool=True) -> dict:
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
                response: dict = await self.fetch_account()
            except Exception:
                response: dict = await self.authenticate(
                    email=email,
                    password=password,
                    device_id=cached[1]
                    )

        else:
            self.sid = None
            self._cached = True
            response: dict = await self.authenticate(
                email=email,
                password=password,
                device_id=device_id
                )

        for key, value in {"email": email, "password": password}.items():
            setattr(self.request, key, value)            

        return response


    async def login(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        sid: Optional[str] = None,
        device_id: Optional[str] = None,
        use_cache: bool = True
        ) -> None:
        """
        Logs in to the client using the provided credentials.

        :param email: The email address associated with the account. Defaults to None.
        :type email: Optional[str]
        :param password: The password for the account. Defaults to None.
        :type password: Optional[str]
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
        if not sid and not email and not password:
            raise MissingEmailPasswordOrSid

        if sid:
            self.sid = sid
            self.request.sid = sid
            self.userId = parse_auid(sid)
            response = await self.fetch_account()
        else:
            response = await self._login_handler(
                email=email,
                password=password,
                device_id=device_id,
                use_cache=use_cache
                )

        if not response:
            raise LoginFailed

        return self._run(response)


    async def run(
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
        return await self.login(email=email, password=password, sid=sid, device_id=device_id, use_cache=use_cache)


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
        >>> client._run(response)
        """
        if response["api:statuscode"] != 0: input(response), exit()

        if not hasattr(self, "profile"): 
            self.profile: UserProfile = UserProfile(response)

        if not self.sid:
            self.sid: str = response["sid"]

        self.userId: str = self.profile.userId
        self.community.userId: str = self.userId
        self.request.sid: str = self.sid
        self.request.userId: str = self.userId
        self.is_authenticated: bool = True

        if hasattr(self.request, "email") and self._cached:
            cache_login(email=self.request.email, device=self.device_id, sid=self.sid)

        if self.debug:
            print(f"{Fore.MAGENTA}Logged in as {self.profile.username} ({self.profile.userId}){Style.RESET_ALL}")

        return response


    @authenticated
    async def disconnect_google(self, password: str) -> dict:
        """
        Disconnects the user's Google account from their account on Amino.

        :param password: The user's account password.
        :type password: str
        :return: A dictionary containing the server response.
        :rtype: dict

        If the client is authenticated, the function sends a POST request to the server to disconnect the user's Google
        account. The request includes the client's device ID, the user's account password, and other required parameters.

        The function returns a dictionary containing the server response.

        **Note:** This function can be used to disconnect the user's Google account from their Amino account, for example if
        the user wants to use a different Google account or does not want to use Google to sign in anymore.
        """
        return await self.request.handler(
            method="POST",
            url="/g/s/auth/disconnect",
            data={
                "deviceID": self.device_id,
                "secret": f"0 {password}",
                "type": 30,
                "timestamp": int(time() * 1000),
                }
            )


    @authenticated
    def logout(self) -> None:
        """
        Logs out the user by clearing the session ID and user ID on the client instance.

        :return: None
        :rtype: None
        :raises LoginRequired: If the authentication fails.

        This function first checks if the client is authenticated by checking for a valid session ID. If the client is not
        authenticated, the function raises a `LoginRequired` exception.

        If the client is authenticated, the function clears the session ID and user ID on the client instance, as well as
        other related attributes. This effectively logs out the user.

        The function returns None.

        **Note:** After calling this function, the client will no longer be authenticated and will need to log in again to
        make authenticated API calls.
        """
        for key in ["sid", "userId", "community.userId", "request.sid", "request.userId", "is_authenticated"]:
            setattr(self, key, None)
        return None


    async def register(self, email: str, password: str, username: str, verificationCode: str) -> Authenticate:
        """
        Registers a new account with the provided email, password, username, and verification code.

        :param email: The email address to register the account with.
        :type email: str
        :param password: The password to use for the account.
        :type password: str
        :param username: The username to use for the account.
        :type username: str
        :param verificationCode: The verification code sent to the email address for account activation.
        :type verificationCode: str
        :return: An `Authenticate` object containing the authenticated user's session ID, user ID, and community user ID.
        :rtype: Authenticate

        This method registers a new account with the provided email, password, username, and verification code. The
        verification code is sent to the email address for account activation. The method returns an `Authenticate` object
        containing the authenticated user's session ID and user ID.
        """
        return await self.account.register(
            email=email, 
            password=password,
            username=username,
            verificationCode=verificationCode
            )


    @authenticated
    async def delete_request(self, email: str, password: str) -> ApiResponse:
        """
        Sends a request to delete the authenticated user's account.

        :param email: The email address associated with the account.
        :type email: str
        :param password: The password for the account.
        :type password: str
        :return: An `ApiResponse` object containing the server's response to the delete request.
        :rtype: ApiResponse

        This method sends a request to delete the authenticated user's account. The email and password parameters are used to
        authenticate the request. The method returns an `ApiResponse` object containing the server's response to the delete
        request.
        """
        return await self.account.delete_request(email=email, password=password)


    @authenticated
    async def delete_request_cancel(self, email: str, password: str) -> ApiResponse:
        """
        Cancels a previously requested account deletion for the authenticated user.

        :param email: The email address associated with the account.
        :type email: str
        :param password: The password for the account.
        :type password: str
        :return: An `ApiResponse` object containing the server's response to the delete request cancellation request.
        :rtype: ApiResponse

        This method cancels a previously requested account deletion for the authenticated user. The email and password
        parameters are used to authenticate the request. The method returns an `ApiResponse` object containing the server's
        response to the delete request cancellation request.
        """
        return await self.account.delete_request_cancel(email=email, password=password)


    async def check_device(self, device_id: str) -> ApiResponse:
        """
        Checks if the given device ID is valid.

        :param device_id: The ID of the device to check.
        :type device_id: str
        :return: An `ApiResponse` object containing the server's response to the device check request.
        :rtype: ApiResponse

        This method checks if the device ID is valid. The device ID is
        passed as a string argument. The method calls the `check_device` method of the `account` object with the
        `deviceId` parameter set to the given device ID. The result is an `ApiResponse` object that contains the server's
        response to the device check request.

        The method returns the `ApiResponse` object obtained from calling the `check_device` method of the `account`
        object. The response will return a `0` status code if the device ID is valid.
        """
        return await self.account.check_device(deviceId=device_id)


    async def fetch_account(self) -> dict:
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
            await self.request.handler(
                method="GET",
                url=f"/g/s/user-profile/{self.userId}"
                ))
        
        return ApiResponse(await self.request.handler(method="GET", url="/g/s/account")).json()


    @authenticated
    async def upload_image(self, image: str) -> str:
        """
        Uploads an image to amino servers.

        :param image: The base64-encoded image data.
        :type image: str
        :return: The URL of the uploaded image.
        :rtype: str

        This method uploads an image to amino servers. The image data is passed as a string argument. The method calls the
        `upload_image` method of the `account` object with the `image` parameter set to the given image data. The result is
        a `mediaValue` object that contains the URL of the uploaded image.

        The method returns the URL of the uploaded image.
        """
        return await self.account.upload_image(image=image)


    @authenticated
    async def fetch_profile(self) -> UserProfile:
        """
        Fetches the user profile of the authenticated user.

        :return: A `UserProfile` object containing the user's profile information.
        :rtype: UserProfile

        This method fetches the user profile of the authenticated user. The method calls the `fetch_profile` method of the
        `account` object to get the profile information. The result is a `UserProfile` object that contains the user's profile
        information.

        The method returns the `UserProfile` object.
        """
        return await self.account.fetch_profile(self.userId)


    @authenticated
    async def set_amino_id(self, aminoId: str) -> ApiResponse:
        """
        Sets the Amino ID of the authenticated user.

        :param aminoId: The Amino ID to set for the user.
        :type aminoId: str
        :return: An `ApiResponse` object containing the server's response to the set Amino ID request.
        :rtype: ApiResponse

        This method sets the Amino ID of the authenticated user. The Amino ID is passed as a string argument. The method calls
        the `set_amino_id` method of the `account` object with the `aminoId` parameter set to the given Amino ID. The result
        is an `ApiResponse` object that contains the server's response to the set Amino ID request.

        The method returns the `ApiResponse` object obtained from calling the `set_amino_id` method of the `account` object.
        The response will return a `0` status code if the Amino ID is set successfully.
        """
        return await self.account.set_amino_id(aminoId=aminoId)


    @authenticated
    async def fetch_wallet(self) -> Wallet:
        """
        Fetches the wallet information for the authenticated user.

        :return: A `Wallet` object containing the user's wallet information.
        :rtype: Wallet

        This method fetches the wallet information for the authenticated user. The wallet information includes the user's
        total number of coins, the number of business coins, and other relevant details. The method calls the `fetch_wallet`
        method of the `account` object. The result is a `Wallet` object that contains the user's wallet information.

        The method returns a `Wallet` object containing the user's wallet information.
        """
        return await self.account.fetch_wallet()


    async def request_security_validation(self, email: str, resetPassword: bool = False) -> ApiResponse:
        """
        Requests security validation for the provided email address.

        :param email: The email address to request security validation for.
        :type email: str
        :param resetPassword: Optional flag to indicate if the user is requesting password reset. Default is False.
        :type resetPassword: bool
        :return: An `ApiResponse` object containing the server's response to the security validation request.
        :rtype: ApiResponse

        This method requests security validation for the provided email address. The email parameter is used to send
        a validation email to the provided email address. If resetPassword parameter is True, then the email will be sent for
        password reset. The method calls the `request_security_validation` method of the `account` object with the `email`
        parameter set to the provided email address and `resetPassword` parameter set to the provided flag. The result is
        an `ApiResponse` object that contains the server's response to the security validation request.

        The method returns an `ApiResponse` object containing the server's response to the security validation request.
        """
        return await self.account.request_security_validation(email=email, resetPassword=resetPassword)


    async def activate_email(self, email: str, code: str) -> ApiResponse:
        """
        Activates the user's email using the provided verification code.

        :param email: The email address to activate.
        :type email: str
        :param code: The verification code sent to the email address for activation.
        :type code: str
        :return: An `ApiResponse` object containing the server's response to the activation request.
        :rtype: ApiResponse

        This method activates the user's email using the provided verification code. The email and verification code
        parameters are used to authenticate the request. The method returns an `ApiResponse` object containing the server's
        response to the activation request.
        """
        return await self.account.activate_email(email=email, code=code)


    @authenticated
    async def reset_password(self, email: str, newPassword: str, code: str) -> ResetPassword:
        """
        Resets the user's password using the provided email, verification code, and new password.

        :param email: The email address associated with the account.
        :type email: str
        :param newPassword: The new password to use for the account.
        :type newPassword: str
        :param code: The verification code sent to the email address for account verification.
        :type code: str
        :return: A `ResetPassword` object containing the user's session ID and user ID.
        :rtype: ResetPassword

        This method resets the user's password using the provided email, verification code, and new password. The email,
        verification code, and new password parameters are used to authenticate the request. The method returns a `ResetPassword`
        object containing the user's session ID and user ID.
        """
        return await self.account.reset_password(email=email, newPassword=newPassword, code=code)
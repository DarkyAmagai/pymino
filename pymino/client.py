from time import time
from typing import Any, Callable, Optional, TypeVar, Union

from .ext.entities import *
from .ext import RequestHandler, Account, Community
from .ext.utilities.generate import device_id as generate_device_id


F = TypeVar("F", bound=Callable[..., Any])

class Client:
    """
    `Client` - This is the main client.

    `**Parameters**``
    - `**kwargs` - any other parameters to use for the client.

    - `device_id` - device id to use for the client.

    - `proxy` - proxy string to use for the client.
    
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
    def __init__(self, **kwargs):
        self._debug:            bool = check_debugger()
        self._is_authenticated: bool = False
        self._userId:           str = None
        self._sid:              str = None
        self._cached:           bool = False
        self.cache:             Cache = Cache("cache")
        self.community_id:      Optional[str] = kwargs.get("comId", kwargs.get("community_id"))
        self.device_id:         Optional[str] = kwargs.get("device_id") or generate_device_id()
        self.request:           RequestHandler = RequestHandler(
                                self,
                                proxy=kwargs.get("proxy")
                                )
        self.account:           Account = Account(
                                session=self.request
                                )
        self.community:         Community = Community(
                                bot=self,
                                session=self.request,
                                community_id=self.community_id
                                )


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
        def wrapper(*args, **kwargs) -> Any:
            try:
                if not args[0].is_authenticated:
                    raise LoginRequired
                return func(*args, **kwargs)
            except AttributeError:
                raise LoginRequired
        return wrapper


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


    def login(
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
        return self.login(email=email, password=password, sid=sid, device_id=device_id, use_cache=use_cache)


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


    def fetch_object_id(self, link: str) -> str:
        """
        Fetches the object ID given a link to the object.

        :param link: The link to the object.
        :type link: str
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: The ID of the object.
        :rtype: str

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        The method caches the object ID for faster access in future calls.

        **Example usage:**

        >>> object_id = client.community.fetch_object_id(link="https://aminoapps.com/p/w2Fs6H")
        >>> print(object_id)
        """

        KEY = str((link, "OBJECT_ID"))
        if not self.cache.get(KEY):
            self.cache.set(KEY, self.request.handler(
                method = "GET",
                url = f"/g/s/link-resolution?q={link}"
                ))
        return LinkInfo(self.cache.get(KEY)).objectId
    

    def fetch_object_info(self, link: str) -> LinkInfo:
        """
        Fetches information about an object given its link.

        :param link: The link to the object.
        :type link: str
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: A LinkInfo object containing information about the object.
        :rtype: LinkInfo

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        The method caches the object information for faster access in future calls.

        `LinkInfo`:

        - `data`: The raw response data from the API.
        - `linkInfoV2`: The link information data.
        - `path`: The path of the object.
        - `extensions`: The extensions data.
        - `objectId`: The ID of the object.
        - `shareURLShortCode`: The short code of the share URL.
        - `targetCode`: The target code.
        - `ndcId`: The NDC ID.
        - `comId`: The community ID.
        - `fullPath`: The full path of the object.
        - `shortCode`: The short code of the object.
        - `objectType`: The type of the object.

        **Example usage:**

        >>> object_info = client.community.fetch_object_info(link="https://aminoapps.com/p/w2Fs6H")
        >>> print(object_info.objectId)
        """

        KEY = str((link, "OBJECT_INFO"))
        if not self.cache.get(KEY):
            self.cache.set(KEY, self.request.handler(
                method = "GET",
                url = f"/g/s/link-resolution?q={link}"
                ))
        return LinkInfo(self.cache.get(KEY))
    
    @authenticated
    def disconnect_google(self, password: str) -> dict:
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
        return self.request.handler(
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


    @authenticated
    def join_community(self, community_id: int, invitationId = None) -> ApiResponse:
        """
        Joins the user to a community with the provided community ID.

        :param community_id: The ID of the community to join.
        :type community_id: int
        :param invitationId: The ID of the invitation link.
        :type invitationId: str
        :return: An ApiResponse object containing the server response.
        :rtype: ApiResponse
        :raises LoginRequired: If the user is not logged in.

        This function first checks if the client is logged in by checking for a valid session ID. If not, it raises a
        LoginRequired exception.

        If the client is logged in, the function sends a POST request to the server to join the specified community.
        The request includes the client's session ID and the ID of the community to join.

        The function returns an ApiResponse object containing the server response.

        **Note:** This function can be used to join the user to a community with the provided community ID. Once joined,
        the user can make API calls related to the community, such as posting or retrieving posts.
        """
        data = {"timestamp": int(time() * 1000)}
        if invitationId:
            data["invitationId"] = invitationId

        return ApiResponse(
            self.request.handler(
                method="POST",
                url=f"/x{community_id}/s/community/join",
                data = data
        ))

    @authenticated
    def leave_community(self, community_id: int) -> ApiResponse:
        """
        Leaves the user from a community with the provided community ID.

        :param community_id: The ID of the community to leave.
        :type community_id: int
        :return: An ApiResponse object containing the server response.
        :rtype: ApiResponse
        :raises LoginRequired: If the user is not logged in.

        This function first checks if the client is logged in by checking for a valid session ID. If not, it raises a
        LoginRequired exception.

        If the client is logged in, the function sends a POST request to the server to leave the specified community.
        The request includes the client's session ID and the ID of the community to leave.

        The function returns an ApiResponse object containing the server response.

        **Note:** This function can be used to leave the user from a community with the provided community ID. Once left,
        the user will no longer have access to the community and will not be able to make API calls related to the community.
        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/x{community_id}/s/community/leave"
            ))

    def fetch_user(self, userId: str) -> UserProfile:
        """
        Fetches the user profile of the user with the provided user ID.

        :param userId: The ID of the user whose profile to fetch.
        :type userId: str
        :return: A UserProfile object representing the user profile.
        :rtype: UserProfile

        This function sends a GET request to the server to fetch the user profile of the user with the provided user ID.
        The request includes the ID of the user to fetch.

        The function returns a UserProfile object representing the user profile. The UserProfile object contains attributes
        such as the user's ID, nickname, avatar URL, and other profile information.

        **Note:** This function can be used to fetch the user profile of a user on Amino. The user profile can be used to
        display information about the user or to make API calls related to the user, such as retrieving the user's posts or
        other information.
        """
        return UserProfile(self.request.handler(
            method="GET",
            url=f"/g/s/user-profile/{userId}"
            ))


    def fetch_community(self, community_id: int) -> CCommunity:
        """
        Fetches the community information for the community with the provided community ID.

        :param community_id: The ID of the community to fetch.
        :type community_id: int
        :return: A CCommunity object representing the community information.
        :rtype: CCommunity

        This function sends a GET request to the server to fetch the community information for the community with the
        provided community ID. The request includes the ID of the community to fetch.

        The function returns a CCommunity object representing the community information. The CCommunity object contains
        attributes such as the members count, the community's layout, and other community information.

        **Note:** This function can be used to fetch the community information for a community on Amino. The community
        information can be used to display information about the community such as the community's name, description, and
        other information.
        """
        return CCommunity(self.request.handler(
            method="GET",
            url=f"/g/s-x{community_id}/community/info"
            ))

    @authenticated
    def joined_communities(self) -> CCommunityList:
        """
        Retrieves the list of communities that the authenticated user has joined.

        :return: The list of communities.
        :rtype: CCommunityList

        This method returns the list of communities that the authenticated user has joined. The list includes information
        such as the community ID, name, description, and theme.

        **Note:** This method requires authentication. If the client is not authenticated, a `LoginRequired` exception will
        be raised.
        """
        return CCommunityList(self.request.handler(
            method="GET",
            url="/g/s/community/joined"
            ))

    @authenticated
    def join_chat(self, chatId: str) -> ApiResponse:
        """
        Joins the authenticated user to a chat thread.

        :param chatId: The ID of the chat thread to join.
        :type chatId: str
        :return: The API response.
        :rtype: ApiResponse

        This method joins the authenticated user to a chat thread. The user must be a member of the community that the chat
        thread belongs to in order to join the thread.

        **Note:** This method requires authentication. If the client is not authenticated, a `LoginRequired` exception will
        be raised.
        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/g/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    @authenticated
    def leave_chat(self, chatId: str) -> ApiResponse:
        """
        Removes the authenticated user from a chat thread.

        :param chatId: The ID of the chat thread to leave.
        :type chatId: str
        :return: The API response.
        :rtype: ApiResponse

        This method removes the authenticated user from a chat thread. The user must be a member of the chat thread in order
        to leave it.

        **Note:** This method requires authentication. If the client is not authenticated, a `LoginRequired` exception will
        be raised.
        """
        return ApiResponse(self.request.handler(
            method="DELETE",
            url=f"/g/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    def register(self, email: str, password: str, username: str, verificationCode: str) -> Authenticate:
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
        return self.account.register(email=email, password=password, username=username, verificationCode=verificationCode)

    @authenticated
    def delete_request(self, email: str, password: str) -> ApiResponse:
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
        return self.account.delete_request(email=email, password=password)

    @authenticated
    def delete_request_cancel(self, email: str, password: str) -> ApiResponse:
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
        return self.account.delete_request_cancel(email=email, password=password)

    def check_device(self, device_id: str) -> ApiResponse:
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
        return self.account.check_device(deviceId=device_id)


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


    @authenticated
    def upload_image(self, image: str) -> str:
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
        return self.account.upload_image(image=image).mediaValue


    @authenticated
    def fetch_profile(self) -> UserProfile:
        """
        Fetches the user profile of the authenticated user.

        :return: A `UserProfile` object containing the user's profile information.
        :rtype: UserProfile

        This method fetches the user profile of the authenticated user. The method calls the `fetch_profile` method of the
        `account` object to get the profile information. The result is a `UserProfile` object that contains the user's profile
        information.

        The method returns the `UserProfile` object.
        """
        return self.account.fetch_profile()


    @authenticated
    def set_amino_id(self, aminoId: str) -> ApiResponse:
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
        return self.account.set_amino_id(aminoId=aminoId)


    @authenticated
    def fetch_wallet(self) -> Wallet:
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


    def request_security_validation(self, email: str, resetPassword: bool = False) -> ApiResponse:
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
        return self.account.request_security_validation(email=email, resetPassword=resetPassword)


    def activate_email(self, email: str, code: str) -> ApiResponse:
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
        return self.account.activate_email(email=email, code=code)


    @authenticated
    def reset_password(self, email: str, newPassword: str, code: str) -> ResetPassword:
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
        return self.account.reset_password(email=email, newPassword=newPassword, code=code)


    @authenticated
    def send_message(self, content: str, chatId: str, **kwargs) -> CMessage:
        """
        Sends a message to a chat thread.

        :param content: The content of the message.
        :type content: str
        :param chatId: The ID of the chat thread to send the message to.
        :type chatId: str
        :param **kwargs: Additional parameters for the message.
        :return: A `CMessage` object containing the details of the sent message.
        :rtype: CMessage

        This method sends a message to a chat thread. The content and chat ID parameters are required. Additional parameters
        can be passed as keyword arguments. The method calls the `PrepareMessage` object's `json` method to prepare the message
        data. The result is a `CMessage` object containing the details of the sent message.
        """
        return CMessage(self.request.handler(
            method="POST", url=f"/g/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content, **kwargs).json()
            ))


    @authenticated
    def edit_profile(
        self,
        nickname: str = None,
        content: str = None,
        icon: str = None,
        backgroundColor: str = None,
        backgroundImage: str = None,
        defaultBubbleId: str = None
        ) -> UserProfile:
        """
        Edits the user's profile.

        :param nickname: The new nickname for the user.
        :type nickname: str
        :param content: The new content for the user's profile.
        :type content: str
        :param icon: The new icon image file for the user.
        :type icon: str
        :param backgroundColor: The new background color for the user's profile.
        :type backgroundColor: str
        :param backgroundImage: The new background image file for the user's profile.
        :type backgroundImage: str
        :param defaultBubbleId: The ID of the default bubble for the user's profile.
        :type defaultBubbleId: str
        :return: The response from the account's `edit_profile` method.
        :rtype: Response

        This method allows the authenticated user to edit their profile settings. Different aspects of the profile can be modified,
        such as the nickname, content, icon, background color, background image, and default bubble. Only the specified parameters will
        be updated. The `userId` parameter is set to the authenticated user's ID automatically.

        **Example usage:**

        To change the nickname and icon for the user:

        >>> response = client.edit_profile(nickname="New Nickname", icon="path/to/icon.jpg")
        ... if response.status == 200:
        ...     print("Profile edited successfully!")
        ... else:
        ...     print("Failed to edit profile.")
        """
        return self.account.edit_profile(userId = self.userId,
                                         nickname = nickname,
                                         content = content,
                                         icon = icon,
                                         backgroundColor = backgroundColor,
                                         backgroundImage = backgroundImage,
                                         defaultBubbleId = defaultBubbleId
                                         )


    @authenticated
    def start_chat(
        self,
        userId: Union[str, list],
        message: str,
        title: str = None,
        content: str = None,
        isGlobal: bool = False,
        publishToGlobal: bool = False
        ) -> ChatThread:
        """
        Starts a chat thread.
        :param userId: The ID or list of IDs of the users to invite to the chat.
        :type userId: Union[str, list]
        :param message: The initial message content.
        :type message: str
        :param title: The title of the chat thread (optional).
        :type title: str, optional
        :param content: Additional content for the message (optional).
        :type content: str, optional
        :param isGlobal: Indicates if the chat is global (optional, default: False).
        :type isGlobal: bool, optional
        :param publishToGlobal: Indicates if the chat should be published globally (optional, default: False).
        :type publishToGlobal: bool, optional
        :return: A `ChatThread` object representing the created chat thread.
        :rtype: ChatThread
        """
        try:
            userIds = [userId] if isinstance(userId, str) else userId
        except Exception as e:
            raise ValueError("Incorrect type for userId. <--- userId can be only a string or a list.") from e

        data = dict(
            title = title,
            inviteeUids = userIds,
            initialMessageContent = message,
            content = content,
            timestamp = int(time() * 1000),
            publishToGlobal = 0
        )

        if isGlobal: data.update({"type": 2, "eventSource": "GlobalComposeMenu"})
        else: data["type"] = 0

        if publishToGlobal: data["publishToGlobal"] = 1

        return ChatThread(
            self.request.handler(method="POST", url="/g/s/chat/thread", data=data)
        )
    
    @authenticated
    def blocker_users(self, start: int = 0, size: int = 25):
        """
        Retrieves a list of users what are blocking the logged account.
        :param start: The index to start retrieving the list from (optional, default: 0).
        :type start: int, optional
        :param size: The number of users to retrieve (optional, default: 25).
        :type size: int, optional
        :return: A list of user IDs representing the blocker users.
        :rtype: list
        """
        return self.request.handler(
            method = "GET",
            url = f"/g/s/block/full-list?start={start}&size={size}"
        )["blockerUidList"]

    def fetch_wall_comments(self, userId: str, sorting: str = "newest", start: int = 0, size: int = 25) -> CommentList:
        """
        Fetches wall comments for a user.

        :param userId: The ID of the user whose wall comments will be fetched.
        :type userId: str
        :param sorting: The sorting method for the comments. Options: "newest" (default), "oldest", "top".
        :type sorting: str, optional
        :param start: The starting index of the comments to fetch (pagination). Default is 0.
        :type start: int, optional
        :param size: The number of comments to fetch (pagination). Default is 25.
        :type size: int, optional
        :return: The list of wall comments for the specified user.
        :rtype: CommentList
        :raises ValueError: If an incorrect sorting method is provided.

        This method retrieves wall comments for a specific user. The comments can be sorted by "newest" (default), "oldest", or "top".
        The `start` parameter specifies the index of the first comment to fetch, while the `size` parameter determines the number of
        comments to retrieve. The comments are returned as a `CommentList` object.

        **Example usage:**

        To fetch the newest 25 wall comments for a user:

        >>> comments = client.fetch_wall_comments(userId="00000000-0000-0000-0000-000000000000")
        >>> for comment in comments:
        ...     print(comment.content)
        """
        if sorting.lower() == "newest": sorting = "newest"
        elif sorting.lower() == "oldest": sorting = "oldest"
        elif sorting.lower() == "top": sorting = "vote"
        else: raise ValueError("Incorrect sorting method.")

        return CommentList(self.request.handler(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}"
        ))
    
    @authenticated
    def delete_message(self, chatId: str, messageId: str):
        """
        Deletes a message in a chat thread.

        :param chatId: The ID of the chat thread where the message is located.
        :type chatId: str
        :param messageId: The ID of the message to delete.
        :type messageId: str
        :return: The API response indicating the success or failure of the deletion.
        :rtype: ApiResponse

        This method allows the authenticated user to delete a specific message in a chat thread. The `chatId` parameter identifies the
        chat thread, while the `messageId` parameter specifies the ID of the message to be deleted.

        **Note:** Only authorized users can delete messages in a chat thread. If the deletion is successful, the API response will indicate
        a successful deletion. Otherwise, an error message will be returned.

        **Example usage:**

        To delete a message with the ID "00000000-0000-0000-0000-000000000000" in a chat thread with the ID "00000000-0000-0000-0000-000000000000":

        >>> response = client.delete_message(chatId="00000000-0000-0000-0000-000000000000", messageId="00000000-0000-0000-0000-000000000000")
        >>> if response.success:
        ...     print("Message deleted successfully!")
        ... else:
        ...     print("Failed to delete message.")
        """
        return ApiResponse(self.request.handler(
            method = "DELETE",
            url = f"/g/s/chat/thread/{chatId}/message/{messageId}"
        ))
    
    @authenticated
    def edit_chat(self,
                  chatId: str,
                  doNotDisturb: bool = None,
                  pinChat: bool = None,
                  title: str = None,
                  icon: str = None,
                  backgroundImage: str = None,
                  content: str = None,
                  announcement: str = None,
                  coHosts: list = None,
                  keywords: list = None,
                  pinAnnouncement: bool = None,
                  publishToGlobal: bool = None,
                  canTip: bool = None,
                  viewOnly: bool = None,
                  canInvite: bool = None,
                  fansOnly: bool = None) -> list:
        """
        Edits the settings of a chat.

        :param chatId: The ID of the chat to be edited.
        :type chatId: str
        :param doNotDisturb: Set to True to enable "Do Not Disturb" mode for the chat, False to disable it. Default is None.
        :type doNotDisturb: bool, optional
        :param pinChat: Set to True to pin the chat, False to unpin it. Default is None.
        :type pinChat: bool, optional
        :param title: The new title for the chat.
        :type title: str, optional
        :param icon: The new icon image file for the chat.
        :type icon: str, optional
        :param backgroundImage: The new background image file for the chat.
        :type backgroundImage: str, optional
        :param content: The new content for the chat.
        :type content: str, optional
        :param announcement: The new announcement for the chat.
        :type announcement: str, optional
        :param coHosts: A list of user IDs to set as co-hosts for the chat.
        :type coHosts: list, optional
        :param keywords: A list of keywords to associate with the chat.
        :type keywords: list, optional
        :param pinAnnouncement: Set to True to pin the announcement, False to unpin it. Default is None.
        :type pinAnnouncement: bool, optional
        :param publishToGlobal: Set to True to publish the chat to the global feed, False to unpublish it. Default is None.
        :type publishToGlobal: bool, optional
        :param canTip: Set to True to enable tipping permissions for the chat, False to disable it. Default is None.
        :type canTip: bool, optional
        :param viewOnly: Set to True to enable view-only mode for the chat, False to disable it. Default is None.
        :type viewOnly: bool, optional
        :param canInvite: Set to True to allow members to invite others to the chat, False to disable it. Default is None.
        :type canInvite: bool, optional
        :param fansOnly: Set to True to enable "Fans Only" mode for the chat, False to disable it. Default is None.
        :type fansOnly: bool, optional
        :return: A list of HTTP status codes for each operation performed during the chat edit.
        :rtype: list

        This method allows the authenticated user to edit various settings of a chat, such as "Do Not Disturb" mode, pinning,
        title, icon, background image, content, announcement, co-hosts, keywords, pinning the announcement, publishing to the
        global feed, tipping permissions, view-only mode, allowing members to invite others, and "Fans Only" mode. Only the
        specified parameters will be updated.

        The function returns a list of HTTP status codes for each operation performed during the chat edit.

        **Example usage:**

        To edit the title and pin the chat:

        >>> response_codes = client.edit_chat(chatId="chat123", title="New Chat Title", pinChat=True)
        >>> if all(code == 200 for code in response_codes):
        ...     print("Chat edited successfully!")
        ... else:
        ...     print("Failed to edit chat.")
        """
        data = {"timestamp": int(time() * 1000)}

        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = self.upload_image(icon)
        if keywords: data["keywords"] = keywords
        if announcement: data["extensions"] = {"announcement": announcement}
        if pinAnnouncement: data["extensions"] = {"pinAnnouncement": pinAnnouncement}
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if publishToGlobal: data["publishToGlobal"] = 0
        if not publishToGlobal: data["publishToGlobal"] = 1

        responses = []

        if doNotDisturb is not None:
            responses.append(ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/member/{self.userId}/alert",
                data = {
                    "alertOption": 2 if doNotDisturb else 1,
                    "timestamp": int(time() * 1000)
                }
            )).status_code)
        
        if pinChat is not None:
            responses.append(ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/{'pin' if pinChat else 'unpin'}"
            )).status_code)
        
        if backgroundImage is not None:
            responses.append(ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/member/{self.userId}/background",
                data = {
                    "media": [100, self.upload_image(backgroundImage), None],
                    "timestamp": int(time() * 1000)
                }
            )).status_code)
        
        if coHosts is not None:
            responses.append(ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/co-host",
                data = {
                    "uidList": coHosts,
                    "timestamp": int(time() * 1000)
                }
            )).status_code)
        
        if viewOnly is not None:
            responses.append(ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/view-only/{'enable' if viewOnly else 'disable'}"
            )).status_code)
        
        if canInvite is not None:
            responses.append(ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/members-can-invite/{'enable' if canInvite else 'disable'}"
            )).status_code)
        
        if canTip is not None:
            responses.append(ApiResponse(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/tipping-perm-status/{'enable' if canTip else 'disable'}"
            ).status_code)
        
        responses.append(ApiResponse(self.request.handler(
            method = "POST",
            url = f"/g/s/chat/thread/{chatId}",
            data = data
        )).status_code)

        return responses
    
    @authenticated
    def follow(self, userId: Union[str, list]):
        """
        Follows a user or a list of users.

        :param userId: The ID of the user or a list of user IDs to follow.
        :type userId: Union[str, list]
        :return: The status code of the API response.
        :rtype: int

        This method allows the authenticated user to follow another user or a list of users. The `userId` parameter can be a single
        user ID (string) or a list of user IDs. If a single user ID is provided, the method will follow that user. If a list of user IDs
        is provided, the method will follow all the users in the list.

        If a single user ID is provided, the function will make a POST request to "/g/s/user-profile/{userId}/member" to follow the user.
        If a list of user IDs is provided, the function will make a POST request to "/g/s/user-profile/{self.userId}/joined" with the
        `targetUidList` parameter set to the list of user IDs and the `timestamp` parameter set to the current timestamp.

        The function returns the status code of the API response.

        **Example usage:**

        To follow a single user:

        >>> response_code = client.follow(userId="user123")
        >>> if response_code == 200:
        ...     print("User followed successfully!")
        ... else:
        ...     print("Failed to follow user.")

        To follow multiple users:

        >>> user_ids = ["user123", "user456", "user789"]
        >>> response_code = client.follow(userId=user_ids)
        >>> if response_code == 200:
        ...     print("Users followed successfully!")
        ... else:
        ...     print("Failed to follow users.")
        """
        if isinstance(userId, str):
            return ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/user-profile/{userId}/member"
            )).status_code
        if isinstance(userId, list):
            return ApiResponse(self.request.handler(
                method = "POST",
                url = f"/g/s/user-profile/{self.userId}/joined",
                data = {
                    "targetUidList": userId,
                    "timestamp": int(time() * 1000)
                }
            )).status_code
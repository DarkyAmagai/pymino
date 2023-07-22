import asyncio
from typing import Optional, Union
from time import time, perf_counter

from .ext.entities import *
from .ext.async_socket import AsyncWSClient
from .ext.utilities.generate import Generator
from .ext.async_community import AsyncCommunity
from .ext.async_global_client import AsyncGlobal
from .ext.utilities.async_request_handler import AsyncRequestHandler


class AsyncBot(AsyncWSClient, AsyncGlobal):
    def __init__(
        self,
        command_prefix: Optional[str] = "!",
        community_id: Union[str, int] = None,
        device_id: Optional[str] = None,
        intents: bool = False,
        online_status: bool = False,
        proxy: Optional[str] = None,
        hash_prefix: Union[str, int] = 19,
        device_key: str = "E7309ECC0953C6FA60005B2765F99DBBC965C8E9",
        signature_key: str  = "DFA5ED192DDA6E88A12FE12130DC6206B1251E44"
        ) -> None:
        self.loop:              asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._cooldown_message  = None
        self._debug:            bool = check_debugger()
        self._intents:          bool = intents
        self._is_ready:         bool = False
        self._userId:           str = None
        self._sid:              str = None
        self._cached:           bool = False
        self.cache:             Cache = Cache("cache")

        self.command_prefix:    Optional[str] = command_prefix
        if self.command_prefix == "":
            raise InvalidCommandPrefix()

        self.community_id:      Union[str, int] = community_id
        self.generate:          Generator = Generator(
                                prefix=hash_prefix,
                                device_key=device_key,
                                signature_key=signature_key
                                )
        self.online_status:     bool = online_status
        self.device_id:         Optional[str] = device_id or self.generate.device_id()
        self.request:           AsyncRequestHandler = AsyncRequestHandler(
                                bot = self,
                                loop = self.loop,
                                proxy=proxy,
                                generator=self.generate
                                )
        self.community:         AsyncCommunity = AsyncCommunity(
                                bot = self,
                                session=self.request,
                                community_id=self.community_id
                                )
        if self.community_id:   self.set_community_id(community_id)

        super().__init__()

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self._debug = value

    @property
    def intents(self) -> bool:
        return self._intents
    
    @intents.setter
    def intents(self, value: bool) -> None:
        self._intents = value

    @property
    def is_ready(self) -> bool:
        return self._is_ready
    
    @is_ready.setter
    def is_ready(self, value: bool) -> None:
        self._is_ready = value


    @property
    def userId(self) -> str:
        return self._userId

    @userId.setter
    def userId(self, value: str) -> None:
        self._userId = value

        
    @property
    def sid(self) -> str:
        return self._sid

    @sid.setter
    def sid(self, value: str) -> None:
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


    async def authenticate(self, email: str, password: str, device_id: str=None) -> dict:
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


    def run(self, email: str=None, password: str=None, sid: str=None, device_id: str=None, use_cache: bool=True) -> None:
        self.loop.run_until_complete(self.__run__(email=email, password=password, sid=sid, device_id=device_id, use_cache=use_cache))


    async def __run__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        sid: Optional[str] = None,
        device_id: Optional[str] = None,
        use_cache: bool = True
    ) -> None:
        """Used internally by the `run` method to log in to the client and start running it."""
        if not sid and not all([email, password]):
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

        return await self._run(response)


    async def _run(self, response: dict) -> dict:
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
        self.is_authenticated: bool = True

        if hasattr(self.request, "email") and self._cached:
            cache_login(email=self.request.email, device=self.device_id, sid=self.sid)

        if not self.is_ready:
            self._is_ready = True
            await self.run_forever()


    async def fetch_account(self) -> dict:
        self.profile: UserProfile = UserProfile(
            await self.request.handler(
                method="GET",
                url=f"/g/s/user-profile/{self.userId}"
                ))
        
        return ApiResponse(await self.request.handler(method="GET", url="/g/s/account")).json()
    

    def set_community_id(self, community_id: Union[str, int]) -> int:
        try:
            if community_id is not None and not isinstance(community_id, int):
                community_id = int(community_id)
        except VerifyCommunityIdIsCorrect as e:
            raise VerifyCommunityIdIsCorrect from e

        self.community_id = community_id
        self.community.community_id = community_id

        return community_id


    async def ping(self) -> float:
        try:
            start = perf_counter()
            await self.request.handler(method="GET", url="/g/s/account")
            end = perf_counter()
            elapsed_time_ms = (end - start) * 1000
            return round(elapsed_time_ms, 2)
        except Exception as e:
            raise PingFailed from e

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
        data = {
                "address": None,
                "latitude": 0,
                "longitude": 0,
                "mediaList": None,
                "eventSource": "UserProfileView",
                "timestamp": int(time() * 1000),
        }

        if nickname: data['nickname'] = nickname
        if icon: data['icon'] = self.upload_image(icon) # Human is gay.
        if content: data['content'] = content
        if backgroundColor:
            data["extensions"] = {
                "style": {
                    "backgroundColor": backgroundColor
                    if backgroundColor.startswith("#")
                    else f"#{backgroundColor}"
                }
            }

        if backgroundImage:
            data["extensions"] = {
                "style": {
                    "backgroundMediaList": [
                        [100, self.upload_image(backgroundImage), None, None, None]
                    ]
                }
            }
        if defaultBubbleId:
            data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        return UserProfile(self.request.handler(
            method = "POST", url = f"/g/s/user-profile/{self.userId}",
            data = data
        ))
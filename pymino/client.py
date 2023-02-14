from time import time
from ujson import loads
from base64 import b64decode
from functools import reduce
from colorama import Fore, Style
from typing import Callable, Optional, Union


from .ext.entities.handlers import check_debugger
from .ext.entities.userprofile import UserProfile
from .ext import RequestHandler, Account, Community
from .ext.entities.messages import CMessage, PrepareMessage
from .ext.utilities.generate import device_id as generate_device_id
from .ext.entities.exceptions import (
    LoginFailed, LoginRequired, MissingEmailPasswordOrSid, VerifyCommunityIdIsCorrect
    )
from .ext.entities.general import (
    ApiResponse, Authenticate, CCommunity, CCommunityList, ResetPassword, Wallet
    )

class Client():
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
        for key, value in kwargs.items(): setattr(self, key, value)
        self.debug:             bool = check_debugger()
        self.is_authenticated:  bool = False
        self.userId:            str = None
        self.sid:               str = None
        self.community_id:      Optional[str] = kwargs.get("comId") or kwargs.get("community_id")
        self.device_id:         Optional[str] = kwargs.get("device_id") or generate_device_id()
        self.request:           RequestHandler = RequestHandler(
                                self,
                                proxy=kwargs.get("proxy")
                                )
        self.account:           Account = Account(
                                session=self.request
                                )
        self.community:         Community = Community(
                                bot = self,
                                session=self.request,
                                community_id=self.community_id
                                )

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
        from pymino import Client

        client = Client()

        client.fetch_community_id("https://aminoapps.com/c/CommunityName")
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
        from pymino import Client

        client = Client()

        client.set_community_id(123456789)
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

    def authenticated(func: Callable):
        def wrapper(*args, **kwargs):
            if not args[0].is_authenticated: raise LoginRequired
            return func(*args, **kwargs)
        return wrapper
    
    def authenticate(self, email: str, password: str, device_id: str=None) -> dict:
        """
        `authenticate` - authenticates the bot.

        [This is used internally.]

        `**Parameters**`
        - `email` - The email to use to login.
        - `password` - The password to use to login.
        - `device_id` - The device id to use to login.

        """
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
                "deviceID": device_id or self.device_id,
                "email": email,
                "v": 2,
                "clientCallbackURL": "narviiapp://default"
                }
            )).json()

    def login(self, email: str=None, password: str=None, sid: str=None, device_id: str=None) -> dict:
        """
        `login` - logs in to the client.

        `**Parameters**`
        - `email` - The email to use to login. Defaults to `None`.
        - `password` - The password to use to login. Defaults to `None`.
        - `sid` - The sid to use to login. Defaults to `None`.
        - `device_id` - The device id to use to login. Defaults to `None`.

        `**Example**`
        ```python
        from pymino import Client

        client = Client()

        client.run(email="email", password="password")
        ```
        """
        if email and password:

            for key, value in {"email": email, "password": password}.items():
                setattr(self.request, key, value)

            response: dict = self.authenticate(email=email, password=password, device_id=device_id)

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
        self.is_authenticated:  bool = True

        if self.debug:
            print(f"{Fore.MAGENTA}Logged in as {self.profile.username} ({self.profile.userId}){Style.RESET_ALL}")

        return response

    @authenticated
    def disconnect_google(self, password: str) -> dict:
        """
        `disconnect_google` - Disconnects the google account from the client account.

        `**Parameters**`
        - `password` - The password of the amino account.

        `**Example**`

        ```python
        from pymino import Client

        client = Client()

        client.disconnect_google(password="sUp3rS3cr3tP4ssw0rd")
        
        ```
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
        `logout` - Log out of the client.

        `**Example**`
        ```python
        from pymino import Client

        client = Client()

        client.logout()
        ```
        """
        for key in ["sid", "userId", "community.userId", "request.sid", "request.userId", "is_authenticated"]:
            setattr(self, key, None)
        return None

    @authenticated
    def join_community(self, community_id: int) -> ApiResponse:
        """
        `join_community` - Joins a community.

        `**Parameters**``
        - `community_id` - The community id to join.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.join_community(community_id=1)
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.

        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/x{community_id}/s/community/join"
            ))

    @authenticated
    def leave_community(self, community_id: int) -> ApiResponse:
        """
        `leave_community` - Leaves a community.

        `**Parameters**``
        - `community_id` - The community id to leave.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.leave_community(community_id=1)
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/x{community_id}/s/community/leave"
            ))

    def fetch_user(self, userId: str) -> UserProfile:
        """
        `fetch_user` - Fetches a user profile.

        `**Parameters**``
        - `userId` - The user id to fetch.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.fetch_user(userId="userId")
        ```

        `**Returns**``
        - `UserProfile` - The user profile object.

        """
        return UserProfile(self.request.handler(
            method="GET",
            url=f"/g/s/user-profile/{userId}"
            ))

    def fetch_community(self, community_id: int) -> CCommunity:
        """
        `fetch_community` - Fetches a community.

        `**Parameters**``
        - `community_id` - The community id to fetch.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.fetch_community(community_id=1)
        ```

        `**Returns**``
        - `CCommunity` - The community object.
        """
        return CCommunity(self.request.handler(
            method="GET",
            url=f"/g/s-x{community_id}/community/info"
            ))

    @authenticated
    def joined_communities(self) -> CCommunityList:
        """
        `joined_communities` - Fetches the communities the client has joined.

        `**Parameters**``
        - `None`

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.joined_communities()
        ```

        `**Returns**``
        - `CCommunityList` - The community list object.
        """
        return CCommunityList(self.request.handler(
            method="GET",
            url="/g/s/community/joined"
            ))

    @authenticated
    def join_chat(self, chatId: int) -> ApiResponse:
        """
        `join_chat` - Joins a chat.

        `**Parameters**``
        - `chatId` - The chat id to join.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.join_chat(chatId=1)
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return ApiResponse(self.request.handler(
            method="POST",
            url=f"/g/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    @authenticated
    def leave_chat(self, chatId: int) -> ApiResponse:
        """
        `leave_chat` - Leaves a chat.

        `**Parameters**``
        - `chatId` - The chat id to leave.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.leave_chat(chatId=1)
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return ApiResponse(self.request.handler(
            method="DELETE",
            url=f"/g/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    def register(self, email: str, password: str, username: str, verificationCode: str) -> Authenticate:
        """
        `register` - Registers an account.

        `**Parameters**``
        - `email` - The email of the account.
        - `password` - The password of the account.
        - `username` - The username of the account.
        - `verificationCode` - The verification code of the account.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.register(email="email", password="password", username="username", verificationCode="verificationCode")
        ```

        `**Returns**``
        - `Authenticate` - The authenticate object.
        """
        return self.account.register(email=email, password=password, username=username, verificationCode=verificationCode)

    @authenticated
    def delete_request(self, email: str, password: str) -> ApiResponse:
        """
        `delete_request` - Deletes an account.

        `**Parameters**``
        - `email` - The email of the account.
        - `password` - The password of the account.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.delete_request(email="email", password="password")
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.delete_request(email=email, password=password)

    @authenticated
    def delete_request_cancel(self, email: str, password: str) -> ApiResponse:
        """
        `delete_request_cancel` - Cancels a delete request.

        `**Parameters**``
        - `email` - The email of the account.
        - `password` - The password of the account.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.delete_request_cancel(email="email", password="password")
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.delete_request_cancel(email=email, password=password)

    def check_device(self, device_id: str) -> ApiResponse:
        """
        `check_device` - Checks if a device id is valid.

        `**Parameters**``
        - `device_id` - The device id to check.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.check_device(device_id="device_id")
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.check_device(deviceId=device_id)

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

    def upload_image(self, image: str) -> ApiResponse:
        """
        `upload_image` - Uploads an image.

        `**Parameters**``
        - `image` - The image to upload.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.upload_image(image="image")
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.upload_image(image=image)

    def fetch_profile(self) -> UserProfile:
        """
        `fetch_profile` - Fetches the profile of the client.

        `**Parameters**``
        - `None`

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.fetch_profile()
        ```

        `**Returns**``
        - `UserProfile` - The profile of the client.
        """
        return self.account.fetch_profile()

    @authenticated
    def set_amino_id(self, aminoId: str) -> ApiResponse:
        """
        `set_amino_id` - Sets the amino id of the client.

        `**Parameters**``
        - `aminoId` - The amino id to set.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.set_amino_id(aminoId="aminoId")
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.set_amino_id(aminoId=aminoId)

    @authenticated
    def fetch_wallet(self) -> Wallet:
        """
        `fetch_wallet` - Fetches the wallet of the client.

        `**Parameters**``
        - `None`

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.fetch_wallet()
        ```

        `**Returns**``
        - `Wallet` - The wallet of the client.
        """
        return self.account.fetch_wallet()

    def request_security_validation(self, email: str, resetPassword: bool = False) -> ApiResponse:
        """
        `request_security_validation` - Requests a security validation.

        `**Parameters**``
        - `email` - The email of the account.
        - `resetPassword` - Whether or not to reset the password.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.request_security_validation(email="email", resetPassword=True)
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.request_security_validation(email=email, resetPassword=resetPassword)

    def activate_email(self, email: str, code: str) -> ApiResponse:
        """
        `activate_email` - Activates an email.

        `**Parameters**``
        - `email` - The email of the account.
        - `code` - The code of the account.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.activate_email(email="email", code="code")
        ```

        `**Returns**``
        - `ApiResponse` - The response of the request.
        """
        return self.account.activate_email(email=email, code=code)

    @authenticated
    def reset_password(self, email: str, new_password: str, code: str) -> ResetPassword:
        """
        `reset_password` - Resets a password.

        `**Parameters**``
        - `email` - The email of the account.
        - `new_password` - The new password of the account.
        - `code` - The code of the account.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.reset_password(email="email", new_password="new_password", code="code")
        ```

        `**Returns**``
        - `ResetPassword` - The response of the request.
        """
        return self.account.reset_password(email=email, newPassword=new_password, code=code)

    @authenticated
    def send_message(self, content: str, chatId: str, **kwargs) -> CMessage:
        """
        `send_message` - Sends a message.

        `**Parameters**``
        - `content` - The message to send.
        - `chatId` - The chat id to send the message to.
        - `**kwargs` - The additional parameters.

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.send_message(content="message", chatId="chatId")
        ```

        `**Returns**``
        - `CMessage` - The message that was sent.
        """
        return CMessage(self.session.handler(
            method="POST", url=f"/g/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content, **kwargs).json()
            ))
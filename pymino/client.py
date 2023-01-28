from time import time
from typing import Optional
from requests import Session as HTTPClient

from .ext.entities import *
from .ext.utilities import *
from .ext import RequestHandler, Account, Community

class Client():
    """
    `Client` - This is the self client.

    `**Parameters**``
    - `**kwargs` - Any other parameters to use for the bot.

        - `device_id` - The device id to use for the bot.

        - `proxy` - The proxy to use for the bot. `proxy` must be `str`.

    `**Example**``
    ```python
    from pymino import Client

    bot = Bot()

    bot.run(sid="sid")
    ```
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.debug:             bool = check_debugger()
        self.authenticated:     bool = False
        self.userId:            str = None
        self.sid:               str = None
        self.community_id:      Optional[str] = kwargs.get("comId") or kwargs.get("community_id")
        self.device_id:         Optional[str] = kwargs.get("device_id") or device_id()
        self.session:           HTTPClient = HTTPClient()
        self.request:           RequestHandler = RequestHandler(
                                self,
                                session=self.session,
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

        bot = Client()

        bot.fetch_community_id("https://aminoapps.com/c/CommunityName")
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

        bot = Client()

        bot.set_community_id(123456789)
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
            if not args[0].authenticated: raise LoginRequired
            return func(*args, **kwargs)
        return wrapper
    
    def login(self, email: str, password: str, device_id: Optional[str] = None) -> ApiResponse:
        """
        `login` - Login to the client.

        `**Parameters**``
        - `email` - The email to login with.
        - `password` - The password to login with.
        - `device_id` - The device id to use for login.

        `**Example**``
        ```python
        from pymino import Client

        bot = Client()

        bot.login(email="email", password="password")
        ```
        """
        return self.__login__(self.request.handler(
            method="POST",
            url="/g/s/auth/login",
            data={
                "email": email,
                "v": 2,
                "secret": f"0 {password}",
                "deviceID": device_id or self.device_id,
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
                }))

    def __login__(self, response: dict) -> ApiResponse:
        if response["api:statuscode"] != 0: input(response), exit()

        if not hasattr(self, "profile"): 
            self.profile:       UserProfile = UserProfile(response)

        self.sid:               str = response['sid']
        self.userId:            str = self.profile.userId
        self.community.userId:  str = self.userId
        self.request.sid:       str = self.sid
        self.request.userId:    str = self.userId
        self.authenticated:     bool = True

        return ApiResponse(response)

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

    def fetch_account(self) -> ApiResponse:
        """
        `fetch_account` - Fetches the account of the client.

        `**Parameters**``
        - `None`

        `**Example**``
        ```python
        from pymino import Client

        client = Client()

        client.fetch_account()
        ```

        `**Returns**``
        - `dict` - The account of the client.

        """
        return self.account.fetch_account()

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
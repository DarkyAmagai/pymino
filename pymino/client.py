from os import path
from json import loads
from time import localtime, time, timezone
from threading import Thread as threadIt
from typing import BinaryIO, Optional

from ._websocket import WSClient, EventHandler

from .ext.http_client import *
from .ext.utilities import *
from .ext.objects import *

class Client(WSClient, EventHandler):
    """
    `Client` is the main class for the wrapper.

    `**Example**`
    ```python
    from pymino import Client

    client = Client()
    client.login(email="email", password="password")
    client.run()
    ```

    `**Parameters**`
    - `debug` - Whether to print debug messages or not. Defaults to `False`.


    """
    def __init__(self, debug: bool=False, proxies: Optional[str]=None, deviceId: Optional[str]=None) -> None:
        WSClient.__init__(self, client=self, debug=debug)
        self._sid: Optional[str] = None
        self._auid: Optional[str] = None
        self._secret: Optional[str] = None
        self.debug = debug
        self.proxies = proxies

        self.deviceId: str = deviceId if deviceId is not None else generate_device_id()

    @property
    def sid(self) -> str:
        """
        `Client.sid` Session Id
        
        `**Example**` `>>> client.sid`
        
        `**Returns**`
        - `str` - Session Id
        
        """
        return self._sid

    @sid.setter
    def sid(self, sid: str) -> None:
        """
        `Client.sid` Session Id
        
        `**Example**` `>>> client.sid = "sid"`
        
        `**Parameters**`
        - `sid` - Session Id
            
        """
        for key, value in zip(["sid", "_sid"], [sid, sid]):
            self.__dict__[key], httpx_handler.sid = value, value
            
    @property
    def auid(self) -> str:
        """
        `Client.auid` User Id
            
        `**Example**` `>>> client.auid`
        
        `**Returns**`
        - `str` - User Id
        
        """
        return self._auid

    @auid.setter
    def auid(self, auid: str) -> None:
        """
        `Client.auid` User Id

        `**Example**` `>>> client.auid = "auid"`

        `**Parameters**`
        - `auid` - User Id

        """
        for key, value in zip(["auid", "_auid"], [auid, auid]):
            self.__dict__[key], httpx_handler.auid = value, value

    @property
    def secret(self) -> str:
        """
        `Client.secret` Secret

        `**Example**` `>>> client.secret`

        `**Returns**`
        - `str` - Secret

        """
        return self._secret

    @secret.setter
    def secret(self, secret: str) -> None:
        """
        `Client.secret` Secret

        `**Example**` `>>> client.secret = "secret"`

        `**Parameters**`
        - `secret` - Secret

        """
        self._secret = secret

    @property
    def profile(self) -> User:
        """
        `Client.profile` Profile

        `**Example**` `>>> client.profile`

        `**Returns**`
        - `User` - User Object

        """
        return self._profile

    @profile.setter
    def profile(self, profile: User) -> None:
        """
        `Client.profile` Profile

        `**Example**` `>>> client.profile = User()`

        `**Parameters**`
        - `profile` - User Object

        """
        self._profile = profile
        
    def login(self, email: str, password: str, deviceId: str=None) -> User:
        """
        `Client.login` Login to Amino

        `**Example**` 
        
        ```python
        from pymino import Client

        client = Client()

        client.login(email="email", password="password")
        ```
        """

        session = self.check_for_session(email)
        if session is not None:
            return User(session)

        if session is None:
            response = httpx_handler(proxies=self.proxies).handler(
                method="POST", endpoint="/g/s/auth/login",
                data={
                    "email": email,
                    "v": 2,
                    "secret": "0 {}".format(password),
                    "deviceID": deviceId if deviceId is not None else self.deviceId,
                    "clientType": 100,
                    "action": "normal",
                    "timestamp": int(time() * 1000)
                })

        if response is None: return None

        for key, value in zip(["sid", "auid", "secret"], [response["sid"], response["auid"], response["secret"]]):
            setattr(self, key, value)

        self.store_session(email, password, deviceId)

        self.profile = User(response)
        return User(response)

    def logout(self) -> None:
        """
        `Client.logout` Logout from Amino

        `**Example**` `>>> client.logout()`

        """

        for key, value in zip(
            ["sid", "auid", "secret"], [None, None, None]):
            setattr(self, key, value)
        return None
            

    def run(self, email: str=None, password: str=None, sid: str=None) -> None:
        """
        `Client.run` Run Websocket Client

        `**Example**` `>>> client.run()`

        """

        if sid is not None: self.sid = sid
        if email is not None and password is not None:
            self.login(email, password)
        if self.sid is None: return None
        threadIt(target=self.connect).start()

    def authenticate(self) -> dict:
        """
        `Client.authenticate` Authenticate Session
        
        `**Example**` `>>> client.authenticate()`
        
        `**Returns**`
        - `dict` - Response
        
        """

        if self.sid is None: return None
        return httpx_handler(proxies=self.proxies).handler(
            method="GET", endpoint=f"/g/s/account")

    def secret_auth(self, email: str, password: str, secret: str, deviceId: str=None) -> dict:
        """
        `Client.secret_auth` Secret Authentication

        `**Example**` `>>> client.secret_auth(email="email@example.com", password="password", secret="secret")`

        `**Parameters**`
        - `email` - Email
        - `password` - Password
        - `secret` - Secret
        - `deviceId` - Device ID

        `**Returns**`
        - `dict` - Response

        """

        response = httpx_handler(proxies=self.proxies).handler(
            method="POST", endpoint=f"/g/s/auth/login",
            data={
                "secret": secret,
                "deviceID": deviceId if deviceId is not None else self.deviceId,
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
            })

        if response is None: return None

        for key, value in zip(["sid", "auid", "secret"], [response["sid"], response["auid"], secret]):
            setattr(self, key, value)

        if (email is not None and password is not None):
            self.update_session(email=email, password=password, sid=self.sid, auid=self.auid, secret=self.secret)

        return response

    def fetch_user(self, userId: str) -> User:
        """
        `Client.fetch_user` Fetch User
        
        `**Example**` `>>> client.fetch_user(userId="userId")`
        
        `**Parameters**`
        - `userId` - User Id
        
        `**Returns**`
        - `User` - User Object
        
        """
        return User(httpx_handler(proxies=self.proxies).handler(
            method="GET", endpoint=f"/g/s/user-profile/{userId}"))

    def edit_profile(self, nickname: str=None, content: str=None, icon: str=None) -> User:
        """
        `Client.edit_profile` Edit Profile

        `**Example**` `>>> client.edit_profile(nickname="nickname", content="content", icon=open("icon.png", "rb"))`

        `**Parameters**`
        - `nickname` - Nickname
        - `content` - Content
        - `icon` - Icon

        `**Returns**`
        - `User` - User Object

        """
        profile_updates = {
            "nickname": nickname,
            "content": content,
            "icon": icon
        }

        data={"timestamp": int(time() * 1000)}
        for key, value in profile_updates.items():
            if value is not None:
                if key == "icon":
                    data["icon"]=self.upload_media(value, 1)
                else:
                    data[key]=value

        return User(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/g/s/user-profile/{self.auid}", data))

    def join_community(self, community_id: str) -> Response:
        """
        `Client.join_community` Join Community
        
        `**Example**` `>>> client.join_community(community_id="communityId")`
        
        `**Parameters**`
        - `community_id` - Community Id
        
        `**Returns**`
        - `Response` - Response Object
        
        """
        return Response(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/x{community_id}/s/community/join"))

    def leave_community(self, community_id: str) -> Response:
        """
        `Client.leave_community` Leave Community
        
        `**Example**` `>>> client.leave_community(community_id="communityId")`
        
        `**Parameters**`
        - `community_id` - Community Id
        
        `**Returns**`
        - `Response` - Response Object
        
        """
        return Response(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/x{community_id}/s/community/leave"))

    def join_chat(self, chatId: str) -> Response:
        """
        `Client.join_chat` Join Chat
        
        `**Example**` `>>> client.join_chat(chatId="chatId")`
        
        `**Parameters**`
        - `chatId` - Chat Id
        
        `**Returns**`
        
        - `Response` - Response Object
        
        """
        return Response(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/g/s/chat/thread/{chatId}/member/{self.auid}"))

    def leave_chat(self, chatId: str) -> Response:
        """
        `Client.leave_chat` Leave Chat

        `**Example**` `>>> client.leave_chat(chatId="chatId")`

        `**Parameters**`
        - `chatId` - Chat Id

        `**Returns**`
        - `Response` - Response Object

        """

        return Response(httpx_handler(proxies=self.proxies).handler(
            "DELETE", f"/g/s/chat/thread/{chatId}/member/{self.auid}"))

    def fetch_community(self, community_id: str) -> Community:
        """
        `Client.fetch_community` Fetch Community

        `**Example**` `>>> client.fetch_community(community_id="communityId")`

        `**Parameters**`
        - `community_id` - Community Id

        `**Returns**`
        - `Community` - Community Object

        """

        return Community(httpx_handler(proxies=self.proxies).handler(
            "GET", f"/g/s-x{community_id}/community/info"), True)

    def joined_communities(self) -> Community:
        """
        `Client.joined_communities` Joined Communities

        `**Example**` `>>> client.joined_communities()`

        `**Returns**`
        - `Community` - Community Object

        """

        return Community(httpx_handler(proxies=self.proxies).handler(
            "GET", f"/g/s/community/joined"), True)

    def fetch_followers(self, userId: str, start: int=0, size: int=25) -> User:
        """
        `Client.fetch_user_followers` Fetch User Followers
        
        `**Example**` `>>> client.fetch_user_followers(userId="userId")`
        
        `**Parameters**`
        - `userId` - User Id
        
        `**Returns**`
        - `User` - User Object
        
        """

        return User(httpx_handler(proxies=self.proxies).handler(
            "GET", f"/g/s/user-profile/{userId}/member?start={start}&size={size}"), True)

    def fetch_following(self, userId: str, start: int=0, size: int=25) -> User:
        """
        `Client.fetch_user_following` Fetch User Following

        `**Example**` `>>> client.fetch_user_following(userId="userId")`

        `**Parameters**`
        - `userId` - User Id

        `**Returns**`
        - `User` - User Object

        """

        return User(httpx_handler(proxies=self.proxies).handler(
            "GET", f"/g/s/user-profile/{userId}/joined?start={start}&size={size}"), True)

    def search_community(self, query: str, start: int=0, size: int=25) -> Community:
        """
        `Client.search_community` Search Community
        
        `**Example**` `>>> client.search_community(query="query")`
        
        `**Parameters**`
        - `query` - Query
        
        `**Returns**`
        - `Community` - Community Object

        """
        return Community(httpx_handler(proxies=self.proxies).handler(
            "GET", f"/g/s/community/search?q={query}&language=en&completeKeyword=1&start={start}&size={size}"), True)
    
    def send_message(self, chatId: str, message: str, messageType: int=0) -> Response:
        """
        `Client.send_message` Send Message
        
        `**Example**` `>>> client.send_message(chatId="chatId", message="message")`

        `**Parameters**`
        - `chatId` - Chat Id
        - `message` - Message
        - `messageType` - Message Type
        
        `**Returns**`
        - `Response` - Response Object
        
        """
        return Response(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/g/s/chat/thread/{chatId}/message",
            data={
                "type": messageType,
                "content": message,
                "timestamp": int(time() * 1000)
            }))
    
    def delete_message(self, chatId: str, message_id: str) -> Response:
        """
        `Client.delete_message` Delete Message
        
        `**Example**` `>>> client.delete_message(chatId="chatId", message_id="messageId")`

        `**Parameters**`
        - `chatId` - Chat Id
        - `message_id` - Message Id
        
        `**Returns**`
        - `Response` - Response Object
        
        """

        return Response(httpx_handler(proxies=self.proxies).handler(
            "DELETE", f"/g/s/chat/thread/{chatId}/message/{message_id}"))
    
    def verify_password(self, password: str) -> Response:
        """
        `Client.verify_password` Verify Password
        
        `**Example**` `>>> client.verify_password(password="password")`
        
        `**Parameters**`
        - `password` - Password
        
        `**Returns**`
        - `Response` - Response Object
        
        """

        return Response(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/g/s/auth/verify-password",
            data={
                "deviceID": self.deviceId,
                "secret": "0 {}".format(password),
                "timestamp": int(time() * 1000)
            }))
    
    def request_security_validation(self, email: str, deviceId: str=None, reset_password: bool=False, verify_info_key: str=None) -> Response:
        """
        `Client.request_security_validation` Request Security Validation
        
        `**Example**` `>>> client.request_security_validation(email="email")`
        
        `**Parameters**`
        
        - `email` - Email
        - `deviceId` - Device Id (Optional)
        - `reset_password` - Reset Password (Optional)
        - `verify_info_key` - Verify Info Key (Optional)
        
        `**Returns**`
        - `Response` - Response Object
        
        """

        data={
            "type": 1,
            "identity": email,
            "deviceID": deviceId if deviceId else self.deviceId,
            "timestamp": int(time() * 1000)
        }
        keys = {
            reset_password: {
                "level": 2,
                "purpose": "reset-password"
            },
            verify_info_key: {
                "verifyInfoKey": verify_info_key
            }
        }
        for key, value in keys.items():
            if key: data.update(value)
            
        return Response(httpx_handler(proxies=self.proxies).handler("POST", f"/g/s/auth/request-security-validation", data))

    def check_security_validation(self, email: str, code: str, deviceId: str=None) -> Response:
        """
        `Client.check_security_validation` Check Security Validation

        `**Example**` `>>> client.check_security_validation(email="email", code="code")`

        `**Parameters**`
        - `email` - Email
        - `code` - Code
        - `deviceId` - Device Id (Optional)

        `**Returns**`
        - `Response` - Response Object

        """

        return Response(httpx_handler(proxies=self.proxies).handler(
            "POST", f"/g/s/auth/check-security-validation",
            data={
            "validationContext": {
                "type": 1,
                "identity": email,
                "data": {
                    "code": code
                }
            },
            "deviceID": deviceId if deviceId else self.deviceId,
            "timestamp": int(time() * 1000)
            }))

    def register_check(self, email: str, deviceId: str=None) -> Response:
        """
        `Client.register_check` Register Check
        
        `**Example**` `>>> client.register_check(email="email")`
        
        `**Parameters**`
        
        - `email` - Email
        - `deviceId` - deviceId (Optional)

        `**Returns**`
        - `Response` - Response Object

        """

        return Response(httpx_handler(proxies=self.proxies).handler("POST",
        f"/g/s/auth/register-check",
        data={
        "deviceID": deviceId if deviceId else self.deviceId,
        "email": email,
        "timestamp": int(time() * 1000)
        }))
    
    def update_email(self, email: str, password: str, new_code: str, deviceId: str=None) -> Response:
        """
        `Client.update_email` Update Email

        `**Example**` `>>> client.update_email(email="email", password="password", new_code="new_code")`

        `**Parameters**`
        - `email` - Email
        - `password` - Password
        - `new_code` - New Code
        - `deviceId` - Device Id (Optional)

        `**Returns**`
        - `Response` - Response Object

        """

        return Response(httpx_handler(proxies=self.proxies).handler("POST",
        f"/g/s/auth/update-email",
        data={
            "deviceID": deviceId if deviceId else self.deviceId,
            "secret": f"0 {password}",
            "newValidationContext": {
                "identity": email,
                "data": {
                    "code": new_code
                    },
                "level": 1,
                "type": 1,
                "deviceID": deviceId if deviceId else self.deviceId,
                },
            "timestamp": int(time() * 1000)
        }))
    
    def get_global_link(self, userId: str) -> str:
        """
        `Client.get_global_link` Get Global Link
        
        `**Example**` `>>> client.get_global_link(userId="userId")`
        
        `**Parameters**`
        - `userId` - User Id
        
        `**Returns**`
        - `str` - Global Link
        
        """

        return f'https://aminoapps.com/u/{self.fetch_user(userId).aminoId}'
    
    def get_from_link(self, link: str) -> linkInfoV2:
        """
        `Client.get_from_link` Get From Link
        
        `**Example**` `>>> client.get_from_link(link="link")`
        
        `**Parameters**`
        - `link` - Link
        
        `**Returns**`
        - `linkInfoV2` - Link Info V2
        
        """

        return linkInfoV2(
            httpx_handler(proxies=self.proxies).handler(
                method="GET", endpoint=f"/g/s/link-resolution?q={link}"
                ))
    
    def upload_media(self, file: BinaryIO, file_type: str) -> Response:
        """
        `Client.upload_media` Upload Media
        
        `**Example**` `>>> client.upload_media(file=open("file", "rb"), file_type=1)`

        `**Parameters**`
        - `file` - File
        - `file_type` - File Type

        `**Returns**`
        - `Response` - mediaValue Response Object

        """

        file_types = {"image": "image/jpg", "audio": "audio/aac"}
        return Response(
            httpx_handler(proxies=self.proxies).handler(
                method="POST", endpoint=f"/g/s/media/upload",
                data=file.read(), type=file_types[file_type]
                ))

    def device_validation(self, deviceId: str) -> Response:
        """
        `Client.device_validation` Device Validation

        `**Example**` `>>> client.device_validation(deviceId="deviceId")`

        `**Parameters**`
        - `deviceId` - Device Id

        `**Returns**`
        - `Response` - Response Object

        """
        return Response(httpx_handler(proxies=self.proxies).handler(
            method="POST", endpoint=f"/g/s/device",
                data={
                    "deviceID": deviceId,
                    "clientType": 100,
                    "timezone": -timezone // 1000,
                    "locale": localtime()[0],
                    "timestamp": int(time() * 1000)
                    }
                ))

    def register_account(self, nickname: str, email: str, password: str, deviceId: str, code: str) -> User:
        """
        `Client.register_account` Register Account

        `**Example**` `>>> client.register_account(nickname="nickname", email="email", password="password", deviceId="deviceId", code="code")`

        `**Parameters**`
        - `nickname` - Nickname
        - `email` - Email
        - `password` - Password
        - `deviceId` - Device Id
        - `code` - Code

        `**Returns**`
        - `User` - User Object

        """

        return User(httpx_handler(proxies=self.proxies).handler(
            method="POST", endpoint=f"/g/s/auth/register",
                data={
                    "secret": f"0 {password}",
                    "deviceID": deviceId,
                    "email": email,
                    "clientType": 100,
                    "nickname": nickname,
                    "validationContext": {
                        "data": {
                            "code": code
                        },
                        "type": 1,
                        "identity": email
                        },
                    "type": 1,
                    "identity": email,
                    "timestamp": int(time() * 1000)
                    }
                ))

    def wallet_info(self) -> Wallet:
        """
        `Client.wallet_info` Wallet Info
        
        `**Example**` `>>> client.wallet_info()`
        
        `**Returns**`
        - `Wallet` - Wallet Object
        
        """

        return Wallet(httpx_handler(proxies=self.proxies).handler(
            method="GET", endpoint=f"/g/s/wallet"
            ))

    def account_exist_check(self, deviceId: str, secret: str) -> Response:
        """
        `Client.account_exist_check` Account Exist Check
        
        `**Example**` `>>> client.account_exist_check(deviceId="deviceId", secret="secret")`
            
            `**Parameters**`
            - `deviceId` - Device Id
            - `secret` - Secret
            
            `**Returns**`
            - `Response` - Response Object
            
            """

        return Response(httpx_handler(proxies=self.proxies).handler(
            method="POST", endpoint=f"/g/s/auth/account-exist-check",
                data={
                    "deviceID": deviceId,
                    "secret": secret,
                    "clientType": 100,
                    "timestamp": int(time() * 1000)
                }
            ))

    def verify_account(self, verify_info_key: str, code: str, email: str, deviceId: str) -> Response:
        """
        `Client.verify_account` Verify Account

        `**Example**` `>>> client.verify_account(verify_info_key="verify_info_key", code="code", email="email", deviceId="deviceId")`

        `**Parameters**`
        - `verify_info_key` - Verify Info Key
        - `code` - Code
        - `email` - Email
        - `deviceId` - Device Id

        `**Returns**`
        - `Response` - Response Object

        """

        return Response(httpx_handler(proxies=self.proxies).handler("POST",
        f"/g/s/auth/verify-account",
        data={
            "verifyInfoKey": verify_info_key,
            "validationContext": {
                "data": {
                    "code": code
                },
                "type": 1,
                "identity": email
            },
            "deviceID": deviceId
        }))

    def invite_chat(self, userId: str or list, chatId: str) -> Response:
        """
        `Client.invite_chat` Invite Chat
        
        `**Example**` `>>> client.invite_chat(userId="userId", chatId="chatId")`
            
            `**Parameters**`
            - `userId` - User Id
            - `chatId` - Chat Id
            
            `**Returns**`
            - `Response` - Response Object
            
            """

        return Response(httpx_handler(proxies=self.proxies).handler("POST",
        f"/g/s/chat/thread/{chatId}/member/invite",
        data={
            "userIds": userId if isinstance(userId, list) else [userId],
            "timestamp": int(time() * 1000)
        }))

    def update_session(self, email: str, password: str=None, deviceId: str=None, sid: str=None, auid: str=None, secret: str=None) -> None:
        """
        `Client.update_session` Update Session
        
        `**Example**` `>>> client.update_session(email="email", password="password", deviceId="deviceId", sid="sid", auid="auid", secret="secret")`

        `**Parameters**`
        - `email` - Email
        - `password` - Password
        - `deviceId` - Device Id
        - `sid` - Sid
        - `auid` - Auid
        - `secret` - Secret

        `**Returns**`
        - `None` - None

        """

        sessions=self.stored_sessions()
        session = [session for session in sessions if email == session["email"]][0]
        if session is None: return None
        for key, value in zip(
            ["password", "deviceId", "sid", "auid", "secret"],
            [password, deviceId, sid, auid, secret]):
            if value is not None: session[key]=value
        return open(self.session_directory, "w").write(dumps(sessions, indent=4))

    def stored_sessions(self) -> list:
        """
        `Client.stored_sessions` Stored Sessions
            
        `**Example**` `>>> client.stored_sessions()`
        
        `**Returns**`
        - `list` - List of Sessions
        
        """

        self.session_directory = fetch_sessions()
        if path.exists(self.session_directory):
            return loads(open(self.session_directory, "r").read())
        else:
            open(self.session_directory, "w").write(dumps([], indent=4))
            return []

    def return_session(self, email: str) -> dict:
        """
        `Client.return_session` Return Session
        
        `**Example**` `>>> client.return_session(email="email")`
        
        `**Parameters**`
        - `email` - Email
        
        `**Returns**`
        - `dict` - Session
        
        """

        for session in self.stored_sessions():
            if email == session["email"]: return session
        return None

    def store_sessions(self, session: dict) -> None:
        """
        `Client.store_sessions` Store Sessions
        
        `**Example**` `>>> client.store_sessions(session="session")`
        
        `**Parameters**`
        - `session` - Session
        
        `**Returns**`
        - `None` - None
        
        """

        return open(self.session_directory, "w").write(dumps(session, indent=4))

    def store_session(self, email: str, password: str, deviceId: str) -> dict:
        """
        `Client.store_session` Store Session
        
        `**Example**` `>>> client.store_session(email="email", password="password", deviceId="deviceId")`

        `**Parameters**`
        - `email` - Email
        - `password` - Password
        - `deviceId` - Device Id

        `**Returns**`
        - `dict` - Session

        """
        sessions=self.stored_sessions()
        sessions.append({
            "email": email,
            "password": password,
            "deviceId": deviceId,
            "sid": self.sid,
            "auid": self.auid,
            "secret": self.secret
        })
        return self.store_sessions(sessions)
        
    def check_for_session(self, email: str) -> dict:
        """
        `Client.check_for_session` Check For Session
        
        `**Example**` `>>> client.check_for_session(email="email")`
        
        `**Parameters**`
        - `email` - Email
        
        `**Returns**`
        - `dict` - Session
        
        """

        session = self.return_session(email)
        if session is None: return None

        self.sid, self.auid, self.secret = [session["sid"], session["auid"], session["secret"]]
        authenticated = self.authenticate()

        if authenticated is not None:
            self.profile = User(self.fetch_user(self.auid).json)
            return authenticated
        print("Failed to authenticate with stored session, removing session...")
        authenticated=self.secret_auth(email=email, password=session["password"], secret=session["secret"])

        if authenticated is not None:
            self.update_session(email, sid=self.sid)
            self.profile = User(authenticated)
            return authenticated
        
        else:
            print("Failed to authenticate with stored session, removing session...")
            sessions=self.stored_sessions()

            for session in sessions:
                if email == session["email"]: sessions.remove(session)

            self.store_sessions(sessions)
            return None

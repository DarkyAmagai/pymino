from uuid import uuid4
from io import BytesIO
from requests import get
from random import randint
from base64 import b64encode
from time import time, timezone

from typing import BinaryIO, List, Optional, Union

from .entities.threads import CThread, CThreadList
from .entities.userprofile import UserProfile, UserProfileList

from .entities.messages import (
    CMessage, CMessages, PrepareMessage
    )
from .entities.exceptions import (
    InvalidImage, MissingCommunityId,
    MissingTimers, NoDataProvided, NotLoggedIn
    )
from .entities.general import (
    ApiResponse, CBlog, CBlogList, CChatMembers,
    CComment, CCommentList, CCommunity, CCommunityList,
    CheckIn, CommunityInvitation, Coupon, FeaturedBlogs,
    InvitationId, LinkInfo, Notification
    )

class Community:
    """
    `Community` is the class that handles community related actions.
    
    `**Parameters**`

    - `bot` or `client` - the client we are using.

    - `session` - the session we use to make requests.

    - `community_id` - comId to use for the methods.

    ----------------------------
    I'm getting a `NotLoggedIn` error, what is the solution?

    - You need to login to the client before using the specific method.

    ----------------------------

    I'm getting a `MissingCommunityId` error, what is the solution?

    - You need to pass the community id to the method or set the community id in the `Community` class.

    ```python
    >>> SET COMMUNITY ID (RECOMMENDED FOR SINGLE-COMMUNITY BOTS)

    from pymino import Bot as Client

    client = Client()

    client.fetch_community_id(community_link="https://aminoapps.com/c/your-community-link")
    # or if you already have the community id
    client.set_community_id(community_id=123456789)

    >>> PASS COMMUNITY ID TO METHOD (RECOMMENDED FOR MULTI-COMMUNITY BOTS)

    client.community.join_community(comId=123456789)
    ```
    ----------------------------
    Does every function require the community id?
    - No, some functions don't require the community id. If the function doesn't require the community id, it will be stated in the documentation.

    ----------------------------
    How do I get a (chat, blog, user) id?
    - You can get the id by using the `fetch_object_id` method.

    ```python
    >>> GET OBJECT ID (CHAT, BLOG, USER) FROM LINK 

    from pymino import Bot as Client # This can be Client or Bot, it's whatever you want to use.

    client = Client()

    objectId = client.community.fetch_object_id(link="https://aminoapps.com/p/w2Fs6H")
    print(objectId) # OUTPUT: The object id from the link.
    ```
    ----------------------------
    How do I send a message to a chat?
    - You can send a message to a chat by using the `send_message` method.

    ```python
    >>> SEND MESSAGE TO CHAT

    from pymino import Bot as Client # This can be Client or Bot, it's whatever you want to use.

    client = Client()

    client.community.send_message(
        chatId="000000-0000-0000-000000",
        content="Hello, world!",
        comId=123456789 # We need to pass the community id because we didn't set it in the Community class.
    )
    ```
    ----------------------------
    How do I send an image to a chat?
    - You can send an image to a chat by using the `send_image` method.
    - It's very similar to the `send_message` method.
    - You'll need either image url or path to the image.

    ```python
    >>> SEND IMAGE TO CHAT

    from pymino import Bot as Client # This can be Client or Bot, it's whatever you want to use.

    client = Client()

    client.community.send_image(
        chatId="000000-0000-0000-000000",
        image="https://i.imgur.com/your-image.png", # or image="path/to/image.png"
        comId=123456789 # We need to pass the community id because we didn't set it in the Community class.
    )
    ```
    ----------------------------
    """
    def __init__(self, bot, session, community_id: Union[str, int] = None) -> None:
        self.bot                = bot
        self.session            = session       
        self.community_id:      Union[str, int] = community_id
        self.userId:            Optional[str] = None
        if self.userId is None: return 

    def community(func):
        def community_func(*args, **kwargs):
            if not args[0].userId: raise NotLoggedIn
            if not any([args[0].community_id, kwargs.get("comId")]):
                raise MissingCommunityId
            return func(*args, **kwargs)
        return community_func

    @community
    def invite_code(self, comId: Union[str, int] = None) -> CommunityInvitation:
        """
        `invite_code` is the method that gets the invite code for the community.

        `**Parameters**`

        - None

        `**Example**`

        ```python

        from pymino import Bot

        bot = Bot()

        bot.community.invite_code()

        bot.run(sid=sid)
        ```
        """
        return CommunityInvitation(self.session.handler(
            method = "POST",
            url = f"/g/s-x{self.community_id if comId is None else comId}/community/invitation",
            data = {"duration": 0, "force": True, "timestamp": int(time() * 1000)}
            ))

    @community
    def fetch_object(self, objectId: str, object_type: int = 0, target_code: int = 1, comId: Union[str, int] = None) -> LinkInfo:
        """
        `fetch_object` is the method that fetches the object info from an object id.

        `**Parameters**`

        - `objectId` - The object id to fetch the object info from.

        - `object_type` - The object type. Defaults to `0`.

        - `target_code` - The target code. Defaults to `1`.

        `**Example**`

        ```python

        from pymino import Bot

        bot = Bot()

        bot.community.fetch_object(objectId = "74b46f21-39b2-4a11-97aa-d68135925703")

        bot.run(sid=sid)
        ```
        """
        return LinkInfo(self.session.handler(
            method = "POST",
            url = f"/g/s-x{self.community_id if comId is None else comId}/link-resolution",
            data = {"objectId": objectId, "targetCode": target_code, "objectType": object_type, "timestamp": int(time() * 1000)}
            ))
    
    def fetch_object_id(self, link: str) -> str:
        """
        `fetch_object_id` is the method that fetches the object id from a link.

        `**Parameters**`

        - `link` - The link to fetch the object id from.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()
        objectId = bot.community.fetch_object_id(link = "https://www.aminoapps.com.com/p/as12s34S")
        bot.run(sid=sid)
        ```
        """
        return LinkInfo(self.session.handler(
            method = "GET",
            url = f"/g/s/link-resolution?q={link}"
            )).objectId

    def fetch_object_info(self, link: str) -> LinkInfo:
        """
        `fetch_object_info` is the method that fetches the object info from a link.

        `**Parameters**`

        - `link` - The link to fetch the object info from.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()
        objectInfo = bot.community.fetch_object_info(link = "https://www.aminoapps.com.com/p/as12s34S")
        bot.run(sid=sid)
        ```
        """
        return LinkInfo(self.session.handler(
            method = "GET",
            url = f"/g/s/link-resolution?q={link}"
            ))
    
    def fetch_community(self, comId: Union[str, int] = None) -> CCommunity:
        """
        `fetch_community` is the method that fetches the community info.

        `**Parameters**`

        - `comId` - The community id to fetch. If not provided, it will use the community id in the client.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_community(comId = "123456789").json()
        bot.run(sid=sid)
        ```
        """
        return CCommunity(self.session.handler(
            method = "GET",
            url = f"/g/s-x{self.community_id if comId is None else comId}/community/info"
            ))
    
    def joined_communities(self, start: int = 0, size: str = 50) -> CCommunityList:
        """
        `joined_communities` is the method that fetches the communities the user has joined.

        `**Parameters**`

        - `start` - The start index of the community list. Defaults to `0`.

        - `size` - The size of the community list. Defaults to `50`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.joined_communities().json
        bot.run(sid=sid)
        ```
        """
        return CCommunityList(self.session.handler(
            method = "GET",
            url = f"/g/s/community/joined?v=1&start={start}&size={size}"
            ))

    @community
    def join_community(self, comId: Union[str, int] = None) -> ApiResponse:
        """
        `join_community` is the method that joins the community.
        
        `**Parameters**`

        - `comId` - The community id to join. If not provided, it will use the community id in the client.
        
        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.join_community()
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/community/join", 
            data={"timestamp": int(time() * 1000)}
            ))
    
    def fetch_invitationId(self, invite_code: str) -> str:
        """
        `fetch_invitationId` is the method that fetches the invitation id from the invite code.

        `**Parameters**`

        - `invite_code` - The invite code to fetch the invitation id from.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()

        invitationId = bot.community.fetch_invitationId(invite_code="123456789")

        bot.run(sid=sid)
        ```

        """
        return InvitationId(self.session.handler(
            method = "GET",
            url = f"/g/s/community/link-identify?q={invite_code}"
            )).invitationId
    
    @community
    def join_community_by_code(self, invite_code: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `join_community_by_code` is the method that joins the community by invite code.

        `**Parameters**`

        - `invite_code` - The invite code to join the community.

        - `comId` - The community id to join. If not provided, it will use the community id in the client.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.join_community_by_code(invite_code = "123456789", comId = "123456789")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/join",
            data = {
                "invitationId": self.fetch_invitationId(invite_code=invite_code),
                "timestamp": int(time() * 1000)
                }
            ))

    @community
    def leave_community(self, comId: Union[str, int] = None) -> ApiResponse:
        """
        `leave_community` is the method that leaves the community.

        `**Parameters**`

        - `comId` - The community id to leave. If not provided, it will use the community id in the client.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.leave_community()
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/leave", 
            data={"timestamp": int(time() * 1000)}
            ))

    @community
    def request_join(self, message: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `request_join` is the method that requests to join the community.

        `**Parameters**`

        - `message` - The message to send with the request.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.request_join("Hello, I would like to join your community!")
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/community/membership-request", 
            data={"message": message, "timestamp": int(time() * 1000)}
            ))

    @community
    def flag_community(self, reason: str, flagType: int, comId: Union[str, int] = None) -> ApiResponse:
        """
        `flag_community` is the method that flags the community.

        `**Parameters**`
        - `reason` - The reason for flagging the community.
        - `flagType` - The type of flag to use. Defaults to `1`.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.flag_community("This community is spamming.")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/flag", 
            data={
            "objectId": self.community_id,
            "objectType": 16,
            "flagType": flagType,
            "message": reason,
            "timestamp": int(time() * 1000)
            }))

    @community
    def check_in(self, timezone: Optional[int] = -300, comId: Union[str, int] = None) -> CheckIn:
        """
        `check_in` is the method that checks in to the community.

        `**Parameters**`

        - `timezone` - The timezone to use. Defaults to `-300`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.check_in()
        bot.run(sid=sid)
        ```
        """
        return CheckIn(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/check-in",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}
            ))

    @community
    def play_lottery(self, timezone: Optional[int] = -300, comId: Union[str, int] = None) -> ApiResponse:
        """
        `play_lottery` is the method that plays the lottery in the community.

        `**Parameters**`

        - `timezone` - The timezone to use. Defaults to `-300`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.play_lottery()
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/check-in/lottery",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}
            ))
    
    @community
    def online_status(self, status: Optional[int] = 1, comId: Union[str, int] = None) -> ApiResponse:
        """
        `online_status` is the method that sets the online status of the community.

        `**Parameters**`

        `status` - The status to set. Defaults to `1`.

            1 - Online
            2 - Offline
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()

        bot.community.online_status(status=2) # Sets the status to offline

        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{self.userId}/online-status",
            data={"status": status, "timestamp": int(time() * 1000)}
            ))

    @community
    def fetch_new_user_coupon(self, comId: Union[str, int] = None) -> Coupon:
        """
        `fetch_new_user_coupon` is the method that fetches the new user coupon.

        `**Parameters**`

        - None
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_new_user_coupon()
        bot.run(sid=sid)
        ```
        """
        return Coupon(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/coupon/new-user-coupon"
            ))

    @community
    def fetch_notifications(self, size: Optional[int] = 25, comId: Union[str, int] = None) -> Notification:
        """
        `fetch_notifications` is the method that fetches the notifications.

        `**Parameters**`

        - `size` - The amount of notifications to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_notifications()
        bot.run(sid=sid)
        ```
        """
        return Notification(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/notification?pagingType=t&size={size}"
            ))

    @community
    def fetch_user(self, userId: str, comId: Union[str, int] = None) -> UserProfile:
        """
        `fetch_user` is the method that fetches a user.

        `**Parameters**`

        - `userId` - The user ID to fetch.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_user("5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfile(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}"
            ))

    @community
    def fetch_users(self, type: Optional[str] = "recent", start: Optional[int] = 0, size: Optional[int] = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        `fetch_users` is the method that fetches users.

        `**Parameters**`

        - `type` - The type of users to fetch. Defaults to `recent`. `[recent, leaders, curators]`

        - `start` - The starting point to fetch users from. Defaults to `0`.

        - `size` - The amount of users to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_users()
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile?type={type}&start={start}&size={size}"
            ))

    @community
    def fetch_online_users(self, start: Optional[int] = 0, size: Optional[int] = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        `fetch_online_users` is the method that fetches online users.

        `**Parameters**`

        - `start` - The starting point to fetch users from. Defaults to `0`.

        - `size` - The amount of users to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
            
        bot = Bot()
        bot.community.fetch_online_users()
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/live-layer?topic=ndtopic:x{self.community_id if comId is None else comId}:online-members&start={start}&size={size}"
            ))

    @community
    def fetch_followers(self, userId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        `fetch_followers` is the method that fetches followers.

        `**Parameters**`

        - `userId` - The user ID to fetch followers from.

        - `start` - The starting point to fetch followers from. Defaults to `0`.

        - `size` - The amount of followers to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_followers(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/member?start={start}&size={size}"
            ))

    @community
    def fetch_following(self, userId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        `fetch_following` is the method that fetches following.

        `**Parameters**`

        - `userId` - The user ID to fetch following from.

        - `start` - The starting point to fetch following from. Defaults to `0`.

        - `size` - The amount of following to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_following(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/joined?start={start}&size={size}"
            ))

    @community
    def fetch_chat(self, chatId: str, comId: Union[str, int] = None) -> CThread:
        """
        `fetch_chat` is the method that fetches a chat.

        `**Parameters**`

        - `chatId` - The chat ID to fetch.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_chat(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CThread(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}"
            ))
    
    @community
    def fetch_chat_mods(self, chatId: str, comId: Union[str, int] = None, moderators: Optional[str] = "all") -> List[str]:
        """
        `fetch_chat_mods` is the method that fetches chat moderators.
        
        `**Parameters**`

        - `chatId` - The chat ID to fetch moderators from.

        - `moderators` - The type of moderators to fetch.
            - `all` - Merges `co-hosts` and `host`.
            - `co-hosts` - Co-hosts.
            - `host` - Host.

        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_chat_mods(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        response = self.fetch_chat(chatId=chatId, comId=comId)

        mods_map = {
            "all": list(response.extensions.coHost) + [response.hostUserId],
            "co-hosts": list(response.extensions.coHost),
            "host": [response.hostUserId]
            }

        try:
            return mods_map[moderators]
        except KeyError as e:
            raise ValueError("Invalid value for `moderators`.") from e

    @community
    def fetch_chats(self, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CThreadList:
        """
        `fetch_chats` is the method that fetches chats.

        `**Parameters**`

        - `start` - The starting point to fetch chats from. Defaults to `0`.

        - `size` - The amount of chats to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
            
        bot = Bot()
        bot.community.fetch_chats()
        bot.run(sid=sid)
        ```
        """
        return CThreadList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread?type=joined-me&start={start}&size={size}"
            ))

    @community
    def fetch_live_chats(self, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CThreadList:
        """
        `fetch_live_chats` is the method that fetches live chats.

        `**Parameters**`

        - `start` - The starting point to fetch chats from. Defaults to `0`.

        - `size` - The amount of chats to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_live_chats()
        bot.run(sid=sid)
        ```
        """
        return CThreadList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/live-layer/public-live-chats?start={start}&size={size}"
            ))

    @community
    def fetch_public_chats(self, type: str = "recommended", start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CThreadList:
        """
        `fetch_public_chats` is the method that fetches public chats.

        `**Parameters**`

        - `type` - The type of chats to fetch. Defaults to `recommended`.

        - `start` - The starting point to fetch chats from. Defaults to `0`.

        - `size` - The amount of chats to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_public_chats()
        bot.run(sid=sid)
        ```
        """
        return CThreadList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}"
            ))

    @community
    def fetch_chat_members(self, chatId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CChatMembers:
        """
        `fetch_chat_members` is the method that fetches chat members.

        `**Parameters**`

        - `chatId` - The chat ID to fetch members from.

        - `start` - The starting point to fetch members from. Defaults to `0`.

        - `size` - The amount of members to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_chat_members(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CChatMembers(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2"
            ))

    @community
    def fetch_messages(self, chatId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CMessages:
        """
        `fetch_messages` is the method that fetches messages.

        `**Parameters**`

        - `chatId` - The chat ID to fetch messages from.

        - `start` - The starting point to fetch messages from. Defaults to `0`.

        - `size` - The amount of messages to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_messages(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CMessages(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message?start={start}&size={size}&type=default"
            ))

    @community
    def fetch_blogs(self, size: int = 25, comId: Union[str, int] = None) -> CBlogList:
        """
        `fetch_blogs` is the method that fetches blogs.

        `**Parameters**`

        - `size` - The amount of blogs to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_blogs()
        bot.run(sid=sid)
        ```
        """
        return CBlogList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/feed/blog-all?pagingType=t&size={size}"
            ))
    
    @community
    def fetch_featured_blogs(self, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> FeaturedBlogs:
        """
        `fetch_featured_blogs` is the method that fetches featured blogs.

        `**Parameters**`

        - `start` - The starting point to fetch blogs from. Defaults to `0`.

        - `size` - The amount of blogs to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.run(sid=sid)
        bot.community.fetch_featured_blogs()
        ```
        """
        return FeaturedBlogs(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/feed/featured?start={start}&size={size}"
            ))

    @community
    def fetch_leaderboard(self, leaderboard: int = 1, start: int = 0, size: int = 20, comId: Union[str, int] = None) -> UserProfileList:
        """
        `fetch_leaderboard` is the method that fetches leaderboard.

        `**Parameters**`

        - `leaderboard` - The leaderboard to fetch. Defaults to `1`.

        - `start` - The starting point to fetch users from. Defaults to `0`.

        - `size` - The amount of users to fetch. Defaults to `20`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_leaderboard()
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/community/leaderboard?rankingType={leaderboard}&start={start}&size={size}"
            ))

    @community
    def fetch_comments(self, userId: Optional[str] = None, blogId: Optional[str] = None, wikiId: Optional[str] = None, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CCommentList:
        """
        `fetch_comments` is the method that fetches comments.

        `**Parameters**`

        - `userId` - The user ID to fetch comments from. Defaults to `None`.

        - `blogId` - The blog ID to fetch comments from. Defaults to `None`.

        - `wikiId` - The wiki ID to fetch comments from. Defaults to `None`.

        - `start` - The starting point to fetch comments from. Defaults to `0`.

        - `size` - The amount of comments to fetch. Defaults to `25`.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_comments(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        
        if any([userId, blogId, wikiId]):
            base_endpoint = "/x{}/s/{}/comment?sort=newest&start={}&size={}"
            endpoint_mapping = {
                "userId": "user-profile/{}",
                "blogId": "blog/{}",
                "wikiId": "item/{}"
            }
            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    return CCommentList(self.session.handler(
                        method = "GET",
                        url = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]), start, size)
                        ))
                
        raise NoDataProvided

    @community
    def set_cohost(self, chatId: str, userIds: Union[str, list], comId: Union[str, int] = None) -> ApiResponse:
        """
        `set_cohost` is the method that sets co-host.

        `**Parameters**`

        - `chatId` - The chat ID to set co-host.

        - `userIds` - The user ID to set co-host.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.set_cohost(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", userIds = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/cohost",
            data={"userIds": userIds if isinstance(userIds, list) else [userIds]}
            ))

    @community
    def remove_cohost(self, chatId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `remove_cohost` is the method that removes co-host.

        `**Parameters**`

        - `chatId` - The chat ID to remove co-host.

        - `userId` - The user ID to remove co-host.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.remove_cohost(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/co-host/{userId}"
            ))

    @community
    def follow(self, userId: Union[str, list], comId: Union[str, int] = None) -> ApiResponse:
        """
        `follow` is the method that follows user.

        `**Parameters**`

        - `userId` - The user ID to follow.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.follow(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(
            self.session.handler(
                method="POST",
                url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/{'member' if isinstance(userId, str) else 'joined'}",
                data={
                    "timestamp": int(time()),
                    "targetUidList": userId
                } if isinstance(userId, list) else None
            )
        )

    @community
    def unfollow(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `unfollow` is the method that unfollows user.

        `**Parameters**`

        - `userId` - The user ID to unfollow.
            
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.unfollow(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/member/{self.userId}"
            ))

    @community
    def block(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `block` is the method that blocks user.

        `**Parameters**`

        - `userId` - The user ID to block.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.block(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/block/{userId}"
            ))

    @community
    def unblock(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `unblock` is the method that unblocks user.

        `**Parameters**`

        - `userId` - The user ID to unblock.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.unblock(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/block/{userId}"
            ))

    @community
    def post_blog(self, title: str, content: str, comId: Union[str, int] = None) -> CBlog:
        """
        `post_blog` is the method that posts blog.

        `**Parameters**`

        - `title` - The title of the blog.

        - `content` - The content of the blog.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.post_blog(title = "title", content = "content")
        bot.run(sid=sid)
        ```
        """
        return CBlog(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog",
            data = {
                "content": content,
                "title": title,
                "timestamp": int(time() * 1000)
                }))
        
    @community
    def delete_blog(self, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_blog` is the method that deletes blog.

        `**Parameters**`

        - `blogId` - The blog ID to delete.
            
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_blog(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}"
            ))

    @community
    def post_wiki(self, title: str, content: str, image: str, comId: Union[str, int] = None) -> ApiResponse: #NOTE: DOESN'T WORK
        """
        `post_wiki` is the method that posts wiki.

        `**Parameters**`

        - `title` - The title of the wiki.
        - `content` - The content of the wiki.
        - `image` - The image of the wiki. [Optional]
        - `value` - Value rating for the wiki. [Optional]
        - `type` - Type rating for the wiki. [Optional]

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.post_wiki(title = "title", content = "content")
        bot.run(sid=sid)
        ```
        """
        image = self.__handle_media__(image, media_value=True)
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/item",
            data = {
            "extensions": {
                "fansOnly": False,
		        "props": []
	        },
	        "address": None,
            "content": content,
            "icon": image,
            "keywords": "",
            "label": title,
            "latitude": 0,
            "longitude": 0,
            "mediaList": [
                [100, image, None]
            ],
            "eventSource": "GlobalComposeMenu",
            "timestamp": int(time() * 1000)
            }))

    @community
    def delete_wiki(self, wikiId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_wiki` is the method that deletes wiki.

        `**Parameters**`

        - `wikiId` - The wiki ID to delete.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_wiki(wikiId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/item/{wikiId}"
            ))

    @community
    def delete_comment(self, commentId: str, userId: Optional[str] = None, blogId: Optional[str] = None, wikiId: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_comment` is the method that deletes comment.

        `**Parameters**`

        - `commentId` - The comment ID to delete.

        - `userId` - The user ID to delete comment. [Optional]

        - `blogId` - The blog ID to delete comment. [Optional]

        - `wikiId` - The wiki ID to delete comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        if any([userId, blogId, wikiId]):
            base_endpoint = "/x{}/s/{}/comment/{}"
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }

            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]), commentId)
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment/{commentId}"

        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = endpoint
            ))
    
    @community
    def delete_wiki_comment(self, commentId: str, wikiId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_wiki_comment` is the method that deletes wiki comment.

        `**Parameters**`

        - `commentId` - The comment ID to delete.

        - `wikiId` - The wiki ID to delete comment.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_wiki_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", wikiId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.delete_comment(commentId = commentId, wikiId = wikiId, comId = comId)

    @community
    def delete_profile_comment(self, commentId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_profile_comment` is the method that deletes profile comment.

        `**Parameters**`

        - `commentId` - The comment ID to delete.

        - `userId` - The user ID to delete comment.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_profile_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.delete_comment(commentId, userId=userId, comId=comId)
    
    @community
    def delete_blog_comment(self, commentId: str, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_blog_comment` is the method that deletes blog comment.

        `**Parameters**`

        - `commentId` - The comment ID to delete.

        - `blogId` - The blog ID to delete comment.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_blog_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.delete_comment(commentId, blogId=blogId, comId=comId)
    
    @community
    def comment(self, content: str, userId: Optional[str] = None, blogId: Optional[str] = None, wikiId: Optional[str] = None, image: Optional[str] = None, comId: Union[str, int] = None) -> CComment:
        """
        `comment` is the method that comments.

        `**Parameters**`

        - `content` - The content of the comment.

        - `userId` - The user ID to comment. [Optional]

        - `blogId` - The blog ID to comment. [Optional]

        - `wikiId` - The wiki ID to comment. [Optional]

        - `image` - The image of the comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.comment(content = "content")
        bot.run(sid=sid)
        ```
        """
        data = {"timestamp": int(time() * 1000), "content": content}

        if any([userId, blogId, wikiId]):
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }
            base_endpoint = "/x{}/s/{}/comment"
            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]))
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment"

        if image:
            data["mediaList"] = [[100,self.__handle_media__(media=image, media_value=True), None, None, None, None]]

        return CComment(self.session.handler(
            method = "POST",
            url = endpoint,
            data = data
            ))
    
    @community
    def comment_on_blog(self, content: str, blogId: str, image: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `comment_on_blog` is the method that comments on blog.

        `**Parameters**`

        - `content` - The content of the comment.

        - `blogId` - The blog ID to comment.

        - `image` - The image of the comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.comment_on_blog(content = "content", blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.comment(content = content, blogId = blogId, image = image, comId = comId)
    
    @community
    def comment_on_wiki(self, content: str, wikiId: str, image: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `comment_on_wiki` is the method that comments on wiki.

        `**Parameters**`

        - `content` - The content of the comment.

        - `wikiId` - The wiki ID to comment.

        - `image` - The image of the comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.comment_on_wiki(content = "content", wikiId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.comment(content=content, wikiId=wikiId, image=image, comId=comId)
    
    @community
    def comment_on_profile(self, content: str, userId: str, image: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `comment_on_profile` is the method that comments on profile.

        `**Parameters**`

        - `content` - The content of the comment.

        - `userId` - The user ID to comment.

        - `image` - The image of the comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.comment_on_profile(content = "content", userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.comment(content = content, userId = userId, image = image, comId = comId)
            
    @community
    def like_comment(self, commentId: str, userId: Optional[str] = None, blogId: Optional[str] = None, wikiId: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `like_comment` is the method that likes a comment.

        `**Parameters**`

        - `commentId` - The comment ID to like.

        - `userId` - The user ID to like comment. [Optional]

        - `blogId` - The blog ID to like comment. [Optional]

        - `wikiId` - The wiki ID to like comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
            
        bot = Bot()
        bot.community.like_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        if any([userId, blogId, wikiId]):
            base_endpoint = "/x{}/s/{}/comment/{}/vote"
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }

            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]), commentId)
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment/{commentId}/vote"

        return ApiResponse(self.session.handler(
            method = "POST",
            url = endpoint,
            data = {
            "value": 1,
            "timestamp": int(time() * 1000),
            "eventSource": "CommentDetailView" if userId is None else "UserProfileView"
            }
            ))
    
    @community
    def like_wiki_comment(self, commentId: str, wikiId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `like_wiki_comment` is the method that likes a wiki comment.

        `**Parameters**`

        - `commentId` - The comment ID to like.

        - `wikiId` - The wiki ID to like comment.

        `**Example**`

        ```python
        from pymino import Bot
            
        bot = Bot()
        bot.community.like_wiki_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", wikiId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.like_comment(commentId = commentId, wikiId = wikiId, comId = comId)
    
    @community
    def like_blog_comment(self, commentId: str, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `like_blog_comment` is the method that likes a blog comment.

        `**Parameters**`

        - `commentId` - The comment ID to like.

        - `blogId` - The blog ID to like comment.

        `**Example**`

        ```python
        from pymino import Bot
            
        bot = Bot()
        bot.community.like_blog_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.like_comment(commentId = commentId, blogId = blogId, comId = comId)

    @community
    def like_profile_comment(self, commentId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `like_profile_comment` is the method that likes a profile comment.

        `**Parameters**`

        - `commentId` - The comment ID to like.

        - `userId` - The user ID to like comment.

        `**Example**`

        ```python
        from pymino import Bot
            
        bot = Bot()
        bot.community.like_profile_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.like_comment(commentId = commentId, userId = userId, comId = comId)

    @community
    def unlike_comment(self, commentId: str, userId: Optional[str] = None, blogId: Optional[str] = None, wikiId: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `unlike_comment` is the method that unlikes a comment.

        `**Parameters**`

        - `commentId` - The comment ID to unlike.

        - `userId` - The user ID to unlike comment. [Optional]

        - `blogId` - The blog ID to unlike comment. [Optional]

        - `wikiId` - The wiki ID to unlike comment. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.unlike_comment(commentId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        if any([userId, blogId, wikiId]):
            base_endpoint = "/x{}/s/{}/comment/{}/vote"
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }

            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]), commentId)
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment/{commentId}/vote"

        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = endpoint
            ))

    @community
    def like_blog(self, blogId: str, userId: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `like_blog` is the method that likes a blog.

        `**Parameters**`

        - `blogId` - The blog ID to like.

        - `userId` - The user ID to like blog. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.like_blog(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/vote",
            data = {
                "value": 4,
                "timestamp": int(time() * 1000),
                "eventSource": "UserProfileView" if userId is None else "PostDetailView"
                }))

    @community
    def unlike_blog(self, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `unlike_blog` is the method that unlikes a blog.

        `**Parameters**`

        - `blogId` - The blog ID to unlike.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.unlike_blog(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/vote"
            ))

    @community
    def upvote_comment(self, blogId: str, commentId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `upvote_comment` is the method that upvotes a comment.

        `**Parameters**`

        - `blogId` - The blog ID to upvote comment.

        - `commentId` - The comment ID to upvote.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.upvote_comment(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a", commentId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/comment/{commentId}/vote",
            data = {
                "value": 1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def downvote_comment(self, blogId: str, commentId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `downvote_comment` is the method that downvotes a comment.

        `**Parameters**`

        - `blogId` - The blog ID to downvote comment.

        - `commentId` - The comment ID to downvote.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.downvote_comment(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a", commentId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/comment/{commentId}/vote",
            data = {
                "value": -1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def fetch_blog(self, blogId: str, comId: Union[str, int] = None) -> CBlog:
        """
        `fetch_blog` is the method that fetches a blog's information.

        `**Parameters**`

        - `blogId` - The blog ID to fetch.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_blog(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CBlog(self.session.handler(
            method = "GET", url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}"))

    @community
    def fetch_wiki(self, wikiId: str, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add Wiki class
        """
        `fetch_wiki` is the method that fetches a wiki's information.

        `**Parameters**`

        - `wikiId` - The wiki ID to fetch.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_wiki(wikiId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "GET", url = f"/x{self.community_id if comId is None else comId}/s/item/{wikiId}"))

    @community
    def fetch_quiz(self, quizId: str, comId: str = None):
        """
        `fetch_quiz` is the method that fetches a quiz's information.
        
        `**Parameters**`
        
        - `quizId` - The quiz ID to fetch.
        
        `**Example**`
        
        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.fetch_quiz(quizId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.session.handler(
            method = "GET", url = f"/x{self.community_id if comId is None else comId}/s/blog/{quizId}")

    @community
    def fetch_user(self, userId: str, comId: Union[str, int] = None) -> UserProfile:
        """
        `fetch_user` is the method that fetches user's profile.

        `**Parameters**`

        - `userId` - The user ID to fetch.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_user(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfile(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}?action=visit"
            ))

    @community
    def reply_wall(self, userId: str, commentId: str, message: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `reply_wall` is the method that replies to a comment on user's wall.

        `**Parameters**`

        - `userId` - The user ID to reply.

        - `commentId` - The comment ID to reply.

        - `message` - The message to reply.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.reply_wall(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", commentId = "5f4d2e0e0a0a0a0a0a0a0a0a", message = "Hello!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/comment",
            data = {
                "content": message,
                "stackedId": None,
                "respondTo": commentId,
                "type": 0,
                "eventSource": "UserProfileView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def vote_poll(self, blogId: str, optionId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `vote_poll` is the method that votes on a poll.

        `**Parameters**`

        - `blogId` - The blog ID to vote.

        - `optionId` - The option ID to vote.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.vote_poll(blogId = "5f4d2e0e0a0a0a0a0a0a0a0a", optionId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/poll/option/{optionId}/vote",
            data = {
                "value": 1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def repost(self, content: str = None, blogId: str = None, wikiId: str = None, comId: Union[str, int] = None) -> CBlog:
        """
        `repost` is the method that reposts a blog or wiki.

        `**Parameters**`

        - `content` - The content to repost.

        - `blogId` - The blog ID to repost.

        - `wikiId` - The wiki ID to repost.

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.repost(content = "Great blog!", blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CBlog(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/blog",
            data = {
                "content": content,
                "refObjectId": blogId if blogId is not None else wikiId,
                "refObjectType": 1 if blogId is not None else 2,
                "type": 2,
                "timestamp": int(time() * 1000)
                }))

    @community
    def ban(self, userId: str, reason: str, banType: int = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `ban` is the method that bans a user.

        `**Parameters**`

        - `userId` - The user ID to ban.

        - `reason` - The reason to ban.

        - `banType` - The ban type to ban.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.ban(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", reason = "Bot!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/ban",
            data = {
                "reasonType": banType,
                "note": {
                    "content": reason
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def unban(self, userId: str, reason: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `unban` is the method that unbans a user.

        `**Parameters**`

        - `userId` - The user ID to unban.

        - `reason` - The reason to unban.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.unban(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", reason = "Misclick!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/unban",
            data = {
                "note": {
                    "content": reason
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def strike(self, userId: str, amount: int = 5, title: str = None, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `strike` is the method that strikes a user.

        `**Parameters**`

        - `userId` - The user ID to strike.

        - `amount` -The time of the strike in hours

            `1` - 1 hour
            `2` - 3 hours
            `3` - 6 hours
            `4` - 12 hours
            `5` - 24 hours

        - `title` - Title of the strike.

        - `reason` - The reason to strike.
        
        `amount` - The time of the strike in hours.
        - 1 hour (1)
        - 3 hours (2)
        - 6 hours (3)
        - 12 hours(4)
        - 24 hours (default) (5)

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.strike(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", amount=1, title = "Bot!", reason = "Bot!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/notice",
            data = {
                "uid": userId,
                "title": title,
                "content": reason,
                "attachedObject": {
                    "objectId": userId,
                    "objectType": 0
                },
                "penaltyType": 1,
                "penaltyValue": [3600, 10800, 21600, 43200, 86400][amount - 1 if amount in range(1, 6) else 86400],
                "adminOpNote": {},
                "noticeType": 4,
                "timestamp": int(time() * 1000)
                }))

    @community
    def warn(self, userId: str, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `warn` is the method that warns a user.

        `**Parameters**`

        - `userId` - The user ID to warn.

        - `reason` - The reason to warn.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.warn(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", reason = "Violating community guidelines!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/notice",
            data = {
                "uid": userId,
                "title": "Custom",
                "content": reason,
                "attachedObject": {
                    "objectId": userId,
                    "objectType": 0
                },
                "penaltyType": 0,
                "adminOpNote": {},
                "noticeType": 7,
                "timestamp": int(time() * 1000)
                }))

    @community
    def edit_titles(self, userId: str, titles: list, colors: list, comId: Union[str, int] = None) -> ApiResponse:
        """
        `edit_titles` is the method that edits a user's titles.

        `**Parameters**`

        - `userId` - The user ID to edit titles.

        - `titles` - The titles to edit.

        - `colors` - The colors to edit.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.edit_titles(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", titles=["Bot", "Developer"], colors=["#ff0000", "#00ff00"])
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/admin",
            data = {
                "adminOpName": 207,
                "adminOpValue": {
                    "titles": [{"title": title, "color": color} for title, color in zip(titles, colors)]
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def fetch_mod_history(self, userId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, size: int = 25, comId: Union[str, int] = None) -> ApiResponse:
        """
        `fetch_mod_history` is the method that fetches a user's moderation history.

        `**Parameters**`

        - `userId` - The user ID to fetch moderation history.

        - `blogId` - The blog ID to fetch moderation history.

        - `wikiId` - The wiki ID to fetch moderation history.

        - `quizId` - The quiz ID to fetch moderation history.

        - `fileId` - The file ID to fetch moderation history.

        - `size` - The size of the moderation history.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_mod_history(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "GET", url = f"/x{self.community_id if comId is None else comId}/s/admin/operation",
            params = {
                "objectId": blogId if blogId is not None else wikiId if wikiId is not None else quizId if quizId is not None else fileId if fileId is not None else userId,
                "objectType": 1 if blogId is not None else 2 if wikiId is not None else 3 if quizId is not None else 109 if fileId is not None else 0,
                "pagingType": "t",
                "size": size
                }))

    @community
    def edit_profile(
        self,
        nickname: str = None,
        content: str = None,
        icon: Union[str, BytesIO] = None,
        background_color: str = None,
        background_image: Union[str, BytesIO] = None,
        cover_image: Union[str, BytesIO] = None,
        comId: Union[str, int] = None
        ) -> UserProfile:
        """
        `edit_profile` is the method that edits a user's profile.

        `**Parameters**`

        - `nickname` - The nickname to edit.

        - `content` - The content to edit.

        - `icon` - The icon to edit.

        - `background_color` - The background color to change to. [Example: `#ffffff`]

        - `background_image` - The background image to change to.

        - `cover_image` - The cover image to change to.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.edit_profile(nickname = "Bot", content = "I am a bot!")
        bot.run(sid=sid)
        ```
        """
        data: dict = {"timestamp": int(time() * 1000), "extensions": {}}

        [data.update({key: value}) for key, value in {
            "nickname": nickname,
            "content": content,
            "icon": self.__handle_media__(media=icon, media_value=True) if icon is not None else None,
            "mediaList": [[100, self.__handle_media__(media=cover_image, media_value=True), None, None, None, None]] if cover_image is not None else None
            }.items() if value is not None]

        if background_color:
            data["extensions"]["style"] = {"backgroundColor": background_color}

        if background_image:
            data["extensions"]["style"] = {"backgroundMediaList": [[100, self.__handle_media__(media=background_image, media_value=True), None, None, None, None]]}

        return UserProfile(
            self.session.handler(
                method = "POST",
                url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{self.userId}",
                data=data
                ))

    @community
    def fetch_user_blogs(self, userId: str, start: int = 0, size: int = 5, comId: Union[str, int] = None) -> CBlogList:
        """
        `fetch_user_blogs` is the method that fetches a user's blogs.

        `**Parameters**`

        - `userId` - The user ID to fetch blogs.

        - `start` - The start of the blogs.

        - `size` - The size of the blogs.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_user_blogs(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CBlogList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/blog?type=user&q={userId}&start={start}&size={size}"
            ))

    @community
    def fetch_user_wikis(self, userId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add WikiList
        """
        `fetch_user_wikis` is the method that fetches a user's wikis.

        `**Parameters**`

        - `userId` - The user ID to fetch wikis.

        - `start` - The start of the wikis.

        - `size` - The size of the wikis.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.fetch_user_wikis(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```

        """
        return ApiResponse(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}"
            ))

    @community
    def fetch_user_check_ins(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `fetch_user_check_ins` is the method that fetches a user's check-ins.

        `**Parameters**`

        - `userId` - The user ID to fetch check-ins.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_user_check_ins(userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/check-in/stats/{userId}?timezone=-300"
            ))
            
    @community
    def send_embed(self, chatId: str, title: str, content: str, image: BinaryIO = None, link: Optional[str] = None, comId: Union[str, int] = None) -> CMessage:
        """
        `send_embed` is the method that sends an embed to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the embed to.

        - `title` - The title of the embed.

        - `content` - The content of the embed.

        - `image` - The image of the embed.

        - `link` - The link of the embed. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_embed(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", title = "Hello World!", content = "This is an embed!")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content = "[c]",
            attachedObject={
                "title": title,
                "content": content,
                "mediaList": [[100, self.__handle_media__(media=image, media_value=True), None]],
                "link": link
                }).json()))

    @community
    def send_link_snippet(self, chatId: str, image: str, message: str = "[c]", link: str = "ndc://user-me", mentioned: list = None, comId: Union[str, int] = None) -> CMessage:
        """
        `send_link_snippet` is the method that sends a link snippet to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the link snippet to.

        - `content` - The message of the link snippet.

        - `image` - The image of the link snippet.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_link_snippet(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", content = "Hello World!", image = "https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        bot.run(sid=sid)
        ```
        """
        if mentioned is None:
            mentioned = []

        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=message,
            extensions = {
            "linkSnippetList": [{
                "link": link,
                "mediaType": 100,
                "mediaUploadValue": self.encode_media(
                    self.__handle_media__(
                        media=image,
                        content_type="image/jpg",
                        media_value=False
                    )
                ),
                "mediaUploadValueContentType": "image/png",
                "mentionedArray": [
                {"uid": self.userId}
                ] if isinstance(mentioned, str) else [{"uid": i} for i in mentioned
                ] if isinstance(mentioned, list) else None
            }]
            }).json()))

    @community
    def send_message(self, chatId: str, content: str, comId: Union[str, int] = None) -> CMessage:
        """
        `send_message` is the method that sends a message to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the message to.

        - `content` - The message to send.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_message(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", content = "Hello World!")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content).json()
            ))

    @community
    def send_image(self, chatId: str, image: BinaryIO = None, comId: Union[str, int] = None) -> CMessage:
        """
        `send_image` is the method that sends an image to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the image to.
        - `image` - The image to send.
        - `comId` - The community ID to send the image to. [Optional]

        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.run(sid=sid)
        bot.community.send_image(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", image = "https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        ```
        """
        return CMessage(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                mediaType = 100,
                mediaUploadValue=self.encode_media(
                    self.__handle_media__(
                    media=image,
                    content_type="image/jpg",
                    media_value=False
                )),
                mediaUploadValueContentType = "image/jpg",
                mediaUhqEnabled = True).json()
                ))

    @community
    def send_audio(self, chatId: str, audio: Union[str, BinaryIO] = None, comId: Union[str, int] = None) -> CMessage: #NOTE: Not sure how long the audio can be.
        """
        `send_audio` is the method that sends an audio to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the audio to.

        - `audio` - The audio to send.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_audio(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", audio = "output.mp3")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                type=2,
                mediaType=110,
                mediaUploadValue=self.encode_media(
                    self.__handle_media__(
                    media=audio,
                    content_type="audio/aac",
                    media_value=False
                    ))
            ).json()))

    @community
    def send_sticker(self, chatId: str, stickerId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `send_sticker` is the method that sends a sticker to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the sticker to.

        - `stickerId` - The sticker ID to send.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_sticker(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", stickerId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                type=3,
                mediaType=113,
                mediaValue=f"ndcsticker://{stickerId}",
                stickerId=stickerId).json()
                ))
    
    def __handle_media__(self, media: str, content_type: str = "image/jpg", media_value: bool = False) -> str:
        response = None
        
        try:
            if media.startswith("http"):
                response = get(media)
                response.raise_for_status()
                media = response.content
            else:
                media = open(media, "rb").read()
        except Exception as e:
            raise InvalidImage from e

        if media_value:
            return self.upload_media(media=media, content_type=content_type)

        if response and not response.headers.get("content-type").startswith("image"):
            raise InvalidImage

        return media

    def encode_media(self, file: bytes) -> str:
        return b64encode(file).decode()

    def upload_media(self, media: Union[str, BinaryIO], content_type: str = "image/jpg") -> str:
        return ApiResponse(self.session.handler(
            method = "POST",
            url = "/g/s/media/upload",
            data = media,
            content_type = content_type
            )).mediaValue

    @community
    def join_chat(self, chatId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `join_chat` is the method that joins a chat.

        `**Parameters**`

        - `chatId` - The chat ID to join.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.join_chat(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    @community
    def leave_chat(self, chatId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `leave_chat` is the method that leaves a chat.

        `**Parameters**`

        - `chatId` - The chat ID to leave.
        
        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.leave_chat(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    @community
    def kick(self, userId: str, chatId: str, allowRejoin: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        `kick` is the method that kicks a user from a chat.

        `**Parameters**`

        - `userId` - The user ID to kick.

        - `chatId` - The chat ID to kick the user from.

        - `allowRejoin` - Whether or not the user can rejoin the chat. [Optional]

            `allowRejoin` defaults to `True`.

        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.kick(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", allowRejoin=True)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={1 if allowRejoin else 0}"
            ))

    @community
    def delete_chat(self, chatId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_chat` is the method that deletes a chat.

        `**Parameters**`

        - `chatId` - The chat ID to delete.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_chat(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}"
            ))

    @community
    def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `delete_message` is the method that deletes a message from a chat.

        `**Parameters**`

        - `chatId` - The chat ID to delete the message from.

        - `messageId` - The message ID to delete.

        - `asStaff` - Whether or not to delete the message as staff. [Optional]

        - `reason` - The reason for deleting the message. [Optional]

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.delete_message(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", messageId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(
            self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message/{messageId}/admin",
            data = {
            "adminOpName": 102,
            "adminOpNote": {"content": reason},
            "timestamp": int(time() * 1000)
            }
            )) if asStaff else ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message/{messageId}"
            ))

    @community
    def transfer_host(self, chatId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `transfer_host` is the method that transfers the host of a chat.

        `**Parameters**`

        - `chatId` - The chat ID to transfer the host of.

        - `userId` - The user ID to transfer the host to.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.transfer_host(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/transfer-organizer",
            data = {
                "uidList": [userId],
                "timestamp": int(time() * 1000)
                }))

    @community
    def accept_host(self, chatId: str, requestId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `accept_host` is the method that accepts the host of a chat.

        `**Parameters**`

        - `chatId` - The chat ID to accept the host of.

        - `requestId` - The request ID to accept the host of.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.accept_host(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", requestId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept"
            ))

    @community
    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """"
        `subscribe` is the method that subscribes to a user.

        `**Parameters**`

        - `userId` - The user ID to subscribe to.

        - `autoRenew` - Whether or not to auto renew the subscription. [Optional]

        - `transactionId` - The transaction ID to use. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.subscribe(userId = "5f4d2e0e0a0a0a0a0a0a0a0a", autoRenew=False, transactionId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        if not transactionId: transactionId = str(uuid4())
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/influencer/{userId}/subscribe",
            data = {
                "paymentContext": {
                    "transactionId": transactionId,
                    "isAutoRenew": autoRenew
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def thank_props(self, chatId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `thank_props` is the method that thanks a user for props.

        `**Parameters**`

        - `chatId` - The chat ID to thank the user for props in.

        - `userId` - The user ID to thank for props.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.thank_props(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", userId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank"
            ))

    @community
    def send_active(
        self,
        tz: int = -timezone // 1000,
        start: int = None,
        end: int = None,
        timers: list = None,
        comId: Union[str, int] = None
        ) -> ApiResponse:
        """
        `send_active` is the method that sends the active time of the user.

        `**Parameters**`

        - `tz` - The timezone of the active time. 

        - `start` - The start time of the active time. [Optional]

        - `end` - The end time of the active time. [Optional]

        - `timers` - The timers of the active time. [Optional]
        
        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_active(timezone=-300, timers=[{"start": time() * 1000, "end": time() * 1000}]])
        bot.run(sid=sid)
        ```
        """
        if not any([start and end, timers]): raise MissingTimers
        
        data={
            "optInAdsFlags": 2147483647,
            "timezone": tz,
            "timestamp": int(time() * 1000)
        }
        if timers is not None:
            data["userActiveTimeChunkList"] = timers
        else:
            data["userActiveTimeChunkList"] = [{"start": start, "end": end}]

        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/stats/user-active-time",
            data=data
            ))

    @community
    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, wikiId: str = None, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `send_coins` is the method that sends coins to a user.

        `**Parameters**`

        - `coins` - The amount of coins to send.

        - `blogId` - The blog ID to send the coins to. [Optional]

        - `chatId` - The chat ID to send the coins to. [Optional]

        - `wikiId` - The wiki ID to send the coins to. [Optional]

        - `transactionId` - The transaction ID to use. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_coins(coins=100, blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url= f'/x{self.community_id if comId is None else comId}/s/{"blog" if blogId else "chat/thread" if chatId else "item"}/{blogId or chatId or wikiId}/tipping',
            data = {
                "coins": coins,
                "tippingContext": {"transactionId": transactionId or (str(uuid4()))},
                "timestamp": int(time() * 1000)
                }
            ))
    
    @community
    def send_chat_props(self, coins: int, chatId: str, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `send_coins_to_chat` is the method that sends coins to a chat.

        `**Parameters**`

        - `coins` - The amount of coins to send.

        - `chatId` - The chat ID to send the coins to.

        - `transactionId` - The transaction ID to use. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_coins_to_chat(coins=100, chatId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.send_coins(coins=coins, chatId=chatId, transactionId=transactionId, comId=comId)
    
    @community
    def send_blog_props(self, coins: int, blogId: str, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `send_coins_to_blog` is the method that sends coins to a blog.

        `**Parameters**`

        - `coins` - The amount of coins to send.

        - `blogId` - The blog ID to send the coins to.

        - `transactionId` - The transaction ID to use. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_coins_to_blog(coins=100, blogId = "5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.send_coins(coins=coins, blogId=blogId, transactionId=transactionId, comId=comId)

    @community
    def start_chat(self, userIds: list, title: str = None, message: str = None, content: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `start_chat` is the method that starts a chat with a user.

        `**Parameters**`

        - `userIds` - The user IDs to start the chat with.

        - `title` - The title of the chat. [Optional]

        - `message` - The message to send in the chat. [Optional]

        - `content` - The chat description. [Optional]

        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.start_chat(userIds=["5f4d2e0e0a0a0a0a0a0a0a0a"], title = "Hello", message = "Hello World!", content = "Hello World!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread",
            data = {
            "title": title,
            "inviteeUids": userIds if isinstance(userIds, list) else [userIds],
            "initialMessageContent": message,
            "content": content,
            "type": 0,
            "publishToGlobal": 0,
            "timestamp": int(time() * 1000)
            }))

    @community
    def invite_chat(self, chatId: str, userIds: list, comId: Union[str, int] = None) -> ApiResponse:
        """
        `invite_chat` is the method that invites a user to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to invite the user to.

        - `userIds` - The user IDs to invite to the chat.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.invite_chat(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", userIds=["5f4d2e0e0a0a0a0a0a0a0a0a"])
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/invite",
            data = {
            "uids": userIds if isinstance(userIds, list) else [userIds],
            "timestamp": int(time() * 1000)
            }))

    @community
    def set_view_only(self, chatId: str, viewOnly: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        `view_only` is the method that makes a chat view only.

        `**Parameters**`

        - `chatId` - The chat ID to make view only.

        - `viewOnly` - Whether the chat should be view only or not. [Optional] `[Default: True]`
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.view_only(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", viewOnly=True)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/view-only/enable" if viewOnly else f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/view-only/disable"
            ))

    @community
    def set_members_can_invite(self, chatId: str, canInvite: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        `members_can_invite` is the method that makes a chat members can invite.

        `**Parameters**`

        - `chatId` - The chat ID to make members can invite.

        - `canInvite` - Whether the chat should be members can invite or not. [Optional] `[Default: True]`
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.members_can_invite(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", canInvite=True)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/members-can-invite/enable" if canInvite else f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/members-can-invite/disable"
            ))

    @community
    def change_chat_background(self, chatId: str, backgroundImage: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `change_chat_background` is the method that changes the background of a chat.

        `**Parameters**`

        - `chatId` - The chat ID to change the background of.

        - `backgroundImage` - The background image to change the chat background to. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.change_chat_background(chatId = "5f4d2e0e0a0a0a0a0a0a0a0a", backgroundImage = "https://i.imgur.com/0QZ0QZ0.png")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}/background",
            data = {
            "media": [[100, self.__handle_media__(media=backgroundImage, media_value=True), None]],
            "timestamp": int(time() * 1000)
            }))
        
    @community
    def solve_quiz(self, quizId: str, quizAnswers: Union[dict, list], hellMode: bool = False, comId: Union[str, int] = None) -> ApiResponse:
        """
        `solve_quiz` is the method that solves a quiz.

        `**Parameters**`

        - `quizId` - The quiz ID to solve.

        - `quizAnswers` - The quiz answers to solve the quiz with.

        - `hellMode` - Whether the quiz should be solved in hell mode or not. [Optional] `[Default: False]`
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.solve_quiz(quizId = "5f4d2e0e0a0a0a0a0a0a0a0a", quizAnswers={"5f4d2e0e0a0a0a0a0a0a0a0a": "5f4d2e0e0a0a0a0a0a0a0a0a"}, hellMode=False)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{quizId}/quiz/result",
            data = {
            "quizAnswerList": quizAnswers if isinstance(quizAnswers, list) else [quizAnswers],
            "mode": 1 if hellMode else 0,
            "timestamp": int(time() * 1000)
            }))

    @community
    def set_channel(self, chatId: str, comId: Union[str, int] = None) -> None:
        """
        `set_channel` is the method that sets the channel of a chat.

        `**Parameters**`

        - `chatId` - The chat ID to set the channel of.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()

        @bot.command("play")
        def play(ctx: Context, message: str):
            bot.community.set_channel(chatId=ctx.chatId)
            sleep(1)
            if bot.channel == None:
                return ctx.reply("Start a voice call first!")
            else:
                # This is just an example, you can do whatever you want here.
                rtc.joinChannel(
                    bot.channel.channelKey,
                    bot.channel.channelName,
                    None,
                    bot.channel.channelUid
                    )
        
        """
        for i in range(2):
            self.bot.send_websocket_message({
                "o": {
                    "ndcId": self.community_id if comId is None else comId,
                    "threadId": chatId,
                    "joinRole": 1 if i == 0 else None,
                    "id": randint(0, 100)
                },
                "t": 112 if i == 0 else 200
                })

    @community
    def start_vc(self, chatId: str, comId: Union[str, int] = None) -> None:
        """
        `start_vc` is the method that starts a voice call in a chat.
        
        `**Parameters**`
        
        - `chatId` - The chat ID to start the voice call in.
        
        `**Example**`
        
        ```python
        from pymino import Bot
        
        bot = Bot()
        
        @bot.command("start")
        def start(ctx: Context):
            bot.community.start_vc(chatId=ctx.chatId)
            
        bot.run(sid=sid)
        ```
        """
        for i in range(2):
            self.bot.send_websocket_message({
                "o": {
                    "ndcId": self.community_id if comId is None else comId,
                    "threadId": chatId,
                    "joinRole": 1 if i == 0 else None,
                    "channelType": 1 if i == 1 else None,
                    "id": randint(0, 100)
                },
                "t": 112 if i == 0 else 108
            })

    @community
    def stop_vc(self, chatId: str, comId: Union[str, int] = None) -> None:
        """
        `stop_vc` is the method that stops a voice call in a chat.
        
        `**Parameters**`
        
        - `chatId` - The chat ID to stop the voice call in.
        
        `**Example**`
        
        ```python
        from pymino import Bot
        
        bot = Bot()
        
        @bot.command("stop")
        def stop(ctx: Context):
            bot.community.stop_vc(chatId=ctx.chatId)
            
        bot.run(sid=sid)
        ```
        """
        self.bot.send_websocket_message({
            "o": {
                "ndcId": self.community_id if comId is None else comId,
                "threadId": chatId,
                "joinRole": 2,
                "id": randint(0, 100)
            },
            "t": 112
        })
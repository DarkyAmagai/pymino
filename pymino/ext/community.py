from .utilities.generate import *

class Community:
    """
    `Community` is the class that handles community related actions.
    
    `**Parameters**`

    - `bot` - The bot client.

    - `session` - The session to use.

    - `community_id` - The community id to use. Defaults to `None`.

    """
    def __init__(self, bot, session: HTTPClient, community_id: Optional[str]=None, comId: Union[str, int] = None) -> None:
        self.bot = bot
        self.session = session
        self.community_id = community_id
        self.userId: Optional[str] = None
        if self.userId is None: return 

    def community(func):
        def community_func(*args, **kwargs):
            if args[0].community_id is None:
                raise Exception("Error: community_id in Bot Client is None. Please provide a community id!")
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
            method="POST",
            url=f"/g/s-x{self.community_id if comId is None else comId}/community/invitation",
            data = {"duration": 0, "force": True, "timestamp": int(time() * 1000)}
            ))

    @community
    def fetch_object_id(self, link: str) -> str:
        """
        `fetch_object_id` is the method that fetches the object id from a link.

        `**Parameters**`

        - `link` - The link to fetch the object id from.

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()
        objectId = bot.community.fetch_object_id(link="https://www.aminoapps.com.com/p/as12s34S")
        bot.run(sid=sid)
        ```
        """
        return LinkInfo(self.session.handler(method="GET", url=f"/g/s/link-resolution?q={link}")).objectId

    @community
    def fetch_object_info(self, link: str) -> LinkInfo:
        """
        `fetch_object_info` is the method that fetches the object info from a link.

        `**Parameters**`

        - `link` - The link to fetch the object info from.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()
        objectInfo = bot.community.fetch_object_info(link="https://www.aminoapps.com.com/p/as12s34S")
        bot.run(sid=sid)
        ```
        """
        return LinkInfo(self.session.handler(method="GET", url=f"/g/s/link-resolution?q={link}"))
 
    @community
    def fetch_community(self, community_id: Union[str, int]) -> CCommunity:
        """
        `fetch_community` is the method that fetches the community info.

        `**Parameters**`

        - None
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_community(community_id="123456789").json
        bot.run(sid=sid)
        ```
        """
        return CCommunity(self.session.handler(method="GET", url=f"/g/s-x{community_id}/community/info"))
    
    @community
    def joined_communities(self, start: int = 0, size: str = 50) -> CCommunityList:
        """
        `joined_communities` is the method that fetches the communities the user has joined.

        `**Parameters**`

        - None
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.joined_communities().json
        bot.run(sid=sid)
        ```
        """
        return CCommunityList(self.session.handler(method="GET", url=f"/g/s/community/joined?v=1&start={start}&size={size}"))

    @community
    def join_community(self, comId: Union[str, int] = None) -> ApiResponse:
        """
        `join_community` is the method that joins the community.
        
        `**Parameters**`

        - None
        
        `**Example**`
        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.join_community()
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/community/join", 
            data={"timestamp": int(time() * 1000)}))

    @community
    def leave_community(self, comId: Union[str, int] = None) -> ApiResponse:
        """
        `leave_community` is the method that leaves the community.

        `**Parameters**`

        - None

        `**Example**`
        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.leave_community()
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/community/leave", 
            data={"timestamp": int(time() * 1000)}))

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
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/community/membership-request", 
            data={"message": message, "timestamp": int(time() * 1000)}))

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
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/community/flag", 
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
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/community/check-in",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}))

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
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/check-in/lottery",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}))
    
    @community
    def online_status(self, status: Optional[int] = 1, comId: Union[str, int] = None) -> ApiResponse:
        """
        `online_status` is the method that sets the online status of the community.

        `**Parameters**`

        - `status` - The status to set. Defaults to `1`.
        - `1` - Online
        - `2` - Offline
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.online_status()
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{self.userId}/online-status",
            data={"status": status, "timestamp": int(time() * 1000)}))

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
            method="GET",
            url=f"/x{self.community_id if comId is None else comId}/s/coupon/new-user-coupon"
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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/notification?pagingType=t&size={size}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/user-profile?type={type}&start={start}&size={size}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/live-layer?topic=ndtopic:x{self.community_id if comId is None else comId}:online-members&start={start}&size={size}"))

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
        bot.community.fetch_followers(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/member?start={start}&size={size}"))

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
        bot.community.fetch_following(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfileList(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/joined?start={start}&size={size}"))

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
        bot.community.fetch_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CThread(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread?type=joined-me&start={start}&size={size}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/live-layer/public-live-chats?start={start}&size={size}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}"))

    @community
    def fetch_chat_members(self, chatId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add CMemberList
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
        bot.community.fetch_chat_members(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2"))

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
        bot.community.fetch_messages(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CMessages(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message?start={start}&size={size}&type=default"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/feed/blog-all?pagingType=t&size={size}"))

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
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/community/leaderboard?rankingType={leaderboard}&start={start}&size={size}"))

    @community
    def fetch_comments(self, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, start: int=0, size: int=25, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add CCommentList
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
        bot.community.fetch_comments(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                object = ["user-profile", "blog", "item"][["userId", "blogId", "wikiId"].index(i)]
                return ApiResponse(self.session.handler(
                    method="GET", url=f"/x{self.community_id if comId is None else comId}/s/{object}/{eval(i)}/comment?sort=newest&start={start}&size={size}"))

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
        bot.community.set_cohost(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userIds="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/cohost",
            data={"userIds": userIds if isinstance(userIds, list) else [userIds]}))

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
        bot.community.remove_cohost(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/co-host/{userId}"))

    @community
    def follow(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        `follow` is the method that follows user.

        `**Parameters**`

        - `userId` - The user ID to follow.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.follow(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/member"))

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
        bot.community.unfollow(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{self.userId}/joined/{userId}"))

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
        bot.community.block(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/block/{userId}"))

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
        bot.community.unblock(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/block/{userId}"))

    @community
    def post_blog(self, title: str, content: str, image: Optional[str]=None, comId: Union[str, int] = None) -> CBlog:
        """
        `post_blog` is the method that posts blog.

        `**Parameters**`

        - `title` - The title of the blog.

        - `content` - The content of the blog.

        - `image` - The image of the blog. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.post_blog(title="title", content="content")
        bot.run(sid=sid)
        ```
        """

        return CBlog(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog",
            data = {
                "title": title,
                "content": content,
                "timestamp": int(time() * 1000),
                "mediaList": [self.upload_image(image, 1)] if image is not None else []
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
        bot.community.delete_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}"))

    @community
    def post_wiki(self, title: str, content: str, image: Optional[str]=None, keyword: Optional[str]=None, value: int=5, type: str="levelStar", comId: Union[str, int] = None) -> ApiResponse: #TODO: Add wiki class
        """
        `post_wiki` is the method that posts wiki.

        `**Parameters**`

        - `title` - The title of the wiki.

        - `content` - The content of the wiki.

        - `image` - The image of the wiki. [Optional]

        - `keyword` - Keywords for the wiki. [Optional]

        - `value` - Value rating for the wiki. [Optional]

        - `type` - Type rating for the wiki. [Optional]

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.post_wiki(title="title", content="content")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/item",
            data = {
                "label": title,
                "content": content,
                "icon": self.upload_image(image, "image") if image is not None else None,
                "keywords": keyword,
                "timestamp": int(time() * 1000),
                "mediaList": [self.upload_image(image, "image")] if image is not None else [],
                "props": [{"title": "My Rating", "value": value, "type": type}]
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
        bot.community.delete_wiki(wikiId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/item/{wikiId}"))

    @community
    def delete_comment(self, commentId: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, comId: Union[str, int] = None) -> ApiResponse:
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
        bot.community.delete_comment(commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                object = ["user-profile", "blog", "item"][["userId", "blogId", "wikiId"].index(i)]
                return ApiResponse(self.session.handler(
                    method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/{object}/{eval(i)}/comment/{commentId}"))

    @community
    def comment(self, content: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, image: Optional[str]=None, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add comment class
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
        bot.community.comment(content="content")
        bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                object = ["user-profile", "blog", "item"][["userId", "blogId", "wikiId"].index(i)]
                return ApiResponse(self.session.handler(
                    method="POST", url=f"/x{self.community_id if comId is None else comId}/s/{object}/{eval(i)}/comment",
                    data = {
                        "content": content,
                        "mediaList": [self.upload_image(image, 1)] if image is not None else [],
                        "stickerId": None,
                        "type": 0,
                        "eventSource": "FeedList" if userId is None else "UserProfileView",
                        "timestamp": int(time() * 1000)
                        }))

    @community
    def like_comment(self, commentId: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, comId: Union[str, int] = None) -> ApiResponse:
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
        bot.community.like_comment(commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                object = ["user-profile", "blog", "item"][["userId", "blogId", "wikiId"].index(i)]
                return ApiResponse(self.session.handler(
                    method="POST", url=f"/x{self.community_id if comId is None else comId}/s/{object}/{eval(i)}/comment/{commentId}/vote",
                    data = {
                        "value": 1,
                        "timestamp": int(time() * 1000),
                        "eventSource": "UserProfileView" if userId is None else "PostDetailView"
                        }))

    @community
    def unlike_comment(self, commentId: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, comId: Union[str, int] = None) -> ApiResponse:
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
        bot.community.unlike_comment(commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                object = ["user-profile", "blog", "item"][["userId", "blogId", "wikiId"].index(i)]
                return ApiResponse(self.session.handler(
                    method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/{object}/{eval(i)}/comment/{commentId}/vote"))

    @community
    def like_blog(self, blogId: str, userId: Optional[str]=None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `like_blog` is the method that likes a blog.

        `**Parameters**`

        - `blogId` - The blog ID to like.

        - `userId` - The user ID to like blog. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.like_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/vote",
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
        bot.community.unlike_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/vote"))

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
        bot.community.upvote_comment(blogId="5f4d2e0e0a0a0a0a0a0a0a0a", commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/comment/{commentId}/vote",
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
        bot.community.downvote_comment(blogId="5f4d2e0e0a0a0a0a0a0a0a0a", commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/comment/{commentId}/vote",
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
        bot.community.fetch_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CBlog(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}"))

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
        bot.community.fetch_wiki(wikiId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/item/{wikiId}"))

    @community
    def fetch_quiz(self, quizId: str, comId: str=None):
        """
        `fetch_quiz` is the method that fetches a quiz's information.
        
        `**Parameters**`
        
        - `quizId` - The quiz ID to fetch.
        
        `**Example**`
        
        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.fetch_quiz(quizId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/blog/{quizId}")

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
        bot.community.fetch_user(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return UserProfile(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}"))

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
        bot.community.reply_wall(userId="5f4d2e0e0a0a0a0a0a0a0a0a", commentId="5f4d2e0e0a0a0a0a0a0a0a0a", message="Hello!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/comment",
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
        bot.community.vote_poll(blogId="5f4d2e0e0a0a0a0a0a0a0a0a", optionId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/poll/option/{optionId}/vote",
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
        bot.community.repost(content="Great blog!", blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CBlog(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog",
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
        bot.community.ban(userId="5f4d2e0e0a0a0a0a0a0a0a0a", reason="Bot!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/ban",
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
        bot.community.unban(userId="5f4d2e0e0a0a0a0a0a0a0a0a", reason="Misclick!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/unban",
            data = {
                "note": {
                    "content": reason
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def strike(self, userId: str, time: int = 5, title: str = None, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `strike` is the method that strikes a user.

        `**Parameters**`

        - `userId` - The user ID to strike.

        - `time` -The time of the strike in hours

            `1` - 1 hour
            `2` - 3 hours
            `3` - 6 hours
            `4` - 12 hours
            `5` - 24 hours

        - `title` - Title of the strike.

        - `reason` - The reason to strike.
        
        `time` - The time of the strike in hours.
        - 1 hour (1)
        - 3 hours (2)
        - 6 hours (3)
        - 12 hours(4)
        - 24 hours (default) (5)

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.strike(userId="5f4d2e0e0a0a0a0a0a0a0a0a", time=1, title="Bot!", reason="Bot!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/notice",
            data = {
                "uid": userId,
                "title": title,
                "content": reason,
                "attachedObject": {
                    "objectId": userId,
                    "objectType": 0
                },
                "penaltyType": 1,
                "penaltyValue": [3600, 10800, 21600, 43200, 86400][time - 1 if time in range(1, 6) else 86400],
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
        bot.community.warn(userId="5f4d2e0e0a0a0a0a0a0a0a0a", reason="Violating community guidelines!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/notice",
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
        bot.community.edit_titles(userId="5f4d2e0e0a0a0a0a0a0a0a0a", titles=["Bot", "Developer"], colors=["#ff0000", "#00ff00"])
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/admin",
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
        bot.community.fetch_mod_history(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/admin/operation",
            params = {
                "objectId": blogId if blogId is not None else wikiId if wikiId is not None else quizId if quizId is not None else fileId if fileId is not None else userId,
                "objectType": 1 if blogId is not None else 2 if wikiId is not None else 3 if quizId is not None else 109 if fileId is not None else 0,
                "pagingType": "t",
                "size": size
                }))

    @community
    def edit_profile(
        self,
        nickname: str=None,
        content: str=None
        ) -> UserProfile:
        """
        `edit_profile` is the method that edits a user's profile.

        `**Parameters**`

        - `nickname` - The nickname to edit.

        - `content` - The content to edit.

        `**Example**`

        ```python
        from pymino import Bot

        bot = Bot()
        bot.community.edit_profile(nickname="Bot", content="I am a bot!")
        bot.run(sid=sid)
        ```
        """
        data = {"timestamp": int(time() * 1000)}
        [data.update({key: value}) for key, value in {"nickname": nickname, "content": content}.items() if value is not None]
        return UserProfile(self.session.handler(method="POST", url=f"/x{self.community_id}/s/user-profile/{self.userId}", data=data))

    @community
    def fetch_user_comments(self, userId: str, sorting: str = "newest", start: int = 0, size: int = 25, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add CCommentList class
        """
        `fetch_user_comments` is the method that fetches a user's comments.

        `**Parameters**`

        - `userId` - The user ID to fetch comments.

        - `sorting` - The sorting of the comments.

            `newest` - Newest comments
            #NOTE: Need to add sorting options.

        - `start` - The start of the comments.

        - `size` - The size of the comments.

        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.fetch_user_comments(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/comment?sort={sorting}&start={start}&size={size}"), True)

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
        bot.community.fetch_user_blogs(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return CBlogList(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/blog?type=user&q={userId}&start={start}&size={size}"))

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
        bot.community.fetch_user_wikis(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```

        """
        return ApiResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}"), True)

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
        bot.community.fetch_user_check_ins(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id if comId is None else comId}/s/check-in/stats/{userId}?timezone=-300"))
            
    @community
    def send_embed(self, chatId: str, title: str, content: str, image: BinaryIO = None, link: Optional[str]=None, comId: Union[str, int] = None) -> CMessage:
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
        bot.community.send_embed(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", title="Hello World!", content="This is an embed!")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content="[c]",
            attachedObject={
                "title": title,
                "content": content,
                "mediaList": [[100, self._prep_file(image), None]],
                "link": link
                }).json()))

    def _prep_file(self, file: str, mediaValue: bool=True) -> BinaryIO:
        """
        `prep_file` - Prepares a file to be uploaded.
        
        `**Parameters**`
        - `file` - The file to prepare.
        - `mediaValue` - Whether to upload file and fetch mediaValue.

        `**Returns**`
        - `BinaryIO` - The binary file.
        """
        file = BytesIO(get(file).content) if file.startswith("http") else open(file, "rb")
        return self.upload_image(file) if mediaValue else file

    @community
    def send_link_snippet(self, chatId: str, content: str, image: BinaryIO = None, comId: Union[str, int] = None) -> ApiResponse:
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
        bot.community.send_link_snippet(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", content="Hello World!", image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content,
            linkSnippetList={
                "link": None,
                "mediaType": 100,
                "mediaUploadValue": b64encode(self._prep_file(image, False).read()).decode(),
                "mediaUploadValueContentType": "image/png"
                }).json()
                ))

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
        bot.community.send_message(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", content="Hello World!")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content).json()
            ))

    @community
    def send_image(self, chatId: str, image: Union[str, BinaryIO] = None, comId: Union[str, int] = None) -> CMessage:
        """
        `send_image` is the method that sends an image to a chat.

        `**Parameters**`

        - `chatId` - The chat ID to send the image to.

        - `image` - The image to send. [Optional]

        - `gif` - The gif to send. [Optional]
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.send_image(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                mediaType = 100,
                mediaUploadValue=b64encode((self._prep_file(image, False)).read()).decode(),
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
        bot.community.send_audio(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", audio="output.mp3")
        bot.run(sid=sid)
        ```
        """
        return CMessage(self.session.handler(
            method="POST",
            url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                type=2,
                mediaType=110,
                mediaUploadValue=b64encode((self._prep_file(audio, False)).read()).decode()).json()
                ))

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
        bot.community.send_sticker(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", stickerId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        pass #TODO: Finish this method.

    def upload_image(self, image: Union[str, BinaryIO]) -> str:
        """
        `upload_image` is the method that uploads an image to the community.

        `**Parameters**`

        - `image` - The image to upload.
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.upload_image(image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        bot.run(sid=sid)
        """
        if isinstance(image, str):
            if image.startswith("http"):
                image = BytesIO(get(image).content)
            elif not image.startswith("http"):
                image = open(image, "rb")
        return ApiResponse(self.session.handler(method="POST", url="/g/s/media/upload",
            data=image.read(), content_type="image/jpg")).mediaValue

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
        bot.community.join_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}"))

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
        bot.community.leave_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}"))

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
        bot.community.kick(userId="5f4d2e0e0a0a0a0a0a0a0a0a", chatId="5f4d2e0e0a0a0a0a0a0a0a0a", allowRejoin=True)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={1 if allowRejoin else 0}"))

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
        bot.community.delete_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}"))

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
        bot.community.delete_message(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", messageId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(
            self.session.handler(
                method="POST",
                url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message/{messageId}/admin",
                data = {"adminOpName": 102, "adminOpNote": {"content": reason}, "timestamp": int(time() * 1000)}
                )) if asStaff else ApiResponse(self.session.handler(
                    method="DELETE",
                    url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message/{messageId}"
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
        bot.community.transfer_host(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/transfer-organizer",
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
        bot.community.accept_host(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", requestId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept"))

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
        bot.community.subscribe(userId="5f4d2e0e0a0a0a0a0a0a0a0a", autoRenew=False, transactionId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        if not transactionId: transactionId = str(uuid4())
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/influencer/{userId}/subscribe",
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
        bot.community.thank_props(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank"))

    @community
    def send_active(self, timezone: int=-300, start: int=time() * 1000, end: int=time() * 1000, timers: list=None, comId: Union[str, int] = None) -> ApiResponse:
        """
        `send_active` is the method that sends the active time of the user.

        `**Parameters**`

        - `timezone` - The timezone of the user. [Optional]

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
        data={
            "optInAdsFlags": 27,
            "timezone": timezone,
            "timestamp": int(time() * 1000)
        }
        if timers is not None:
            data["userActiveTimeChunkList"] = timers
        else:
            data["userActiveTimeChunkList"] = [{"start": start, "end": end}]

        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/community/stats/user-active-time", data=data))

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
        bot.community.send_coins(coins=100, blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url= f'/x{self.community_id if comId is None else comId}/s/{"blog" if blogId else "chat/thread" if chatId else "item"}/{blogId or chatId or wikiId}/tipping',
            data = {
                "coins": coins,
                "tippingContext": {"transactionId": transactionId or (str(uuid4()))},
                "timestamp": int(time() * 1000)
                }
            ))

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
        bot.community.start_chat(userIds=["5f4d2e0e0a0a0a0a0a0a0a0a"], title="Hello", message="Hello World!", content="Hello World!")
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread",
            data = {
                "title": title,
                "inviteeUids": userIds if isinstance(userIds, list) else [userIds],
                "initialMessageContent": message,
                "content": content,
                "type": 0,
                "publishToGlobal": 0,
                "timestamp": int(time() * 1000)
            }
        ))

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
        bot.community.invite_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userIds=["5f4d2e0e0a0a0a0a0a0a0a0a"])
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/invite",
            data = {
                "uids": userIds if isinstance(userIds, list) else [userIds],
                "timestamp": int(time() * 1000)
            }
        ))

    @community
    def view_only(self, chatId: str, viewOnly: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        `view_only` is the method that makes a chat view only.

        `**Parameters**`

        - `chatId` - The chat ID to make view only.

        - `viewOnly` - Whether the chat should be view only or not. [Optional] `[Default: True]`
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.view_only(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", viewOnly=True)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/view-only/enable" if viewOnly else f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/view-only/disable"))

    @community
    def members_can_invite(self, chatId: str, canInvite: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        `members_can_invite` is the method that makes a chat members can invite.

        `**Parameters**`

        - `chatId` - The chat ID to make members can invite.

        - `canInvite` - Whether the chat should be members can invite or not. [Optional] `[Default: True]`
        
        `**Example**`

        ```python
        from pymino import Bot
        
        bot = Bot()
        bot.community.members_can_invite(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", canInvite=True)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/members-can-invite/enable" if canInvite else f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/members-can-invite/disable"))

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
        bot.community.change_chat_background(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", backgroundImage="https://i.imgur.com/0QZ0QZ0.png")
        bot.run(sid=sid)
        ```
        """
        image = self._prep_file(backgroundImage)
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}/background",
            data = {
                "media": [100, self.upload_image(image), None],
                "timestamp": int(time() * 1000)
            }
        ))
        
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
        bot.community.solve_quiz(quizId="5f4d2e0e0a0a0a0a0a0a0a0a", quizAnswers={"5f4d2e0e0a0a0a0a0a0a0a0a": "5f4d2e0e0a0a0a0a0a0a0a0a"}, hellMode=False)
        bot.run(sid=sid)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id if comId is None else comId}/s/blog/{quizId}/quiz/result",
            data = {
                "quizAnswerList": quizAnswers if isinstance(quizAnswers, list) else [quizAnswers],
                "mode": 1 if hellMode else 0,
                "timestamp": int(time() * 1000)
            }
        ))

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
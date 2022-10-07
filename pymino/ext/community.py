from .generate import *

class Community:
    """
    `Community` is the class that handles community related actions.
    
    `**Parameters**`
    - `session` - The session to use.
    - `community_id` - The community id to use. Defaults to `None`.
    - `debug` - Whether to print debug messages or not. Defaults to `False`.
    """
    def __init__(self, session: Session, community_id: Optional[str]=None, debug: Optional[bool] = False) -> None:
        self.session = session
        self.community_id = community_id
        self.debug = debug
        self.userId: Optional[str] = None
        if self.userId == None: return 

    def community(func):
        def wrapper(*args, **kwargs):
            if args[0].community_id is None:
                raise Exception("Error: community_id in Bot Client is None. Please provide a community id!")
            return func(*args, **kwargs)
        return wrapper

    @community
    def invite_code(self) -> SResponse:
        """
        `invite_code` is the method that gets the invite code for the community.

        `**Example**`
        ```python
        >>> from pymino import Bot

        >>> bot = Bot()
        >>> bot.community.invite_code()
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/g/s-x{self.community_id}/community/invitation",
            data={"duration": 0, "force": True, "timestamp": int(time() * 1000)}))

    @community
    def fetch_object_id(self, link: str) -> linkInfoV2:
        """
        `fetch_object_id` is the method that fetches the object id from a link.

        `**Example**`
        ```python
        >>> from pymino import Bot

        >>> bot = Bot()
        >>> objectId = bot.community.fetch_object_id(link="https://www.aminoapps.com.com/p/as12s34S")
        >>> bot.run(sid=sid)
        ```
        """
        return linkInfoV2(self.session.handler(method="GET", url=f"/g/s/link-resolution?q={link}")).objectId

    @community
    def join_community(self) -> SResponse:
        """
        `join_community` is the method that joins the community.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.join_community()
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/community/join", 
            data={"timestamp": int(time() * 1000)}))

    @community
    def leave_community(self) -> SResponse:
        """
        `leave_community` is the method that leaves the community.

        `**Example**`
        ```python
        >>> from pymino import Bot

        >>> bot = Bot()
        >>> bot.community.leave_community()
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/community/leave", 
            data={"timestamp": int(time() * 1000)}))

    @community
    def request_join(self, message: str) -> SResponse:
        """
        `request_join` is the method that requests to join the community.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.request_join("Hello, I would like to join your community!")
        ```"""
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/community/membership-request", 
            data={"message": message, "timestamp": int(time() * 1000)}))

    @community
    def flag_community(self, reason: str, flagType: int) -> SResponse:
        """
        `flag_community` is the method that flags the community.

        `**Parameters**`
        - `reason` - The reason for flagging the community.
        - `flagType` - The type of flag to use. Defaults to `1`.

        `**Example**`
        ```python
        >>> from pymino import Bot

        >>> bot = Bot()
        >>> bot.community.flag_community("This community is spamming.")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/community/flag", 
            data={
            "objectId": self.community_id,
            "objectType": 16,
            "flagType": flagType,
            "message": reason,
            "timestamp": int(time() * 1000)
        }))

    @community
    def check_in(self, timezone: Optional[int] = -300) -> CheckIn:
        """
        `check_in` is the method that checks in to the community.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.check_in()
        >>> bot.run(sid=sid)
        ```
        """
        return CheckIn(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/community/check-in",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}))

    @community
    def play_lottery(self, timezone: Optional[int] = -300) -> SResponse:
        """
        `play_lottery` is the method that plays the lottery in the community.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.play_lottery()
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/check-in/lottery",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}))
    
    @community
    def online_status(self, status: Optional[int] = 1) -> SResponse:
        """
        `online_status` is the method that sets the online status of the community.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.online_status()
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/user-profile/{self.userId}/online-status",
            data={"status": status, "timestamp": int(time() * 1000)}))

    @community
    def fetch_new_user_coupon(self) -> Coupon:
        """
        `fetch_new_user_coupon` is the method that fetches the new user coupon.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_new_user_coupon()
        >>> bot.run(sid=sid)
        ```
        """
        return Coupon(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/coupon/new-user-coupon"))

    @community
    def fetch_notifications(self, size: Optional[int] = 25) -> Notification:
        """
        `fetch_notifications` is the method that fetches the notifications.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_notifications()
        >>> bot.run(sid=sid)
        ```
        """
        return Notification(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/notification?pagingType=t&size={size}"), True)

    @community
    def fetch_user(self, userId: str) -> User:
        """
        `fetch_user` is the method that fetches a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_user("5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/user-profile/{userId}"))

    @community
    def fetch_users(self, type: Optional[str] = "recent", start: Optional[int] = 0, size: Optional[int] = 25) -> User:
        """
        `fetch_users` is the method that fetches users.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_users()
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/user-profile?type={type}&start={start}&size={size}"), True)

    @community
    def fetch_online_users(self, start: Optional[int] = 0, size: Optional[int] = 25) -> User:
        """
        `fetch_online_users` is the method that fetches online users.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
            
        >>> bot = Bot()
        >>> bot.community.fetch_online_users()
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/live-layer?topic=ndtopic:x{self.community_id}:online-members&start={start}&size={size}"), True)

    @community
    def fetch_followers(self, userId: str, start: int = 0, size: int = 25) -> User:
        """
        `fetch_followers` is the method that fetches followers.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_followers(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/user-profile/{userId}/member?start={start}&size={size}"), True)

    @community
    def fetch_following(self, userId: str, start: int = 0, size: int = 25) -> User:
        """
        `fetch_following` is the method that fetches following.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_following(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/user-profile/{userId}/joined?start={start}&size={size}"), True)

    @community
    def fetch_chat(self, chatId: str) -> ChatThread:
        """
        `fetch_chat` is the method that fetches a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return ChatThread(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/chat/thread/{chatId}"))

    @community
    def fetch_chats(self, start: int = 0, size: int = 25) -> ChatThread:
        """
        `fetch_chats` is the method that fetches chats.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
            
        >>> bot = Bot()
        >>> bot.community.fetch_chats()
        >>> bot.run(sid=sid)
        ```
        """
        return ChatThread(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/chat/thread?type=joined-me&start={start}&size={size}"), True)

    @community
    def fetch_live_chats(self, start: int = 0, size: int = 25) -> ChatThread:
        """
        `fetch_live_chats` is the method that fetches live chats.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_live_chats()
        >>> bot.run(sid=sid)
        ```
        """
        return ChatThread(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/live-layer/public-live-chats?start={start}&size={size}"), True)

    @community
    def fetch_public_chats(self, type: str = "recommended", start: int = 0, size: int = 25) -> ChatThread:
        """
        `fetch_public_chats` is the method that fetches public chats.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_public_chats()
        >>> bot.run(sid=sid)
        ```
        """
        return ChatThread(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}"), True)

    @community
    def fetch_chat_members(self, chatId: str, start: int = 0, size: int = 25) -> chatMembers:
        """
        `fetch_chat_members` is the method that fetches chat members.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_chat_members(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return chatMembers(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/chat/thread/{chatId}/member?start={start}&size={size}"), True)

    @community
    def fetch_messages(self, chatId: str, start: int = 0, size: int = 25) -> Message:
        """
        `fetch_messages` is the method that fetches messages.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_messages(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return Message(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message?start={start}&size={size}&type=default"), True)

    @community
    def fetch_blogs(self, size: int = 25) -> Blog:
        """
        `fetch_blogs` is the method that fetches blogs.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_blogs()
        >>> bot.run(sid=sid)
        ```
        """
        return Blog(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/feed/blog-all?pagingType=t&size={size}"), True)

    @community
    def fetch_leaderboard(self, leaderboard: int = 1, start: int = 0, size: int = 20) -> User:
        """
        `fetch_leaderboard` is the method that fetches leaderboard.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_leaderboard()
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/community/leaderboard?rankingType={leaderboard}&start={start}&size={size}"), True)

    @community
    def fetch_comments(self, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, start: int=0, size: int=25) -> Comment:
        """
        `fetch_comments` is the method that fetches comments.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_comments(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                return Comment(self.session.handler(
                    method="GET", url=f"/x{self.community_id}/s/{i.split('Id')[0] if i != 'wikiId' else 'item'}/{eval(i)}/comment?sort=newest&start={start}&size={size}"), True)

    @community
    def set_cohost(self, chatId: str, userIds: Union[str, list]) -> SResponse:
        """
        `set_cohost` is the method that sets co-host.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.set_cohost(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userIds="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/cohost",
            data={"userIds": userIds if isinstance(userIds, list) else [userIds]}))

    @community
    def remove_cohost(self, chatId: str, userId: str) -> SResponse:
        """
        `remove_cohost` is the method that removes co-host.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.remove_cohost(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/chat/thread/{chatId}/co-host/{userId}"))

    @community
    def follow(self, userId: str) -> SResponse:
        """
        `follow` is the method that follows user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.follow(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/s/user-profile/{userId}/member"))

    @community
    def unfollow(self, userId: str) -> SResponse:
        """
        `unfollow` is the method that unfollows user.
            
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.unfollow(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/s/user-profile/{userId}/member"))

    @community
    def block(self, userId: str) -> SResponse:
        """
        `block` is the method that blocks user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.block(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/block/{userId}"))

    @community
    def unblock(self, userId: str) -> SResponse:
        """
        `unblock` is the method that unblocks user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.unblock(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/block/{userId}"))

    @community
    def post_blog(self, title: str, content: str, image: Optional[str]=None) -> Blog:
        """
        `post_blog` is the method that posts blog.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.post_blog(title="title", content="content")
        >>> bot.run(sid=sid)
        ```
        """

        return Blog(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog",
            data = {
                "title": title,
                "content": content,
                "timestamp": int(time() * 1000),
                "mediaList": [self.upload_image(image, 1)] if image is not None else []
            }))
        
    @community
    def delete_blog(self, blogId: str) -> SResponse:
        """
        `delete_blog` is the method that deletes blog.
            
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.delete_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/blog/{blogId}"))

    @community
    def post_wiki(self, title: str, content: str, image: Optional[str]=None, keyword: Optional[str]=None, value: int=5, type: str="levelStar") -> Wiki:
        """
        `post_wiki` is the method that posts wiki.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.post_wiki(title="title", content="content")
        >>> bot.run(sid=sid)
        ```
        """
        return Wiki(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/item",
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
    def delete_wiki(self, wikiId: str) -> SResponse:
        """
        `delete_wiki` is the method that deletes wiki.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.delete_wiki(wikiId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/item/{wikiId}"))

    @community
    def delete_comment(self, commentId: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None) -> SResponse:
        """
        `delete_comment` is the method that deletes comment.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.delete_comment(commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                return SResponse(self.session.handler(
                    method="DELETE", url=f"/x{self.community_id}/s/{i.split('Id')[0] if i != 'wikiId' else 'item'}/{eval(i)}/comment/{commentId}"))

    @community
    def comment(self, content: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None, image: Optional[str]=None) -> Comment:
        """
        `comment` is the method that comments.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.comment(content="content")
        >>> bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                return Comment(self.session.handler(
                    method="POST", url=f"/x{self.community_id}/s/{i.split('Id')[0] if i != 'wikiId' else 'item'}/{eval(i)}/comment",
                    data = {
                        "content": content,
                        "mediaList": [self.upload_image(image, 1)] if image is not None else [],
                        "stickerId": None,
                        "type": 0,
                        "eventSource": "FeedList" if userId is None else "UserProfileView",
                        "timestamp": int(time() * 1000)
                        }))

    @community
    def like_comment(self, commentId: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None) -> SResponse:
        """
        `like_comment` is the method that likes a comment.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
            
        >>> bot = Bot()
        >>> bot.community.like_comment(commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                return SResponse(self.session.handler(
                    method="POST", url=f"/x{self.community_id}/s/{i.split('Id')[0] if i != 'wikiId' else 'item'}/{eval(i)}/comment/{commentId}/vote",
                    data = {
                        "value": 1,
                        "timestamp": int(time() * 1000),
                        "eventSource": "UserProfileView" if userId is None else "PostDetailView"
                        }))

    @community
    def unlike_comment(self, commentId: str, userId: Optional[str]=None, blogId: Optional[str]=None, wikiId: Optional[str]=None) -> SResponse:
        """
        `unlike_comment` is the method that unlikes a comment.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.unlike_comment(commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        for i in ["userId", "blogId", "wikiId"]:
            if eval(i) is not None:
                return SResponse(self.session.handler(
                    method="DELETE", url=f"/x{self.community_id}/s/{i.split('Id')[0] if i != 'wikiId' else 'item'}/{eval(i)}/comment/{commentId}/vote"))

    @community
    def like_blog(self, blogId: str, userId: Optional[str]=None) -> SResponse:
        """
        `like_blog` is the method that likes a blog.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.like_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog/{blogId}/vote",
            data = {
                "value": 4,
                "timestamp": int(time() * 1000),
                "eventSource": "UserProfileView" if userId is None else "PostDetailView"
                }))

    @community
    def unlike_blog(self, blogId: str) -> SResponse:
        """
        `unlike_blog` is the method that unlikes a blog.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.unlike_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/blog/{blogId}/vote"))

    @community
    def upvote_comment(self, blogId: str, commentId: str) -> SResponse:
        """
        `upvote_comment` is the method that upvotes a comment.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.upvote_comment(blogId="5f4d2e0e0a0a0a0a0a0a0a0a", commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog/{blogId}/comment/{commentId}/vote",
            data = {
                "value": 1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def downvote_comment(self, blogId: str, commentId: str) -> SResponse:
        """
        `downvote_comment` is the method that downvotes a comment.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.downvote_comment(blogId="5f4d2e0e0a0a0a0a0a0a0a0a", commentId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog/{blogId}/comment/{commentId}/vote",
            data = {
                "value": -1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def fetch_blog(self, blogId: str) -> Blog:
        """
        `fetch_blog` is the method that fetches a blog's information.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_blog(blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return Blog(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/blog/{blogId}"))

    @community
    def fetch_wiki(self, wikiId: str) -> Wiki:
        """
        `fetch_wiki` is the method that fetches a wiki's information.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_wiki(wikiId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return Wiki(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/item/{wikiId}"))

    @community
    def fetch_quiz(self, quizId: str):
        return self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/blog/{quizId}")

    @community
    def fetch_user(self, userId: str) -> User:
        """
        `fetch_user` is the method that fetches user's profile.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_user(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return User(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/user-profile/{userId}"))

    @community
    def reply_wall(self, userId: str, commentId: str, message: str) -> SResponse:
        """
        `reply_wall` is the method that replies to a comment on user's wall.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.reply_wall(userId="5f4d2e0e0a0a0a0a0a0a0a0a", commentId="5f4d2e0e0a0a0a0a0a0a0a0a", message="Hello!")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/user-profile/{userId}/comment",
            data = {
                "content": message,
                "stackedId": None,
                "respondTo": commentId,
                "type": 0,
                "eventSource": "UserProfileView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def vote_poll(self, blogId: str, optionId: str) -> SResponse:
        """
        `vote_poll` is the method that votes on a poll.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.vote_poll(blogId="5f4d2e0e0a0a0a0a0a0a0a0a", optionId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog/{blogId}/poll/option/{optionId}/vote",
            data = {
                "value": 1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))

    @community
    def repost(self, content: str = None, blogId: str = None, wikiId: str = None) -> Blog:
        """
        `repost` is the method that reposts a blog or wiki.

        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.repost(content="Great blog!", blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return Blog(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog",
            data = {
                "content": content,
                "refObjectId": blogId if blogId is not None else wikiId,
                "refObjectType": 1 if blogId is not None else 2,
                "type": 2,
                "timestamp": int(time() * 1000)
                }))

    @community
    def ban(self, userId: str, reason: str, banType: int = None) -> SResponse:
        """
        `ban` is the method that bans a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.ban(userId="5f4d2e0e0a0a0a0a0a0a0a0a", reason="Bot!")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/user-profile/{userId}/ban",
            data = {
                "reasonType": banType,
                "note": {
                    "content": reason
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def unban(self, userId: str, reason: str) -> SResponse:
        """
        `unban` is the method that unbans a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.unban(userId="5f4d2e0e0a0a0a0a0a0a0a0a", reason="Misclick!")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/user-profile/{userId}/unban",
            data = {
                "note": {
                    "content": reason
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def strike(self, userId: str, time: int = 5, title: str = None, reason: str = None) -> SResponse:
        """
        `strike` is the method that strikes a user.
        
        `time` - The time of the strike in hours.
        - 1 hour (1)
        - 3 hours (2)
        - 6 hours (3)
        - 12 hours(4)
        - 24 hours (default) (5)

        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.strike(userId="5f4d2e0e0a0a0a0a0a0a0a0a", time=1, title="Bot!", reason="Bot!")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/notice",
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
    def warn(self, userId: str, reason: str = None) -> SResponse:
        """
        `warn` is the method that warns a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.warn(userId="5f4d2e0e0a0a0a0a0a0a0a0a", reason="Violating community guidelines!")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/notice",
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
    def edit_titles(self, userId: str, titles: list, colors: list) -> SResponse:
        """
        `edit_titles` is the method that edits a user's titles.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.edit_titles(userId="5f4d2e0e0a0a0a0a0a0a0a0a", titles=["Bot", "Developer"], colors=["#ff0000", "#00ff00"])
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/user-profile/{userId}/admin",
            data = {
                "adminOpName": 207,
                "adminOpValue": {
                    "titles": [{"title": title, "color": color} for title, color in zip(titles, colors)]
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def fetch_mod_history(self, userId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, size: int = 25) -> SResponse:
        """
        `fetch_mod_history` is the method that fetches a user's moderation history.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_mod_history(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/admin/operation",
            params = {
                "objectId": blogId if blogId is not None else wikiId if wikiId is not None else quizId if quizId is not None else fileId if fileId is not None else userId,
                "objectType": 1 if blogId is not None else 2 if wikiId is not None else 3 if quizId is not None else 109 if fileId is not None else 0,
                "pagingType": "t",
                "size": size
                }))
    
    @community
    def fetch_user_comments(self, userId: str, sorting: str = "newest", start: int = 0, size: int = 25) -> Comment:
        """
        `fetch_user_comments` is the method that fetches a user's comments.
        
        #NOTE: Need to add sorting options.

        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_user_comments(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return Comment(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/user-profile/{userId}/comment?sort={sorting}&start={start}&size={size}"))

    @community
    def fetch_user_blogs(self, userId: str, start: int = 0, size: int = 25) -> Blog:
        """
        `fetch_user_blogs` is the method that fetches a user's blogs.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_user_blogs(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return Blog(self.session.handler(
            method="GET", url=f"x{self.community_id}/s/blog?type=user&q={userId}&start={start}&size={size}"))

    @community
    def fetch_user_wikis(self, userId: str, start: int = 0, size: int = 25) -> Wiki:
        """
        `fetch_user_wikis` is the method that fetches a user's wikis.

        `**Example**`
        ```python
        >>> from pymino import Bot

        >>> bot = Bot()
        >>> bot.community.fetch_user_wikis(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```

        """
        return Wiki(self.session.handler(
            method="GET", url=f"x{self.community_id}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}"))

    @community
    def fetch_user_check_ins(self, userId: str) -> SResponse:
        """
        `fetch_user_check_ins` is the method that fetches a user's check-ins.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.fetch_user_check_ins(userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="GET", url=f"/x{self.community_id}/s/check-in/stats/{userId}?timezone=-300"))
            
    @community
    def send_embed(self, chatId: str, title: str, content: str, image: BinaryIO = None, link: Optional[str]=None) -> Message:
        """
        `send_embed` is the method that sends an embed to a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_embed(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", title="Hello World!", content="This is an embed!")
        >>> bot.run(sid=sid)
        ```
        """
        return Message(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message",
            data = {
                "type": 0,
                "content": "[c]",
                "clientRefId": int(time() / 10 % 1000000000),
                "attachedObject": {
                    "link": link,
                    "title": title,
                    "content": content,
                    "mediaList": [[100, self.upload_image(image), None]] if image else None
                },
                "extensions": {},
                "timestamp": int(time() * 1000)
                }))

    def _prep_image(self, image: str) -> BinaryIO:
        """
        `_prep_image` is the method that prepares an image for sending.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community._prep_image(image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        >>> bot.run(sid=sid)
        ```
        """

        if image.startswith("http"):
            [open("temp.png", "wb").write(get(image).content), image := open("temp.png", "rb")]
        else:
            image = open(image, "rb")

        return image

    @community
    def send_link_snippet(self, chatId: str, message: str, image: BinaryIO = None) -> SResponse:
        """
        `send_link_snippet` is the method that sends a link snippet to a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_link_snippet(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", message="Hello World!", image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        >>> bot.run(sid=sid)
        ```
        """
        image = self._prep_image(image)
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message",
            data = {
                "type": 0,
                "content": message,
                "clientRefId": int(time() / 10 % 1000000000),
                "attachedObject": {},
                "extensions": {
                    "linkSnippetList": [{
                        "link": None,
                        "mediaType": 100,
                        "mediaUploadValue": b64encode(image.read()).decode(),
                        "mediaUploadValueContentType": "image/png"
                        }]
                    },
                "timestamp": int(time() * 1000)
                }))

    @community
    def send_message(self, chatId: str, message: str) -> Message:
        """
        `send_message` is the method that sends a message to a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_message(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", message="Hello World!")
        >>> bot.run(sid=sid)
        ```
        """
        return Message(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message",
            data = {
                "type": 0,
                "content": message,
                "clientRefId": int(time() / 10 % 1000000000),
                "extensions": {},
                "timestamp": int(time() * 1000)
                }))

    @community
    def send_image(self, chatId: str, image: Union[str, BinaryIO] = None, gif: Union[str, BinaryIO] = None) -> Message:
        """
        `send_image` is the method that sends an image to a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_image(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        >>> bot.run(sid=sid)
        ```
        """
        image = self._prep_image(image)
        return Message(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message",
            data = {
                "type": 0,
                "content": None,
                "clientRefId": int(time() / 10 % 1000000000),
                "attachedObject": None,
                "mediaType": 100,
                "mediaUploadValue": b64encode((image if image else gif).read()).decode(),
                "mediaUploadValueContentType": "image/jpg" if image else "image/gif",
                "mediaUhqEnabled": True,
                "timestamp": int(time() * 1000)
                }))
                
    @community
    def send_sticker(self, chatId: str, stickerId: str) -> SResponse:
        """
        `send_sticker` is the method that sends a sticker to a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_sticker(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", stickerId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message",
            data = {
                "type": 3,
                "content": None,
                "clientRefId": int(time() / 10 % 1000000000),
                "stickerId": stickerId,
                "extensions": {},
                "timestamp": int(time() * 1000)
                }))

    def upload_image(self, image: Union[str, BinaryIO]) -> str:
        """
        `upload_image` is the method that uploads an image to the community.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.upload_image(image="https://i.imgur.com/5f4d2e0e0a0a0a0a0a0a0a0a.png")
        >>> bot.run(sid=sid)
        """
        if isinstance(image, str) and image.startswith("http"):
            image = get(image).content
            open("temp.jpg", "wb").write(image)
            image = open("temp.jpg", "rb")
        elif isinstance(image, str) and not image.startswith("http"):
            image = open(image, "rb")
        return SResponse(self.session.handler(method="POST", url=f"/g/s/media/upload",
            data=image.read(), content_type="image/jpg")).mediaValue

    @community
    def join_chat(self, chatId: str) -> SResponse:
        """
        `join_chat` is the method that joins a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.join_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/member/{self.userId}"))

    @community
    def leave_chat(self, chatId: str) -> SResponse:
        """
        `leave_chat` is the method that leaves a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.leave_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/chat/thread/{chatId}/member/{self.userId}"))

    @community
    def kick(self, userId: str, chatId: str, allowRejoin: bool = True):
        """
        `kick` is the method that kicks a user from a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.kick(userId="5f4d2e0e0a0a0a0a0a0a0a0a", chatId="5f4d2e0e0a0a0a0a0a0a0a0a", allowRejoin=True)
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={1 if allowRejoin else 0}"))

    @community
    def delete_chat(self, chatId: str) -> SResponse:
        """
        `delete_chat` is the method that deletes a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.delete_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/chat/thread/{chatId}"))

    @community
    def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None) -> SResponse:
        """
        `delete_message` is the method that deletes a message from a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.delete_message(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", messageId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        data = {
            "adminOpName": 102,
            "timestamp": int(time() * 1000)
        }
        if asStaff and reason:
            data["adminOpNote"] = {"content": reason}

        if not asStaff: return SResponse(self.session.handler(
            method="DELETE", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message/{messageId}"))
        else: return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/message/{messageId}/admin",
            data=data))

    @community
    def transfer_host(self, chatId: str, userId: str):
        """
        `transfer_host` is the method that transfers the host of a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.transfer_host(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/transfer-organizer",
            data = {
                "uidList": [userId],
                "timestamp": int(time() * 1000)
                }))

    @community
    def accept_host(self, chatId: str, requestId: str):
        """
        `accept_host` is the method that accepts the host of a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.accept_host(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", requestId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept"))

    @community
    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None):
        """"
        `subscribe` is the method that subscribes to a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.subscribe(userId="5f4d2e0e0a0a0a0a0a0a0a0a", autoRenew=False, transactionId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        if not transactionId: transactionId = str(uuid4())
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/influencer/{userId}/subscribe",
            data = {
                "paymentContext": {
                    "transactionId": transactionId,
                    "isAutoRenew": autoRenew
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def thank_props(self, chatId: str, userId: str):
        """
        `thank_props` is the method that thanks a user for props.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.thank_props(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank"))

    @community
    def send_active(self, timezone: int=-300, start: int=time() * 1000, end: int=time() * 1000, timers: list=None) -> SResponse:
        """
        `send_active` is the method that sends the active time of the user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_active(timezone=-300, timers=[{"start": time() * 1000, "end": time() * 1000}]])
        >>> bot.run(sid=sid)
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

        return Response(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/community/stats/user-active-time", data=data))

    @community
    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, wikiId: str = None, transactionId: str = None) -> SResponse:
        """
        `send_coins` is the method that sends coins to a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.send_coins(coins=100, blogId="5f4d2e0e0a0a0a0a0a0a0a0a")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url= f'/x{self.community_id}/s/{"blog" if blogId else "chat/thread" if chatId else "item"}/{blogId if blogId else chatId if chatId else wikiId}/tipping',
            data = {
                "coins": coins,
                "tippingContext": {"transactionId": transactionId if transactionId else (str(uuid4()))},
                "timestamp": int(time() * 1000)
                }
            ))

    @community
    def start_chat(self, userIds: list, title: str = None, message: str = None, content: str = None) -> SResponse:
        """
        `start_chat` is the method that starts a chat with a user.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.start_chat(userIds=["5f4d2e0e0a0a0a0a0a0a0a0a"], title="Hello", message="Hello World!", content="Hello World!")
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread",
            data = {
                "title": title,
                "inviteeUids": userIds if isinstance(userIds, list) else [userIds],
                "initialMessageContent": message,
                "content": content,
                "timestamp": int(time() * 1000)
            }
        ))

    @community
    def invite_chat(self, chatId: str, userIds: list) -> SResponse:
        """
        `invite_chat` is the method that invites a user to a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.invite_chat(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", userIds=["5f4d2e0e0a0a0a0a0a0a0a0a"])
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/member/invite",
            data = {
                "uids": userIds if isinstance(userIds, list) else [userIds],
                "timestamp": int(time() * 1000)
            }
        ))

    @community
    def view_only(self, chatId: str, viewOnly: bool = True) -> SResponse:
        """
        `view_only` is the method that makes a chat view only.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.view_only(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", viewOnly=True)
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/view-only/enable" if viewOnly else f"/x{self.community_id}/s/chat/thread/{chatId}/view-only/disable"))

    @community
    def members_can_invite(self, chatId: str, canInvite: bool = True) -> SResponse:
        """
        `members_can_invite` is the method that makes a chat members can invite.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.members_can_invite(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", canInvite=True)
        >>> bot.run(sid=sid)
        ```
        """
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/members-can-invite/enable" if canInvite else f"/x{self.community_id}/s/chat/thread/{chatId}/members-can-invite/disable"))

    @community
    def change_chat_background(self, chatId: str, backgroundImage: str = None) -> SResponse:
        """
        `change_chat_background` is the method that changes the background of a chat.
        
        `**Example**`
        ```python
        >>> from pymino import Bot
        
        >>> bot = Bot()
        >>> bot.community.change_chat_background(chatId="5f4d2e0e0a0a0a0a0a0a0a0a", backgroundImage="https://i.imgur.com/0QZ0QZ0.png")
        >>> bot.run(sid=sid)
        ```
        """
        image = self._prep_image(backgroundImage)
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/chat/thread/{chatId}/member/{self.userId}/background",
            data = {
                "media": [100, self.upload_image(image), None],
                "timestamp": int(time() * 1000)
            }
        ))

    @community
    def solve_quiz(self, quizId: str, quizAnswers: Union[dict, list], hellMode: bool = False) -> SResponse:
        return SResponse(self.session.handler(
            method="POST", url=f"/x{self.community_id}/s/blog/{quizId}/quiz/result",
            data = {
                "quizAnswerList": quizAnswers if isinstance(quizAnswers, list) else [quizAnswers],
                "mode": 1 if hellMode else 0,
                "timestamp": int(time() * 1000)
            }
        ))

from time import time
from typing import BinaryIO
from .ext import *

class SubClient():
    """
    `SuBClient` is a class that handles SubClient functions.

    `**Example**`

    ```python
    from pymino import Client, SubClient

    client = Client()

    client.login(email="email", password="password")

    subClient = SubClient(comId="comId")

    subClient.edit_profile(username="New Username", bio="New Bio", avatar=open("avatar.png", "rb")

    ```
    """
    def __init__(self, comId: str, proxies: Optional[str]=None, debug: bool=False):
        self.sid = httpx_handler.sid
        self.auid = httpx_handler.auid
        self.httpx = httpx_handler(proxies=proxies, debug=debug)
        self.comId = comId

    def edit_profile(self, username: str = None, bio: str = None, avatar: str = None) -> User:
        """
        `SubClient.edit_profile` Edit your profile in the community

        `**Example**` 
        -  `>>> client.edit_profile(username="New Username", bio="New Bio", avatar=open("avatar.png", "rb"))`

        `**Parameters**`
        -  `username` - New username [Optional]
        -  `bio` - New bio [Optional]
        -  `avatar` - New avatar [Optional]

        `**Returns**`
        -  `User` - User Object

        """

        data = {"timestamp": int(time() * 1000)}
        options = {"username": username, "bio": bio, "avatar": avatar}
        for key, value in options.items():
            if value is not None:
                if key == "avatar":
                    data["icon"] = self.upload_media(value)
                else:
                    data[key] = value
        return User(self.httpx.send(
            method="POST", endpoint=f"/x{self.comId}/s/user-profile/{self.auid}", data=data))
    

    def online_status(self, status: int = 1) -> Response:
        """
        `SubClient.online_status` Change your online status in the community

        `**Example**` `>>> subClient.online_status(status=1)`

        `**Parameters**`
        -  `status` - Online status to change to [Optional] `>>> (1. Online, 2. Offline)`

        `**Returns**`
        -  `Response` - Response object

        """

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/user-profile/{self.auid}/online-status",
            data = {
                "status": status,
                "timestamp": int(time() * 1000)
            }))


    def play_lottery(self, timezone: int = -300) -> Response:
        """
        `SubClient.play_lottery` Play the lottery in the community

        `**Example** `>>> subClient.play_lottery(timezone=-300)`

        `**Parameters**`
        -  `timezone` - Timezone to play the lottery in [Optional]

        `**Returns**`
        -  `Response` - Response object

        """

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/check-in/lottery",
            data={
                "timestamp": int(time() * 1000),
                "timezone": timezone
            }))


    def check_in(self, timezone: int = -300) -> CheckIn:
        """
        `SubClient.check_in` Check in to the community

        `**Example**` `>>> subClient.check_in(timezone=-300)`

        `**Parameters**`

        -  `timezone` - Timezone to check in in [Optional]

        `**Returns**`
        
        """

        return CheckIn(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/check-in",
            data={
                "timestamp": int(time() * 1000),
                "timezone": timezone
            }))


    def generate_invite(self) -> Response:
        """
        `SubClient.generate_invite` Generate an invite link for the community

        `**Example**` `>>> subClient.generate_invite()`

        `**Returns**`
        -  `Response` - Response object
        
        """

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/g/s-x{self.comId}/community/invitation",
            data={
                "duration": 0,
                "force": "true",
                "timestamp": int(time() * 1000)
            }))

 
    def upload_media(self, file: BinaryIO, file_type: int) -> Response:
        """
        `SubClient.upload_media` Upload media to the community

        `**Example**` `>>> subClient.upload_media(file=open("image.png", "rb"), file_type=1)`

        `**Parameters**`
        -  `file` - File to upload
        -  `file_type` - File type to upload [Optional] 
        -  ` >>> (1: Image, 2: Audio)

        `**Returns**`
        -  `Response` - Response object

        """

        file_types = {"image": "image/jpg", "audio": "audio/aac"}
        return Response(
            self.httpx.handler(
                method="POST", endpoint=f"/g/s/media/upload",
                data=file.read(), type=file_types[file_type]
                )).mediaValue


    def fetch_new_user_coupon(self) -> Coupon:
        """
        `SubClient.fetch_new_user_coupon` Fetch new user coupon

        `**Example**` `>>> subClient.fetch_new_user_coupon()`

        `**Returns**`
        -  `Coupon` - Coupon object

        """

        return Coupon(self.httpx.handler(
            "GET", f"/x{self.comId}/s/coupon/new-user-coupon"))

  
    def fetch_notifications(self, size: int = 25) -> Notification:
        """
        `SubClient.fetch_notifications` Fetch notifications

        `**Example**` `>>> subClient.fetch_notifications(size=25)`

        `**Parameters**`
        -  `size` - Amount of notifications to fetch [Optional]

        `**Returns**`
        -  `Notification` - Notification object
        
        """

        return Notification(self.httpx.handler(
            "GET", f"/x{self.comId}/s/notification?pagingType=t&size={size}"), True)


    def fetch_user(self, userId: str) -> User:
        """
        `SubClient.fetch_user` Fetch a user in the community

        `**Example**` `>>> subClient.fetch_user(userId="123456789")`

        `**Parameters**`
        -  `userId` - User id to fetch information for [Required]

        `**Returns**`
        -  `User` - User object

        """

        return User(self.httpx.handler(
            "GET",f"/x{self.comId}/s/user-profile/{userId}"))


    def fetch_users(self, type: str = "recent", start: int = 0, size: int = 25) -> User:
        """
        `SubClient.fetch_users` Fetch users in the community

        `**Example**` `>>> subClient.fetch_users(type="recent", start=0, size=25)`

        `**Parameters**`
        -  `type` - Type of users to fetch [Optional] `>>> (leaders, curators, recent)`
        -  `start` - Start index of users to fetch [Optional]
        -  `size` - Amount of users to fetch [Optional]

        `**Returns**`
        -  `User` - User object

        """

        userTypes=["leaders", "curators", "recent"]
        if type not in userTypes: raise ValueError("Invalid Type! Valid Types: " + ", ".join(userTypes))
        return User(self.httpx.handler(
            "GET", f"/x{self.comId}/s/user-profile?type={type}&start={start}&size={size}"), True)


    def fetch_online_users(self, start: int = 0, size: int = 25) -> User:
        """
        `SubClient.fetch_online_users` Fetch online users in the community

        `**Example**` `>>> subClient.fetch_online_users(start=0, size=25)`

        `**Parameters**`
        -  `start` - Start index of users to fetch [Optional]
        -  `size` - Amount of users to fetch [Optional]

        `**Returns**`
        -  `User` - User object

        """

        return User(self.httpx.handler(
            "GET", f"/x{self.comId}/s/live-layer?topic=ndtopic:x{self.comId}:online-members&start={start}&size={size}"), True)


    def fetch_followers(self, userId: str, start: int = 0, size: int = 25) -> User:
        """
        `SubClient.fetch_followers` Fetch a user's followers

        `**Example**` `>>> subClient.fetch_followers(userId="123456789", start=0, size=25)`

        `**Parameters**`
        -  `userId` - User id to fetch followers of [Required]
        -  `start` - Start index of followers to fetch [Optional]
        -  `size` - Amount of followers to fetch [Optional]

        `**Returns**`
        -  `User` - User object

        """

        return User(self.httpx.handler(
            "GET", f"/x{self.comId}/s/user-profile/{userId}/member?start={start}&size={size}"), True)


    def fetch_following(self, userId: str, start: int = 0, size: int = 25) -> User:
        """
        `SubClient.fetch_following` Fetch a user's following

        `**Example**` `>>> subClient.fetch_following(userId="123456789", start=0, size=25)`

        `**Parameters**`
        -  `userId` - User id to fetch following of [Required]
        -  `start` - Start index of following to fetch [Optional]
        -  `size` - Amount of following to fetch [Optional]

        `**Returns**`
        -  `User` - User object
        
        """

        return User(self.httpx.handler(
            "GET", f"/x{self.comId}/s/user-profile/{userId}/joined?start={start}&size={size}"), True)


    def fetch_chat(self, chatId: str) -> Thread:
        """
        `SubClient.fetch_chat` Fetch a chat in the community

        `**Example**` `>>> subClient.fetch_chat(chatId="123456789")`

        `**Parameters**`
        -  `chatId` - Chat id to fetch [Required]

        `**Returns**`
        -  `Thread` - Thread object

        """

        return Thread(self.httpx.handler(
            "GET", f"/x{self.comId}/s/chat/thread/{chatId}"))


    def fetch_live_chats(self, start: int = 0, size: int = 25) -> Thread:
        """
        `SubClient.fetch_live_chats` Fetch live chats in the community
        
        `**Example**` `>>> fetch_live_chats(start=0, size=25)`
        
        `**Parameters**`
        -  `start` - Start index of chats to fetch [Optional]
        -  `size` - Amount of chats to fetch [Optional]
        
        `**Returns**`
        -  `Thread` - Thread object
        
        """

        return Thread(self.httpx.handler(
            "GET", f"/x{self.comId}/s/live-layer/public-live-chats?start={start}&size={size}"), True)  


    def fetch_chats(self, start: int = 0, size: int = 25) -> Thread:
        """
        `SubClient.fetch_chats` Fetch chats in the community
        
        `**Example**` `>>> fetch_chats(start=0, size=25)`
        
        `**Parameters**`
        -  `start` - Start index of chats to fetch [Optional]
        -  `size` - Amount of chats to fetch [Optional]
        
        `**Returns**`
        -  `Thread` - Thread object
        
        """

        return Thread(self.httpx.handler(
            "GET", f"/x{self.comId}/s/chat/thread?type=joined-me&start={start}&size={size}"), True)


    def fetch_public_chats(self, type: str = "recommended", start: int = 0, size: int = 25) -> Thread:
        """
        `SubClient.fetch_public_chats` Fetch public chats in the community

        `**Example**` `>>> fetch_public_chats(type="recommended", start=0, size=25)`

        `**Parameters**`
        - `type` - Type of chats to fetch [Optional]

        `>>> types = ["recommended", "latest", "popular"]`

        - `start` - Start index of chats to fetch [Optional]
        - `size` - Amount of chats to fetch [Optional]

        `**Returns**`
        -  `Thread` - Thread object

        """

        chatTypes = ["recommended", "latest", "popular"]
        if type not in chatTypes: raise ValueError("Invalid Type! Valid Types: " + ", ".join(chatTypes))
        return Thread(self.httpx.handler(
            "GET", f"/x{self.comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}"), True)


    def fetch_members(self, chatId: str, start: int = 0, size: int = 25) -> chatMembers:
        """
        `SubClient.fetch_members` Fetch members in a chat

        `**Example**` `>>> fetch_members(chatId="123456789", start=0, size=25)`

        `**Parameters**`

        -  `chatId`: Chat ID to fetch members from

        -  `start`: Start index of members to fetch [Optional]

        -  `size`: Amount of members to fetch [Optional]

        -  `Returns` chatMembers object

        """

        return chatMembers(self.httpx.handler(
            "GET", f"/x{self.comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default"))


    def fetch_messages(self, chatId: str, start: int = 0, size: int = 25) -> Message:
        """
        `SubClient.fetch_messages` Fetch messages from a chat

        `**Example**` `>>> fetch_messages(chatId="123456789", start=0, size=25)`

        `**Parameters**`

        -  `chatId`: Chat ID to fetch messages from

        -  `start`: Start index of messages to fetch [Optional]

        -  `size`: Amount of messages to fetch [Optional]

        -  `Returns` Message object

        """

        return Message(self.httpx.handler(
            "GET", f"/x{self.comId}/s/chat/thread/{chatId}/message?start={start}&size={size}&type=default"), True)


    def fetch_blogs(self, size: int = 25) -> Blog:
        """
        `SubClient.fetch_blogs` Fetch blogs in the community

        `**Example**` `>>> fetch_blogs(size=25)`

        `**Parameters**`

        -  `size`: Amount of blogs to fetch [Optional]

        -  `Returns` Blog object

        """

        return Blog(self.httpx.handler(
            "GET", f"/x{self.comId}/s/feed/blog-all?pagingType=t&size={size}"), True)


    def fetch_leaderboard(self, leaderboard: int = 1, start: int = 0, size: int = 20) -> User:
        """
        `SubClient.fetch_leaderboard` Fetch leaderboard in the community

        `**Example**` `>>> fetch_leaderboard(leaderboard=1, start=0, size=20)`

        `**Parameters**`

        -  `leaderboard`: Leaderboard type to fetch [Optional]

        `>>> (1: active-24h, 2: active-7d, 3: hall-of-fame, 4: highest-checkin, 5: highest-quiz-score)`

        -  `start`: Start index of leaderboard to fetch [Optional]

        -  `size`: Amount of leaderboard to fetch [Optional]

        -  `Returns` User object
        
        """

        return User(self.httpx.handler(
            "GET", f"/g/s-x{self.comId}/community/leaderboard?rankingType={leaderboard}&start={start}&size={size}"), True)


    def fetch_comments(self, userId: str=None, blogId: str=None, wikiId: str=None, start: int=0, size: int=25) -> Comment:
        """
        `SubClient.fetch_comments` Fetch comments in the community

        `**Example**` `>>> fetch_comments(userId="123456789", start=0, size=25)`

        `**Parameters**`

        -  `userId`: User ID to fetch comments from [Optional]
        -  `blogId`: Blog ID to fetch comments from [Optional]
        -  `wikiId`: Wiki ID to fetch comments from [Optional]
        -  `start`: Start index of comments to fetch [Optional]
        -  `size`: Amount of comments to fetch [Optional]

        -  `Returns` Comment object

        """
        if userId is None and blogId is None: raise Exception("User id or Blog Id is required.")
        if blogId is not None: return Comment(self.httpx.handler(
            "GET", f"/x{self.comId}/s/blog/{blogId}/comment?sort=newest&start={start}&size={size}"), True)
        if userId is not None: return Comment(self.httpx.handler(
            "GET", f"/x{self.comId}/s/user-profile/{userId}/comment?sort=newest&start={start}&size={size}"), True)
        if wikiId is not None: return Comment(self.httpx.handler(
            "GET", f"/x{self.comId}/s/item/{wikiId}/comment?sort=newest&start={start}&size={size}"), True)
            

    def set_cohost(self, chatId: str, uids: str or list) -> Response:
        """
        `SubClient.set_cohost` Set co-hosts in a chat

        `**Example**` `>>> set_cohost(chatId="123456789", uids=["123456789", "987654321"])`

        `**Parameters**`

        -  `chatId`: Chat ID to set co-hosts of

        -  `uids`: User ids to set as co-hosts

        -  `Returns` Response object

        """
        
        if type(uids) is str: uids = [uids]

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/chat/thread/{chatId}/co-host",
            data={"uidList": uids, "timestamp": int(time() * 1000)}))


    def remove_cohost(self, chatId: str, uid: str) -> Response:
        """
        `SubClient.remove_cohost` Remove co-hosts in a chat
            
            `**Example**` `>>> remove_cohost(chatId="123456789", uid="123456789")`

            `**Parameters**`
    
            -  `chatId`: Chat ID to remove co-hosts of
            
            -  `uid`: User id to remove as co-host
            
            -  `Returns` Response object
            
            """

        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/chat/thread/{chatId}/co-host/{uid}"))


    def follow(self, userId: str) -> Response:
        """
        `SubClient.follow` Follow a user

        `**Example**` `>>> follow(userId="123456789")`

        `**Parameters**`

        -  `userId`: User id to follow

        -  `Returns` Response object

        """

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/user-profile/{userId}/member"))


    def unfollow(self, userId: str) -> Response:
        """
        `SubClient.unfollow` Unfollow a user

        `**Example**` `>>> unfollow(userId="123456789")`

        `**Parameters**`

        -  `userId`: User id to unfollow

        -  `Returns` Response object

        """
        
        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/user-profile/{userId}/member"))


    def block(self, userId: str) -> Response:
        """
        `SubClient.block` Block a user
        
        `**Example**` `>>> block(userId="123456789")`

        `**Parameters**`
        
        -  `userId`: User id to block
        
        -  `Returns` Response object
        
        """

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/block/{userId}"))


    def unblock(self, userId: str) -> Response:
        """
        `SubClient.unblock` Unblock a user

        `**Example**` `>>> unblock(userId="123456789")`

        `**Parameters**`

        -  `userId`: User id to unblock

        -  `Returns` Response object

        """

        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/block/{userId}"))


    def post_blog(self, title: str, content: str, image: BinaryIO=None) -> Blog:
        """
        `SubClient.post_blog` Post a blog in the community
        
        `**Example**` `>>> post_blog(title="Hello World!", content="This is a blog post.", image=open("image.png", "rb"))`

        `**Parameters**`

        -  `title`: Title of the blog post

        -  `content`: Content of the blog post

        -  `image`: Image to upload [Optional] 

        -  `Returns` Blog object

        """

        return Blog(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/blog",
            data = {
                "title": title,
                "content": content,
                "timestamp": int(time() * 1000),
                "mediaList": [self.upload_media(image, 1)] if image is not None else []
            }))


    def delete_blog(self, blogId: str) -> Response:
        """
        `SubClient.delete_blog` Delete a blog in the community

        `**Example**` `>>> delete_blog(blogId="123456789")`

        -  `blogId`: Blog id to delete

        -  `Returns` Response object

        """

        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/blog/{blogId}"))

    
    def post_wiki(self, title: str, content: str, image: BinaryIO=None, keyword: str=None, value: int=5, type: str="levelStar") -> Wiki:
        """
        `SubClient.post_wiki` Post a wiki in the community
        
        `**Example**` `>>> post_wiki(title="Hello World!", content="This is a wiki post.", image=open("image.png", "rb"))`

        -  `title`: Title of the wiki post

        -  `content`: Content of the wiki post

        -  `image`: Image to upload [Optional] 

        -  `keyword`: Keyword of the wiki post [Optional]

        -  `value`: Value of the wiki post [Optional]

        -  `type`: Type of the wiki post [Optional]

        -  `Returns` Wiki object

        """
    
        return Wiki(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/item",
            data = {
                "label": title,
                "content": content,
                "icon": self.upload_media(image, "image") if image is not None else None,
                "keywords": keyword,
                "timestamp": int(time() * 1000),
                "mediaList": [self.upload_media(image, "image")] if image is not None else [],
                "props": [{"title": "My Rating", "value": value, "type": type}]
                }))


    def delete_wiki(self, wikiId: str) -> Response:
        """
        `SubClient.delete_wiki` Delete a wiki in the community

        `**Example**` `>>> delete_wiki(wikiId="123456789")`

        -  `wikiId`: Wiki id to delete

        -  `Returns` Response object

        """
        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/item/{wikiId}"))


    def delete_comment(self, commentId: str, userId: str=None, blogId: str=None, wikiId: str=None) -> Response:
        """
        `SubClient.delete_comment` Delete a comment in the community

        `**Example**` `>>> delete_comment(commentId="123456789")`

        -  `commentId`: Comment id to delete

        -  `userId`: User id to delete comment from [Optional]

        -  `blogId`: Blog id to delete comment from [Optional]

        -  `wikiId`: Wiki id to delete comment from [Optional]

        -  `Returns` Response object

        """

        if userId is None and blogId is None and wikiId is None: raise Exception("Specify a type.")
        if userId is not None: return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/user-profile/{userId}/comment/{commentId}"))
        if blogId is not None: return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/blog/{blogId}/comment/{commentId}"))
        if wikiId is not None: return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/item/{wikiId}/comment/{commentId}"))


    def comment(self, content: str, image: BinaryIO=None, userId: str=None, blogId: str=None, wikiId: str=None) -> Comment:
        """
        `SubClient.comment` Comment on a user, blog, or wiki

        `**Example**` `>>> comment(content="Hello World!"), userId="123456789")`

        -  `content`: Content of the comment

        -  `image`: Image to upload [Optional]

        -  `userId`: User id to comment on [Optional]

        -  `blogId`: Blog id to comment on [Optional]

        -  `wikiId`: Wiki id to comment on [Optional]

        -  `Returns` Comment object

        """

        if userId is None and blogId is None and wikiId is None: raise Exception("Specify a type.")
        data = {
            "content": content,
            "mediaList": [self.upload_media(image, 1)] if image is not None else [],
            "stickerId": None,
            "type": 0,
            "eventSource": "FeedList" if userId is None else "UserProfileView",
            "timestamp": int(time() * 1000)
            }
        if userId is not None: return Comment(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/user-profile/{userId}/comment",
            data=data))
        if blogId is not None: return Comment(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/blog/{blogId}/comment",
            data=data))
        if wikiId is not None: return Comment(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/item/{wikiId}/comment",
            data=data))

    
    def like(self, commentId: str=None, userId: str=None, blogId: str=None, wikiId: str=None) -> Response:
        """
        `SubClient.like` Like a comment, user, blog, or wiki

        `**Example**` `>>> like(commentId="123456789")`

        -  `commentId`: Comment id to like [Optional]

        -  `userId`: User id to like [Optional]

        -  `blogId`: Blog id to like [Optional]

        -  `wikiId`: Wiki id to like [Optional]

        -  `Returns` Response object

        """

        if commentId is None and blogId is None and wikiId is None: raise Exception("Specify a type.")
        data = {
            "value": 1 if commentId is not None else 4,
            "eventSource": "CommentDetailView" if commentId is not None else "UserProfileView" if userId is not None else "FeedList",
            "timestamp": int(time() * 1000)
            }

        if commentId:
            if userId is not None:
                return Response(self.httpx.handler(
                    method="POST", endpoint=f"/x{self.comId}/s/user-profile/{userId}/comment/{commentId}/vote?cv=1.2&value={data['value']}", data=data))

            if blogId is not None:
                return Response(self.httpx.handler(
                    method="POST", endpoint=f"/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value={data['value']}", data=data))

            if wikiId is not None:
                return Response(self.httpx.handler(
                    method="POST", endpoint=f"/x{self.comId}/s/item/{wikiId}/comment/{commentId}/vote?cv=1.2&value={data['value']}", data=data))

        else:
            if blogId is not None:
                return Response(self.httpx.handler(
                    method="POST", endpoint=f"/x{self.comId}/s/blog/{blogId}/vote?cv=1.2&value={data['value']}", data=data))

        if wikiId is not None:
                return Response(self.httpx.handler(
                    method="POST", endpoint=f"/x{self.comId}/s/item/{wikiId}/vote?cv=1.2&value={data['value']}", data=data))


    def unlike(self, commentId: str=None, userId: str=None, blogId: str=None, wikiId: str=None) -> Response:
        """
        `SubClient.unlike` Unlike a comment, user, blog, or wiki

        `**Example**` `>>> unlike(commentId="123456789")`

        -  `commentId`: Comment id to unlike [Optional]

        -  `userId`: User id to unlike [Optional]

        -  `blogId`: Blog id to unlike [Optional]

        -  `wikiId`: Wiki id to unlike [Optional]

        -  `Returns` Response object

        """

        if commentId is None and blogId is None and wikiId is None: raise Exception("Specify a type.")

        if commentId:
            if userId is not None:
                return Response(self.httpx.handler(
                    "DELETE", f"/x{self.comId}/s/user-profile/{userId}/comment/{commentId}/vote?eventSource=UserProfileView"))

            if blogId is not None:
                return Response(self.httpx.handler(
                    "DELETE", f"/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?eventSource=CommentDetailView"))

            if wikiId is not None:
                return Response(self.httpx.handler(
                    "DELETE", f"/x{self.comId}/s/item/{wikiId}/comment/{commentId}/vote?eventSource=CommentDetailView"))
        
        else:
            if blogId is not None:
                return Response(self.httpx.handler(
                    "DELETE", f"/x{self.comId}/s/blog/{blogId}/vote?eventSource=FeedList"))

            if wikiId is not None:
                return Response(self.httpx.handler(
                    "DELETE", f"/x{self.comId}/s/item/{wikiId}/vote?eventSource=FeedList"))


    def invite_chat(self, chatId, userId) -> Response:
        """
        `SubClient.invite_chat` Invite a user to a chat
        
        `**Example**` `>>> invite_chat(chatId="123456789", userId="123456789")`

        -  `chatId`: Chat id to invite to

        -  `userId`: User id to invite

        -  `Returns` Response object

        """

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/chat/thread/{chatId}/member/invite",
                data={
                    "uids": userId if type(userId) == list else [userId],
                    "timestamp": int(time() * 1000)
                }))


    def delete_message(self, chatId: str, messageId: str, asModerator: bool = False, reason: str = None) -> Response:
        """
        `SubClient.delete_message` Delete a message from a chat
        
        `**Example**` `>>> delete_message(chatId="123456789", messageId="123456789")`

        -  `chatId`: Chat id to delete message from

        -  `messageId`: Message id to delete

        -  `asModerator`: Delete as moderator [Optional]

        -  `reason`: Reason for deletion [Optional]

        -  `Returns` Response object

        """
        #NOTE: asModerator not implemented yet
        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}"))


    def send_message(self, chatId: str, message: str, messageType: int = 0) -> Response:
        """
        `SubClient.send_message` Send a message to a chat

        `**Example**` `>>> send_message(chatId="123456789", message="Hello!")`

        -  `chatId`: Chat id to send message to

        -  `message`: Message to send

        -  `messageType`: Message type [Optional]

        -  `Returns` Response object

        """
        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/chat/thread/{chatId}/message",
            data = {
                "content": message,
                "timestamp": int(time() * 1000),
                "type": messageType
            }))

        
    def join_chat(self, chatId: str) -> Response:
        """
        `SubClient.join_chat` Join a chat
        
        `**Example**` `>>> join_chat(chatId="123456789")`
        
        -  `chatId`: Chat id to join
        
        -  `Returns` Response object
        
        """
        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/chat/thread/{chatId}/member/{self.auid}"))
            

    def leave_chat(self, chatId: str) -> Response:
        """
        `SubClient.leave_chat` Leave a chat

        `**Example**` `>>> leave_chat(chatId="123456789")`

        -  `chatId`: Chat id to leave

        -  `Returns` Response object

        """
        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/chat/thread/{chatId}/member/{self.auid}"))


    def kick(self, chatId: str, userId: str, allowRejoin: bool=False) -> Response:
        """
        `SubClient.kick` Kick a user from a chat

        `**Example**` `>>> kick(chatId="123456789", userId="123456789")`

        -  `chatId`: Chat id to kick from

        -  `userId`: User id to kick

        -  `allowRejoin`: Allow user to rejoin chat [Optional] (0: False, 1: True)

        -  `Returns` Response object

        """

        return Response(self.httpx.handler(
            "DELETE", f"/x{self.comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={1 if allowRejoin else 0}"))


    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None) -> Response:
        """
        `SubClient.subscribe` Subscribe to a user

        `**Example**` `>>> subscribe(userId="123456789")`

        -  `userId`: User id to subscribe to

        -  `autoRenew`: Auto renew subscription [Optional] (0: False, 1: True)

        -  `transactionId`: Transaction id [Optional]

        -  `Returns` Response object

        """
        if transactionId is None: transactionId = str(uuid4())

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/influencer/{userId}/subscribe",
            data = {
                "paymentContext": {
                    "transactionId": transactionId,
                    "isAutoRenew": autoRenew
                },
                "timestamp": int(time() * 1000)
            }))
            

    def edit_chat(self, chatId: str, chatTitle: str = None, chatDescription: str = None, fansOnly: int = 0, publishToGlobal: int = 0, announcement: str = None, coverImage: str = None, backgroundImage: str = None, viewOnlyMode: bool = False) -> Response:
        """
        `SubClient.edit_chat` Edit a chat
        
        `**Example**` `>>> edit_chat(chatId="123456789", chatTitle="New Title", chatDescription="New Description", fansOnly=0, publishToGlobal=0, announcement="New Announcement", coverImage="New Cover Image", backgroundImage="New Background Image", viewOnlyMode=False)`
        
        -  `chatId`: Chat id to edit
        
        -  `chatTitle`: Chat title [Optional]
        
        -  `chatDescription`: Chat description [Optional]
        
        -  `fansOnly`: Fans only [Optional] (0: False, 1: True)
        
        -  `publishToGlobal`: Publish to global [Optional] (0: False, 1: True)
        
        -  `announcement`: Chat announcement [Optional]
        
        -  `coverImage`: Chat cover image [Optional]
        
        -  `backgroundImage`: Chat background image [Optional]
        
        -  `viewOnlyMode`: Chat view only mode [Optional] (0: False, 1: True)
        
        -  `Returns` Response object
        
        """
        attributes = {
            "title": chatTitle,
            "content": chatDescription,
            "fansOnly": fansOnly,
            "publishToGlobal": publishToGlobal,
            "announcement": announcement,
            "icon": coverImage,
            "backgroundImage": backgroundImage,
            "viewOnly": viewOnlyMode
        }

        data = {"timestamp": int(time() * 1000)}

        for key, value in attributes.items():
            if value is not None:
                if key == "announcement": data["extensions"] = {"announcement": value, "pinAnnouncement": True}
                elif key == "fansOnly": data["extensions"] = {"fansOnly": value}
                elif key == "backgroundImage":
                    self.httpx.handler(
                        method="POST", endpoint=f"/x{self.comId}/s/chat/thread/{chatId}/member/{self.auid}/background",
                        data={"media": [100, value, None], "timestamp": int(time() * 1000)})
                elif key == "viewOnly":
                    self.httpx.handler("POST", f"/x{self.comId}/s/chat/thread/{chatId}/view-only/{value}")

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/chat/thread/{chatId}", data=data))
        

    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, transactionId: str = None) -> Response:
        """
        `SubClient.send_coins` Send coins to a user

        `**Example**` `>>> send_coins(coins=100, blogId="123456789")`

        -  `coins`: Coins to send

        -  `blogId`: Blog id to send to [Optional]

        -  `chatId`: Chat id to send to [Optional]

        -  `transactionId`: Transaction id [Optional]

        -  `Returns` Response object

        """

        if blogId:
            endlink = f"/x{self.comId}/s/blog/{blogId}/tipping"

        elif chatId:
            endlink = f"/x{self.comId}/s/chat/thread/{chatId}/tipping"

        data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId if transactionId else (str(uuid4()))},
            "timestamp": int(time() * 1000)
            }
        
        return Response(self.httpx.handler(
            "POST", endlink= endlink, data=data))


    def ban(self, userId: str, reason: str="B", banType: int=None) -> Response:
        """
        `SubClient.ban` Ban a user

        `**Example**` `>>> ban(userId="123456789", reason="B")`

        -  `userId`: User id to ban

        -  `reason`: Ban reason [Optional]

        -  `banType`: Ban type [Optional]

        -  `Returns` Response object

        """

        return Response(self.httpx.handler("POST", f"/x{self.comId}/s/user-profile/{userId}/ban",
            data = {
                "reasonType": banType,
                "note": {
                    "content": reason
                },
                "timestamp": int(time() * 1000)
            }))


    def send_active(self, timezone: int=-300, start: int=time() * 1000, end: int=time() * 1000, timers: list=None) -> Response:
        """
        `SubClient.send_active` Send active time

        `**Example**` `>>> send_active(timezone=-300, start=time() * 1000, end=time() * 1000, timers=None)`

        -  `timezone`: Timezone [Optional]

        -  `start`: Start time [Optional]

        -  `end`: End time [Optional]

        -  `timers`: List of timers [Optional] 
        
        -  `Example` `>>> timers=[{"start": time() * 1000, "end": time() * 1000}, {"start": time() * 1000, "end": time() * 1000}]`

        -  `Returns` Response object

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

        return Response(self.httpx.handler(
            method="POST", endpoint=f"/x{self.comId}/s/community/stats/user-active-time", data=data))

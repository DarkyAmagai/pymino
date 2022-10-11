from typing import List, Dict, Union

class Objects:
    def __init__(self): pass

    def fetch_key(self, data: Union[Dict, List], key: str, isList: bool=False) -> Union[str, List]:
        """
        Fetches a key from a dictionary or list of dictionaries. 

        `data` - The dictionary or list of dictionaries to fetch the key from. 

        `key` - The key to fetch. [str]

        `isList` - Whether you want to return a list of the keys or not. [bool]

        `**Example**`:
        ```py
        from xamino import Objects

        objects = Objects()
        data = {
            "timestamp": 123456789,
            "message": "Hello, world!"
            "author": {
                "name": "pymino user",
                "uid": "123456789"
            }

        print(objects.fetch_key(data=data, key="name"))
        # Output: pymino user
        """
        if isinstance(data, dict):
            """
            If the data is a dictionary, then it will return the value of the key.
            """
            if key in data:
                if isList: return [data[key]]
                else: return data[key]
            else:
                if isList: res = []
                else: res = None
                for k, v in data.items():
                    if isinstance(v, (dict, list)):
                        if isList: res += self.fetch_key(v, key, isList)
                        else: res = self.fetch_key(v, key, isList)
                        if res and not isList: return res
                return res

        elif isinstance(data, list):
            """
            If the data is a list, then it will return a list of the values of the key.
            """
            if isList: res = []
            else: res = None
            for item in data:
                if isinstance(item, (dict, list)):
                    if isList: res += self.fetch_key(item, key, isList)
                    else: res = self.fetch_key(item, key, isList)
                    if res and not isList: return res
            return res
        else: return None

class EventTypes:
    """
    A class that contains the event types for Socket.
    """
    text_message = "0:0"
    image_message = "0:100"
    youtube_message = "0:103"
    strike_message = "1:0"
    voice_message = "2:110"
    sticker_message = "3:113"
    vc_not_answered = "52:0"
    vc_not_cancelled = "53:0"
    vc_not_declined = "54:0"
    video_chat_not_answered = "55:0"
    video_chat_not_cancelled = "56:0"
    video_chat_not_declined = "57:0"
    avatar_chat_not_answered = "58:0"
    avatar_chat_not_cancelled = "59:0"
    avatar_chat_not_declined = "60:0"
    delete_message = "100:0"
    member_join = "101:0"
    member_leave = "102:0"
    chat_invite = "103:0"
    chat_background_changed = "104:0"
    chat_title_changed = "105:0"
    chat_icon_changed = "106:0"
    vc_start = "107:0"
    video_chat_start = "108:0"
    avatar_chat_start = "109:0"
    vc_end = "110:0"
    video_chat_end = "111:0"
    avatar_chat_end = "112:0"
    chat_content_changed = "113:0"
    screen_room_start = "114:0"
    screen_room_end = "115:0"
    chat_host_transfered = "116:0"
    text_message_force_removed = "117:0"
    chat_removed_message = "118:0"
    mod_deleted_message = "119:0"
    chat_tip = "120:0"
    chat_pin_announcement = "121:0"
    vc_permission_open_to_everyone = "122:0"
    vc_permission_invited_and_requested = "123:0"
    vc_permission_invite_only = "124:0"
    chat_view_only_enabled = "125:0"
    chat_view_only_disabled = "126:0"
    chat_unpin_announcement = "127:0"
    chat_tipping_enabled = "128:0"
    chat_tipping_disabled = "129:0"
    timestamp_message = "65281:0"
    welcome_message = "65282:0"
    invite_message = "65283:0"

class User:
    """
    Contains the user's properties such as their username, userId, and more.
    """
    def __init__(self, data: dict, isList: bool=False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        """
        Fetches a key from the user's data.
        """
        try: return [i[key] for i in self._json["userProfileList"]] if self._list else self._json["userProfile"][key]
        except (KeyError, TypeError): return Objects().fetch_key(self._json, key, self._list)

    @property
    def moodSticker(self) -> str: return self._fetch("moodSticker")
    @property
    def itemsCount(self) -> int: return self._fetch("itemsCount")
    @property
    def consecutiveCheckInDays(self) -> int: return self._fetch("consecutiveCheckInDays")
    @property
    def userId(self) -> str: return self._fetch("uid")
    @property
    def modifiedTime(self) -> str: return self._fetch("modifiedTime")
    @property
    def followingStatus(self) -> int: return self._fetch("followingStatus")
    @property
    def onlineStatus(self) -> int: return self._fetch("onlineStatus") 
    @property
    def accountMembershipStatus(self) -> int: return self._fetch("accountMembershipStatus")
    @property
    def isGlobal(self) -> bool: return self._fetch("isGlobal")
    @property
    def avatarFrameId(self) -> str: return self._fetch("avatarFrameId")
    @property
    def fanClubList(self) -> list: return self._fetch("fanClubList")
    @property
    def reputation(self) -> int: return self._fetch("reputation")
    @property
    def postsCount(self) -> int: return self._fetch("postsCount")
    @property
    def avatarFrame(self) -> dict: return self._fetch("avatarFrame")
    @property
    def followers(self) -> int: return self._fetch("membersCount")
    @property
    def username(self) -> str: return self._fetch("nickname")
    @property
    def mediaList(self) -> list: return self._fetch("mediaList")
    @property
    def avatar(self) -> str: return self._fetch("icon")
    @property
    def isNicknameVerified(self) -> bool: return self._fetch("isNicknameVerified")
    @property
    def visitorsCount(self) -> int: return self._fetch("visitorsCount")
    @property
    def mood(self) -> str: return self._fetch("mood")
    @property
    def level(self) -> int: return self._fetch("level")        
    @property
    def notificationSubscriptionStatus(self) -> int: return self._fetch("notificationSubscriptionStatus")
    @property
    def pushEnabled(self) -> bool: return self._fetch("pushEnabled")
    @property
    def membershipStatus(self) -> int: return self._fetch("membershipStatus")
    @property
    def bio(self) -> str: return self._fetch("content")
    @property
    def following(self) -> int: return self._fetch("joinedCount")
    @property
    def role(self) -> int: return self._fetch("role")
    @property
    def commentsCount(self) -> int: return self._fetch("commentsCount")
    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def extensions(self) -> dict: return self._fetch("extensions")
    @property
    def privilegeOfCommentOnUserProfile(self) -> int: return self._fetch("privilegeOfCommentOnUserProfile")
    @property
    def style(self) -> dict: return self._fetch("style")
    @property
    def backgroundColor(self) -> str: return self._fetch("backgroundColor")
    @property
    def customTitles(self) -> list: return self._fetch("customTitles")
    @property
    def defaultBubbleId(self) -> str: return self._fetch("defaultBubbleId")
    @property
    def isHidden(self) -> bool: return self._fetch("hideUserProfile")
    @property
    def privilegeOfChatInviteRequest(self) -> int: return self._fetch("privilegeOfChatInviteRequest")
    @property
    def visitPrivacy(self) -> int: return self._fetch("visitPrivacy")
    @property
    def storiesCount(self) -> int: return self._fetch("storiesCount")
    @property
    def blogsCount(self) -> int: return self._fetch("blogsCount")
    @property
    def showStoreBadge(self) -> bool: return self._fetch("showStoreBadge")    
    @property
    def aminoId(self) -> str: return self._fetch("aminoId")
    @property
    def json(self) -> dict: return self._json

class Authenticate:
    """
    Contains the authentication properties such as the sid, secret, and more.

    Usually used for login/registration.
    """
    def __init__(self, data: dict) -> None:
        self._json = data

    def _fetch(self, key: str) -> Union[str, List]:
        """
        Fetches a key from the authentication data.
        """
        try: return self._json.get(key)
        except: Objects().fetch_key(self._json, key)

    @property
    def sid(self) -> str: return self._fetch("sid")
    @property
    def userId(self) -> str: return self._fetch("auid")
    @property
    def profile(self) -> User: return User(self._fetch("userProfile"))
    @property
    def secret(self) -> str: return self._fetch("secret")
    @property
    def json(self) -> dict: return self._json


class linkInfoV2:
    """
    Contains properties such as ndcId, objectId and more.

    Uses fetch_key() from Objects class to fetch the key.
    """
    def __init__(self, data: dict) -> None:
        self._json = data
    
    @property
    def fullPath(self) -> str: return (Objects().fetch_key(self._json, "fullPath", False))
    @property
    def comId(self) -> int: return (Objects().fetch_key(self._json, "ndcId", False))
    @property
    def objectId(self) -> str: return (Objects().fetch_key(self._json, "objectId", False))
    @property
    def objectType(self) -> int: return (Objects().fetch_key(self._json, "objectType", False))
    @property
    def shortCode(self) -> str: return (Objects().fetch_key(self._json, "shortCode", False))
    @property
    def targetCode(self) -> int: return (Objects().fetch_key(self._json, "targetCode", False))
    @property
    def path(self) -> str: return (Objects().fetch_key(self._json, "path", False))
    @property
    def json(self) -> dict: return self._json

class SResponse:
    """
    Contains the response from the API.
    """
    def __init__(self, data: dict) -> None:
        self._json = data

    @property
    def statuscode(self) -> int: return self._json["api:statuscode"]
    @property
    def duration(self) -> str: return self._json["api:duration"]
    @property
    def message(self) -> str: return self._json["api:message"]
    @property
    def timestamp(self) -> str: return self._json["api:timestamp"]
    @property
    def devOptions(self) -> dict: return self._json["devOptions"]
    @property
    def mediaValue(self) -> str: return self._json["mediaValue"]
    @property
    def json(self) -> dict: return self._json

class ResetPassword:
    """
    Contains the response from the API when resetting the password.
    """
    def __init__(self, data: dict) -> None:
        self._json = data

    @property
    def response(self) -> SResponse: return SResponse(self._json)
    @property
    def secret(self): return self._json["secret"]
    @property
    def json(self): return self._json

class Comment:
    """
    Contains comment properties such as content, author, and more.
    """
    def __init__(self, data: dict, isList: bool=False):
        self._json = data
        self._list = isList

    def _fetch(self, key):
        """
        Fetches a key from the comment data.
        """
        try: return [i[key] for i in self._json["commentList"]] if self._list else self._json["comment"][key]
        except (KeyError, TypeError): Objects().fetch_key(self._json, key, self._list)

    @property
    def modifiedTime(self) -> str: return self._fetch("modifiedTime")
    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def votedValue(self) -> int: return self._fetch("votedValue")
    @property
    def parentType(self) -> int: return self._fetch("parentType")
    @property
    def commentId(self) -> str: return self._fetch("commentId")
    @property
    def parentndcId(self) -> int: return self._fetch("parentndcId")
    @property
    def mediaList(self) -> list: return self._fetch("mediaList")
    @property
    def votesSum(self) -> int: return self._fetch("votesSum")
    @property
    def user(self) -> User: return User([i["author"] for i in self._json["commentList"]], True) if self._list else User(self._json["comment"]["author"])
    @property
    def content(self) -> str: return self._fetch("content")
    @property
    def extensions(self) -> dict: return self._fetch("extensions")
    @property
    def parentId(self) -> str: return self._fetch("parentId")
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def subcommentsCount(self) -> int: return self._fetch("subcommentsCount")
    @property
    def type(self) -> int: return self._fetch("type")
    @property
    def json(self) -> dict: return self._json

class Blog:
    """
    Contains blog properties such as title, content, and more.
    """
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        try: return [i[key] for i in self._json["blogList"]] if self._list else self._json["blog"][key]
        except (KeyError, TypeError): Objects().fetch_key(self._json, key, self._list)
        
    @property
    def globalVotesCount(self) -> int: return self._fetch("globalVotesCount")
    @property
    def globalVotedValue(self) -> int: return self._fetch("globalVotedValue")
    @property
    def votedValue(self) -> int: return self._fetch("votedValue")
    @property
    def keywords(self) -> str: return self._fetch("keywords")
    @property
    def mediaList(self) -> list: return self._fetch("mediaList")
    @property
    def style(self) -> int: return self._fetch("style")
    @property
    def totalQuizPlayCount(self) -> int: return self._fetch("totalQuizPlayCount")
    @property
    def title(self) -> str: return self._fetch("title")
    @property
    def tipInfo(self) -> dict: return self._fetch("tipInfo")
    @property
    def contentRating(self) -> int: return self._fetch("contentRating")
    @property
    def content(self) -> str: return self._fetch("content")
    @property
    def needHidden(self) -> bool: return self._fetch("needHidden")
    @property
    def guestVotesCount(self) -> int: return self._fetch("guestVotesCount")
    @property
    def type(self) -> int: return self._fetch("type")
    @property
    def status(self) -> int: return self._fetch("status")
    @property
    def globalCommentsCount(self) -> int: return self._fetch("globalCommentsCount")
    @property
    def modifiedTime(self) -> str: return self._fetch("modifiedTime")
    @property
    def widgetDisplayInterval(self) -> None: return self._fetch("widgetDisplayInterval")
    @property
    def totalPollVoteCount(self) -> int: return self._fetch("totalPollVoteCount")
    @property
    def blogId(self) -> str: return self._fetch("blogId")
    @property
    def viewCount(self) -> int: return self._fetch("viewCount")
    @property
    def language(self) -> None: return self._fetch("language")
    @property
    def author(self) -> User:
        return User([author["author"] for author in self._json["blogList"]], isList=True)
    @property
    def extensions(self) -> dict: return self._fetch("extensions")
    @property
    def votesCount(self) -> int: return self._fetch("votesCount")
    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def endTime(self) -> None: return self._fetch("endTime")
    @property
    def commentsCount(self) -> int: return self._fetch("commentsCount")
    @property
    def json(self) -> dict: return self._json
        
class Wiki:
    """
    Contains wiki properties such as author, content, and more.
    """
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        """
        Fetches a key from the wiki data.
        """
        try: return [i[key] for i in self._json["itemList"]] if self._list else self._json["item"][key]
        except KeyError: Objects().fetch_key(self._json, key, self._list)
      
    @property
    def globalVotesCount(self) -> int: return self._fetch("globalVotesCount")
    @property
    def globalVotedValue(self) -> int: return self._fetch("globalVotedValue")
    @property
    def votedValue(self) -> int: return self._fetch("votedValue")
    @property
    def keywords(self) -> str: return self._fetch("keywords")
    @property
    def mediaList(self) -> list: return self._fetch("mediaList")
    @property
    def style(self) -> int: return self._fetch("style")
    @property
    def author(self) -> User: return User([author["author"] for author in self._json["itemList"]], isList=True)
    @property
    def contentRating(self) -> int: return self._fetch("contentRating")
    @property
    def label(self) -> str: return self._fetch("label")
    @property
    def content(self) -> str: return self._fetch("content")
    @property
    def needHidden(self) -> bool: return self._fetch("needHidden")
    @property
    def guestVotesCount(self) -> int: return self._fetch("guestVotesCount")
    @property
    def status(self) -> int: return self._fetch("status")
    @property
    def globalCommentsCount(self) -> int: return self._fetch("globalCommentsCount")
    @property
    def modifiedTime(self) -> str: return self._fetch("modifiedTime")
    @property
    def wikiId(self) -> str: return self._fetch("wikiId")
    @property
    def extensions(self) -> dict: return self._fetch("extensions")
    @property
    def votesCount(self) -> int: return self._fetch("votesCount")
    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def commentsCount(self) -> int: return self._fetch("commentsCount")
    @property
    def json(self) -> dict: return self._json

class chatMembers:
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data["memberList"]
        self._list = isList

    @property
    def members(self) -> User: return User([user for user in self._json], isList=True)
    @property
    def json(self) -> dict: return self._json

class ReplyMessage:
    def __init__(self, data: dict):
        try:
            self._json = data["chatMessage"]["extensions"]["replyMessage"]
        except KeyError:
            self._json = data

    @property
    def includedInSummary(self) -> bool: return self._json["includedInSummary"]
    @property
    def uid(self) -> str: return self._json["uid"]
    @property
    def author(self) -> User: return User(self._json["author"])
    @property
    def isHidden(self) -> bool: return self._json["isHidden"]
    @property
    def messageId(self) -> str: return self._json["messageId"]
    @property
    def mediaType(self) -> int: return self._json["mediaType"]
    @property
    def content(self) -> str: return self._json["content"]
    @property
    def clientRefId(self) -> int: return self._json["clientRefId"]
    @property
    def threadId(self) -> str: return self._json["threadId"]
    @property
    def createdTime(self) -> str: return self._json["createdTime"]
    @property
    def extensions(self) -> dict: return self._json["extensions"]
    @property
    def type(self) -> int: return self._json["type"]
    @property
    def json(self) -> dict: return self._json

class messageExtensions: #NOTE: This is a work in progress! I Have not even tested this yet.
    def __init__(self, data: dict):
        self._json = data

    @property
    def replyMessageId(self) -> str: return self._json["replyMessageId"]
    @property
    def replyMessage(self) -> ReplyMessage:
        return ReplyMessage(self._json["replyMessage"])
    @property
    def json(self) -> dict: return self._json

class Message:
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList
        self.message = ["message"]

        try:
            if self._json["o"]: self._json = self._json["o"]
            self.message = ["chatMessage"]
        except KeyError: pass

    def _fetch(self, key) -> Union[str, List]:
        try: return [i[key] for i in self._json["messageList"]] if self._list else self._json[self.message][key]
        except (KeyError, TypeError): return Objects().fetch_key(self._json, key, self._list)

    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def userId(self) -> str: return self._fetch("uid")
    @property 
    def author(self) -> User: return User(self._json, isList=self._list)
    @property
    def chatId(self) -> str: return self._fetch("threadId")
    @property
    def mediaType(self) -> int: return self._fetch("mediaType")
    @property
    def content(self) -> str: return self._fetch("content")
    @property
    def clientRefId(self) -> int: return self._fetch("clientRefId")
    @property
    def messageId(self) -> str: return self._fetch("messageId")
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def type(self) -> int: return self._fetch("type")
    @property
    def isHidden(self) -> bool: return self._fetch("isHidden")
    @property
    def includedInSummary(self) -> bool: return self._fetch("includedInSummary")
    @property
    def chatBubbleId(self) -> str: return self._fetch("chatBubbleId")
    @property
    def chatBubbleVersion(self) -> int: return self._fetch("chatBubbleVersion")
    @property
    def extensions(self) -> messageExtensions: return messageExtensions(self._fetch("extensions"))
    @property
    def json(self) -> dict: return self._json


class chatExtensions:
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        try: return [i[key] for i in self._json] if self._list else self._json[key]
        except (KeyError, TypeError): return Objects().fetch_key(self._json, key, self._list)

    @property
    def viewOnly(self) -> bool: return self._fetch("viewOnly")
    @property
    def coHost(self) -> list: return self._fetch("coHost")
    @property
    def language(self) -> str: return self._fetch("language")
    @property
    def membersCanInvite(self) -> bool: return self._fetch("membersCanInvite")
    @property
    def screeningRoomPermission(self) -> dict: return self._fetch("screeningRoomPermission")
    @property
    def chatBackground(self) -> int: return self._fetch("bm")
    @property
    def avchatMemberUidList(self) -> list: return self._fetch("avchatMemberUidList")
    @property
    def screeningRoomUidList(self) -> list: return self._fetch("screeningRoomUidList")
    @property
    def creatorUid(self) -> str: return self._fetch("creatorUid")
    @property
    def visibility(self) -> int: return self._fetch("visibility")
    @property
    def bannedMemberUidList(self) -> list: return self._fetch("bannedMemberUidList")
    @property
    def lastMembersSummaryUpdateTime(self) -> str: return self._fetch("lastMembersSummaryUpdateTime")
    @property
    def fansOnly(self) -> bool: return self._fetch("fansOnly")
    @property
    def announcement(self) -> str: return self._fetch("announcement")
    @property
    def channelTypeLastCreatedTime(self) -> str: return self._fetch("channelTypeLastCreatedTime")
    @property
    def avchatId(self) -> str: return self._fetch("avchatId")
    @property
    def channelType(self) -> int: return self._fetch("channelType")
    @property
    def pinAnnouncement(self) -> str: return self._fetch("pinAnnouncement")
    @property
    def vvChatJoinType(self) -> int: return self._fetch("vvChatJoinType")
    @property
    def isDisabled(self) -> str: return self._fetch("__disabledTime__")

    @property
    def json(self) -> dict: return self._json


class ChatThread:
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        try: return [i[key] for i in self._json["threadList"]] if self._list else self._json[key]["thread"]
        except (KeyError, TypeError): return Objects().fetch_key(self._json, key, self._list)

    @property
    def userAddedTopicList(self) -> list: return self._fetch("userAddedTopicList")
    @property
    def membersQuota(self) -> int: return self._fetch("membersQuota")
    @property
    def chatId(self) -> str: return self._fetch("threadId")
    @property
    def keywords(self) -> str: return self._fetch("keywords")
    @property
    def membersCount(self) -> int: return self._fetch("membersCount")
    @property
    def strategyInfo(self) -> dict: return self._fetch("strategyInfo")
    @property
    def isPinned(self) -> bool: return self._fetch("isPinned")
    @property
    def title(self) -> str: return self._fetch("title")
    @property
    def tipInfo(self) -> dict: return self._fetch("tipInfo")
    @property
    def membershipStatus(self) -> int: return self._fetch("membershipStatus")
    @property
    def description(self) -> str: return self._fetch("content")
    @property
    def needHidden(self) -> bool: return self._fetch("needHidden")
    @property
    def alertOption(self) -> int: return self._fetch("alertOption")
    @property
    def lastReadTime(self) -> str: return self._fetch("lastReadTime")
    @property
    def type(self) -> int: return self._fetch("type")
    @property
    def status(self) -> int: return self._fetch("status")
    @property
    def publishToGlobal(self) -> bool: return self._fetch("publishToGlobal")
    @property
    def modifiedTime(self) -> str: return self._fetch("modifiedTime")
    @property
    def condition(self) -> int: return self._fetch("condition")
    @property
    def icon(self) -> str: return self._fetch("icon")
    @property
    def latestActivityTime(self) -> str: return self._fetch("latestActivityTime")
    @property
    def author(self) -> User: return User(self._fetch("author"), self._list)
    @property
    def extensions(self) -> chatExtensions: return chatExtensions(self._fetch("extensions"), self._list)
    @property
    def lastMessageSummary(self) -> Message: return Message(self._fetch("lastMessageSummary"), self._list)
        
    @property
    def json(self) -> dict: return self._json


class Notification:
    """
    Contains notification properties such as object id, type, and more.
    """
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        try: return [i[key] for i in self._json["notificationList"]] if self._list else self._json["notification"][key]
        except (KeyError, TypeError): return Objects().fetch_key(self._json, key, self._list)

    @property
    def parentText(self) -> str: return self._fetch("parentText")
    @property
    def objectId(self) -> str: return self._fetch("objectId")
    @property
    def contextText(self) -> str: return self._fetch("contextText")
    @property
    def type(self) -> int: return self._fetch("type")
    @property
    def parentId(self) -> str: return self._fetch("parentId")
    @property
    def operator(self) -> User: return User(self._fetch("operator"), self._list)
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def parentType(self) -> int: return self._fetch("parentType")
    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def notificationId(self) -> str: return self._fetch("notificationId")
    @property
    def objectText(self) -> str: return self._fetch("objectText")
    @property
    def contextValue(self) -> str: return self._fetch("contextValue")
    @property
    def contextComId(self) -> int: return self._fetch("contextNdcId")
    @property
    def objectType(self) -> int: return self._fetch("objectType")
    @property
    def json(self) -> dict: return self._json

class themePack:
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList
        
    @property
    def themeColor(self) -> str: return self._json["themeColor"]
    @property
    def themePackHash(self) -> str: return self._json["themePackHash"]
    @property
    def themePackRevision(self) -> int: return self._json["themePackRevision"]
    @property
    def themePackUrl(self) -> str: return self._json["themePackUrl"]
    @property
    def json(self) -> dict: return self._json

class SCommunity:
    def __init__(self, data: dict, isList: bool = False) -> None:
        self._json = data
        self._list = isList

    def _fetch(self, key) -> Union[str, List]:
        try: return [i["community"][key] for i in self._json["communityList"]] if self._list else self._json[key]["community"]
        except (KeyError, TypeError): return Objects().fetch_key(self._json, key, self._list)
        
    @property
    def isCurrentUserJoined(self) -> bool: return self._json["isCurrentUserJoined"]
    @property
    def currentUserInfo(self) -> User: return User(self._json("currentUserInfo"), self._list)
    @property
    def isStandaloneAppMonetizationEnabled(self) -> bool: return self._json["community"]["isStandaloneAppMonetizationEnabled"] if not self._list else self._fetch("isStandaloneAppMonetizationEnabled")
    @property
    def keywords(self) -> List: return self._json["community"]["keywords"] if not self._list else self._fetch("keywords")
    @property
    def isStandaloneAppDeprecated(self) -> bool: return self._json["community"]["isStandaloneAppDeprecated"] if not self._list else self._fetch("isStandaloneAppDeprecated")
    @property
    def activeInfo(self) -> dict: return self._json["community"]["activeInfo"] if not self._list else self._fetch("activeInfo")
    @property
    def promotionalMediaList(self) -> List: return self._json["community"]["promotionalMediaList"] if not self._list else self._fetch("promotionalMediaList")
    @property
    def themePack(self) -> themePack: return themePack(self._json["community"]["themePack"]) if not self._list else themePack(self._fetch("themePack"))
    @property
    def status(self) -> int: return self._json["community"]["status"] if not self._list else self._fetch("status")
    @property
    def probationStatus(self) -> int: return self._json["community"]["probationStatus"] if not self._list else self._fetch("probationStatus")
    @property
    def updatedTime(self) -> str: return self._json["community"]["updatedTime"] if not self._list else self._fetch("updatedTime")
    @property
    def primaryLanguage(self) -> str: return self._json["community"]["primaryLanguage"] if not self._list else self._fetch("primaryLanguage")
    @property
    def modifiedTime(self) -> str: return self._json["community"]["modifiedTime"] if not self._list else self._fetch("modifiedTime")
    @property
    def membersCount(self) -> int: return self._json["community"]["membersCount"] if not self._list else self._fetch("membersCount")
    @property
    def tagline(self) -> str: return self._json["community"]["tagline"] if not self._list else self._fetch("tagline")
    @property
    def name(self) -> str: return self._json["community"]["name"] if not self._list else self._fetch("name")
    @property
    def endpoint(self) -> str: return self._json["community"]["endpoint"] if not self._list else self._fetch("endpoint")
    @property
    def communityHeadList(self) -> List: return self._json["community"]["communityHeadList"] if not self._list else self._fetch("communityHeadList")
    @property
    def listedStatus(self) -> int: return self._json["community"]["listedStatus"] if not self._list else self._fetch("listedStatus")
    @property
    def extensions(self) -> List: return self._json["community"]["extensions"] if not self._list else self._fetch("extensions")
    @property
    def mediaList(self) -> List: return self._json["community"]["mediaList"] if not self._list else self._fetch("mediaList")
    @property
    def userAddedTopicList(self) -> List: return self._json["community"]["userAddedTopicList"] if not self._list else self._fetch("userAddedTopicList")
    @property
    def communityHeat(self) -> int: return self._json["community"]["communityHeat"] if not self._list else self._fetch("communityHeat")
    @property
    def templateId(self) -> int: return self._json["community"]["templateId"] if not self._list else self._fetch("templateId")
    @property
    def searchable(self) -> bool: return self._json["community"]["searchable"] if not self._list else self._fetch("searchable")
    @property
    def createdTime(self) -> str: return self._json["community"]["createdTime"] if not self._list else self._fetch("createdTime")
    @property
    def json(self) -> dict: return self._json["community"]
    
class CheckInHistory:
    def __init__(self, data: dict) -> None:
        self._json = data

    def _fetch(self, key) -> Union[str, List]:
        try: return self._json[key]
        except KeyError: return Objects().fetch_key(self._json, key)

    @property
    def joinedTime(self) -> int: return self._fetch("joinedTime")
    @property
    def stopTime(self) -> int: return self._fetch("stopTime")
    @property
    def consecutiveCheckInDays(self) -> int: return self._fetch("consecutiveCheckInDays")
    @property
    def streakRepairCoinCost(self) -> int: return self._fetch("streakRepairCoinCost")
    @property
    def startTime(self) -> int: return self._fetch("startTime")
    @property
    def hasCheckInToday(self) -> bool: return self._fetch("hasCheckInToday")
    @property
    def streakRepairWindowSize(self) -> int: return self._fetch("streakRepairWindowSize")
    @property
    def hasAnyCheckIn(self) -> bool: return self._fetch("hasAnyCheckIn")
    @property
    def history(self) -> str: return self._fetch("history")
    @property
    def json(self) -> dict: return self._json

class CheckIn:
    def __init__(self, data: dict) -> None:
        self._json = data
    
    def _fetch(self, key) -> str:
        try: return self._json[key]
        except KeyError: return Objects().fetch_key(self._json, key)

    @property
    def consecutiveCheckInDays(self) -> int: return self._fetch("consecutiveCheckInDays")
    @property
    def canPlayLottery(self) -> bool: return self._fetch("canPlayLottery")
    @property
    def earnedReputationPoint(self) -> int: return self._fetch("earnedReputationPoint")
    @property
    def additionalReputationPoint(self) -> int: return self._fetch("additionalReputationPoint")
    @property
    def checkInHistory(self) -> CheckInHistory: return CheckInHistory(self._fetch("checkInHistory"))
    @property
    def profile(self) -> User: return User(self._fetch("userProfile"))
    @property
    def json(self) -> dict: return self._json

class Wallet:
    def __init__(self, data: dict):
        self._json = data
        
    @property
    def totalCoinsFloat(self) -> float: return self._json["totalCoinsFloat"]
    @property
    def adsEnabled(self) -> bool: return self._json["adsEnabled"]
    @property
    def adsVideoStats(self) -> dict: return self._json["adsVideoStats"]
    @property
    def adsFlags(self) -> int: return self._json["adsFlags"]
    @property
    def totalCoins(self) -> int: return self._json["totalCoins"]
    @property
    def businessCoinsEnabled(self) -> bool: return self._json["businessCoinsEnabled"]
    @property
    def totalBusinessCoins(self) -> int: return self._json["totalBusinessCoins"]
    @property
    def totalBusinessCoinsFloat(self) -> float: return self._json["totalBusinessCoinsFloat"]
    @property
    def json(self) -> dict: return self._json

class Coupon:
    def __init__(self, data: dict):
        self._json = data
    @property
    def expiredTime(self) -> str: return self._json["expiredTime"]
    @property
    def couponId(self) -> str: return self._json["couponId"]
    @property
    def scopeDesc(self) -> str: return self._json["scopeDesc"]
    @property
    def status(self) -> int: return self._json["status"]
    @property
    def modifiedTime(self) -> str: return self._json["modifiedTime"]
    @property
    def couponValue(self) -> int: return self._json["couponValue"]
    @property
    def expiredType(self) -> int: return self._json["expiredType"]
    @property
    def title(self) -> str: return self._json["title"]
    @property
    def couponType(self) -> int: return self._json["couponType"]
    @property
    def createdTime(self) -> str: return self._json["createdTime"]
    @property
    def json(self) -> dict: return self._json



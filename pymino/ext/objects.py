class Objects:
    def __init__(self): pass

    def fetch_key(self, data, key, List: bool=False):
        if isinstance(data, dict):
            if key in data:
                if List: return [data[key]]
                else: return data[key]
            else:
                if List: res = []
                else: res = None
                for k, v in data.items():
                    if isinstance(v, (dict, list)):
                        if List: res += self.fetch_key(v, key, List)
                        else: res = self.fetch_key(v, key, List)
                        if res and not List: return res
                return res

        elif isinstance(data, list):
            if List: res = []
            else: res = None
            for item in data:
                if isinstance(item, (dict, list)):
                    if List: res += self.fetch_key(item, key, List)
                    else: res = self.fetch_key(item, key, List)
                    if res and not List: return res
            return res
        else: return None

class User:
    def __init__(self, data: dict, List: bool=False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["userProfileList"]] if self.__List__ else self.__data__["userProfile"][key]
        except (KeyError, TypeError):
            return Objects().fetch_key(self.__data__, key, self.__List__)

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
    def hideUserProfile(self) -> bool: return self._fetch("hideUserProfile")
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
    def json(self) -> dict: return self.__data__

class Authenticate:
    def __init__(self, data: dict):
        self.__data__ = data

    def _fetch(self, key: str) -> any:
        try:
            return self.__data__.get(key)
        except:
            Objects().fetch_key(self.__data__, key)

    @property
    def sid(self) -> str: return self._fetch("sid")
    @property
    def userId(self) -> str: return self._fetch("auid")
    @property
    def user_info(self) -> User: return User(self._fetch("userProfile"))
    @property
    def secret(self) -> str: return self._fetch("secret")
    @property
    def json(self) -> dict: return self.__data__


class linkInfoV2:
    def __init__(self, data: dict):
        self.__data__ = data
    
    @property
    def fullPath(self) -> str: return (Objects().fetch_key(self.__data__, "fullPath", False))
    @property
    def comId(self) -> int: return (Objects().fetch_key(self.__data__, "ndcId", False))
    @property
    def objectId(self) -> str: return (Objects().fetch_key(self.__data__, "objectId", False))
    @property
    def objectType(self) -> int: return (Objects().fetch_key(self.__data__, "objectType", False))
    @property
    def shortCode(self) -> str: return (Objects().fetch_key(self.__data__, "shortCode", False))
    @property
    def targetCode(self) -> int: return (Objects().fetch_key(self.__data__, "targetCode", False))
    @property
    def path(self) -> str: return (Objects().fetch_key(self.__data__, "path", False))
    @property
    def json(self) -> dict: return self.__data__

class SResponse:
    def __init__(self, data: dict):
        self.__data__ = data

    @property
    def statuscode(self) -> int: return self.__data__["api:statuscode"]
    @property
    def duration(self) -> str: return self.__data__["api:duration"]
    @property
    def message(self) -> str: return self.__data__["api:message"]
    @property
    def timestamp(self) -> str: return self.__data__["api:timestamp"]
    @property
    def devOptions(self) -> dict: return self.__data__["devOptions"]
    @property
    def mediaValue(self) -> str: return self.__data__["mediaValue"]
    @property
    def json(self) -> dict: return self.__data__

class ResetPassword:
    def __init__(self, data: dict):
        self.__data__ = data

    @property
    def response(self) -> SResponse: return SResponse(self.__data__)
    @property
    def secret(self): return self.__data__["secret"]
    @property
    def json(self): return self.__data__

class Comment:
    def __init__(self, data: dict, List: bool=False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["commentList"]] if self.__List__ else self.__data__["comment"][key]
        except (KeyError, TypeError):
            Objects().fetch_key(self.__data__, key, self.__List__)

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
    def user(self) -> User:
        return User([i["author"] for i in self.__data__["commentList"]], True) if self.__List__ else User(self.__data__["comment"]["author"])
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
    def json(self) -> dict: return self.__data__

class Blog:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["blogList"]] if self.__List__ else self.__data__["blog"][key]
        except (KeyError, TypeError):
            Objects().fetch_key(self.__data__, key, self.__List__)
        
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
    def user(self) -> User:
        return User([author["author"] for author in self.__data__], List=True)
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
    def json(self) -> dict: return self.__data__
        
class Wiki:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["itemList"]] if self.__List__ else self.__data__["item"][key]
        except KeyError:
            Objects().fetch_key(self.__data__, key, self.__List__)
      
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
    def user(self) -> User:
        return User([author["author"] for author in self.__data__], List=True)
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
    def json(self) -> dict: return self.__data__

class chatMembers:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data["memberList"]
        self.__List__ = List

    @property
    def chatMembers(self) -> User:
        return User([user for user in self.__data__], List=True)
    @property
    def json(self) -> dict: return self.__data__

class Message:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List
        self.message = ["message"]

        try:
            if self.__data__["o"]:
                self.__data__ = self.__data__["o"]
                self.message = ["chatMessage"]
        except KeyError: pass

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["messageList"]] if self.__List__ else self.__data__[self.message][key]
        except (KeyError, TypeError):
            return Objects().fetch_key(self.__data__, key, self.__List__)

    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def userId(self) -> str: return self._fetch("uid")
    @property 
    def author(self) -> User: return User(self.__data__, List=self.__List__)
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
    def extensions(self) -> dict: return self._fetch("extensions")
    @property
    def json(self) -> dict: return self.__data__

class chatExtensions:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__] if self.__List__ else self.__data__[key]
        except (KeyError, TypeError):
            return Objects().fetch_key(self.__data__, key, self.__List__)

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
    def json(self) -> dict: return self.__data__


class ChatThread:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["threadList"]] if self.__List__ else self.__data__[key]["thread"]
        except (KeyError, TypeError):
            return Objects().fetch_key(self.__data__, key, self.__List__)

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
    def chatTitle(self) -> str: return self._fetch("title")
    @property
    def tipInfo(self) -> dict: return self._fetch("tipInfo")
    @property
    def membershipStatus(self) -> int: return self._fetch("membershipStatus")
    @property
    def chatDescription(self) -> str: return self._fetch("content")
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
    def author(self) -> User: return User(self._fetch("author"), self.__List__)
    @property
    def extensions(self) -> chatExtensions: return chatExtensions(self._fetch("extensions"), self.__List__)
    @property
    def lastMessageSummary(self) -> Message: return Message(self._fetch("lastMessageSummary"), self.__List__)
        
    @property
    def json(self) -> dict: return self.__data__


class Notification:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["notificationList"]] if self.__List__ else self.__data__["notification"][key]
        except (KeyError, TypeError):
            return Objects().fetch_key(self.__data__, key, self.__List__)

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
    def operator(self) -> User: return User(self._fetch("operator"), self.__List__)
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
    def json(self) -> dict: return self.__data__

class themePack:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List
        
    @property
    def themeColor(self) -> str: return self.__data__["themeColor"]
    @property
    def themePackHash(self) -> str: return self.__data__["themePackHash"]
    @property
    def themePackRevision(self) -> int: return self.__data__["themePackRevision"]
    @property
    def themePackUrl(self) -> str: return self.__data__["themePackUrl"]
    @property
    def json(self) -> dict: return self.__data__

class Community:
    def __init__(self, data: dict, List: bool = False):
        self.__data__ = data
        self.__List__ = List

    def _fetch(self, key):
        try:
            return [i[key] for i in self.__data__["communityList"]] if self.__List__ else self.__data__[key]["community"]
        except (KeyError, TypeError):
            return Objects().fetch_key(self.__data__, key, self.__List__)

    @property
    def userAddedTopicList(self) -> list: return self._fetch("userAddedTopicList")
    @property
    def agent(self) -> User: return User(self._fetch("agent"), self.__List__)
    @property
    def listedStatus(self) -> int: return self._fetch("listedStatus")
    @property
    def probationStatus(self) -> int: return self._fetch("probationStatus")
    @property
    def themePack(self) -> themePack: return themePack(self._fetch("themePack"), self.__List__)
    @property
    def membersCount(self) -> int: return self._fetch("membersCount")
    @property
    def primaryLanguage(self) -> str: return self._fetch("primaryLanguage")
    @property
    def communityHeat(self) -> int: return self._fetch("communityHeat")
    @property
    def strategyInfo(self) -> dict: return self._fetch("strategyInfo")
    @property
    def tagline(self) -> str: return self._fetch("tagline")
    @property
    def joinType(self) -> int: return self._fetch("joinType")
    @property
    def status(self) -> int: return self._fetch("status")
    @property
    def launchPage(self) -> int: return self._fetch("launchPage")
    @property
    def modifiedTime(self) -> str: return self._fetch("modifiedTime")
    @property
    def comId(self) -> int: return self._fetch("ndcId")
    @property
    def activeInfo(self) -> dict: return self._fetch("activeInfo")
    @property
    def link(self) -> str: return self._fetch("link")
    @property
    def icon(self) -> str: return self._fetch("icon")
    @property
    def updatedTime(self) -> str: return self._fetch("updatedTime")
    @property
    def endpoint(self) -> str: return self._fetch("endpoint")
    @property
    def name(self) -> str: return self._fetch("name")
    @property
    def templateId(self) -> int: return self._fetch("templateId")
    @property
    def createdTime(self) -> str: return self._fetch("createdTime")
    @property
    def promotionalMediaList(self) -> list: return self._fetch("promotionalMediaList")
    @property
    def json(self) -> dict: return self.__data__

class CheckInHistory:
    def __init__(self, data: dict):
        self.__data__ = data

    def _fetch(self, key):
        try:
            return self.__data__[key]
        except KeyError:
            return Objects().fetch_key(self.__data__, key)

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
    def json(self) -> dict: return self.__data__

class CheckIn:
    def __init__(self, data: dict):
        self.__data__ = data
    
    def _fetch(self, key):
        try:
            return self.__data__[key]
        except KeyError:
            return Objects().fetch_key(self.__data__, key)

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
    def userProfile(self) -> User: return User(self._fetch("userProfile"))
    @property
    def json(self) -> dict: return self.__data__

class Wallet:
    def __init__(self, data: dict):
        self.__data__ = data
        
    @property
    def totalCoinsFloat(self) -> float: return self.__data__["totalCoinsFloat"]
    @property
    def adsEnabled(self) -> bool: return self.__data__["adsEnabled"]
    @property
    def adsVideoStats(self) -> dict: return self.__data__["adsVideoStats"]
    @property
    def adsFlags(self) -> int: return self.__data__["adsFlags"]
    @property
    def totalCoins(self) -> int: return self.__data__["totalCoins"]
    @property
    def businessCoinsEnabled(self) -> bool: return self.__data__["businessCoinsEnabled"]
    @property
    def totalBusinessCoins(self) -> int: return self.__data__["totalBusinessCoins"]
    @property
    def totalBusinessCoinsFloat(self) -> float: return self.__data__["totalBusinessCoinsFloat"]
    @property
    def json(self) -> dict: return self.__data__

class Coupon:
    def __init__(self, data: dict):
        self.__data__ = data
    @property
    def expiredTime(self) -> str: return self.__data__["expiredTime"]
    @property
    def couponId(self) -> str: return self.__data__["couponId"]
    @property
    def scopeDesc(self) -> str: return self.__data__["scopeDesc"]
    @property
    def status(self) -> int: return self.__data__["status"]
    @property
    def modifiedTime(self) -> str: return self.__data__["modifiedTime"]
    @property
    def couponValue(self) -> int: return self.__data__["couponValue"]
    @property
    def expiredType(self) -> int: return self.__data__["expiredType"]
    @property
    def title(self) -> str: return self.__data__["title"]
    @property
    def couponType(self) -> int: return self.__data__["couponType"]
    @property
    def createdTime(self) -> str: return self.__data__["createdTime"]
    @property
    def json(self) -> dict: return self.__data__

class EventTypes:
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

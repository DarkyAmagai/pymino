import re
from collections.abc import Iterator
from typing import Any, Literal, Optional, cast

from pymino.ext.entities import api_response, userprofile

__all__ = (
    'Authenticate',
    'CBlog',
    'CBlogList',
    'CChatMembers',
    'CCommunity',
    'CCommunityList',
    'CWiki',
    'CWikiList',
    'CheckIn',
    'CommunityInvitation',
    'Coupon',
    'FeaturedBlog',
    'FeaturedBlogs',
    'FetchNotification',
    'GlobalNotificationList',
    'InvitationId',
    'Notification',
    'NotificationList',
    'QuizRanking',
    'QuizRankingList',
    'ResetPassword',
    'Themepack',
    'Wallet',
)


class CommunityInvitation:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data
        self.communityInvitation: dict[str, Any] = self.data.get("communityInvitation", data)

    def __bool__(self) -> bool:
        return bool(self.invitationId)

    @property
    def status(self) -> int:
        return self.communityInvitation.get("status", 0)

    @property
    def duration(self) -> Optional[str]:
        return self.communityInvitation.get("duration")

    @property
    def invitationId(self) -> str:
        return self.communityInvitation.get("invitationId", '')

    @property
    def link(self) -> str:
        return self.communityInvitation.get("link", '')

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.communityInvitation.get("modifiedTime")

    @property
    def ndcId(self) -> int:
        return self.communityInvitation.get("ndcId", 0)

    @property
    def createdTime(self) -> str:
        return self.communityInvitation.get("createdTime", '')

    @property
    def inviteCode(self) -> str:
        return self.communityInvitation.get("inviteCode", '')

    def json(self) -> dict[str, Any]:
        return self.data


class CheckIn:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.data)

    @property
    def checkInHistory(self) -> dict[str, Any]:
        return self.data.get("checkInHistory") or {}

    @property
    def consecutiveCheckInDays(self) -> int:
        return self.checkInHistory.get("consecutiveCheckInDays") or 0

    @property
    def hasCheckInToday(self) -> bool:
        return self.checkInHistory.get("hasCheckInToday", False)

    @property
    def hasAnyCheckIn(self) -> bool:
        return self.checkInHistory.get("hasAnyCheckIn", False)

    @property
    def history(self) -> dict[str, Any]:
        return self.checkInHistory.get("history") or {}

    @property
    def userProfile(self) -> dict[str, Any]:
        return self.data.get("userProfile") or {}

    def json(self) -> dict[str, Any]:
        return self.data


class InvitationId:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def status(self) -> int:
        return self.data.get("status", 0)

    @property
    def duration(self) -> Optional[str]:
        return self.data.get("duration")

    @property
    def invitationId(self) -> str:
        return self.data.get("invitationId", '')

    @property
    def link(self) -> str:
        return self.data.get("link", '')

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.data.get("modifiedTime")

    @property
    def ndcId(self) -> int:
        return self.data.get("ndcId") or 0

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", '')

    @property
    def inviteCode(self) -> str:
        return self.data.get("inviteCode", '')

    def json(self) -> dict[str, Any]:
        return self.data


class CCommunity:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("community", data)

    @property
    def keywords(self) -> str:
        return self.data.get("keywords") or ''

    @property
    def activeInfo(self) -> dict[str, Any]:
        return self.data.get("activeInfo") or {}

    @property
    def themePack(self) -> dict[str, Any]:
        return self.data.get("themePack") or {}

    @property
    def status(self) -> int:
        return self.data.get("status", 0)

    @property
    def probationStatus(self) -> int:
        return self.data.get("probationStatus", 0)

    @property
    def updatedTime(self) -> Optional[str]:
        return self.data.get("updatedTime")

    @property
    def primaryLanguage(self) -> str:
        return self.data.get("primaryLanguage", "en")

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.data.get("modifiedTime")

    @property
    def membersCount(self) -> int:
        return self.data.get("membersCount", 0)

    @property
    def tagline(self) -> str:
        return self.data.get("tagline", "")

    @property
    def name(self) -> str:
        return self.data.get("name", "")

    @property
    def endpoint(self) -> str:
        return self.data.get("endpoint", "")

    @property
    def communityHeadList(self) -> list[dict[str, Any]]:
        return self.data.get("communityHeadList") or []

    @property
    def listedStatus(self) -> int:
        return self.data.get("listedStatus", 0)

    @property
    def extensions(self) -> dict[str, Any]:
        return self.data.get("extensions") or {}

    @property
    def mediaList(self) -> list[tuple[int, str, Optional[str], Optional[str]]]:
        return [(
            m[0],
            m[1],
            m[2] if len(m) > 2 else None,
            m[3] if len(m) > 3 else None
        ) for m in cast(list[Any], self.data.get("mediaList") or [])]

    @property
    def userAddedTopicList(self) -> list[dict[str, Any]]:
        return self.data.get("userAddedTopicList") or []

    @property
    def communityHeat(self) -> float:
        return self.data.get("communityHeat") or 0.0

    @property
    def templateId(self) -> int:
        return self.data.get("templateId", 0)

    @property
    def searchable(self) -> bool:
        return self.data.get("searchable", False)

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", '')

    @property
    def joinType(self) -> Literal[1, 2, 3]:
        return self.data.get("joinType") or 1

    @property
    def invitation(self) -> InvitationId:
        return InvitationId(self.data.get("invitation") or {})

    @property
    def ndcId(self) -> int:
        return self.data.get("ndcId") or int(re.findall(r"\d+", self.data.get("linkInfoV2", {}).get("path"))[0]) 

    @property
    def comId(self) -> int:
        return self.ndcId

    @property
    def icon(self) -> str:
        return self.data.get("icon", "")

    def json(self) -> dict[str, Any]:
        return self.data


class CCommunityList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = data.get("communityList") or []

    def __iter__(self) -> Iterator[CCommunity]:
        return (CCommunity(data) for data in self.data)

    @property
    def keywords(self) -> list[str]:
        return [x.keywords for x in self]

    @property
    def activeInfo(self) -> list[dict[str, Any]]:
        return [x.activeInfo for x in self]

    @property
    def themePack(self) -> list[dict[str, Any]]:
        return [x.themePack for x in self]

    @property
    def status(self) -> list[int]:
        return [x.status for x in self]

    @property
    def probationStatus(self) -> list[int]:
        return [x.probationStatus for x in self]

    @property
    def updatedTime(self) -> list[Optional[str]]:
        return [x.updatedTime for x in self]

    @property
    def primaryLanguage(self) -> list[str]:
        return [x.primaryLanguage for x in self]

    @property
    def modifiedTime(self) -> list[Optional[str]]:
        return [x.modifiedTime for x in self]

    @property
    def membersCount(self) -> list[int]:
        return [x.membersCount for x in self]

    @property
    def tagline(self) -> list[str]:
        return [x.tagline for x in self]

    @property
    def name(self) -> list[str]:
        return [x.name for x in self]

    @property
    def endpoint(self) -> list[str]:
        return [x.endpoint for x in self]

    @property
    def communityHeadList(self) -> list[list[dict[str, Any]]]:
        return [x.communityHeadList for x in self]

    @property
    def listedStatus(self) -> list[int]:
        return [x.listedStatus for x in self]

    @property
    def extensions(self) -> list[dict[str, Any]]:
        return [x.extensions for x in self]

    @property
    def mediaList(self) -> list[list[tuple[int, str, Optional[str], Optional[str]]]]:
        return [x.mediaList for x in self]

    @property
    def userAddedTopicList(self) -> list[list[dict[str, Any]]]:
        return [x.userAddedTopicList for x in self]

    @property
    def communityHeat(self) -> list[float]:
        return [x.communityHeat for x in self]

    @property
    def templateId(self) -> list[int]:
        return [x.templateId for x in self]

    @property
    def searchable(self) -> list[bool]:
        return [x.searchable for x in self]

    @property
    def createdTime(self) -> list[str]:
        return [x.createdTime for x in self]

    @property
    def ndcId(self) -> list[int]:
        return [x.ndcId for x in self]

    @property
    def comId(self) -> list[int]:
        return [x.comId for x in self]

    @property
    def icon(self) -> list[str]:
        return [x.icon for x in self]

    @property
    def joinType(self) -> list[Literal[1, 2, 3]]:
        return [x.joinType for x in self]

    def json(self) -> list[dict[str, Any]]:
        return self.data


class CBlog:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("blog", data)

    @property
    def globalVotesCount(self) -> int:
        return self.data.get("globalVotesCount") or 0

    @property
    def globalVotedValue(self) -> int:
        return self.data.get("globalVotedValue") or 0

    @property
    def votedValue(self) -> int:
        return self.data.get("votedValue") or 0

    @property
    def keywords(self) -> str:
        return self.data.get("keywords", "")

    @property
    def mediaList(self) -> list[tuple[int, str, Optional[str], Optional[str]]]:
        return [(
            m[0],
            m[1],
            m[2] if len(m) > 2 else None,
            m[3] if len(m) > 3 else None
        ) for m in cast(list[Any], self.data.get("mediaList") or [])]

    @property
    def style(self) -> dict[str, Any]:
        return self.data.get("style") or {}

    @property
    def totalQuizPlayCount(self) -> int:
        return self.data.get("totalQuizPlayCount", 0)

    @property
    def title(self) -> str:
        return self.data.get("title", "")

    @property
    def tipInfo(self) -> dict[str, Any]:
        return self.data.get("tipInfo") or {}

    @property
    def contentRating(self) -> int:
        return self.data.get("contentRating") or 0

    @property
    def content(self) -> Optional[str]:
        return self.data.get("content")

    @property
    def needHidden(self) -> bool:
        return self.data.get("needHidden", False)

    @property
    def guestVotesCount(self) -> int:
        return self.data.get("guestVotesCount") or 0

    @property
    def type(self) -> int:
        return self.data.get("type") or 0

    @property
    def status(self) -> int:
        return self.data.get("status", 0)

    @property
    def globalCommentsCount(self) -> int:
        return self.data.get("globalCommentsCount") or 0

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.data.get("modifiedTime")

    @property
    def widgetDisplayInterval(self) -> Optional[str]:
        return self.data.get("widgetDisplayInterval")

    @property
    def totalPollVoteCount(self) -> int:
        return self.data.get("totalPollVoteCount") or 0

    @property
    def blogId(self) -> str:
        return self.data.get("blogId", "")

    @property
    def viewCount(self) -> int:
        return self.data.get("viewCount") or 0

    @property
    def language(self) -> str:
        return self.data.get("language", "en")

    @property
    def author(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.data.get("author") or {})

    @property
    def extensions(self) -> dict[str, Any]:
        return self.data.get("extensions") or {}

    @property
    def votesCount(self) -> int:
        return self.data.get("votesCount") or 0

    @property
    def ndcId(self) -> int:
        return self.data.get("ndcId") or 0

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", "")

    @property
    def endTime(self) -> Optional[str]:
        return self.data.get("endTime")

    @property
    def commentsCount(self) -> int:
        return self.data.get("commentsCount") or 0

    def json(self) -> dict[str, Any]:
        return self.data


class CWiki:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("item", data)

    @property
    def globalVotesCount(self) -> int:
        return self.data.get("globalVotesCount") or 0

    @property
    def globalVotedValue(self) -> int:
        return self.data.get("globalVotedValue") or 0

    @property
    def votedValue(self) -> int:
        return self.data.get("votedValue") or 0

    @property
    def keywords(self) -> str:
        return self.data.get("keywords", "")

    @property
    def mediaList(self) -> list[tuple[int, str, Optional[str], Optional[str]]]:
        return [(
            m[0],
            m[1],
            m[2] if len(m) > 2 else None,
            m[3] if len(m) > 3 else None
        ) for m in cast(list[Any], self.data.get("mediaList") or [])]

    @property
    def style(self) -> dict[str, Any]:
        return self.data.get("style") or {}

    @property
    def totalQuizPlayCount(self) -> int:
        return self.data.get("totalQuizPlayCount", 0)

    @property
    def title(self) -> str:
        return self.data.get("title", "")

    @property
    def tipInfo(self) -> dict[str, Any]:
        return self.data.get("tipInfo") or {}

    @property
    def contentRating(self) -> int:
        return self.data.get("contentRating") or 0

    @property
    def content(self) -> Optional[str]:
        return self.data.get("content")

    @property
    def needHidden(self) -> bool:
        return self.data.get("needHidden", False)

    @property
    def guestVotesCount(self) -> int:
        return self.data.get("guestVotesCount") or 0

    @property
    def type(self) -> int:
        return self.data.get("type") or 0

    @property
    def status(self) -> int:
        return self.data.get("status", 0)

    @property
    def globalCommentsCount(self) -> int:
        return self.data.get("globalCommentsCount") or 0

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.data.get("modifiedTime")

    @property
    def widgetDisplayInterval(self) -> Optional[str]:
        return self.data.get("widgetDisplayInterval")

    @property
    def totalPollVoteCount(self) -> int:
        return self.data.get("totalPollVoteCount") or 0

    @property
    def wikiId(self) -> str:
        return self.data.get("itemId", "")

    @property
    def viewCount(self) -> int:
        return self.data.get("viewCount") or 0

    @property
    def language(self) -> str:
        return self.data.get("language", "en")

    @property
    def author(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.data.get("author") or {})

    @property
    def extensions(self) -> dict[str, Any]:
        return self.data.get("extensions") or {}

    @property
    def votesCount(self) -> int:
        return self.data.get("votesCount") or 0

    @property
    def ndcId(self) -> int:
        return self.data.get("ndcId") or 0

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", "")

    @property
    def endTime(self) -> Optional[str]:
        return self.data.get("endTime")

    @property
    def commentsCount(self) -> int:
        return self.data.get("commentsCount") or 0

    def json(self) -> dict[str, Any]:
        return self.data


class CWikiList:
    def __init__(self, data: dict[str, Any]):
        self.data: list[dict[str, Any]] = data.get("itemList") or []
        parser = [CWiki(x) for x in self.data]
        self.author = userprofile.UserProfileList([x.author.json() for x in parser])
        self.globalVotesCount = [x.globalVotesCount for x in parser]
        self.globalVotedValue = [x.globalVotedValue for x in parser]
        self.votedValue = [x.votedValue for x in parser]
        self.keywords = [x.keywords for x in parser]
        self.mediaList = [x.mediaList for x in parser]
        self.style = [x.style for x in parser]
        self.totalQuizPlayCount = [x.totalQuizPlayCount for x in parser]
        self.title = [x.title for x in parser]
        self.tipInfo = [x.tipInfo for x in parser]
        self.contentRating = [x.contentRating for x in parser]
        self.content = [x.content for x in parser]
        self.needHidden = [x.needHidden for x in parser]
        self.guestVotesCount = [x.guestVotesCount for x in parser]
        self.type = [x.type for x in parser]
        self.status = [x.status for x in parser]
        self.globalCommentsCount = [x.globalCommentsCount for x in parser]
        self.modifiedTime = [x.modifiedTime for x in parser]
        self.widgetDisplayInterval = [x.widgetDisplayInterval for x in parser]
        self.totalPollVoteCount = [x.totalPollVoteCount for x in parser]
        self.wikiId = [x.wikiId for x in parser]
        self.viewCount = [x.viewCount for x in parser]
        self.language = [x.language for x in parser]
        self.extensions = [x.extensions for x in parser]
        self.votesCount = [x.votesCount for x in parser]
        self.ndcId = [x.ndcId for x in parser]
        self.createdTime = [x.createdTime for x in parser]
        self.endTime = [x.endTime for x in parser]
        self.commentsCount = [x.commentsCount for x in parser]

    def json(self) -> list[dict[str, Any]]:
        return self.data


class CBlogList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]]= data.get("blogList") or []
        parser = [CBlog(x) for x in self.data]
        self.author = userprofile.UserProfileList([x.author.json() for x in parser])
        self.globalVotesCount = [x.globalVotesCount for x in parser]
        self.globalVotedValue = [x.globalVotedValue for x in parser]
        self.votedValue = [x.votedValue for x in parser]
        self.keywords = [x.keywords for x in parser]
        self.mediaList = [x.mediaList for x in parser]
        self.style = [x.style for x in parser]
        self.totalQuizPlayCount = [x.totalQuizPlayCount for x in parser]
        self.title = [x.title for x in parser]
        self.tipInfo = [x.tipInfo for x in parser]
        self.contentRating = [x.contentRating for x in parser]
        self.content = [x.content for x in parser]
        self.needHidden = [x.needHidden for x in parser]
        self.guestVotesCount = [x.guestVotesCount for x in parser]
        self.type = [x.type for x in parser]
        self.status = [x.status for x in parser]
        self.globalCommentsCount = [x.globalCommentsCount for x in parser]
        self.modifiedTime = [x.modifiedTime for x in parser]
        self.widgetDisplayInterval = [x.widgetDisplayInterval for x in parser]
        self.totalPollVoteCount = [x.totalPollVoteCount for x in parser]
        self.blogId = [x.blogId for x in parser]
        self.viewCount = [x.viewCount for x in parser]
        self.language = [x.language for x in parser]
        self.extensions = [x.extensions for x in parser]
        self.votesCount = [x.votesCount for x in parser]
        self.ndcId = [x.ndcId for x in parser]
        self.createdTime = [x.createdTime for x in parser]
        self.endTime = [x.endTime for x in parser]
        self.commentsCount = [x.commentsCount for x in parser]

    def json(self) -> list[dict[str, Any]]:
        return self.data


class Coupon:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("coupon", data)

    @property
    def expiredTime(self) -> Optional[str]:
        return self.data.get("expiredTime")

    @property
    def couponId(self) -> str:
        return self.data.get("couponId", "")

    @property
    def scopeDesc(self) -> Optional[str]:
        return self.data.get("scopeDesc")

    @property
    def status(self) -> int:
        return self.data.get("status", 0)

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.data.get("modifiedTime")

    @property
    def couponValue(self) -> int:
        return self.data.get("couponValue", 0)

    @property
    def expiredType(self) -> int:
        return self.data.get("expiredType", 0)

    @property
    def title(self) -> str:
        return self.data.get("title", "")

    @property
    def couponType(self) -> int:
        return self.data.get("couponType", 0)

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", "")

    def json(self) -> dict[str, Any]:
        return self.data


class Wallet:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("wallet", data)

    @property
    def totalCoinsFloat(self) -> float:
        return self.data.get("totalCoinsFloat") or 0.0

    @property
    def adsEnabled(self) -> bool:
        return self.data.get("adsEnabled", False)

    @property
    def adsVideoStats(self) -> dict[str, Any]:
        return self.data.get("adsVideoStats") or {}

    @property
    def adsFlags(self) -> int:
        return self.data.get("adsFlags", 0)

    @property
    def totalCoins(self) -> int:
        return self.data.get("totalCoins") or 0

    @property
    def businessCoinsEnabled(self) -> bool:
        return self.data.get("businessCoinsEnabled", False)

    @property
    def totalBusinessCoins(self) -> int:
        return self.data.get("totalBusinessCoins") or 0

    @property
    def totalBusinessCoinsFloat(self) -> float:
        return self.data.get("totalBusinessCoinsFloat") or 0.0

    def json(self) -> dict[str, Any]:
        return self.data


class Themepack:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def themeColor(self) -> str:
        return self.data.get("themeColor", "#ffffff")

    @property
    def themePackHash(self) -> str:
        return self.data.get("themePackHash", "")

    @property
    def themePackRevision(self) -> int:
        return self.data.get("themePackRevision", 0)

    @property
    def themePackUrl(self) -> str:
        return self.data.get("themePackUrl", "")

    def json(self) -> dict[str, Any]:
        return self.data


class Notification:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def parentText(self) -> Optional[str]:
        return self.data.get("parentText")

    @property
    def objectId(self) -> str:
        return self.data.get("objectId", "")

    @property
    def contextText(self) -> Optional[str]:
        return self.data.get("contextText")

    @property
    def type(self) -> int:
        return self.data.get("type", 0)

    @property
    def parentId(self) -> str:
        return self.data.get("parentId", "")

    @property
    def operator(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.data.get("operator") or {})

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", "")

    @property
    def parentType(self) -> int:
        return self.data.get("parentType", 0)

    @property
    def ndcId(self) -> int:
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        return self.ndcId

    @property
    def notificationId(self) -> str:
        return self.data.get("notificationId", "")

    @property
    def objectText(self) -> str:
        return self.data.get("objectText", "")

    @property
    def contextValue(self) -> Optional[str]:
        return self.data.get("contextValue")

    @property
    def contextComId(self) -> Optional[str]:
        return self.data.get("contextNdcId")

    @property
    def objectType(self) -> int:
        return self.data.get("objectType", 0)

    def json(self) -> dict[str, Any]:
        return self.data

class NotificationList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = data.get("notificationList") or []
        self.parser = [Notification(x) for x in self.data]
        self.parentText = [x.parentText for x in self.parser]
        self.objectId = [x.objectId for x in self.parser]
        self.contextText = [x.contextText for x in self.parser]
        self.type = [x.type for x in self.parser]
        self.parentId = [x.parentId for x in self.parser]
        self.operator = userprofile.UserProfileList([x.operator.json() for x in self.parser])
        self.createdTime = [x.createdTime for x in self.parser]
        self.parentType = [x.parentType for x in self.parser]
        self.comId = [x.comId for x in self.parser]
        self.notificationId = [x.notificationId for x in self.parser]
        self.objectText = [x.objectText for x in self.parser]
        self.contextValue = [x.contextValue for x in self.parser]
        self.contextComId = [x.contextComId for x in self.parser]
        self.objectType = [x.objectType for x in self.parser]

    def json(self) -> list[dict[str, Any]]:
        return self.data


class ResetPassword:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def response(self) -> api_response.ApiResponse:
        return api_response.ApiResponse(self.data or {})

    @property
    def secret(self) -> str:
        return self.data.get("secret", "")

    def json(self) -> dict[str, Any]:
        return self.data


class Authenticate:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data    = data

    @property
    def sid(self) -> str:
        return self.data.get("sid", "")

    @property
    def userId(self) -> str:
        return self.data.get("auid", "")

    @property
    def profile(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.data.get("userProfile") or {})

    @property
    def secret(self) -> Optional[str]:
        return self.data.get("secret")

    def json(self) -> dict[str, Any]:
        return self.data


class CChatMembers:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def members(self) -> userprofile.UserProfileList:
        return userprofile.UserProfileList(self.data.get("memberList") or [])

    def json(self) -> dict[str, Any]:
        return self.data


class FeaturedBlog:
    def __init__(self, data: dict[str, Any]):
        self.data = data

    @property
    def ref_object_type(self) -> int:
        return self.data.get("refObjectType", 0)

    @property
    def ref_object_id(self) -> str:
        return self.data.get("refObjectId", "")

    @property
    def expired_time(self) -> Optional[str]:
        return self.data.get('expiredTime')

    @property
    def featured_type(self) -> int:
        return self.data.get('featuredType', 0)

    @property
    def created_time(self) -> str:
        return self.data.get('createdTime', "")

    @property
    def ref_object(self) -> dict[str, Any]:
        return self.data.get('refObject') or {}

    @property
    def global_votes_count(self) -> int:
        return self.ref_object.get('globalVotesCount', 0)

    @property
    def global_voted_count(self) -> int:
        return self.ref_object.get('globalVotedCount', 0)

    @property
    def voted_value(self) -> int:
        return self.ref_object.get('votedValue', 0)

    @property
    def keywords(self) -> str:
        return self.ref_object.get('keywords') or ""

    @property
    def strategy_info(self) -> str:
        return self.ref_object.get('strategyInfo') or "{}"

    @property
    def media_list(self) -> list[tuple[int, str, Optional[str], Optional[str]]]:
        return [(
            m[0],
            m[1],
            m[2] if len(m) > 2 else None,
            m[3] if len(m) > 3 else None
        ) for m in cast(list[Any], self.ref_object.get('mediaList') or [])]

    @property
    def style(self) -> dict[str, Any]:
        return self.ref_object.get('style') or {}

    @property
    def total_quiz_play_count(self) -> int:
        return self.ref_object.get('totalQuizPlayCount') or 0

    @property
    def title(self) -> str:
        return self.ref_object.get('title', "")

    @property
    def tip_info(self) -> dict[str, Any]:
        return self.ref_object.get('tipInfo') or {}

    @property
    def content(self) -> Optional[str]:
        return self.ref_object.get('content')

    @property
    def content_rating(self) -> int:
        return self.ref_object.get('contentRating') or 0

    @property
    def need_hidden(self) -> bool:
        return self.ref_object.get('needHidden', False)

    @property
    def guest_votes_count(self) -> int:
        return self.ref_object.get('guestVotesCount') or 0

    @property
    def global_comments_count(self) -> int:
        return self.ref_object.get('globalCommentsCount') or 0

    @property
    def modified_time(self) -> Optional[str]:
        return self.ref_object.get('modifiedTime')

    @property
    def widget_display_interval(self) -> Optional[int]:
        return self.ref_object.get('widgetDisplayInterval')

    @property
    def total_poll_vote_count(self) -> int:
        return self.ref_object.get('totalPollVoteCount') or 0

    @property
    def blogId(self) -> str:
        return self.ref_object.get('blogId', "")

    @property
    def view_count(self) -> int:
        return self.ref_object.get('viewCount') or 0

    @property
    def author(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.ref_object.get('author') or {})

    def json(self) -> dict[str, Any]:
        return self.data


class FeaturedBlogs:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = data.get("featuredList") or []
        parser = [FeaturedBlog(x) for x in self.data]
        self.ref_object_type = [x.ref_object_type for x in parser]
        self.ref_object_id = [x.ref_object_id for x in parser]
        self.expired_time = [x.expired_time for x in parser]
        self.featured_type = [x.featured_type for x in parser]
        self.created_time = [x.created_time for x in parser]
        self.ref_object = [x.ref_object for x in parser]
        self.global_votes_count = [x.global_votes_count for x in parser]
        self.global_voted_count = [x.global_voted_count for x in parser]
        self.voted_value = [x.voted_value for x in parser]
        self.keywords = [x.keywords for x in parser]
        self.strategy_info = [x.strategy_info for x in parser]
        self.media_list = [x.media_list for x in parser]
        self.style = [x.style for x in parser]
        self.total_quiz_play_count = [x.total_quiz_play_count for x in parser]
        self.title = [x.title for x in parser]
        self.tip_info = [x.tip_info for x in parser]
        self.content = [x.content for x in parser]
        self.content_rating = [x.content_rating for x in parser]
        self.need_hidden = [x.need_hidden for x in parser]
        self.guest_votes_count = [x.guest_votes_count for x in parser]
        self.global_comments_count = [x.global_comments_count for x in parser]
        self.modified_time = [x.modified_time for x in parser]
        self.widget_display_interval = [x.widget_display_interval for x in parser]
        self.total_poll_vote_count = [x.total_poll_vote_count for x in parser]
        self.blogId = [x.blogId for x in parser]
        self.view_count = [x.view_count for x in parser]
        self.ref_object_type = [x.ref_object_type for x in parser]
        self.ref_object_id = [x.ref_object_id for x in parser]
        self.author = userprofile.UserProfileList([x.author.json() for x in parser])

    def json(self) -> list[dict[str, Any]]:
        return self.data


class QuizRanking:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def highest_mode(self) -> Optional[int]:
        return self.data.get('highestMode')

    @property
    def modified_time(self) -> Optional[str]:
        return self.data.get('modifiedTime')

    @property
    def is_finished(self) -> bool:
        return self.data.get('isFinished', False)

    @property
    def hell_is_finished(self) -> bool:
        return self.data.get('hellIsFinished', False)

    @property
    def highest_score(self) -> int:
        return self.data.get('highestScore', 0)

    @property
    def beat_rate(self) -> int:
        return self.data.get('beatRate', 0)

    @property
    def last_beat_rate(self) -> Optional[int]:
        return self.data.get('lastBeatRate')
    
    @property
    def total_times(self) -> int:
        return self.data.get('totalTimes', 0)

    @property
    def latest_score(self) -> int:
        return self.data.get('latestScore') or 0

    @property
    def author(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.data.get('author') or {})

    @property
    def latest_mode(self) -> Optional[int]:
        return self.data.get('latestMode')

    @property
    def created_time(self) -> str:
        return self.data.get('createdTime', "")

    def json(self) -> dict[str, Any]:
        return self.data


class QuizRankingList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = data.get("quizResultRankingList") or []
        parser = [QuizRanking(x) for x in self.data]
        self.highest_mode = [x.highest_mode for x in parser]
        self.modified_time = [x.modified_time for x in parser]
        self.is_finished = [x.is_finished for x in parser]
        self.hell_is_finished = [x.hell_is_finished for x in parser]
        self.highest_score = [x.highest_score for x in parser]
        self.beat_rate = [x.beat_rate for x in parser]
        self.last_beat_rate = [x.last_beat_rate for x in parser]
        self.total_times = [x.total_times for x in parser]
        self.latest_score = [x.latest_score for x in parser]
        self.author = userprofile.UserProfileList([x.author.json() for x in parser])
        self.latest_mode = [x.latest_mode for x in parser]
        self.created_time = [x.created_time for x in parser]

    def json(self) -> list[dict[str, Any]]:
        return self.data


class FetchNotification:
    def __init__(self, data: dict[str, Any]):
        self.data = data

    @property
    def parentText(self) -> Optional[str]:
        return self.data.get("parentText")

    @property
    def objectId(self) -> str:
        return self.data.get("objectId", "")

    @property
    def contextText(self) -> Optional[str]:
        return self.data.get("contextText")

    @property
    def type(self) -> int:
        return self.data.get("type", 0)

    @property
    def parentId(self) -> str:
        return self.data.get("parentId", "")

    @property
    def operator(self) -> userprofile.UserProfile:
        return userprofile.UserProfile(self.data.get("operator") or {})

    @property
    def createdTime(self) -> str:
        return self.data.get("createdTime", "")

    @property
    def parentType(self) -> int:
        return self.data.get("parentType", 0)

    @property
    def ndcId(self) -> int:
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        return self.ndcId

    @property
    def notificationId(self) -> str:
        return self.data.get("notificationId", "")

    @property
    def objectText(self) -> str:
        return self.data.get("objectText", "")

    @property
    def contextValue(self) -> Optional[str]:
        return self.data.get("contextValue")

    @property
    def contextComId(self) -> Optional[str]:
        return self.data.get("contextNdcId")

    @property
    def objectType(self) -> int:
        return self.data.get("objectType", 0)

    def json(self) -> dict[str, Any]:
        return self.data


class GlobalNotificationList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = data.get('notificationList') or []

    def __iter__(self) -> Iterator[FetchNotification]:
        return (FetchNotification(x) for x in self.data)

    @property
    def parentText(self) -> list[Optional[str]]:
        """Returns a list of the parent text of the notification."""
        return [x.parentText for x in self]

    @property
    def objectId(self) -> list[str]:
        """Returns a list of the object id of the notification."""
        return [x.objectId for x in self]

    @property
    def contextText(self) -> list[Optional[str]]:
        """Returns a list of the context text of the notification."""
        return [x.contextText for x in self]

    @property
    def type(self):
        """Returns a list of the type of the notification."""
        return [x.type for x in self]

    @property
    def parentId(self):
        """Returns a list of the parent id of the notification."""
        return [x.parentId for x in self]

    @property
    def operator(self) -> userprofile.UserProfileList:
        """Returns a list of the operator of the notification."""
        return userprofile.UserProfileList([x.operator.json() for x in self])

    @property
    def createdTime(self) -> list[str]:
        """Returns a list of the time the notification was created."""
        return [x.createdTime for x in self]

    @property
    def notificationId(self) -> list[str]:
        """Returns a list of the notification id."""
        return [x.notificationId for x in self]

    @property
    def ndcId(self) -> list[int]:
        """Returns a list of the ndc id of the notification."""
        return [x.ndcId for x in self]

    @property
    def comId(self) -> list[int]:
        """Returns a list of the com id of the notification."""
        return [x.comId for x in self]

    @property
    def objectText(self) -> list[str]:
        """Returns a list of the object text of the notification."""
        return [x.objectText for x in self]

    @property
    def contextValue(self) -> list[Optional[str]]:
        """Returns a list of the context value of the notification."""
        return [x.contextValue for x in self]

    @property
    def contextComId(self) -> list[Optional[str]]:
        """Returns a list of the context ndc id of the notification."""
        return [x.contextComId for x in self]

    @property
    def objectType(self) -> list[int]:
        """Returns a list of the object type of the notification."""
        return [x.objectType for x in self]

    @property
    def parentType(self) -> list[int]:
        """Returns a list of the parent type of the notification."""
        return [x.parentType for x in self]

    def json(self) -> list[dict[str, Any]]:
        return self.data

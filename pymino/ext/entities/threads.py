from collections.abc import Iterator
from typing import Any, Dict, List, Optional, Union

__all__ = (
    "CThreadExtensionsList",
    "CThreadExtensions",
    "CThreadList",
    "CThread",
    "MemberSummary",
)


class CThreadExtensions:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data: Dict[str, Any] = data.get("extensions", data) or {}

    @property
    def coHost(self) -> List[str]:
        return self.data.get("coHost") or []

    @property
    def language(self) -> str:
        return self.data.get("language", "en")

    @property
    def membersCanInvite(self) -> bool:
        return self.data.get("membersCanInvite", False)

    @property
    def background(self) -> List[Any]:
        return self.data["bm"]

    @property
    def creatorUid(self) -> str:
        return self.data.get("creatorUid", "")

    @property
    def visibility(self) -> int:
        return self.data.get("visibility", 0)

    @property
    def lastMembersSummaryUpdateTime(self) -> Optional[str]:
        return self.data.get("lastMembersSummaryUpdateTime")

    @property
    def fansOnly(self) -> bool:
        return self.data.get("fansOnly", False)

    @property
    def channelType(self) -> Optional[int]:
        return self.data.get("channelType")

    @property
    def vvChatJoinType(self) -> Optional[int]:
        return self.data.get("vvChatJoinType")

    @property
    def avchatMemberUidList(self) -> List[str]:
        return self.data.get("avchatMemberUidList") or []

    @property
    def screeningRoomPermission(self) -> Dict[str, Any]:
        return self.data.get("screeningRoomPermission") or {}

    @property
    def disabledTime(self) -> Optional[str]:
        return self.data.get("__disabledTime__")

    def json(self) -> Dict[str, Any]:
        return self.data


class CThreadExtensionsList:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = data

    def __iter__(self) -> "Iterator[CThreadExtensions]":
        return (CThreadExtensions(x) for x in self.data)

    @property
    def coHost(self) -> List[List[str]]:
        return [x.coHost for x in self]

    @property
    def language(self) -> List[str]:
        return [x.language for x in self]

    @property
    def membersCanInvite(self) -> List[bool]:
        return [x.membersCanInvite for x in self]

    @property
    def background(self) -> List[List[Any]]:
        return [x.background for x in self]

    @property
    def creatorUid(self) -> List[str]:
        return [x.creatorUid for x in self]

    @property
    def visibility(self) -> List[int]:
        return [x.visibility for x in self]

    @property
    def lastMembersSummaryUpdateTime(self) -> List[Optional[str]]:
        return [x.lastMembersSummaryUpdateTime for x in self]

    @property
    def fansOnly(self) -> List[bool]:
        return [x.fansOnly for x in self]

    @property
    def channelType(self) -> List[Optional[int]]:
        return [x.channelType for x in self]

    @property
    def vvChatJoinType(self) -> List[Optional[int]]:
        return [x.vvChatJoinType for x in self]

    @property
    def avchatMemberUidList(self) -> List[List[str]]:
        return [x.avchatMemberUidList for x in self]

    @property
    def screeningRoomPermission(self) -> List[Dict[str, Any]]:
        return [x.screeningRoomPermission for x in self]

    @property
    def disabledTime(self) -> List[Optional[str]]:
        return [x.disabledTime for x in self]

    def json(self) -> List[Dict[str, Any]]:
        return self.data


class MemberSummary:
    def __init__(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> None:
        if isinstance(data, dict):
            data = list(data.get("membersSummary") or [])
        self.data = data

    @property
    def status(self) -> List[int]:
        return [x.get("status", 0) for x in self.data]

    @property
    def uid(self) -> List[str]:
        return [x.get("uid", "") for x in self.data]

    @property
    def userId(self) -> List[str]:
        return self.uid

    @property
    def membershipStatus(self) -> List[int]:
        return [x.get("membershipStatus", 0) for x in self.data]

    @property
    def role(self) -> List[int]:
        return [x.get("role", 0) for x in self.data]

    @property
    def nickname(self) -> List[str]:
        return [x.get("nickname", "") for x in self.data]

    @property
    def username(self) -> List[str]:
        return self.nickname

    @property
    def icon(self) -> List[Optional[str]]:
        return [x.get("icon") for x in self.data]

    @property
    def avatar(self) -> List[Optional[str]]:
        return self.icon

    def json(self) -> List[Dict[str, Any]]:
        return self.data


class CThread:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data: Dict[str, Any] = data.get("thread", data) or {}

    def __bool__(self) -> bool:
        return bool(self.threadId)

    @property
    def userAddedTopicList(self) -> List[int]:
        return self.data.get("userAddedTopicList") or []

    @property
    def uid(self) -> str:
        return self.data.get("uid", "")

    @property
    def hostUserId(self) -> str:
        return self.uid

    @property
    def membersQuota(self) -> int:
        return self.data.get("membersQuota", 1000)

    @property
    def membersSummary(self) -> MemberSummary:
        return MemberSummary(self.data.get("membersSummary") or {})

    @property
    def threadId(self) -> str:
        return self.data.get("threadId", "")

    @property
    def chatId(self) -> str:
        return self.threadId

    @property
    def keywords(self) -> str:
        return self.data.get("keywords", "")

    @property
    def membersCount(self) -> int:
        return self.data.get("membersCount", 0)

    @property
    def strategyInfo(self) -> str:
        return self.data.get("strategyInfo", "{}")

    @property
    def isPinned(self) -> bool:
        return self.data.get("isPinned", False)

    @property
    def title(self) -> Optional[str]:
        return self.data.get("title")

    @property
    def membershipStatus(self) -> int:
        return self.data.get("membershipStatus", 0)

    @property
    def content(self) -> Optional[str]:
        return self.data.get("content")

    @property
    def needHidden(self) -> bool:
        return self.data.get("needHidden", False)

    @property
    def alertOption(self) -> int:
        return self.data.get("alertOption", 0)

    @property
    def lastReadTime(self) -> Optional[str]:
        return self.data.get("lastReadTime")

    @property
    def type(self) -> int:
        return self.data.get("type", 0)

    @property
    def status(self) -> int:
        return self.data.get("status", 0)

    @property
    def publishToGlobal(self) -> bool:
        return self.data.get("publishToGlobal", False)

    @property
    def modifiedTime(self) -> Optional[str]:
        return self.data.get("modifiedTime")

    @property
    def lastMessageSummary(self) -> Any:
        return self.data.get("lastMessageSummary")

    @property
    def extensions(self) -> CThreadExtensions:
        return CThreadExtensions(self.data.get("extensions") or {})

    def json(self) -> Dict[str, Any]:
        return self.data


class CThreadList:
    def __init__(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
        if isinstance(data, dict):
            data = list(data.get("threadList") or [])
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.data)

    def __iter__(self) -> "Iterator[CThread]":
        return (CThread(x) for x in self.data)

    @property
    def extensions(self) -> CThreadExtensionsList:
        return CThreadExtensionsList([x.extensions.json() for x in self])

    @property
    def membersSummary(self) -> List[MemberSummary]:
        return [x.membersSummary for x in self]

    @property
    def userAddedTopicList(self) -> List[List[int]]:
        return [x.userAddedTopicList for x in self]

    @property
    def uid(self) -> List[str]:
        return [x.uid for x in self]

    @property
    def hostUserId(self) -> List[str]:
        return [x.hostUserId for x in self]

    @property
    def membersQuota(self) -> List[int]:
        return [x.membersQuota for x in self]

    @property
    def threadId(self) -> List[str]:
        return [x.threadId for x in self]

    @property
    def chatId(self) -> List[str]:
        return [x.chatId for x in self]

    @property
    def keywords(self) -> List[str]:
        return [x.keywords for x in self]

    @property
    def membersCount(self) -> List[int]:
        return [x.membersCount for x in self]

    @property
    def strategyInfo(self) -> List[str]:
        return [x.strategyInfo for x in self]

    @property
    def isPinned(self) -> List[bool]:
        return [x.isPinned for x in self]

    @property
    def title(self) -> List[Optional[str]]:
        return [x.title for x in self]

    @property
    def membershipStatus(self) -> List[int]:
        return [x.membershipStatus for x in self]

    @property
    def content(self) -> List[Optional[str]]:
        return [x.content for x in self]

    @property
    def needHidden(self) -> List[bool]:
        return [x.needHidden for x in self]

    @property
    def alertOption(self) -> List[int]:
        return [x.alertOption for x in self]

    @property
    def lastReadTime(self) -> List[Optional[str]]:
        return [x.lastReadTime for x in self]

    @property
    def type(self) -> List[int]:
        return [x.type for x in self]

    @property
    def status(self) -> List[int]:
        return [x.status for x in self]

    @property
    def publishToGlobal(self) -> List[bool]:
        return [x.publishToGlobal for x in self]

    @property
    def modifiedTime(self) -> List[Optional[str]]:
        return [x.modifiedTime for x in self]

    @property
    def lastMessageSummary(self) -> List[Any]:
        return [x.lastMessageSummary for x in self]

    def json(self) -> List[Dict[str, Any]]:
        return self.data

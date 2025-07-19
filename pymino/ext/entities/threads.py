from collections.abc import Iterator
from typing import Any, Optional, Union

__all__ = (
    "CThreadExtensionsList",
    "CThreadExtensions",
    "CThreadList",
    "CThread",
    "MemberSummary",
)


class CThreadExtensions:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("extensions", data) or {}

    @property
    def coHost(self) -> list[str]:
        return self.data.get("coHost") or []

    @property
    def language(self) -> str:
        return self.data.get("language", "en")

    @property
    def membersCanInvite(self) -> bool:
        return self.data.get("membersCanInvite", False)

    @property
    def background(self) -> list[Any]:
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
    def avchatMemberUidList(self) -> list[str]:
        return self.data.get("avchatMemberUidList") or []

    @property
    def screeningRoomPermission(self) -> dict[str, Any]:
        return self.data.get("screeningRoomPermission") or {}

    @property
    def disabledTime(self) -> Optional[str]:
        return self.data.get("__disabledTime__")

    def json(self) -> dict[str, Any]:
        return self.data


class CThreadExtensionsList:
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.data = data

    def __iter__(self) -> Iterator[CThreadExtensions]:
        return (CThreadExtensions(x) for x in self.data)

    @property
    def coHost(self) -> list[list[str]]:
        return [x.coHost for x in self]

    @property
    def language(self) -> list[str]:
        return [x.language for x in self]

    @property
    def membersCanInvite(self) -> list[bool]:
        return [x.membersCanInvite for x in self]

    @property
    def background(self) -> list[list[Any]]:
        return [x.background for x in self]

    @property
    def creatorUid(self) -> list[str]:
        return [x.creatorUid for x in self]

    @property
    def visibility(self) -> list[int]:
        return [x.visibility for x in self]

    @property
    def lastMembersSummaryUpdateTime(self) -> list[Optional[str]]:
        return [x.lastMembersSummaryUpdateTime for x in self]

    @property
    def fansOnly(self) -> list[bool]:
        return [x.fansOnly for x in self]

    @property
    def channelType(self) -> list[Optional[int]]:
        return [x.channelType for x in self]

    @property
    def vvChatJoinType(self) -> list[Optional[int]]:
        return [x.vvChatJoinType for x in self]

    @property
    def avchatMemberUidList(self) -> list[list[str]]:
        return [x.avchatMemberUidList for x in self]

    @property
    def screeningRoomPermission(self) -> list[dict[str, Any]]:
        return [x.screeningRoomPermission for x in self]

    @property
    def disabledTime(self) -> list[Optional[str]]:
        return [x.disabledTime for x in self]

    def json(self) -> list[dict[str, Any]]:
        return self.data


class MemberSummary:
    def __init__(self, data: Union[list[dict[str, Any]], dict[str, Any]]) -> None:
        if isinstance(data, dict):
            data = list(data.get("membersSummary") or [])
        self.data = data

    @property
    def status(self) -> list[int]:
        return [x.get("status", 0) for x in self.data]

    @property
    def uid(self) -> list[str]:
        return [x.get("uid", "") for x in self.data]

    @property
    def userId(self) -> list[str]:
        return self.uid

    @property
    def membershipStatus(self) -> list[int]:
        return [x.get("membershipStatus", 0) for x in self.data]

    @property
    def role(self) -> list[int]:
        return [x.get("role", 0) for x in self.data]

    @property
    def nickname(self) -> list[str]:
        return [x.get("nickname", "") for x in self.data]

    @property
    def username(self) -> list[str]:
        return self.nickname

    @property
    def icon(self) -> list[Optional[str]]:
        return [x.get("icon") for x in self.data]

    @property
    def avatar(self) -> list[Optional[str]]:
        return self.icon

    def json(self) -> list[dict[str, Any]]:
        return self.data


class CThread:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("thread", data) or {}

    def __bool__(self) -> bool:
        return bool(self.threadId)

    @property
    def userAddedTopicList(self) -> list[int]:
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

    def json(self) -> dict[str, Any]:
        return self.data


class CThreadList:
    def __init__(self, data: Union[dict[str, Any], list[dict[str, Any]]]) -> None:
        if isinstance(data, dict):
            data = list(data.get("threadList") or [])
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.data)

    def __iter__(self) -> Iterator[CThread]:
        return (CThread(x) for x in self.data)

    @property
    def extensions(self) -> CThreadExtensionsList:
        return CThreadExtensionsList([x.extensions.json() for x in self])

    @property
    def membersSummary(self) -> list[MemberSummary]:
        return [x.membersSummary for x in self]

    @property
    def userAddedTopicList(self) -> list[list[int]]:
        return [x.userAddedTopicList for x in self]

    @property
    def uid(self) -> list[str]:
        return [x.uid for x in self]

    @property
    def hostUserId(self) -> list[str]:
        return [x.hostUserId for x in self]

    @property
    def membersQuota(self) -> list[int]:
        return [x.membersQuota for x in self]

    @property
    def threadId(self) -> list[str]:
        return [x.threadId for x in self]

    @property
    def chatId(self) -> list[str]:
        return [x.chatId for x in self]

    @property
    def keywords(self) -> list[str]:
        return [x.keywords for x in self]

    @property
    def membersCount(self) -> list[int]:
        return [x.membersCount for x in self]

    @property
    def strategyInfo(self) -> list[str]:
        return [x.strategyInfo for x in self]

    @property
    def isPinned(self) -> list[bool]:
        return [x.isPinned for x in self]

    @property
    def title(self) -> list[Optional[str]]:
        return [x.title for x in self]

    @property
    def membershipStatus(self) -> list[int]:
        return [x.membershipStatus for x in self]

    @property
    def content(self) -> list[Optional[str]]:
        return [x.content for x in self]

    @property
    def needHidden(self) -> list[bool]:
        return [x.needHidden for x in self]

    @property
    def alertOption(self) -> list[int]:
        return [x.alertOption for x in self]

    @property
    def lastReadTime(self) -> list[Optional[str]]:
        return [x.lastReadTime for x in self]

    @property
    def type(self) -> list[int]:
        return [x.type for x in self]

    @property
    def status(self) -> list[int]:
        return [x.status for x in self]

    @property
    def publishToGlobal(self) -> list[bool]:
        return [x.publishToGlobal for x in self]

    @property
    def modifiedTime(self) -> list[Optional[str]]:
        return [x.modifiedTime for x in self]

    @property
    def lastMessageSummary(self) -> list[Any]:
        return [x.lastMessageSummary for x in self]

    def json(self) -> list[dict[str, Any]]:
        return self.data

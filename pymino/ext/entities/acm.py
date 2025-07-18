from typing import Any, Optional

__all__ = (
    "Applicant",
    "ApplicantList",
    "CommunityMembershipRequest",
    "CommunityMembershipRequestList",
    "CommunityStats",
    "InvitationLog",
    "InvitationLogList",
)


class CommunityStats:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("communityStats", data) or {}

    @property
    def daily_active_members(self) -> int:
        """Returns the daily active members of the community."""
        return self.data.get("dailyActiveMembers", 0)

    @property
    def monthly_active_members(self) -> int:
        """Returns the monthly active members of the community."""
        return self.data.get("monthlyActiveMembers", 0)

    @property
    def total_time_spent(self) -> int:
        """Returns the total time spent in the community."""
        return self.data.get("totalTimeSpent", 0)

    @property
    def total_posts_created(self) -> int:
        """Returns the total posts created in the community."""
        return self.data.get("totalPostsCreated", 0)

    @property
    def new_members_today(self) -> int:
        """Returns the new members today in the community."""
        return self.data.get("newMembersToday", 0)

    @property
    def total_members(self) -> int:
        """Returns the total members in the community."""
        return self.data.get("totalMembers", 0)


class Applicant:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("applicant", data) or {}

    @property
    def status(self) -> int:
        """Returns the status of the applicant."""
        return self.data.get("status", 0)

    @property
    def uid(self) -> str:
        """Returns the uid of the applicant."""
        return self.data.get("uid", "")

    @property
    def is_global(self) -> bool:
        """Returns whether the applicant is global."""
        return self.data.get("isGlobal", False)

    @property
    def role(self) -> int:
        """Returns the role of the applicant."""
        return self.data.get("role", 0)

    @property
    def is_staff(self) -> bool:
        """Returns whether the applicant is staff."""
        return self.data.get("isStaff", False)

    @property
    def nickname(self) -> Optional[str]:
        """Returns the nickname of the applicant."""
        return self.data.get("nickname")

    @property
    def icon(self) -> Optional[str]:
        """Returns the icon of the applicant."""
        return self.data.get("icon")


class ApplicantList:
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.data = data

    @property
    def status(self) -> list[int]:
        """Returns the status of the applicant."""
        return [applicant.get("status", 0) for applicant in self.data]

    @property
    def uid(self) -> list[str]:
        """Returns the uid of the applicant."""
        return [applicant.get("uid", "") for applicant in self.data]

    @property
    def is_global(self) -> list[bool]:
        """Returns whether the applicant is global."""
        return [applicant.get("isGlobal", False) for applicant in self.data]

    @property
    def role(self) -> list[int]:
        """Returns the role of the applicant."""
        return [applicant.get("role", 0) for applicant in self.data]

    @property
    def is_staff(self) -> list[bool]:
        """Returns whether the applicant is staff."""
        return [applicant.get("isStaff", False) for applicant in self.data]

    @property
    def nickname(self) -> list[Optional[str]]:
        """Returns the nickname of the applicant."""
        return [applicant.get("nickname") for applicant in self.data]

    @property
    def icon(self) -> list[Optional[str]]:
        """Returns the icon of the applicant."""
        return [applicant.get("icon") for applicant in self.data]


class CommunityMembershipRequest:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def status(self) -> int:
        """Returns the status of the community membership request."""
        return self.data.get("status", 0)

    @property
    def request_id(self) -> str:
        """Returns the request id of the community membership request."""
        return self.data.get("requestId", "")

    @property
    def modified_time(self) -> Optional[str]:
        """Returns the modified time of the community membership request."""
        return self.data.get("modifiedTime")

    @property
    def ndcId(self) -> int:
        """Returns the ndc id of the community membership request."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        """Returns the ndc id of the community membership request list."""
        return self.ndcId

    @property
    def created_time(self) -> str:
        """Returns the created time of the community membership request."""
        return self.data.get("createdTime", "")

    @property
    def message(self) -> Optional[str]:
        """Returns the message of the community membership request."""
        return self.data.get("message")

    @property
    def applicant(self) -> Applicant:
        """Returns the applicant of the community membership request."""
        return Applicant(self.data.get("applicant") or {})

    @property
    def uid(self) -> str:
        """Returns the uid of the community membership request."""
        return self.data.get("uid", "")


class CommunityMembershipRequestList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = (
            data.get("communityMembershipRequestList") or []
        )

    @property
    def parser(self) -> list[CommunityMembershipRequest]:
        """Returns the parser of the community membership request list."""
        return [CommunityMembershipRequest(data) for data in self.data]

    @property
    def status(self) -> list[int]:
        """Returns the status of the community membership request list."""
        return [x.get("status", 0) for x in self.data]

    @property
    def request_id(self) -> list[str]:
        """Returns the request id of the community membership request list."""
        return [x.get("requestId", "") for x in self.data]

    @property
    def modified_time(self) -> list[Optional[str]]:
        """Returns the modified time of the community membership request list."""
        return [x.get("modifiedTime") for x in self.data]

    @property
    def ndcId(self) -> list[int]:
        """Returns the ndc id of the community membership request list."""
        return [x.get("ndcId", 0) for x in self.data]

    @property
    def comId(self) -> list[int]:
        """Returns the ndc id of the community membership request list."""
        return self.ndcId

    @property
    def created_time(self) -> list[str]:
        """Returns the created time of the community membership request list."""
        return [x.get("createdTime", "") for x in self.data]

    @property
    def message(self) -> list[Optional[str]]:
        """Returns the message of the community membership request list."""
        return [x.get("message") for x in self.data]

    @property
    def applicant(self) -> ApplicantList:
        """Returns the applicant of the community membership request list."""
        return ApplicantList([x.get("applicant") or {} for x in self.data])

    @property
    def uid(self) -> list[str]:
        """Returns the uid of the community membership request list."""
        return [x.get("uid", "") for x in self.data]

    @property
    def userId(self) -> list[str]:
        """Returns the user id of the community membership request list."""
        return self.uid


class InvitationLog:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def created_time(self) -> str:
        """Returns the created time of the invitation log."""
        return self.data.get("createdTime", "")

    @property
    def invitationId(self) -> str:
        """Returns the invitation id of the invitation log."""
        return self.data.get("invitationId", "")

    @property
    def isNicknameVerified(self) -> bool:
        """Returns whether the nickname is verified of the invitation log."""
        return self.data.get("userProfile", {}).get("isNicknameVerified", False)

    @property
    def uid(self) -> str:
        """Returns the uid of the invitation log."""
        return self.data.get("userProfile", {}).get("uid", "")

    @property
    def userId(self) -> str:
        """Returns the user id of the invitation log."""
        return self.uid

    @property
    def level(self) -> int:
        """Returns the level of the invitation log."""
        return self.data.get("userProfile", {}).get("level", 0)

    @property
    def followingStatus(self) -> int:
        """Returns the following status of the invitation log."""
        return self.data.get("userProfile", {}).get("followingStatus", 0)

    @property
    def accountMembershipStatus(self) -> int:
        """Returns the account membership status of the invitation log."""
        return self.data.get("userProfile", {}).get("accountMembershipStatus", 0)

    @property
    def isGlobal(self) -> bool:
        """Returns whether the invitation log is global."""
        return self.data.get("userProfile", {}).get("isGlobal", False)

    @property
    def membershipStatus(self) -> int:
        """Returns the membership status of the invitation log."""
        return self.data.get("userProfile", {}).get("membershipStatus", 0)

    @property
    def reputation(self) -> int:
        """Returns the reputation of the invitation log."""
        return self.data.get("userProfile", {}).get("reputation", 0)

    @property
    def role(self) -> int:
        """Returns the role of the invitation log."""
        return self.data.get("userProfile", {}).get("role", 0)

    @property
    def ndcId(self) -> int:
        """Returns the ndc id of the invitation log."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        """Returns the community id of the invitation log."""
        return self.ndcId

    @property
    def membersCount(self) -> int:
        """Returns the members count of the invitation log."""
        return self.data.get("userProfile", {}).get("membersCount", 0)

    @property
    def nickname(self) -> str:
        """Returns the nickname of the invitation log."""
        return self.data.get("userProfile", {}).get("nickname", "")

    @property
    def username(self) -> str:
        """Returns the username of the invitation log."""
        return self.nickname

    @property
    def icon(self) -> Optional[str]:
        """Returns the icon of the invitation log."""
        return self.data.get("userProfile", {}).get("icon")


class InvitationLogList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = data.get("invitationLogList") or []
        parser: list[InvitationLog] = [InvitationLog(x) for x in self.data]
        self.created_time = [x.created_time for x in parser]
        self.invitationId = [x.invitationId for x in parser]
        self.isNicknameVerified = [x.isNicknameVerified for x in parser]
        self.uid = [x.uid for x in parser]
        self.userId = [x.userId for x in parser]
        self.level = [x.level for x in parser]
        self.followingStatus = [x.followingStatus for x in parser]
        self.accountMembershipStatus = [x.accountMembershipStatus for x in parser]
        self.isGlobal = [x.isGlobal for x in parser]
        self.membershipStatus = [x.membershipStatus for x in parser]
        self.reputation = [x.reputation for x in parser]
        self.role = [x.role for x in parser]
        self.ndcId = [x.ndcId for x in parser]
        self.comId = [x.comId for x in parser]
        self.membersCount = [x.membersCount for x in parser]
        self.nickname = [x.nickname for x in parser]
        self.username = [x.username for x in parser]
        self.icon = [x.icon for x in parser]

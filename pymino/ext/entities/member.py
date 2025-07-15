from typing import Any, Dict, Optional

__all__ = ("Member", "MemberAvatar")


class MemberAvatar:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.frameId)

    @property
    def status(self) -> int:
        """Returns the status of the member avatar."""
        return self.data.get("status", 0)

    @property
    def version(self) -> int:
        """Returns the version of the member avatar."""
        return self.data.get("version", 0)

    @property
    def resourceUrl(self) -> str:
        """Returns the resource URL of the member avatar."""
        return self.data.get("resourceUrl", "")

    @property
    def name(self) -> str:
        """Returns the name of the member avatar."""
        return self.data.get("name", "")

    @property
    def icon(self) -> str:
        """Returns the icon of the member avatar."""
        return self.data.get("icon", "")

    @property
    def frameType(self) -> int:
        """Returns the frame type of the member avatar."""
        return self.data.get("frameType", 0)

    @property
    def frameId(self) -> str:
        """Returns the frame ID of the member avatar."""

        return self.data.get("frameId", "")


class Member:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.uid)

    @property
    def uid(self) -> str:
        """Returns the uid of the member."""
        return self.data.get("uid", "")

    @property
    def userId(self) -> str:
        """Returns the userId of the member."""
        return self.uid

    @property
    def status(self) -> int:
        """Returns the status of the member."""
        return self.data.get("status", 0)

    @property
    def icon(self) -> Optional[str]:
        """Returns the icon of the member."""
        return self.data.get("icon")

    @property
    def reputation(self) -> int:
        """Returns the reputation of the member."""
        return self.data.get("reputation", 0)

    @property
    def role(self) -> int:
        """Returns the role of the member."""
        return self.data.get("role", 0)

    @property
    def nickname(self) -> str:
        """Returns the nickname of the member."""
        return self.data.get("nickname", "")

    @property
    def level(self) -> int:
        """Returns the level of the member."""
        return self.data.get("level", 0)

    @property
    def membership_status(self) -> int:
        """Returns the accountMembershipStatus of the member."""
        return self.data.get("accountMembershipStatus", 0)

    @property
    def avatar(self) -> MemberAvatar:
        """Returns the avatar of the member."""
        return MemberAvatar(self.data.get("avatarFrame") or {})

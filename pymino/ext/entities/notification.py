from typing import Any, Optional

__all__ = ("Notification",)


class Notification:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("o") or {}

    def __bool___(self) -> bool:
        return bool(self.id)

    @property
    def payload(self) -> dict[str, Any]:
        """Returns the payload of the notification."""
        return self.data.get("payload") or {}

    @property
    def exp(self) -> int:
        """Returns the expiration date of the notification."""
        return self.payload.get("exp", 0)

    @property
    def ndcId(self) -> Optional[int]:
        """Returns the NDC ID of the notification."""
        return self.payload.get("ndcId")

    @property
    def comId(self) -> Optional[int]:
        """Returns the COM ID of the notification."""
        return self.ndcId

    @property
    def chatId(self) -> str:
        """Returns the chat ID of the notification."""
        return self.payload.get("tid", "")

    @property
    def aps(self) -> dict[str, Any]:
        """Returns the APS of the notification."""
        return self.payload.get("aps") or {}

    @property
    def sound(self) -> str:
        """Returns the sound of the notification."""
        return self.aps.get("sound", "")

    @property
    def alert(self) -> str:
        """Returns the alert of the notification."""
        return self.aps.get("alert", "")

    @property
    def notification_type(self) -> int:
        """Returns the notification type of the notification."""
        return self.payload.get("notifType", 0)

    @property
    def id(self) -> str:
        """Returns the ID of the notification."""
        return self.payload.get("id", "")

    def json(self) -> dict[str, Any]:
        """Returns the JSON data of the notification."""
        return self.data

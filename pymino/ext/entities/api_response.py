from typing import Any, Dict, Optional

__all__ = ("ApiResponse",)


class ApiResponse:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def message(self) -> str:
        """Returns the message of the API response."""
        return self.data.get("api:message", "")

    @property
    def status_code(self) -> int:
        """Returns the status code of the API response."""
        return self.data.get("api:statuscode", 0)

    @property
    def duration(self) -> str:
        """Returns the duration of the API response."""
        return self.data.get("api:duration", "")

    @property
    def timestamp(self) -> str:
        """Returns the timestamp of the API response."""
        return self.data.get("api:timestamp", "")

    @property
    def media_value(self) -> Optional[str]:
        """Returns the media value of the API response."""
        return self.data.get("mediaValue") or self.data.get("result", {}).get(
            "mediaValue"
        )

    @property
    def mediaValue(self) -> Optional[str]:
        # NOTE: This will be removed in the future.
        """Returns the media value of the API response."""
        return self.media_value

    def json(self) -> Dict[str, Any]:
        """Returns the JSON data of the API response."""
        return self.data

    def __repr__(self) -> str:
        """Returns the representation of the API response."""
        return f"<ApiResponse status_code={self.status_code} message={self.message} media_value={self.media_value}>"

from typing import Any

__all__ = ("LinkInfo",)


class LinkInfo:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def linkInfoV2(self) -> dict[str, Any]:
        """Returns the linkInfoV2 of the API response."""
        return self.data.get("linkInfoV2") or {}

    @property
    def path(self) -> str:
        """Returns the path of the API response."""
        return self.data.get("path") or self.linkInfoV2.get("path", "")

    @property
    def extensions(self) -> dict[str, Any]:
        """Returns the extensions of the API response."""
        return self.data.get("extensions") or self.linkInfoV2.get("extensions") or {}

    @property
    def objectId(self) -> str:
        """Returns the objectId of the API response."""
        return self.data.get("objectId") or self.extensions.get("linkInfo", {}).get(
            "objectId", ""
        )

    @property
    def shareURLShortCode(self) -> str:
        """Returns the shareURLShortCode of the API response."""
        return (
            self.data.get("shareURLShortCode")
            or self.extensions.get("linkInfo", {}).get("shareURLShortCode")
            or ""
        )

    @property
    def targetCode(self) -> int:
        return (
            self.data.get("targetCode")
            or self.extensions.get("linkInfo", {}).get("targetCode")
            or 1
        )

    @property
    def ndcId(self) -> int:
        """Returns the ndcId of the API response."""
        return (
            self.data.get("ndcId")
            or self.extensions.get("linkInfo", {}).get("ndcId")
            or 0
        )

    @property
    def comId(self) -> int:
        """Returns the comId of the API response."""
        return self.ndcId

    @property
    def fullPath(self) -> str:
        """Returns the fullPath of the API response."""
        return (
            self.data.get("fullPath")
            or self.extensions.get("linkInfo", {}).get("fullPath")
            or ""
        )

    @property
    def shortCode(self) -> str:
        """Returns the shortCode of the API response."""
        return (
            self.data.get("shortCode")
            or self.extensions.get("linkInfo", {}).get("shortCode")
            or ""
        )

    @property
    def objectType(self) -> int:
        """Returns the objectType of the API response."""
        return (
            self.data.get("objectType")
            or self.extensions.get("linkInfo", {}).get("objectType")
            or 0
        )

    def json(self) -> dict[str, Any]:
        """Returns the JSON data of the API response."""
        return self.data

    def __repr__(self) -> str:
        """Returns the representation of the Link Info response."""
        return f"<LinkInfo data={self.data}>"

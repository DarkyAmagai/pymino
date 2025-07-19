from collections.abc import Iterator
from typing import Any, Optional, Union

from pymino.ext.entities import userprofile

__all__ = (
    "Comment",
    "CommentExtensions",
    "CommentList",
    "CommentSticker",
    "CommentStickerCollectionSummary",
)


class CommentStickerCollectionSummary:
    def __init__(self, data: dict[str, Any]):
        self.data: dict[str, Any] = data.get("stickerCollectionSummary", data) or {}

    @property
    def status(self) -> int:
        """Returns the status of the sticker collection summary."""
        return self.data.get("status", 0)

    @property
    def collectionType(self) -> int:
        """Returns the collection type of the sticker collection summary."""
        return self.data.get("collectionType", 0)

    @property
    def userId(self) -> str:
        """Returns the userId of the sticker collection summary."""
        return self.data.get("uid", "")

    @property
    def modifiedTime(self) -> Optional[str]:
        """Returns the modified time of the sticker collection summary."""
        return self.data.get("modifiedTime")

    @property
    def bannerUrl(self) -> str:
        """Returns the banner URL of the sticker collection summary."""
        return self.data.get("bannerUrl", "")

    @property
    def smallIcon(self) -> str:
        """Returns the small icon of the sticker collection summary."""
        return self.data.get("smallIcon", "")

    @property
    def stickersCount(self) -> int:
        """Returns the sticker count of the sticker collection summary."""
        return self.data.get("stickersCount", 0)

    @property
    def usedCount(self) -> int:
        """Returns the used count of the sticker collection summary."""
        return self.data.get("usedCount", 0)

    @property
    def icon(self) -> str:
        """Returns the icon of the sticker collection summary."""
        return self.data.get("icon", "")

    @property
    def name(self) -> str:
        """Returns the name of the sticker collection summary."""
        return self.data.get("name", "")

    @property
    def collectionId(self) -> str:
        """Returns the collection ID of the sticker collection summary."""
        return self.data.get("collectionId", "")

    @property
    def createdTime(self) -> str:
        """Returns the created time of the sticker collection summary."""
        return self.data.get("createdTime", "")


class CommentSticker:
    def __init__(self, data: dict[str, Any]):
        self.data: dict[str, Any] = data.get("sticker", data) or {}

    @property
    def status(self) -> int:
        """Returns the status of the sticker."""
        return self.data.get("status", 0)

    @property
    def iconV2(self) -> str:
        """Returns the icon of the sticker."""
        return self.data.get("iconV2", "")

    @property
    def name(self) -> str:
        """Returns the name of the sticker."""
        return self.data.get("name", "")

    @property
    def stickerId(self) -> str:
        """Returns the ID of the sticker."""
        return self.data.get("stickerId", "")

    @property
    def icon_url(self) -> str:
        """Returns the icon URL of the sticker."""
        return self.data.get("icon", "")

    @property
    def smallIconV2(self) -> str:
        """Returns the small icon of the sticker."""
        return self.data.get("smallIconV2", "")

    @property
    def smallIcon(self) -> str:
        """Returns the small icon of the sticker."""
        return self.data.get("smallIcon", "")

    @property
    def stickerCollectionId(self) -> str:
        """Returns the sticker collection ID of the sticker."""
        return self.data.get("stickerCollectionId", "")

    @property
    def mediumIcon(self) -> str:
        """Returns the medium icon of the sticker."""
        return self.data.get("mediumIcon", "")

    @property
    def stickerCollectionSummary(self) -> CommentStickerCollectionSummary:
        """Returns the sticker collection summary of the sticker."""
        return CommentStickerCollectionSummary(self.data)


class CommentExtensions:
    def __init__(self, data: dict[str, Any]):
        self.data: dict[str, Any] = data.get("extensions", data) or {}

    @property
    def sticker(self) -> CommentSticker:
        """Returns the sticker of the comment."""
        return CommentSticker(self.data.get("sticker") or {})

    @property
    def stickerId(self) -> str:
        """Returns the sticker ID of the comment."""
        return self.data.get("stickerId", "")


class Comment:
    """
    Represents a comment object retrieved from an API response.

    :param data: The raw data of the comment.
    :type data: Union[dict, str]
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def author(self) -> dict[str, Any]:
        """Returns the author of the comment."""
        return self.data.get("author") or {}

    @property
    def commentId(self) -> str:
        """Returns the ID of the comment."""
        return self.data.get("commentId", "")

    @property
    def content(self) -> Optional[str]:
        """Returns the content of the comment."""
        return self.data.get("content")

    @property
    def createdTime(self) -> str:
        """Returns the creation time of the comment."""
        return self.data.get("createdTime", "")

    @property
    def extensions(self) -> CommentExtensions:
        """Returns the extensions of the comment."""
        return CommentExtensions(self.data.get("extensions") or {})

    @property
    def mediaList(self) -> list[tuple[int, str]]:
        """Returns the media list of the comment."""
        mediaList: list[list[Any]] = self.data.get("mediaList") or []
        return [(m[0], m[1]) for m in mediaList]

    @property
    def modifiedTime(self) -> Optional[str]:
        """Returns the modification time of the comment."""
        return self.data.get("modifiedTime")

    @property
    def ndcId(self) -> int:
        """Returns the community ID of the comment."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        """Returns the community ID of the comment."""
        return self.ndcId

    @property
    def parentId(self) -> str:
        """Returns the ID of the object the comment is on."""
        return self.data.get("parentId", "")

    @property
    def objectId(self) -> str:
        """Returns the ID of the object the comment is on."""
        return self.parentId

    @property
    def parentNdcId(self) -> int:
        """Returns the NDC ID of the parent comment."""
        return self.data.get("parentNdcId", 0)

    @property
    def parentComId(self) -> int:
        """Returns the NDC ID of the parent comment."""
        return self.parentNdcId

    @property
    def parentType(self) -> int:
        """Returns the type of the parent comment."""
        return self.data.get("parentType", 0)

    @property
    def subcommentsCount(self) -> int:
        """Returns the count of subcomments for the comment."""
        return self.data.get("subcommentsCount", 0)

    @property
    def type(self) -> int:
        """Returns the type of the comment."""
        return self.data.get("type", 0)

    @property
    def votedValue(self) -> int:
        """Returns the voted value of the comment."""
        return self.data.get("votedValue", 0)

    @property
    def votesSum(self) -> int:
        """Returns the sum of votes for the comment."""
        return self.data.get("votesSum", 0)

    def json(self) -> dict[str, Any]:
        """Returns the raw data of the comment."""
        return self.data


class CommentList:
    """
    Represents a list of comments retrieved from an API response.

    :param data: The raw data of the comment list.
    :type data: dict
    """

    def __init__(self, data: Union[list[dict[str, Any]], dict[str, Any]]):
        if not isinstance(data, list):
            data = list(data.get("commentList", data) or [])
        self.data = data

    def __iter__(self) -> "Iterator[Comment]":
        """Iterator function to iterate over the comments in the comment list."""
        return (Comment(data) for data in self.data)

    @property
    def author(self) -> userprofile.UserProfileList:
        """Returns a list of authors of the comments in the comment list."""
        return userprofile.UserProfileList([comment.author for comment in self])

    @property
    def commentId(self) -> list[str]:
        """Returns a list of comment IDs in the comment list."""
        return [comment.commentId for comment in self]

    @property
    def content(self) -> list[Optional[str]]:
        """Returns a list of comment IDs in the comment list."""
        return [comment.content for comment in self]

    @property
    def createdTime(self) -> list[str]:
        """Returns a list of creation times of the comments in the comment list."""
        return [comment.createdTime for comment in self]

    @property
    def extensions(self) -> list[CommentExtensions]:
        """Returns a list of extensions of the comments in the comment list."""
        return [comment.extensions for comment in self]

    @property
    def mediaList(self) -> list[list[tuple[int, str]]]:
        """Returns a list of media lists of the comments in the comment list."""
        return [comment.mediaList for comment in self]

    @property
    def modifiedTime(self) -> list[Optional[str]]:
        """Returns a list of modification times of the comments in the comment list."""
        return [comment.modifiedTime for comment in self]

    @property
    def ndcId(self) -> list[int]:
        """Returns a list of NDC IDs of the comments in the comment list."""
        return [comment.comId for comment in self]

    @property
    def comId(self) -> list[int]:
        """Returns a list of NDC IDs of the comments in the comment list."""
        return [comment.comId for comment in self]

    @property
    def parentId(self) -> list[str]:
        """Returns a list of parent IDs of the comments in the comment list."""
        return [comment.parentId for comment in self]

    @property
    def parentNdcId(self) -> list[int]:
        """Returns a list of parent NDC IDs of the comments in the comment list."""
        return [comment.parentNdcId for comment in self]

    @property
    def parentComId(self) -> list[int]:
        """Returns a list of parent community IDs of the comments in the comment list."""
        return [comment.parentComId for comment in self]

    @property
    def parentType(self) -> list[int]:
        """Returns a list of parent types of the comments in the comment list."""
        return [comment.parentType for comment in self]

    @property
    def subcommentsCount(self) -> list[int]:
        """Returns a list of subcomment counts for the comments in the comment list."""
        return [comment.subcommentsCount for comment in self]

    @property
    def type(self) -> list[int]:
        """Returns a list of types of the comments in the comment list."""
        return [comment.type for comment in self]

    @property
    def votedValue(self) -> list[int]:
        """Returns a list of voted values of the comments in the comment list."""
        return [comment.votedValue for comment in self]

    @property
    def votesSum(self) -> list[int]:
        """Returns a list of vote sums for the comments in the comment list."""
        return [comment.votesSum for comment in self]

    def json(self) -> list[dict[str, Any]]:
        """Returns the raw data of the comment list."""
        return self.data

from typing import Union
from . import UserProfileList


class CommentStickerCollectionSummary:
    def __init__(self, data: dict):
        try:
            self.data = data.get("stickerCollectionSummary", {})
        except AttributeError:
            self.data = None


    def _check_stickerCollectionSummary(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper


    @property
    @_check_stickerCollectionSummary
    def status(self) -> int:
        """
        Returns the status of the sticker collection summary.
        """
        return self.data.get("status", 0)


    @property
    @_check_stickerCollectionSummary
    def collectionType(self) -> int:
        """
        Returns the collection type of the sticker collection summary.
        """
        return self.data.get("collectionType", 0)


    @property
    @_check_stickerCollectionSummary
    def userId(self) -> str:
        """
        Returns the userId of the sticker collection summary.
        """
        return self.data.get("uid", "")


    @property
    @_check_stickerCollectionSummary
    def modifiedTime(self) -> str:
        """
        Returns the modified time of the sticker collection summary.
        """
        return self.data.get("modifiedTime", "")


    @property
    @_check_stickerCollectionSummary
    def bannerUrl(self) -> str:
        """
        Returns the banner URL of the sticker collection summary.
        """
        return self.data.get("bannerUrl", "")


    @property
    @_check_stickerCollectionSummary
    def smallIcon(self) -> str:
        """
        Returns the small icon of the sticker collection summary.
        """
        return self.data.get("smallIcon", "")


    @property
    @_check_stickerCollectionSummary
    def stickersCount(self) -> int:
        """
        Returns the sticker count of the sticker collection summary.
        """
        return self.data.get("stickersCount", 0)


    @property
    @_check_stickerCollectionSummary
    def usedCount(self) -> int:
        """
        Returns the used count of the sticker collection summary.
        """
        return self.data.get("usedCount", 0)


    @property
    @_check_stickerCollectionSummary
    def icon(self) -> str:
        """
        Returns the icon of the sticker collection summary.
        """
        return self.data.get("icon", "")


    @property
    @_check_stickerCollectionSummary
    def name(self) -> str:
        """
        Returns the name of the sticker collection summary.
        """
        return self.data.get("name", "")


    @property
    @_check_stickerCollectionSummary
    def collectionId(self) -> str:
        """
        Returns the collection ID of the sticker collection summary.
        """
        return self.data.get("collectionId", "")


    @property
    @_check_stickerCollectionSummary
    def createdTime(self) -> str:
        """
        Returns the created time of the sticker collection summary.
        """
        return self.data.get("createdTime", "")


class CommentSticker:
    def __init__(self, data: dict):
        try:
            self.data = data.get("sticker", {})
        except AttributeError:
            self.data = None


    def _check_sticker(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper


    @property
    @_check_sticker
    def status(self) -> int:
        """
        Returns the status of the sticker.
        """
        return self.data.get("status", 0)
    
    @property
    @_check_sticker
    def iconV2(self) -> str:
        """
        Returns the icon of the sticker.
        """
        return self.data.get("iconV2", "")
    
    @property
    @_check_sticker
    def name(self) -> str:
        """
        Returns the name of the sticker.
        """
        return self.data.get("name", "")
    
    @property
    @_check_sticker
    def stickerId(self) -> str:
        """
        Returns the ID of the sticker.
        """
        return self.data.get("stickerId", "")
    
    @property
    @_check_sticker
    def icon_url(self) -> str:
        """
        Returns the icon URL of the sticker.
        """
        return self.data.get("icon", "")
    
    @property
    @_check_sticker
    def smallIconV2(self) -> str:
        """
        Returns the small icon of the sticker.
        """
        return self.data.get("smallIconV2", "")
    
    @property
    @_check_sticker
    def smallIcon(self) -> str:
        """
        Returns the small icon of the sticker.
        """
        return self.data.get("smallIcon", "")
    
    @property
    @_check_sticker
    def stickerCollectionId(self) -> str:
        """
        Returns the sticker collection ID of the sticker.
        """
        return self.data.get("stickerCollectionId", "")
    
    @property
    @_check_sticker
    def mediumIcon(self) -> str:
        """
        Returns the medium icon of the sticker.
        """
        return self.data.get("mediumIcon", "")
    
    @property
    @_check_sticker
    def stickerCollectionSummary(self) -> CommentStickerCollectionSummary:
        """
        Returns the sticker collection summary of the sticker.
        """
        return CommentStickerCollectionSummary(self.data)


class CommentExtensions:
    def __init__(self, data: dict):
        try:
            self.data = data
        except AttributeError:
            self.data = None


    def _check_commentExtensions(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper


    @property
    @_check_commentExtensions
    def sticker(self) -> CommentSticker:
        """
        Returns the sticker of the comment.
        """
        return CommentSticker(self.data.get("sticker"))


    @property
    @_check_commentExtensions
    def stickerId(self) -> str:
        """
        Returns the sticker ID of the comment.
        """
        return self.data.get("stickerId")

    
class Comment:
    """
    Represents a comment object retrieved from an API response.

    :param data: The raw data of the comment.
    :type data: Union[dict, str]
    """
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data


    @property
    def author(self) -> dict:
        """
        Returns the author of the comment.
        """
        return self.data.get("author")


    @property
    def commentId(self) -> str:
        """
        Returns the ID of the comment.
        """
        return self.data.get("commentId")


    @property
    def content(self) -> str:
        """
        Returns the content of the comment.
        """
        return self.data.get("content")


    @property
    def createdTime(self) -> str:
        """
        Returns the creation time of the comment.
        """
        return self.data.get("createdTime")


    @property
    def extensions(self) -> CommentExtensions:
        """
        Returns the extensions of the comment.
        """
        return CommentExtensions(self.data.get("extensions", {}))


    @property
    def modifiedTime(self) -> str:
        """
        Returns the modification time of the comment.
        """
        return self.data.get("modifiedTime")


    @property
    def comId(self) -> str:
        """
        Returns the community ID of the comment.
        """
        return self.data.get("ndcId")


    @property
    def objectId(self) -> str:
        """
        Returns the ID of the object the comment is on.
        """
        return self.data.get("parentId")


    @property
    def parentNdcId(self) -> str:
        """
        Returns the NDC ID of the parent comment.
        """
        return self.data.get("parentNdcId")


    @property
    def parentType(self) -> str:
        """
        Returns the type of the parent comment.
        """
        return self.data.get("parentType")


    @property
    def subcommentsCount(self) -> int:
        """
        Returns the count of subcomments for the comment.
        """
        return self.data.get("subcommentsCount")


    @property
    def type(self) -> str:
        """
        Returns the type of the comment.
        """
        return self.data.get("type")


    @property
    def votedValue(self) -> int:
        """
        Returns the voted value of the comment.
        """
        return self.data.get("votedValue")


    @property
    def votesSum(self) -> int:
        """
        Returns the sum of votes for the comment.
        """
        return self.data.get("votesSum")


    def json(self) -> Union[dict, str]:
        """
        Returns the raw data of the comment.
        """
        return self.data


class CommentList:
    """
    Represents a list of comments retrieved from an API response.

    :param data: The raw data of the comment list.
    :type data: dict
    """
    def __init__(self, data: dict):
        self.data = data


    def __iterator__(self):
        """
        Iterator function to iterate over the comments in the comment list.
        """
        for comment in self.data.get("commentList"):
            yield Comment(comment)


    @property
    def author(self) -> UserProfileList:
        """
        Returns a list of authors of the comments in the comment list.
        """
        return UserProfileList([comment.author for comment in self.__iterator__()])


    @property
    def commentId(self) -> list:
        """
        Returns a list of comment IDs in the comment list.
        """
        return [comment.commentId for comment in self.__iterator__()]


    @property
    def content(self) -> list:
        """
        Returns a list of contents of the comments in the comment list.
        """
        return [comment.content for comment in self.__iterator__()]


    @property
    def createdTime(self) -> list:
        """
        Returns a list of creation times of the comments in the comment list.
        """
        return [comment.createdTime for comment in self.__iterator__()]


    @property
    def extensions(self) -> list:
        """
        Returns a list of extensions of the comments in the comment list.
        """
        return [comment.extensions for comment in self.__iterator__()]


    @property
    def mediaList(self) -> list:
        """
        Returns a list of media lists of the comments in the comment list.
        """
        return [comment.mediaList for comment in self.__iterator__()]


    @property
    def modifiedTime(self) -> list:
        """
        Returns a list of modification times of the comments in the comment list.
        """
        return [comment.modifiedTime for comment in self.__iterator__()]


    @property
    def ndcId(self) -> list:
        """
        Returns a list of NDC IDs of the comments in the comment list.
        """
        return [comment.comId for comment in self.__iterator__()]


    @property
    def parentId(self) -> list:
        """
        Returns a list of parent IDs of the comments in the comment list.
        """
        return [comment.objectId for comment in self.__iterator__()]


    @property
    def parentNdcId(self) -> list:
        """
        Returns a list of parent NDC IDs of the comments in the comment list.
        """
        return [comment.parentNdcId for comment in self.__iterator__()]


    @property
    def parentType(self) -> list:
        """
        Returns a list of parent types of the comments in the comment list.
        """
        return [comment.parentType for comment in self.__iterator__()]


    @property
    def subcommentsCount(self) -> list:
        """
        Returns a list of subcomment counts for the comments in the comment list.
        """
        return [comment.subcommentsCount for comment in self.__iterator__()]


    @property
    def type(self) -> list:
        """
        Returns a list of types of the comments in the comment list.
        """
        return [comment.type for comment in self.__iterator__()]


    @property
    def votedValue(self) -> list:
        """
        Returns a list of voted values of the comments in the comment list.
        """
        return [comment.votedValue for comment in self.__iterator__()]


    @property
    def votesSum(self) -> list:
        """
        Returns a list of vote sums for the comments in the comment list.
        """
        return [comment.votesSum for comment in self.__iterator__()]


    def json(self) -> Union[dict, str]:
        """
        Returns the raw data of the comment list.
        """
        return self.data
from collections.abc import Iterator
from typing import Any, Literal, Optional, Union, cast

__all__ = (
    "AvatarFrame",
    "CustomTitle",
    "FollowerList",
    "InfluencerInfo",
    "MoodSticker",
    "OnlineMembers",
    "Pagging",
    "UserExtensions",
    "UserProfile",
    "UserProfileList",
)


class AvatarFrame:
    """Class representing a avatar frame"""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.frame_id)

    @property
    def status(self) -> int:
        """The status of the request."""
        return self.data.get("status", 0)

    @property
    def ownership_status(self) -> int:
        """The ownership status of the avatar frame."""
        return self.data.get("ownershipStatus", 0)

    @property
    def version(self) -> int:
        """The version of the avatar frame."""
        return self.data.get("version", 0)

    @property
    def resource_url(self) -> str:
        """The resource url of the avatar frame."""
        return self.data.get("resourceUrl", "")

    @property
    def name(self) -> str:
        """The name of the avatar frame."""
        return self.data.get("name", "")

    @property
    def icon(self) -> str:
        """The icon of the avatar frame."""
        return self.data.get("icon", "")

    @property
    def frame_type(self) -> int:
        """The frame type of the avatar frame."""
        return self.data.get("frameType", 0)

    @property
    def frame_id(self) -> str:
        """The frame id of the avatar frame."""
        return self.data.get("frameId", "")


class InfluencerInfo:
    """Class representing a influencer info."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.monthly_fee)

    @property
    def pinned(self) -> bool:
        """The pinned status of the influencer."""
        return self.data.get("pinned", False)

    @property
    def created_time(self) -> int:
        """The influencer created time."""
        return self.data.get("createdTime", "")

    @property
    def fans_count(self) -> int:
        """The fans count of the of the influencer."""
        return self.data.get("fansCount", 0)

    @property
    def monthly_fee(self) -> int:
        """The monthly fee of the influencer."""
        return self.data.get("monthlyFee", 0)


class CustomTitle:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.title)

    @property
    def color(self) -> Optional[str]:
        return self.data.get("color")

    @property
    def title(self) -> str:
        return self.data.get("title", "")


class UserExtensions:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.data)

    @property
    def privilege_of_comment_on_user_profile(self) -> Literal[1, 2, 3]:
        return self.data.get("privilegeOfCommentOnUserProfile") or 1

    @property
    def style(self) -> dict[str, Any]:
        return self.data.get("style", {})

    @property
    def title_names(self) -> list[str]:
        return [title["title"] for title in self.titles]

    @property
    def title_colors(self) -> list[str]:
        return [title["color"] for title in self.titles]

    @property
    def titles(self) -> list[dict[str, Any]]:
        return self.data.get("customTitles") or []

    @property
    def privilege_of_chat_invite_request(self) -> Literal[1, 2, 3]:
        return self.data.get("privilegeOfChatInviteRequest") or 1

    @property
    def is_user_hidden(self) -> bool:
        """Whether the user is hidden."""
        return self.data.get("hideUserProfile", False)

    @property
    def is_user_banned(self) -> bool:
        """Whether the user is banned."""
        return bool(self.data.get("__disabledTime__", False))


class MoodSticker:
    """Mood sticker the user has set."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.sticker_id)

    @property
    def status(self) -> int:
        """Is the status of request."""
        return self.data.get("status", 0)

    @property
    def icon_v2(self) -> str:
        """The icon v2 of the mood sticker."""
        return self.data.get("iconV2", "")

    @property
    def name(self) -> str:
        """The name of the mood sticker."""
        return self.data.get("name", "")

    @property
    def sticker_id(self) -> str:
        """The sticker id of the mood sticker."""
        return self.data.get("stickerId", "")

    @property
    def small_icon_v2(self) -> str:
        """The small icon v2 of the mood sticker."""
        return self.data.get("smallIconV2", "")

    @property
    def small_icon(self) -> str:
        """The small icon of the mood sticker."""
        return self.data.get("smallIcon", "")

    @property
    def sticker_collection_id(self) -> str:
        """The sticker collection id of the mood sticker."""
        return self.data.get("stickerCollectionId", "")

    @property
    def medium_icon(self) -> str:
        """The medium icon of the mood sticker."""
        return self.data.get("mediumIcon", "")

    @property
    def extensions(self) -> dict[str, Any]:
        """The extensions of the mood sticker."""
        return self.data.get("extensions") or {}

    @property
    def used_count(self) -> int:
        """The used count of the mood sticker."""
        return self.data.get("usedCount", 0)

    @property
    def medium_icon_v2(self) -> str:
        """The medium icon v2 of the mood sticker."""
        return self.data.get("mediumIconV2", "")

    @property
    def created_time(self) -> int:
        """The created time of the mood sticker."""
        return self.data.get("createdTime", "")

    @property
    def icon(self) -> str:
        """The icon of the mood sticker."""
        return self.data.get("icon", "")


class UserProfile:
    """Class representing a user profile."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("userProfile", data) or {}

    def __bool__(self) -> bool:
        return bool(self.uid)

    @property
    def status(self) -> int:
        """is the status of request."""
        return self.data.get("status", 0)

    @property
    def mood_sticker(self) -> MoodSticker:
        """Mood sticker the user has set."""
        return MoodSticker(self.data.get("moodSticker") or {})

    @property
    def wiki_count(self) -> int:
        """The amount of wiki the user has created."""
        return self.data.get("itemsCount", 0)

    @property
    def consecutive_check_in_days(self) -> int:
        """The amount of consecutive days the user has checked in."""
        return self.data.get("consecutiveCheckInDays", 0)

    @property
    def uid(self) -> str:
        """The user's uid."""
        return self.data.get("uid", "")

    @property
    def userId(self) -> str:
        """The user's uid."""
        return self.uid

    @property
    def aminoId(self) -> str:
        """The user's amino id."""
        return self.data.get("aminoId", "")

    @property
    def modified_time(self) -> Optional[str]:
        """The time the user's profile was last modified."""
        return self.data.get("modifiedTime")

    @property
    def following_status(self) -> int:
        """Whether the user is following the current user."""
        return self.data.get("followingStatus", 0)

    @property
    def online_status(self) -> Literal[1, 2]:
        """The user's online status."""
        return self.data.get("onlineStatus") or 2

    @property
    def account_membership_status(self) -> int:
        """The user's account membership status."""
        return self.data.get("accountMembershipStatus", 0)

    @property
    def is_global(self) -> bool:
        """Whether the user is a global user."""
        return self.data.get("isGlobal", False)

    @property
    def avatar_frame_id(self) -> Optional[str]:
        """The user's avatar frame id."""
        return self.data.get("avatarFrameId")

    @property
    def fan_club_list(self) -> list[dict[str, Any]]:
        """The user's fan club list."""
        return self.data.get("fanClubList", [])

    @property
    def reputation(self) -> int:
        """The user's reputation."""
        return self.data.get("reputation", 0)

    @property
    def posts_count(self) -> int:
        """The amount of posts the user has created."""
        return self.data.get("postsCount", 0)

    @property
    def avatar_frame(self) -> AvatarFrame:
        """The user's avatar frame."""
        return AvatarFrame(self.data.get("avatarFrame") or {})

    @property
    def follower_count(self) -> int:
        """The amount of followers the user has."""
        return self.data.get("membersCount", 0)

    @property
    def nickname(self) -> str:
        """The user's nickname."""
        return self.data.get("nickname", "")

    @property
    def username(self) -> str:
        """The user's username."""
        return self.nickname

    @property
    def media_list(self) -> list[tuple[int, str, Optional[str], Optional[str]]]:
        """The user's media list."""
        return [
            (
                m[0],
                m[1],
                m[2] if len(m) > 2 else None,
                m[3] if len(m) > 3 else None,
            )
            for m in cast(list[Any], self.data.get("mediaList") or [])
        ]

    @property
    def icon(self) -> Optional[str]:
        """The user's icon."""
        return self.data.get("icon")

    @property
    def avatar(self) -> Optional[str]:
        """The user's avatar."""
        return self.icon

    @property
    def is_nickname_verified(self) -> bool:
        """The user's nickname verification status."""
        return self.data.get("isNicknameVerified", False)

    @property
    def mood(self) -> Optional[str]:
        """The user's mood."""
        return self.data.get("mood")

    @property
    def level(self) -> int:
        """The user's level."""
        return self.data.get("level", 0)

    @property
    def push_enabled(self) -> bool:
        """The user's push notification status."""
        return self.data.get("pushEnabled", False)

    @property
    def membership_status(self) -> int:
        """The user's membership status."""
        return self.data.get("membershipStatus", 0)

    @property
    def influencer_info(self) -> InfluencerInfo:
        """The user's influencer info."""
        return InfluencerInfo(self.data.get("influencerInfo") or {})

    @property
    def content(self) -> Optional[str]:
        """The user's profile content."""
        return self.data.get("content")

    @property
    def following_count(self) -> int:
        """The amount of users the user is following."""
        return self.data.get("joinedCount", 0)

    @property
    def role(self) -> int:
        """The user's role."""
        return self.data.get("role", 0)

    @property
    def comments_count(self) -> int:
        """The amount of comments the user has on their wall."""
        return self.data.get("commentsCount", 0)

    @property
    def ndcId(self) -> Optional[int]:
        """The community the user is in."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> Optional[int]:
        """The community the user is in."""
        return self.ndcId

    @property
    def created_time(self) -> str:
        """The time the user was created."""
        return self.data.get("createdTime", "")

    @property
    def is_user_hidden(self) -> bool:
        """Whether the user is hidden."""
        return self.extensions.is_user_hidden

    @property
    def is_user_banned(self) -> bool:
        """Whether the user is banned."""
        return self.extensions.is_user_banned

    @property
    def extensions(self) -> UserExtensions:
        """Whether the user is hidden."""
        return UserExtensions(self.data.get("extensions") or {})

    @property
    def visit_privacy(self) -> int:
        """The user's visit privacy."""
        return self.data.get("visitPrivacy", 0)

    @property
    def stories_count(self) -> int:
        """The amount of stories the user has."""
        return self.data.get("storiesCount", 0)

    @property
    def blogs_count(self) -> int:
        """The amount of blogs the user has."""
        return self.data.get("blogsCount", 0)

    def json(self) -> dict[str, Any]:
        """The json response from the api."""
        return self.data


class OnlineMembers:
    """The online members of a community."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data.get("o", data)
        self._user: dict[str, Any] = self.data.get("userProfileList")[0]

    def __bool__(self) -> bool:
        return bool(self.users_online)

    @property
    def topic(self) -> str:
        """The community's topic."""
        return self.data.get("topic", "")

    @property
    def ndcId(self) -> int:
        """The community's id."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        """The community's id."""
        return self.ndcId

    @property
    def users_online(self) -> int:
        """The amount of users online."""
        return self.data.get("userProfileCount", 0)

    @property
    def is_guest(self) -> bool:
        """If the user is a guest."""
        return self._user.get("isGuest", False)

    @property
    def uid(self) -> str:
        """The user's id."""
        return self._user.get("uid", "")

    @property
    def userId(self) -> str:
        """The user's id."""
        return self.uid

    @property
    def status(self) -> int:
        """The user's status."""
        return self._user.get("status", 0)

    @property
    def icon(self) -> str:
        """The user's icon."""
        return self._user.get("icon", "")

    @property
    def avatar(self) -> str:
        """The user's icon."""
        return self.icon

    @property
    def reputation(self) -> int:
        """The user's reputation."""
        return self._user.get("reputation", 0)

    @property
    def role(self) -> int:
        """The user's role."""
        return self._user.get("role", 0)

    @property
    def nickname(self) -> str:
        """The user's nickname."""
        return self._user.get("nickname", "")

    @property
    def username(self) -> str:
        """The user's nickname."""
        return self.nickname

    @property
    def level(self) -> int:
        """The user's level."""
        return self._user.get("level", 0)

    @property
    def extensions(self) -> UserExtensions:
        """The user's extensions."""
        return UserExtensions(self._user.get("extensions") or {})

    @property
    def account_membership_status(self) -> str:
        """The user's account membership status."""
        return self._user.get("accountMembershipStatus", 0)

    @property
    def avatar_frame_id(self) -> Optional[str]:
        """The user's avatar frame id."""
        return self._user.get("avatarFrameId")

    @property
    def avatar_frame(self) -> AvatarFrame:
        """The user's avatar frame."""
        return AvatarFrame(self._user.get("avatarFrame") or {})

    @property
    def is_nickname_verified(self) -> bool:
        """If the user's nickname is verified."""
        return self._user.get("isNicknameVerified", False)

    def json(self) -> dict[str, Any]:
        """Api response in json format."""
        return self.data


class UserProfileList:
    def __init__(self, data: Union[dict[str, Any], list[dict[str, Any]]]) -> None:
        self.data: list[dict[str, Any]] = (
            (data.get("userProfileList") or []) if isinstance(data, dict) else data
        )

    def __bool__(self) -> bool:
        return bool(self.data)

    def __iter__(self) -> Iterator[UserProfile]:
        return (UserProfile(data) for data in self.data)

    @property
    def status(self) -> list[int]:
        return [x.status for x in self]

    @property
    def mood_sticker(self) -> list[MoodSticker]:
        return [x.mood_sticker for x in self]

    @property
    def wiki_count(self) -> list[int]:
        return [x.wiki_count for x in self]

    @property
    def consecutive_check_in_days(self) -> list[int]:
        return [x.consecutive_check_in_days for x in self]

    @property
    def uid(self) -> list[str]:
        return [x.uid for x in self]

    @property
    def userId(self) -> list[str]:
        return self.uid

    @property
    def modified_time(self) -> list[Optional[str]]:
        return [x.modified_time for x in self]

    @property
    def following_status(self) -> list[int]:
        return [x.following_status for x in self]

    @property
    def online_status(self) -> list[int]:
        return [x.online_status for x in self]

    @property
    def account_membership_status(self) -> list[int]:
        return [x.account_membership_status for x in self]

    @property
    def is_global(self) -> list[bool]:
        return [x.is_global for x in self]

    @property
    def avatar_frame_id(self) -> list[Optional[str]]:
        return [x.avatar_frame_id for x in self]

    @property
    def fan_club_list(self) -> list[list[dict[str, Any]]]:
        return [x.fan_club_list for x in self]

    @property
    def reputation(self) -> list[int]:
        return [x.reputation for x in self]

    @property
    def posts_count(self) -> list[int]:
        return [x.posts_count for x in self]

    @property
    def avatar_frame(self) -> list[AvatarFrame]:
        return [x.avatar_frame for x in self]

    @property
    def follower_count(self) -> list[int]:
        return [x.follower_count for x in self]

    @property
    def nickname(self) -> list[str]:
        return [x.nickname for x in self]

    @property
    def username(self) -> list[str]:
        return self.nickname

    @property
    def media_list(self) -> list[list[tuple[int, str, Optional[str], Optional[str]]]]:
        return [x.media_list for x in self]

    @property
    def icon(self) -> list[Optional[str]]:
        return [x.icon for x in self]

    @property
    def avatar(self) -> list[Optional[str]]:
        return self.icon

    @property
    def is_nickname_verified(self) -> list[bool]:
        return [x.is_nickname_verified for x in self]

    @property
    def mood(self) -> list[Optional[str]]:
        return [x.mood for x in self]

    @property
    def level(self) -> list[int]:
        return [x.level for x in self]

    @property
    def pushEnabled(self) -> list[bool]:
        return [x.push_enabled for x in self]

    @property
    def membership_status(self) -> list[int]:
        return [x.membership_status for x in self]

    @property
    def influencer_info(self) -> list[InfluencerInfo]:
        return [x.influencer_info for x in self]

    @property
    def content(self) -> list[Optional[str]]:
        return [x.content for x in self]

    @property
    def following_count(self) -> list[int]:
        return [x.following_count for x in self]

    @property
    def role(self) -> list[int]:
        return [x.role for x in self]

    @property
    def comments_count(self) -> list[int]:
        return [x.comments_count for x in self]

    @property
    def ndcId(self) -> list[Optional[int]]:
        return [x.ndcId for x in self]

    @property
    def comId(self) -> list[Optional[int]]:
        return self.ndcId

    @property
    def created_time(self) -> list[str]:
        return [x.created_time for x in self]

    @property
    def extensions(self) -> list[UserExtensions]:
        return [x.extensions for x in self]

    @property
    def visit_privacy(self) -> list[int]:
        return [x.visit_privacy for x in self]

    @property
    def stories_count(self) -> list[int]:
        return [x.stories_count for x in self]

    @property
    def blogs_count(self) -> list[int]:
        return [x.blogs_count for x in self]


class Pagging:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("paging", data) or {}

    def __bool__(self) -> bool:
        return bool(self.data)

    @property
    def prev_page_token(self) -> Optional[str]:
        return self.data.get("prevPageToken")

    @property
    def next_page_token(self) -> Optional[str]:
        return self.data.get("nextPageToken")

    def json(self) -> dict[str, Any]:
        return self.data


class FollowerList:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.data)

    @property
    def paging(self) -> Pagging:
        return Pagging(self.data.get("paging") or {})

    @property
    def members(self) -> UserProfileList:
        return UserProfileList(self.data.get("userProfileList") or [])

    def json(self) -> dict[str, Any]:
        return self.data

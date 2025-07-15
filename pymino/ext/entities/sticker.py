from collections.abc import Iterator
from typing import Any, Dict, List, Optional, Union

__all__ = (
    "CommunitySticker",
    "CommunityStickerList",
    "OriginalCommunity",
    "Sticker",
    "StickerAuthor",
    "StickerExtensions",
    "StickerList",
)


class StickerAuthor:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.uid)

    @property
    def is_global(self) -> bool:
        """Returns True if the author is global, False if not."""
        return self.data.get("isGlobal", False)

    @property
    def comId(self) -> int:
        """Returns the author's community ID."""
        return self.data.get("ndcId", 0)

    @property
    def role(self) -> int:
        """Returns the author's role."""
        return self.data.get("role", 0)

    @property
    def is_nickname_verified(self) -> bool:
        """Returns True if the author's nickname is verified, False if not."""
        return self.data.get("isNicknameVerified", False)

    @property
    def following_status(self) -> int:
        """Returns the author's following status."""
        return self.data.get("followingStatus", 0)

    @property
    def followers(self) -> int:
        """Returns the author's follower count."""
        return self.data.get("membersCount", 0)

    @property
    def membership_status(self) -> int:
        """Returns the author's membership status."""
        return self.data.get("membershipStatus", 0)

    @property
    def status(self) -> int:
        """Returns the author's status."""
        return self.data.get("status", 0)

    @property
    def account_membership_status(self) -> int:
        """Returns the author's account membership status."""
        return self.data.get("accountMembershipStatus", 0)

    @property
    def reputation(self) -> int:
        """Returns the author's reputation."""
        return self.data.get("reputation", 0)

    @property
    def level(self) -> int:
        """Returns the author's level."""
        return self.data.get("level", 0)

    @property
    def icon(self) -> Optional[str]:
        """Returns the author's icon."""
        return self.data.get("icon")

    @property
    def uid(self) -> str:
        """Returns the author's UID."""
        return self.data.get("uid", "")

    @property
    def nickname(self) -> str:
        """Returns the author's nickname."""
        return self.data.get("nickname", "")

    def json(self) -> Dict[str, Any]:
        """Returns the author's data as a dictionary."""
        return self.data


class OriginalCommunity:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.comId)

    @property
    def status(self) -> int:
        """Returns the community's status."""
        return self.data.get("status", 0)

    @property
    def icon(self) -> str:
        """Returns the community's icon."""
        return self.data.get("icon", "")

    @property
    def endpoint(self) -> str:
        """Returns the community's endpoint."""
        return self.data.get("endpoint", "")

    @property
    def name(self) -> str:
        """Returns the community's name."""
        return self.data.get("name", "")

    @property
    def comId(self) -> int:
        """Returns the community's ndc id."""
        return self.data.get("ndcId", 0)

    def json(self) -> Dict[str, Any]:
        """Returns the community's json."""
        return self.data


class StickerExtensions:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.data)

    @property
    def icon_source_sticker_id(self) -> str:
        """Returns the sticker's icon source sticker id."""
        return self.data.get("iconSourceStickerId", "")

    @property
    def original_author(self) -> StickerAuthor:
        """Returns the sticker's original author."""
        return StickerAuthor(self.data.get("originalAuthor") or {})

    @property
    def original_community(self) -> OriginalCommunity:
        """Returns the sticker's original community."""
        return OriginalCommunity(self.data.get("originalCommunity") or {})

    def json(self) -> Dict[str, Any]:
        """Returns the sticker's extensions as a dictionary."""
        return self.data


class Sticker:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.created_time)

    @property
    def ref_object_type(self) -> int:
        """Returns the sticker's reference object type."""
        return self.data.get("refObjectType", 0)

    @property
    def ref_object_id(self) -> str:
        """Returns the sticker's reference object ID."""
        return self.data.get("refObjectId", "")

    @property
    def created_time(self) -> str:
        """Returns the sticker's creation time."""
        return self.data.get("createdTime", "")

    @property
    def item_basic_info(self) -> Dict[str, Any]:
        """Returns the sticker's basic info."""
        return self.data.get("itemBasicInfo") or {}

    @property
    def icon(self) -> str:
        """Returns the sticker's icon."""
        return self.item_basic_info.get("icon", "")

    @property
    def name(self) -> str:
        """Returns the sticker's name."""
        return self.item_basic_info.get("name", "")

    @property
    def item_restriction_info(self) -> Dict[str, Any]:
        """Returns the sticker's restriction info."""
        return self.data.get("itemRestrictionInfo") or {}

    @property
    def discount_value(self) -> Union[int, None]:
        """Returns the sticker's discount value."""
        return self.item_restriction_info.get("discountValue")

    @property
    def discount_status(self) -> int:
        """Returns the sticker's discount status."""
        return self.item_restriction_info.get("discountStatus", 0)

    @property
    def owner_uid(self) -> Optional[str]:
        """Returns the sticker's owner UID."""
        return self.item_restriction_info.get("ownerUid")

    @property
    def owner_type(self) -> int:
        """Returns the sticker's owner type."""
        return self.item_restriction_info.get("ownerType", 0)

    @property
    def restrict_type(self) -> int:
        """Returns the sticker's restriction type."""
        return self.item_restriction_info.get("restrictType", 0)

    @property
    def restrict_value(self) -> Optional[int]:
        """Returns the sticker's restriction value."""
        return self.item_restriction_info.get("restrictValue")

    @property
    def available_duration(self) -> Optional[int]:
        """Returns the sticker's available duration."""
        return self.item_restriction_info.get("availableDuration")

    @property
    def ref_object(self) -> Dict[str, Any]:
        """Returns the sticker's reference object."""
        return self.data.get("refObject") or {}

    @property
    def modified_time(self) -> Optional[str]:
        """Returns the sticker's modification time."""
        return self.ref_object.get("modifiedTime")

    @property
    def ownership_status(self) -> Optional[int]:
        """Returns the sticker's ownership status."""
        return self.ref_object.get("ownershipStatus")

    @property
    def is_owned(self) -> bool:
        """Returns the sticker list's ownership status."""
        return self.ref_object.get("isOwned", False)

    @property
    def used_count(self) -> int:
        """Returns the sticker's used count."""
        return self.ref_object.get("usedCount", 0)

    @property
    def extensions(self) -> Dict[str, Any]:
        """Returns the sticker's extensions."""
        return self.ref_object.get("extensions") or {}

    @property
    def available_community_ids(self) -> List[int]:
        """Returns the sticker's available community IDs."""
        return self.ref_object.get("availableNdcIds") or []

    @property
    def status(self) -> int:
        """Returns the sticker's status."""
        return self.ref_object.get("status", 0)

    @property
    def author(self) -> StickerAuthor:
        """Returns the sticker's author."""
        return StickerAuthor(self.ref_object.get("author") or {})

    @property
    def is_new(self) -> bool:
        """Returns the sticker's new status."""
        return self.ref_object.get("isNew", False)

    @property
    def stickers_count(self) -> int:
        """Returns the sticker's count."""
        return self.ref_object.get("stickersCount", 0)

    @property
    def restriction_info(self) -> Dict[str, Any]:
        """Returns the sticker's restriction info."""
        return self.ref_object.get("restrictionInfo") or {}

    @property
    def collection_id(self) -> Optional[str]:
        """Returns the sticker's collection ID."""
        return self.ref_object.get("collectionId")

    @property
    def is_activated(self) -> bool:
        """Returns the sticker's activation status."""
        return self.ref_object.get("isActivated", False)

    @property
    def collection_type(self) -> int:
        """Returns the sticker's collection type."""
        return self.ref_object.get("collectionType", 0)

    @property
    def uid(self) -> Optional[str]:
        """Returns the sticker's UID."""
        return self.ref_object.get("uid")

    @property
    def small_icon(self) -> str:
        """Returns the sticker's small icon."""
        return self.ref_object.get("smallIcon", "")

    @property
    def description(self) -> Optional[str]:
        """Returns the sticker's description."""
        return self.ref_object.get("description")

    @property
    def is_globally_available(self) -> bool:
        """Returns the sticker's global availability status."""
        return self.ref_object.get("isGloballyAvailable", False)

    @property
    def banner_url(self) -> str:
        """Returns the sticker's banner URL."""
        return self.ref_object.get("bannerUrl", "")

    def json(self) -> Dict[str, Any]:
        """Returns the sticker's data in JSON format."""
        return self.data


class StickerList:
    def __init__(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]):
        if isinstance(data, dict):
            data = list(data.get("storeItemList") or [])
        self.data = data

    def __iter__(self) -> "Iterator[Sticker]":
        return (Sticker(sticker) for sticker in self.data)

    @property
    def ref_object_type(self) -> List[int]:
        """Returns the sticker list's ref object type."""
        return [sticker.ref_object_type for sticker in self]

    @property
    def ref_object_id(self) -> List[str]:
        """Returns the sticker list's ref object ID."""
        return [sticker.ref_object_id for sticker in self]

    @property
    def created_time(self) -> List[str]:
        """Returns the sticker list's creation time."""
        return [sticker.created_time for sticker in self]

    @property
    def item_basic_info(self) -> List[Dict[str, Any]]:
        """Returns the sticker list's basic info."""
        return [sticker.item_basic_info for sticker in self]

    @property
    def icon(self) -> List[str]:
        """Returns the sticker list's icon."""
        return [sticker.icon for sticker in self]

    @property
    def name(self) -> List[str]:
        """Returns the sticker list's name."""
        return [sticker.name for sticker in self]

    @property
    def item_restriction_info(self) -> List[Dict[str, Any]]:
        """Returns the sticker list's restriction info."""
        return [sticker.item_restriction_info for sticker in self]

    @property
    def discount_value(self) -> List[Optional[int]]:
        """Returns the sticker list's discount value."""
        return [sticker.discount_value for sticker in self]

    @property
    def discount_status(self) -> List[int]:
        """Returns the sticker list's discount status."""
        return [sticker.discount_status for sticker in self]

    @property
    def owner_uid(self) -> List[Optional[str]]:
        """Returns the sticker list's owner UID."""
        return [sticker.owner_uid for sticker in self]

    @property
    def owner_type(self) -> List[int]:
        """Returns the sticker list's owner type."""
        return [sticker.owner_type for sticker in self]

    @property
    def restrict_type(self) -> List[int]:
        """Returns the sticker list's restrict type."""
        return [sticker.restrict_type for sticker in self]

    @property
    def restrict_value(self) -> List[Optional[int]]:
        """Returns the sticker list's restrict value."""
        return [sticker.restrict_value for sticker in self]

    @property
    def available_duration(self) -> List[Optional[int]]:
        """Returns the sticker list's available duration."""
        return [sticker.available_duration for sticker in self]

    @property
    def ownership_status(self) -> List[Optional[int]]:
        """Returns the sticker list's ownership status."""
        return [sticker.ownership_status for sticker in self]

    @property
    def is_owned(self) -> List[bool]:
        """Returns the sticker list's ownership status."""
        return [sticker.is_owned for sticker in self]

    @property
    def is_new(self) -> List[bool]:
        """Returns the sticker list's new status."""
        return [sticker.is_new for sticker in self]

    @property
    def is_activated(self) -> List[bool]:
        """Returns the sticker list's activation status."""
        return [sticker.is_activated for sticker in self]

    @property
    def collection_id(self) -> List[Optional[str]]:
        """Returns the sticker list's collection ID."""
        return [sticker.collection_id for sticker in self]

    @property
    def collection_type(self) -> List[int]:
        """Returns the sticker list's collection type."""
        return [sticker.collection_type for sticker in self]

    @property
    def uid(self) -> List[Optional[str]]:
        """Returns the sticker list's UID."""
        return [sticker.uid for sticker in self]

    @property
    def small_icon(self) -> List[str]:
        """Returns the sticker list's small icon."""
        return [sticker.small_icon for sticker in self]

    @property
    def description(self) -> List[Optional[str]]:
        """Returns the sticker list's description."""
        return [sticker.description for sticker in self]

    @property
    def is_globally_available(self) -> List[bool]:
        """Returns the sticker list's global availability."""
        return [sticker.is_globally_available for sticker in self]

    @property
    def banner_url(self) -> List[str]:
        """Returns the sticker list's banner URL."""
        return [sticker.banner_url for sticker in self]

    def json(self) -> List[Dict[str, Any]]:
        """Returns the sticker list's JSON data."""
        return self.data


class CommunitySticker:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def status(self) -> int:
        """Returns the sticker's status."""
        return self.data.get("status", 0)

    @property
    def is_activated(self) -> bool:
        """Returns True if the sticker is activated, False otherwise."""
        return self.data.get("isActivated", False)

    @property
    def collection_type(self) -> int:
        """Returns the sticker's collection type."""
        return self.data.get("collectionType", 0)

    @property
    def is_new(self) -> bool:
        """Returns True if the sticker is new, False otherwise."""
        return self.data.get("isNew", False)

    @property
    def banner_url(self) -> str:
        """Returns the sticker's banner url."""
        return self.data.get("bannerUrl", "")

    @property
    def is_owned(self) -> bool:
        """Returns True if the sticker is owned, False otherwise."""
        return self.data.get("isOwned", False)

    @property
    def used_count(self) -> int:
        """Returns the sticker's used count."""
        return self.data.get("usedCount", False)

    @property
    def available_community_ids(self) -> List[int]:
        """Returns a list of available community ids."""
        return self.data.get("availableNdcIds") or []

    @property
    def icon(self) -> str:
        """Returns the sticker's icon url."""
        return self.data.get("icon", "")

    @property
    def name(self) -> str:
        """Returns the sticker's name."""
        return self.data.get("name", "")

    @property
    def collection_id(self) -> str:
        """Returns the sticker's collection id."""
        return self.data.get("collectionId", "")

    @property
    def description(self) -> Optional[str]:
        """Returns the sticker's description."""
        return self.data.get("description")

    @property
    def author(self) -> StickerAuthor:
        """Returns the sticker's author."""
        return StickerAuthor(self.data.get("author") or {})

    @property
    def ownership_info(self) -> Dict[str, Any]:
        """Returns the sticker's ownership info."""
        return self.data.get("ownershipInfo") or {}

    @property
    def is_auto_renew(self) -> bool:
        """Returns True if the sticker is auto renew, False otherwise."""
        return self.ownership_info.get("isAutoRenew", False)

    @property
    def expired_time(self) -> Optional[str]:
        """Returns the sticker's expired time."""
        return self.ownership_info.get("expiredTime")

    @property
    def extensions(self) -> StickerExtensions:
        """Returns the sticker's extensions."""
        return StickerExtensions(self.data.get("extensions") or {})

    @property
    def created_time(self) -> str:
        """Returns the sticker's created time."""
        return self.data.get("createdTime", "")

    @property
    def is_globally_available(self) -> bool:
        """Returns True if the sticker is globally available, False otherwise."""
        return self.data.get("isGloballyAvailable", False)

    @property
    def restriction_info(self) -> Dict[str, Any]:
        """Returns the sticker's restriction info."""
        return self.data.get("restrictionInfo") or {}

    @property
    def discount_status(self) -> int:
        """Returns the sticker's discount status."""
        return self.restriction_info.get("discountStatus", 0)

    @property
    def owner_uid(self) -> Optional[str]:
        """Returns the sticker's owner uid."""
        return self.restriction_info.get("ownerUid")

    @property
    def owner_type(self) -> int:
        """Returns the sticker's owner type."""
        return self.restriction_info.get("ownerType", 0)

    @property
    def restrict_type(self) -> int:
        """Returns the sticker's restrict type."""
        return self.restriction_info.get("restrictType", 0)

    @property
    def restrict_value(self) -> int:
        """Returns the sticker's restrict value."""
        return self.restriction_info.get("restrictValue", 0)

    @property
    def available_duration(self) -> Optional[str]:
        """Returns the sticker's available duration."""
        return self.restriction_info.get("availableDuration")

    @property
    def discount_value(self) -> Optional[int]:
        """Returns the sticker's discount value."""
        return self.restriction_info.get("discountValue")

    def json(self) -> Dict[str, Any]:
        """Returns the sticker's data as a dict."""
        return self.data


class CommunityStickerList:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data: List[Dict[str, Any]] = data.get("stickerCollectionList") or []

    def __iter__(self) -> "Iterator[CommunitySticker]":
        return (CommunitySticker(sticker) for sticker in self.data)

    @property
    def status(self) -> List[int]:
        """Returns the sticker's status."""
        return [sticker.status for sticker in self]

    @property
    def is_activated(self) -> List[bool]:
        """Returns True if the sticker is activated, False otherwise."""
        return [sticker.is_activated for sticker in self]

    @property
    def collection_type(self) -> List[int]:
        """Returns the sticker's collection type."""
        return [sticker.collection_type for sticker in self]

    @property
    def is_new(self) -> List[bool]:
        """Returns True if the sticker is new, False otherwise."""
        return [sticker.is_new for sticker in self]

    @property
    def banner_url(self) -> List[str]:
        """Returns the sticker's banner url."""
        return [sticker.banner_url for sticker in self]

    @property
    def is_owned(self) -> List[bool]:
        """Returns True if the sticker is owned, False otherwise."""
        return [sticker.is_owned for sticker in self]

    @property
    def used_count(self) -> List[int]:
        """Returns the sticker's used count."""
        return [sticker.used_count for sticker in self]

    @property
    def available_community_ids(self) -> List[List[int]]:
        """Returns a list of available community ids."""
        return [sticker.available_community_ids for sticker in self]

    @property
    def icon(self) -> List[str]:
        """Returns the sticker's icon url."""
        return [sticker.icon for sticker in self]

    @property
    def name(self) -> List[str]:
        """Returns the sticker's name."""
        return [sticker.name for sticker in self]

    @property
    def collection_id(self) -> List[str]:
        """Returns the sticker's collection id."""
        return [sticker.collection_id for sticker in self]

    @property
    def description(self) -> List[Optional[str]]:
        """Returns the sticker's description."""
        return [sticker.description for sticker in self]

    @property
    def ownership_info(self) -> List[Dict[str, Any]]:
        """Returns the sticker's ownership info."""
        return [sticker.ownership_info for sticker in self]

    @property
    def is_auto_renew(self) -> List[bool]:
        """Returns True if the sticker is auto renew, False otherwise."""
        return [sticker.is_auto_renew for sticker in self]

    @property
    def expired_time(self) -> List[Optional[str]]:
        """Returns the sticker's expired time."""
        return [sticker.expired_time for sticker in self]

    @property
    def extensions(self) -> List[StickerExtensions]:
        """Returns the sticker's extensions."""
        return [sticker.extensions for sticker in self]

    @property
    def created_time(self) -> List[str]:
        """Returns the sticker's created time."""
        return [sticker.created_time for sticker in self]

    @property
    def is_globally_available(self) -> List[bool]:
        """Returns True if the sticker is globally available, False otherwise."""
        return [sticker.is_globally_available for sticker in self]

    @property
    def restriction_info(self) -> List[Dict[str, Any]]:
        """Returns the sticker's restriction info."""
        return [sticker.restriction_info for sticker in self]

    @property
    def discount_status(self) -> List[int]:
        """Returns the sticker's discount status."""
        return [sticker.discount_status for sticker in self]

    @property
    def owner_uid(self) -> List[Optional[str]]:
        """Returns the sticker's owner uid."""
        return [sticker.owner_uid for sticker in self]

    @property
    def owner_type(self) -> List[int]:
        """Returns the sticker's owner type."""
        return [sticker.owner_type for sticker in self]

    @property
    def restrict_type(self) -> List[int]:
        """Returns the sticker's restrict type."""
        return [sticker.restrict_type for sticker in self]

    @property
    def restrict_value(self) -> List[int]:
        """Returns the sticker's restrict value."""
        return [sticker.restrict_value for sticker in self]

    @property
    def available_duration(self) -> List[Optional[str]]:
        """Returns the sticker's available duration."""
        return [sticker.available_duration for sticker in self]

    @property
    def discount_value(self) -> List[Optional[int]]:
        """Returns the sticker's discount value."""
        return [sticker.discount_value for sticker in self]

    def json(self) -> List[Dict[str, Any]]:
        """Returns the sticker's data as a dict."""
        return self.data

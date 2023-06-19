from typing import List, Union


class StickerAuthor:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except Exception:
            self.data = None

    def _check_author(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    @property
    @_check_author
    def is_global(self) -> bool:
        """Returns True if the author is global, False if not."""
        return self.data.get("isGlobal")
    
    @property
    @_check_author
    def comId(self) -> int:
        """Returns the author's community ID."""
        return self.data.get("ndcId")
    
    @property
    @_check_author
    def role(self) -> int:
        """Returns the author's role."""
        return self.data.get("role")
    
    @property
    @_check_author
    def is_nickname_verified(self) -> bool:
        """Returns True if the author's nickname is verified, False if not."""
        return self.data.get("isNicknameVerified")
    
    @property
    @_check_author
    def following_status(self) -> int:
        """Returns the author's following status."""
        return self.data.get("followingStatus")
    
    @property
    @_check_author
    def followers(self) -> int:
        """Returns the author's follower count."""
        return self.data.get("membersCount")
    
    @property
    @_check_author
    def membership_status(self) -> int:
        """Returns the author's membership status."""
        return self.data.get("membershipStatus")
    
    @property
    @_check_author
    def status(self) -> int:
        """Returns the author's status."""
        return self.data.get("status")
    
    @property
    @_check_author
    def account_membership_status(self) -> int:
        """Returns the author's account membership status."""
        return self.data.get("accountMembershipStatus")
    
    @property
    @_check_author
    def reputation(self) -> int:
        """Returns the author's reputation."""
        return self.data.get("reputation")
    
    @property
    @_check_author
    def level(self) -> int:
        """Returns the author's level."""
        return self.data.get("level")
    
    @property
    @_check_author
    def icon(self) -> str:
        """Returns the author's icon."""
        return self.data.get("icon")
    
    @property
    @_check_author
    def uid(self) -> str:
        """Returns the author's UID."""
        return self.data.get("uid")
    
    @property
    @_check_author
    def nickname(self) -> str:
        """Returns the author's nickname."""
        return self.data.get("nickname")
    
    def json(self) -> dict:
        """Returns the author's data as a dictionary."""
        return self.data


class OriginalCommunity:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except Exception:
            self.data = None

    def _check_community(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    @property
    @_check_community
    def status(self) -> int:
        """Returns the community's status."""
        return self.data.get("status")
    
    @property
    @_check_community
    def icon(self) -> str:
        """Returns the community's icon."""
        return self.data.get("icon")
    
    @property
    @_check_community
    def endpoint(self) -> str:
        """Returns the community's endpoint."""
        return self.data.get("endpoint")
    
    @property
    @_check_community
    def name(self) -> str:
        """Returns the community's name."""
        return self.data.get("name")
    
    @property
    @_check_community
    def comId(self) -> int:
        """Returns the community's ndc id."""
        return self.data.get("ndcId")
    
    def json(self) -> dict:
        """Returns the community's json."""
        return self.data


class StickerExtensions:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except Exception:
            self.data = None

    def _check_extension(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    @property
    @_check_extension
    def icon_source_sticker_id(self) -> str:
        """Returns the sticker's icon source sticker id."""
        return self.data.get("iconSourceStickerId")
    
    @property
    @_check_extension
    def original_author(self) -> StickerAuthor:
        """Returns the sticker's original author."""
        return StickerAuthor(self.data.get("originalAuthor"))
    
    @property
    @_check_extension
    def original_community(self) -> OriginalCommunity:
        """Returns the sticker's original community."""
        return OriginalCommunity(self.data.get("originalCommunity"))
    
    def json(self) -> dict:
        """Returns the sticker's extensions as a dictionary."""
        return self.data


class Sticker:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except Exception:
            self.data = None

    def _check_sticker(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper

    @property
    @_check_sticker
    def ref_object_type(self) -> int:
        """Returns the sticker's reference object type."""
        return self.data.get("refObjectType")

    @property
    @_check_sticker
    def ref_object_id(self) -> str:
        """Returns the sticker's reference object ID."""
        return self.data.get("refObjectId")

    @property
    @_check_sticker
    def created_time(self) -> str:
        """Returns the sticker's creation time."""
        return self.data.get("createdTime")

    @property
    @_check_sticker
    def item_basic_info(self) -> dict:
        """Returns the sticker's basic info."""
        return self.data.get("itemBasicInfo")

    @property
    @_check_sticker
    def icon(self) -> str:
        """Returns the sticker's icon."""
        return self.item_basic_info.get("icon")

    @property
    @_check_sticker
    def name(self) -> str:
        """Returns the sticker's name."""
        return self.item_basic_info.get("name")

    @property
    @_check_sticker
    def item_restriction_info(self) -> dict:
        """Returns the sticker's restriction info."""
        return self.data.get("itemRestrictionInfo")

    @property
    @_check_sticker
    def discount_value(self) -> Union[int, None]:
        """Returns the sticker's discount value."""
        return self.item_restriction_info.get("discountValue")

    @property
    @_check_sticker
    def discount_status(self) -> int:
        """Returns the sticker's discount status."""
        return self.item_restriction_info.get("discountStatus")

    @property
    @_check_sticker
    def owner_uid(self) -> Union[str, None]:
        """Returns the sticker's owner UID."""
        return self.item_restriction_info.get("ownerUid")

    @property
    @_check_sticker
    def owner_type(self) -> int:
        """Returns the sticker's owner type."""
        return self.item_restriction_info.get("ownerType")

    @property
    @_check_sticker
    def restrict_type(self) -> int:
        """Returns the sticker's restriction type."""
        return self.item_restriction_info.get("restrictType")

    @property
    @_check_sticker
    def restrict_value(self) -> int:
        """Returns the sticker's restriction value."""
        return self.item_restriction_info.get("restrictValue")

    @property
    @_check_sticker
    def available_duration(self) -> Union[int, None]:
        """Returns the sticker's available duration."""
        return self.item_restriction_info.get("availableDuration")

    @property
    @_check_sticker
    def ref_object(self) -> dict:
        """Returns the sticker's reference object."""
        return self.data.get("refObject")

    @property
    @_check_sticker
    def modified_time(self) -> str:
        """Returns the sticker's modification time."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("modifiedTime")

    @property
    @_check_sticker
    def ownership_status(self) -> Union[int, None]:
        """Returns the sticker's ownership status."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("ownershipStatus")

    @property
    @_check_sticker
    def used_count(self) -> int:
        """Returns the sticker's used count."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("usedCount")

    @property
    @_check_sticker
    def extensions(self) -> Union[dict, None]:
        """Returns the sticker's extensions."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("extensions")

    @property
    @_check_sticker
    def available_community_ids(self) -> list:
        """Returns the sticker's available community IDs."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("availableNdcIds")

    @property
    @_check_sticker
    def status(self) -> int:
        """Returns the sticker's status."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("status")

    @property
    @_check_sticker
    def author(self) -> StickerAuthor:
        """Returns the sticker's author."""
        return StickerAuthor(self.ref_object.get("author"))

    @property
    @_check_sticker
    def is_new(self) -> bool:
        """Returns the sticker's new status."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("isNew")

    @property
    @_check_sticker
    def stickers_count(self) -> int:
        """Returns the sticker's count."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("stickersCount")

    @property
    @_check_sticker
    def restriction_info(self) -> dict:
        """Returns the sticker's restriction info."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("restrictionInfo")

    @property
    @_check_sticker
    def collection_id(self) -> str:
        """Returns the sticker's collection ID."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("collectionId")

    @property
    @_check_sticker
    def is_activated(self) -> bool:
        """Returns the sticker's activation status."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("isActivated")

    @property
    @_check_sticker
    def collection_type(self) -> int:
        """Returns the sticker's collection type."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("collectionType")

    @property
    @_check_sticker
    def uid(self) -> str:
        """Returns the sticker's UID."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("uid")

    @property
    @_check_sticker
    def small_icon(self) -> str:
        """Returns the sticker's small icon."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("smallIcon")

    @property
    @_check_sticker
    def description(self) -> str:
        """Returns the sticker's description."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("description")

    @property
    @_check_sticker
    def is_globally_available(self) -> bool:
        """Returns the sticker's global availability status."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("isGloballyAvailable")

    @property
    @_check_sticker
    def banner_url(self) -> str:
        """Returns the sticker's banner URL."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("bannerUrl")
        
    def json(self) -> dict:
        """Returns the sticker's data in JSON format."""
        return self.data
    

class StickerList:
    def __init__(self, data: dict):
        try:
            self.data = data.get("storeItemList")
        except Exception:
            self.data = None

    def _check_stickers(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    def __iterator__(self):
        """
        Iterator function to iterate over the sticker list.
        """
        for sticker in self.data:
            yield Sticker(sticker)

    @property
    @_check_stickers
    def ref_object_type(self) -> List[int]:
        """Returns the sticker list's ref object type."""
        return [sticker.ref_object_type for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def ref_object_id(self) -> List[str]:
        """Returns the sticker list's ref object ID."""
        return [sticker.ref_object_id for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def created_time(self) -> List[str]:
        """Returns the sticker list's creation time."""
        return [sticker.created_time for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def item_basic_info(self) -> List[dict]:
        """Returns the sticker list's basic info."""
        return [sticker.item_basic_info for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def icon(self) -> List[str]:
        """Returns the sticker list's icon."""
        return [sticker.icon for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def name(self) -> List[str]:
        """Returns the sticker list's name."""
        return [sticker.name for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def item_restriction_info(self) -> List[dict]:
        """Returns the sticker list's restriction info."""
        return [sticker.item_restriction_info for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def discount_value(self) -> List[str]:
        """Returns the sticker list's discount value."""
        return [sticker.discount_value for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def discount_status(self) -> List[int]:
        """Returns the sticker list's discount status."""
        return [sticker.discount_status for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def owner_uid(self) -> List[str]:
        """Returns the sticker list's owner UID."""
        return [sticker.owner_uid for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def owner_type(self) -> List[int]:
        """Returns the sticker list's owner type."""
        return [sticker.owner_type for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def restrict_type(self) -> List[int]:
        """Returns the sticker list's restrict type."""
        return [sticker.restrict_type for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def restrict_value(self) -> List[int]:
        """Returns the sticker list's restrict value."""
        return [sticker.restrict_value for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def available_duration(self) -> List[str]:
        """Returns the sticker list's available duration."""
        return [sticker.available_duration for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def ownership_status(self) -> List[int]:
        """Returns the sticker list's ownership status."""
        return [sticker.ownership_status for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def is_owned(self) -> List[bool]:
        """Returns the sticker list's ownership status."""
        return [sticker.is_owned for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def is_new(self) -> List[bool]:
        """Returns the sticker list's new status."""
        return [sticker.is_new for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def is_activated(self) -> List[bool]:
        """Returns the sticker list's activation status."""
        return [sticker.is_activated for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def collection_id(self) -> List[str]:
        """Returns the sticker list's collection ID."""
        return [sticker.collection_id for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def collection_type(self) -> List[int]:
        """Returns the sticker list's collection type."""
        return [sticker.collection_type for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def uid(self) -> List[str]:
        """Returns the sticker list's UID."""
        return [sticker.uid for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def small_icon(self) -> List[str]:
        """Returns the sticker list's small icon."""
        return [sticker.small_icon for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def description(self) -> List[str]:
        """Returns the sticker list's description."""
        return [sticker.description for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def is_globally_available(self) -> List[bool]:
        """Returns the sticker list's global availability."""
        return [sticker.is_globally_available for sticker in self.__iterator__()]
    
    @property
    @_check_stickers
    def banner_url(self) -> List[str]:
        """Returns the sticker list's banner URL."""
        return [sticker.banner_url for sticker in self.__iterator__()]
    
    def json(self) -> dict:
        """Returns the sticker list's JSON data."""
        return self.data


class CommunitySticker:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except Exception:
            self.data = None

    def _check_sticker(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    @property
    @_check_sticker
    def status(self) -> int:
        """Returns the sticker's status."""
        return self.data.get("status")
    
    @property
    @_check_sticker
    def is_activated(self) -> bool:
        """Returns True if the sticker is activated, False otherwise."""
        return self.data.get("isActivated")
    
    @property
    @_check_sticker
    def collection_type(self) -> int:
        """Returns the sticker's collection type."""
        return self.data.get("collectionType")
    
    @property
    @_check_sticker
    def is_new(self) -> bool:
        """Returns True if the sticker is new, False otherwise."""
        return self.data.get("isNew")
    
    @property
    @_check_sticker
    def banner_url(self) -> str:
        """Returns the sticker's banner url."""
        return self.data.get("bannerUrl")

    @property
    @_check_sticker
    def is_owned(self) -> bool:
        """Returns True if the sticker is owned, False otherwise."""
        return self.data.get("isOwned")
    
    @property
    @_check_sticker
    def used_count(self) -> int:
        """Returns the sticker's used count."""
        return self.data.get("usedCount")
    
    @property
    @_check_sticker
    def available_community_ids(self) -> list:
        """Returns a list of available community ids."""
        return self.data.get("availableNdcIds")
    
    @property
    @_check_sticker
    def icon(self) -> str:
        """Returns the sticker's icon url."""
        return self.data.get("icon")
    
    @property
    @_check_sticker
    def name(self) -> str:
        """Returns the sticker's name."""
        return self.data.get("name")

    @property
    @_check_sticker
    def collection_id(self) -> str:
        """Returns the sticker's collection id."""
        return self.data.get("collectionId")

    @property
    @_check_sticker
    def description(self) -> str:
        """Returns the sticker's description."""
        return self.data.get("description")

    @property
    @_check_sticker
    def author(self) -> StickerAuthor:
        """Returns the sticker's author."""
        return StickerAuthor(self.data.get("author"))

    @property
    @_check_sticker
    def ownership_info(self) -> dict:
        """Returns the sticker's ownership info."""
        return self.data.get("ownershipInfo")

    @property
    @_check_sticker
    def is_auto_renew(self) -> bool:
        """Returns True if the sticker is auto renew, False otherwise."""
        if self.owner_info is None:
            return None
        return self.owner_info.get("isAutoRenew")

    @property
    @_check_sticker
    def expired_time(self) -> str:
        """Returns the sticker's expired time."""
        if self.owner_info is None:
            return None
        return self.owner_info.get("expiredTime")

    @property
    @_check_sticker
    def extensions(self) -> StickerExtensions:
        """Returns the sticker's extensions."""
        return StickerExtensions(self.data.get("extensions"))

    @property
    @_check_sticker
    def created_time(self) -> str:
        """Returns the sticker's created time."""
        return self.data.get("createdTime")

    @property
    @_check_sticker
    def is_globally_available(self) -> bool:
        """Returns True if the sticker is globally available, False otherwise."""
        return self.data.get("isGloballyAvailable")

    
    @property   
    @_check_sticker
    def restriction_info(self) -> dict:
        """Returns the sticker's restriction info."""
        return self.data.get("restrictionInfo")

    @property
    @_check_sticker
    def discount_status(self) -> int:
        """Returns the sticker's discount status."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("discountStatus")

    @property
    @_check_sticker
    def owner_uid(self) -> str:
        """Returns the sticker's owner uid."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("ownerUid")

    @property
    @_check_sticker
    def owner_type(self) -> int:
        """Returns the sticker's owner type."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("ownerType")

    @property
    @_check_sticker
    def restrict_type(self) -> int:
        """Returns the sticker's restrict type."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("restrictType")

    @property
    @_check_sticker
    def restrict_value(self) -> int:
        """Returns the sticker's restrict value."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("restrictValue")

    @property
    @_check_sticker
    def available_duration(self) -> str:
        """Returns the sticker's available duration."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("availableDuration")

    @property
    @_check_sticker
    def discount_value(self) -> str:
        """Returns the sticker's discount value."""
        if self.restriction_info is None:
            return None
        return self.restriction_info.get("discountValue")

    def json(self) -> dict:
        """Returns the sticker's data as a dict."""
        return self.data
    

class CommunityStickerList:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data.get("stickerCollectionList")
        except Exception:
            self.data = None

    def _check_sticker(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper

    def __iterator__(self):
        """
        Iterator function to iterate over the stickers in the sticker list.
        """
        for sticker in self.data:
            yield CommunitySticker(sticker)

    @property
    @_check_sticker
    def status(self) -> List[int]:
        """Returns the sticker's status."""
        return [sticker.status for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def is_activated(self) -> bool:
        """Returns True if the sticker is activated, False otherwise."""
        return [sticker.is_activated for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def collection_type(self) -> int:
        """Returns the sticker's collection type."""
        return [sticker.collection_type for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def is_new(self) -> bool:
        """Returns True if the sticker is new, False otherwise."""
        return [sticker.is_new for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def banner_url(self) -> str:
        """Returns the sticker's banner url."""
        return [sticker.banner_url for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def is_owned(self) -> bool:
        """Returns True if the sticker is owned, False otherwise."""
        return [sticker.is_owned for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def used_count(self) -> int:
        """Returns the sticker's used count."""
        return [sticker.used_count for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def available_community_ids(self) -> list:
        """Returns a list of available community ids."""
        return [sticker.available_community_ids for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def icon(self) -> str:
        """Returns the sticker's icon url."""
        return [sticker.icon for sticker in self.__iterator__()]
    
    @property
    @_check_sticker
    def name(self) -> str:
        """Returns the sticker's name."""
        return [sticker.name for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def collection_id(self) -> str:
        """Returns the sticker's collection id."""
        return [sticker.collection_id for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def description(self) -> str:
        """Returns the sticker's description."""
        return [sticker.description for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def ownership_info(self) -> dict:
        """Returns the sticker's ownership info."""
        return [sticker.ownership_info for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def is_auto_renew(self) -> bool:
        """Returns True if the sticker is auto renew, False otherwise."""
        if self.owner_info is None:
            return None
        return [sticker.is_auto_renew for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def expired_time(self) -> str:
        """Returns the sticker's expired time."""
        if self.owner_info is None:
            return None
        return [sticker.expired_time for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def extensions(self) -> StickerExtensions:
        """Returns the sticker's extensions."""
        return StickerExtensions(self.data.get("extensions"))

    @property
    @_check_sticker
    def created_time(self) -> str:
        """Returns the sticker's created time."""
        return [sticker.created_time for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def is_globally_available(self) -> bool:
        """Returns True if the sticker is globally available, False otherwise."""
        return [sticker.is_globally_available for sticker in self.__iterator__()]
    
    @property   
    @_check_sticker
    def restriction_info(self) -> dict:
        """Returns the sticker's restriction info."""
        return [sticker.restriction_info for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def discount_status(self) -> int:
        """Returns the sticker's discount status."""
        if self.restriction_info is None:
            return None
        return [sticker.discount_status for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def owner_uid(self) -> str:
        """Returns the sticker's owner uid."""
        if self.restriction_info is None:
            return None
        return [sticker.owner_uid for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def owner_type(self) -> int:
        """Returns the sticker's owner type."""
        if self.restriction_info is None:
            return None
        return [sticker.owner_type for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def restrict_type(self) -> int:
        """Returns the sticker's restrict type."""
        if self.restriction_info is None:
            return None
        return [sticker.restrict_type for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def restrict_value(self) -> int:
        """Returns the sticker's restrict value."""
        if self.restriction_info is None:
            return None
        return [sticker.restrict_value for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def available_duration(self) -> str:
        """Returns the sticker's available duration."""
        if self.restriction_info is None:
            return None
        return [sticker.available_duration for sticker in self.__iterator__()]

    @property
    @_check_sticker
    def discount_value(self) -> str:
        """Returns the sticker's discount value."""
        if self.restriction_info is None:
            return None
        return [sticker.discount_value for sticker in self.__iterator__()]

    def json(self) -> dict:
        """Returns the sticker's data as a dict."""
        return self.data
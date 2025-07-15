from collections.abc import Iterator
from typing import Any, Dict, List, Optional, Union

__all__ = ("Bubble", "BubbleList")


class Bubble:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def ref_object_id(self) -> str:
        """Returns the ref object id of the bubble."""
        return self.data.get("refObjectId", "")

    @property
    def created_time(self) -> str:
        """Returns the time the bubble was created."""
        return self.data.get("createdTime", "")

    @property
    def item_basic_info(self) -> Dict[str, Any]:
        """Returns the basic info of the bubble."""
        return self.data.get("itemBasicInfo") or {}

    @property
    def icon(self) -> str:
        """Returns the icon url of the bubble."""
        return self.item_basic_info.get("icon", "")

    @property
    def name(self) -> str:
        """Returns the name of the bubble."""
        return self.item_basic_info.get("name", "")

    @property
    def item_restriction_info(self) -> Dict[str, Any]:
        """Returns the restriction info of the bubble."""
        return self.data.get("itemRestrictionInfo") or {}

    @property
    def owner_uid(self) -> Optional[str]:
        """Returns the owner uid of the bubble."""
        return self.item_restriction_info.get("ownerUid")

    @property
    def owner_type(self) -> int:
        """Returns the owner type of the bubble."""
        return self.item_restriction_info.get("ownerType", 0)

    @property
    def restrict_type(self) -> int:
        """Returns the restict type of the bubble."""
        return self.item_restriction_info.get("restrictType", 0)

    @property
    def restrict_value(self) -> Optional[int]:
        """Returns the restrict value of the bubble."""
        return self.item_restriction_info.get("restrictValue")

    @property
    def available_duration(self) -> Optional[str]:
        """Returns the available duration of the bubble."""
        return self.item_restriction_info.get("availableDuration")

    @property
    def discount_value(self) -> Optional[int]:
        """Returns the discount value of the bubble."""
        return self.item_restriction_info.get("discountValue")

    @property
    def discount_status(self) -> int:
        """Returns the discount status of the bubble."""
        return self.item_restriction_info.get("discountStatus", 0)

    @property
    def ref_object(self) -> Dict[str, Any]:
        """Returns the ref object of the bubble."""
        return self.data.get("refObject") or {}

    @property
    def is_global(self) -> bool:
        """Returns whether the bubble is globally available."""
        return self.ref_object.get("isGloballyAvailable", False)

    @property
    def available_community_ids(self) -> List[int]:
        """Return the available community ids of the bubble."""
        return self.ref_object.get("availableNdcIds") or []

    @property
    def bubble_type(self) -> int:
        """Returns the bubble type of the bubble."""
        return self.ref_object.get("bubbleType", 0)

    @property
    def bubble_id(self) -> str:
        """Returns the bubble id of the bubble."""
        return self.ref_object.get("bubbleId", "")

    @property
    def background_image(self) -> Optional[str]:
        """Returns the background image of the bubble."""
        return self.ref_object.get("backgroundImage")

    @property
    def status(self) -> int:
        """Returns the status of the bubble."""
        return self.ref_object.get("status", 0)

    @property
    def is_new(self) -> bool:
        """Returns whether the bubble is new."""
        return self.ref_object.get("isNew", False)

    @property
    def bubble_name(self) -> str:
        """Returns the name of the bubble."""
        return self.ref_object.get("name", "")

    @property
    def banner_image(self) -> Optional[str]:
        """Returns the banner image of the bubble."""
        return self.ref_object.get("bannerImage")

    @property
    def resource_url(self) -> str:
        """Returns the resource url of the bubble."""
        return self.ref_object.get("resourceUrl", "")

    @property
    def ownership_status(self) -> int:
        """Returns the ownership status of the bubble."""
        return self.ref_object.get("ownershipStatus", 0)

    @property
    def deletable(self) -> bool:
        """Returns whether the bubble is deletable."""
        return self.ref_object.get("deletable", False)

    @property
    def config(self) -> Dict[str, Any]:
        """Returns the config of the bubble."""
        return self.ref_object.get("config") or {}

    @property
    def version(self) -> int:
        """Returns the version of the bubble."""
        return self.ref_object.get("version", 0)

    @property
    def modified_time(self) -> Optional[str]:
        """Returns the modified time of the bubble."""
        return self.ref_object.get("modifiedTime")

    @property
    def is_activated(self) -> bool:
        """Returns whether the bubble is activated."""
        return self.ref_object.get("isActivated", False)

    @property
    def cover_image(self) -> Optional[str]:
        """Returns the cover image of the bubble."""
        return self.ref_object.get("coverImage")

    @property
    def extensions(self) -> Dict[str, Any]:
        """Returns the extensions of the bubble."""
        return self.ref_object.get("extensions") or {}

    @property
    def template_id(self) -> int:
        """Returns the template id of the bubble."""
        return self.ref_object.get("templateId", 0)

    @property
    def uid(self) -> str:
        """Returns the uid of the bubble."""
        return self.ref_object.get("uid", "")

    @property
    def md5(self) -> Optional[str]:
        """Returns the md5 of the bubble."""
        return self.ref_object.get("md5")

    @property
    def ref_object_type(self) -> int:
        """Returns the ref object type of the bubble."""
        return self.data.get("refObjectType", 0)


class BubbleList:
    def __init__(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> None:
        if isinstance(data, dict):
            data = list(data.get("storeItemList") or [])
        self.data = data or []

    def __iter__(self) -> "Iterator[Bubble]":
        return (Bubble(bubble) for bubble in self.data)

    @property
    def ref_object_id(self) -> List[str]:
        """Returns the ref object id of the bubble list."""
        return [bubble.ref_object_id for bubble in self]

    @property
    def created_time(self) -> List[str]:
        """Returns the created time of the bubble list."""
        return [bubble.created_time for bubble in self]

    @property
    def item_basic_info(self) -> List[Dict[str, Any]]:
        """Returns the item basic info of the bubble list."""
        return [bubble.item_basic_info for bubble in self]

    @property
    def icon(self) -> List[str]:
        """Returns the icon of the bubble list."""
        return [bubble.icon for bubble in self]

    @property
    def name(self) -> List[str]:
        """Returns the name of the bubble list."""
        return [bubble.name for bubble in self]

    @property
    def item_restriction_info(self) -> List[Dict[str, Any]]:
        """Returns the item restriction info of the bubble list."""
        return [bubble.item_restriction_info for bubble in self]

    @property
    def owner_uid(self) -> List[Optional[str]]:
        """Returns the owner uid of the bubble list."""
        return [bubble.owner_uid for bubble in self]

    @property
    def owner_type(self) -> List[int]:
        """Returns the owner type of the bubble list."""
        return [bubble.owner_type for bubble in self]

    @property
    def restrict_type(self) -> List[int]:
        """Returns the restrict type of the bubble list."""
        return [bubble.restrict_type for bubble in self]

    @property
    def restrict_value(self) -> List[Optional[int]]:
        """Returns the restrict value of the bubble list."""
        return [bubble.restrict_value for bubble in self]

    @property
    def available_duration(self) -> List[Optional[str]]:
        """Returns the available duration of the bubble list."""
        return [bubble.available_duration for bubble in self]

    @property
    def discount_value(self) -> List[Optional[int]]:
        """Returns the discount value of the bubble list."""
        return [bubble.discount_value for bubble in self]

    @property
    def discount_status(self) -> List[int]:
        """Returns the discount status of the bubble list."""
        return [bubble.discount_status for bubble in self]

    @property
    def ref_object(self) -> List[Dict[str, Any]]:
        """Returns the ref object of the bubble list."""
        return [bubble.ref_object for bubble in self]

    @property
    def is_global(self) -> List[bool]:
        """Returns the is global of the bubble list."""
        return [bubble.is_global for bubble in self]

    @property
    def available_community_ids(self) -> List[List[int]]:
        """Returns the available community ids of the bubble list."""
        return [bubble.available_community_ids for bubble in self]

    @property
    def bubble_type(self) -> List[int]:
        """Returns the bubble type of the bubble list."""
        return [bubble.bubble_type for bubble in self]

    @property
    def bubble_id(self) -> List[str]:
        """Returns the bubble id of the bubble list."""
        return [bubble.bubble_id for bubble in self]

    @property
    def background_image(self) -> List[Optional[str]]:
        """Returns the background image of the bubble list."""
        return [bubble.background_image for bubble in self]

    @property
    def status(self) -> List[int]:
        """Returns the status of the bubble list."""
        return [bubble.status for bubble in self]

    @property
    def is_new(self) -> List[bool]:
        """Returns the is new of the bubble list."""
        return [bubble.is_new for bubble in self]

    @property
    def banner_image(self) -> List[Optional[str]]:
        """Returns the banner image of the bubble list."""
        return [bubble.banner_image for bubble in self]

    @property
    def resource_url(self) -> List[str]:
        """Returns the resource url of the bubble list."""
        return [bubble.resource_url for bubble in self]

    @property
    def ownership_status(self) -> List[int]:
        """Returns the ownership status of the bubble list."""
        return [bubble.ownership_status for bubble in self]

    @property
    def deletable(self) -> List[bool]:
        """Returns the deletable of the bubble list."""
        return [bubble.deletable for bubble in self]

    @property
    def config(self) -> List[Dict[str, Any]]:
        """Returns the config of the bubble list."""
        return [bubble.config for bubble in self]

    @property
    def version(self) -> List[int]:
        """Returns the version of the bubble list."""
        return [bubble.version for bubble in self]

    @property
    def modified_time(self) -> List[Optional[str]]:
        """Returns the modified time of the bubble list."""
        return [bubble.modified_time for bubble in self]

    @property
    def is_activated(self) -> List[bool]:
        """Returns the is activated of the bubble list."""
        return [bubble.is_activated for bubble in self]

    @property
    def cover_image(self) -> List[Optional[str]]:
        """Returns the cover image of the bubble list."""
        return [bubble.cover_image for bubble in self]

    @property
    def extensions(self) -> List[Dict[str, Any]]:
        """Returns the extensions of the bubble list."""
        return [bubble.extensions for bubble in self]

    @property
    def template_id(self) -> List[int]:
        """Returns the template id of the bubble list."""
        return [bubble.template_id for bubble in self]

    @property
    def uid(self) -> List[str]:
        """Returns the uid of the bubble list."""
        return [bubble.uid for bubble in self]

    @property
    def md5(self) -> List[Optional[str]]:
        """Returns the md5 of the bubble list."""
        return [bubble.md5 for bubble in self]

    def json(self) -> List[Dict[str, Any]]:
        """Returns the json of the bubble list."""
        return self.data

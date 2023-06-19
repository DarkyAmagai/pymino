from typing import List, Union


class Bubble:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None
    
    def _check_bubble(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper

    @property
    @_check_bubble
    def ref_object_id(self) -> str:
        """Returns the ref object id of the bubble."""
        return self.data.get("refObjectId")

    @property
    @_check_bubble
    def created_time(self) -> str:
        """Returns the time the bubble was created."""
        return self.data.get("createdTime")

    @property
    @_check_bubble
    def item_basic_info(self) -> dict:
        """Returns the basic info of the bubble."""
        return self.data.get("itemBasicInfo")

    @property
    @_check_bubble
    def icon(self) -> str:
        """Returns the icon url of the bubble."""
        if self.item_basic_info is None:
            return None
        else:
            return self.item_basic_info.get("icon")
        
    @property
    @_check_bubble
    def name(self) -> str:
        """Returns the name of the bubble."""
        if self.item_basic_info is None:
            return None
        else:
            return self.item_basic_info.get("name")
        
    @property
    @_check_bubble
    def item_restriction_info(self) -> dict:
        """Returns the restriction info of the bubble."""
        return self.data.get("itemRestrictionInfo")


    @property
    @_check_bubble
    def owner_uid(self) -> Union[str, None]:
        """Returns the owner uid of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("ownerUid")
        
    @property
    @_check_bubble
    def owner_type(self) -> Union[int, None]:
        """Returns the owner type of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("ownerType")
        
    @property
    @_check_bubble
    def restrict_type(self) -> Union[int, None]:
        """Returns the restict type of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("restrictType")
        
    @property
    @_check_bubble
    def restrict_value(self) -> Union[int, None]:
        """Returns the restrict value of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("restrictValue")
        
    @property
    @_check_bubble
    def available_duration(self) -> Union[int, None]:
        """Returns the available duration of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("availableDuration")
        
    @property
    @_check_bubble
    def discount_value(self) -> Union[int, None]:
        """Returns the discount value of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("discountValue")
        
    @property
    @_check_bubble
    def discount_status(self) -> Union[int, None]:
        """Returns the discount status of the bubble."""
        if self.item_restriction_info is None:
            return None
        else:
            return self.item_restriction_info.get("discountStatus")
        
    @property
    @_check_bubble
    def ref_object(self) -> dict:
        """Returns the ref object of the bubble."""
        return self.data.get("refObject")

    @property
    @_check_bubble
    def is_global(self) -> bool:
        """Returns whether the bubble is globally available."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("isGloballyAvailable")
        
    @property
    @_check_bubble
    def available_community_ids(self) -> list:
        """Return the available community ids of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("availableNdcIds")
        
    @property
    @_check_bubble
    def bubble_type(self) -> int:
        """Returns the bubble type of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("bubbleType")
        
    @property
    @_check_bubble
    def bubble_id(self) -> str:
        """Returns the bubble id of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("bubbleId")
        
    @property
    @_check_bubble
    def background_image(self) -> str:
        """Returns the background image of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("backgroundImage")
        
    @property
    @_check_bubble
    def status(self) -> int:
        """Returns the status of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("status")
        
    @property
    @_check_bubble
    def is_new(self) -> bool:
        """Returns whether the bubble is new."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("isNew")
        
    @property
    @_check_bubble
    def bubble_name(self) -> str:
        """Returns the name of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("name")
        
    @property
    @_check_bubble
    def banner_image(self) -> str:
        """Returns the banner image of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("bannerImage")
        
    @property
    @_check_bubble
    def resource_url(self) -> str:
        """Returns the resource url of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("resourceUrl")
        
    @property
    @_check_bubble
    def ownership_status(self) -> dict:
        """Returns the ownership status of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("ownershipStatus")
        
    @property
    @_check_bubble
    def deletable(self) -> bool:
        """Returns whether the bubble is deletable."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("deletable")
        
    @property
    @_check_bubble
    def config(self) -> dict:
        """Returns the config of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("config")
        
    @property
    @_check_bubble
    def version(self) -> int:
        """Returns the version of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("version")
        
    @property
    @_check_bubble
    def modified_time(self) -> str:
        """Returns the modified time of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("modifiedTime")
        
    @property
    @_check_bubble
    def is_activated(self) -> bool:
        """Returns whether the bubble is activated."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("isActivated")
        
    @property
    @_check_bubble
    def cover_image(self) -> str:
        """Returns the cover image of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("coverImage")
        
    @property
    @_check_bubble
    def extensions(self) -> dict:
        """Returns the extensions of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("extensions")
        
    @property
    @_check_bubble
    def template_id(self) -> str:
        """Returns the template id of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("templateId")

    @property
    @_check_bubble
    def uid(self) -> str:
        """Returns the uid of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("uid")
        
    @property
    @_check_bubble
    def md5(self) -> str:
        """Returns the md5 of the bubble."""
        if self.ref_object is None:
            return None
        else:
            return self.ref_object.get("md5")
        
    @property
    @_check_bubble
    def ref_object_type(self) -> int:
        """Returns the ref object type of the bubble."""
        if self.data is None:
            return None
        else:
            return self.data.get("refObjectType")
        


class BubbleList:
    def __init__(self, data: dict):
        try:
            self.data = data.get("storeItemList")
        except Exception:
            self.data = None

    def _check_bubbles(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    def __iterator__(self):
        """
        Iterator function to iterate over the bubbles in the bubble list.
        """
        for bubble in self.data:
            yield Bubble(bubble)

    @property
    @_check_bubbles
    def ref_object_id(self) -> List[str]:
        """Returns the ref object id of the bubble list."""
        return [bubble.ref_object_id for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def created_time(self) -> List[str]:
        """Returns the created time of the bubble list."""
        return [bubble.created_time for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def item_basic_info(self) -> List[dict]:
        """Returns the item basic info of the bubble list."""
        return [bubble.item_basic_info for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def icon(self) -> List[str]:
        """Returns the icon of the bubble list."""
        return [bubble.icon for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def name(self) -> List[str]:
        """Returns the name of the bubble list."""
        return [bubble.name for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def item_restriction_info(self) -> List[dict]:
        """Returns the item restriction info of the bubble list."""
        return [bubble.item_restriction_info for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def owner_uid(self) -> List[str]:
        """Returns the owner uid of the bubble list."""
        return [bubble.owner_uid for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def owner_type(self) -> List[int]:
        """Returns the owner type of the bubble list."""
        return [bubble.owner_type for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def restrict_type(self) -> List[int]:
        """Returns the restrict type of the bubble list."""
        return [bubble.restrict_type for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def restrict_value(self) -> List[int]:
        """Returns the restrict value of the bubble list."""
        return [bubble.restrict_value for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def available_duration(self) -> List[str]:
        """Returns the available duration of the bubble list."""
        return [bubble.available_duration for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def discount_value(self) -> List[str]:
        """Returns the discount value of the bubble list."""
        return [bubble.discount_value for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def discount_status(self) -> List[int]:
        """Returns the discount status of the bubble list."""
        return [bubble.discount_status for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def ref_object(self) -> List[dict]:
        """Returns the ref object of the bubble list."""
        return [bubble.ref_object for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def is_global(self) -> List[str]:
        """Returns the is global of the bubble list."""
        return [bubble.is_global for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def available_community_ids(self) -> List[int]:
        """Returns the available community ids of the bubble list."""
        return [bubble.available_community_ids for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def bubble_type(self) -> List[int]:
        """Returns the bubble type of the bubble list."""
        return [bubble.bubble_type for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def bubble_id(self) -> List[str]:
        """Returns the bubble id of the bubble list."""
        return [bubble.bubble_id for bubble in self.__iterator__()]
    
    @property
    @_check_bubbles
    def background_image(self) -> List[str]:
        """Returns the background image of the bubble list."""
        return [bubble.background_image for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def status(self) -> List[int]:
        """Returns the status of the bubble list."""
        return [bubble.status for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def is_new(self) -> List[str]:
        """Returns the is new of the bubble list."""
        return [bubble.is_new for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def name(self) -> List[str]:
        """Returns the name of the bubble list."""
        return [bubble.name for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def banner_image(self) -> List[str]:
        """Returns the banner image of the bubble list."""
        return [bubble.banner_image for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def resource_url(self) -> List[str]:
        """Returns the resource url of the bubble list."""
        return [bubble.resource_url for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def ownership_status(self) -> List[str]:
        """Returns the ownership status of the bubble list."""
        return [bubble.ownership_status for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def deletable(self) -> List[str]:
        """Returns the deletable of the bubble list."""
        return [bubble.deletable for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def config(self) -> List[dict]:
        """Returns the config of the bubble list."""
        return [bubble.config for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def version(self) -> List[int]:
        """Returns the version of the bubble list."""
        return [bubble.version for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def modified_time(self) -> List[str]:
        """Returns the modified time of the bubble list."""
        return [bubble.modified_time for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def is_activated(self) -> List[str]:
        """Returns the is activated of the bubble list."""
        return [bubble.is_activated for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def cover_image(self) -> List[str]:
        """Returns the cover image of the bubble list."""
        return [bubble.cover_image for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def extensions(self) -> List[str]:
        """Returns the extensions of the bubble list."""
        return [bubble.extensions for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def template_id(self) -> List[str]:
        """Returns the template id of the bubble list."""
        return [bubble.template_id for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def uid(self) -> List[str]:
        """Returns the uid of the bubble list."""
        return [bubble.uid for bubble in self.__iterator__()]

    @property
    @_check_bubbles
    def md5(self) -> List[str]:
        """Returns the md5 of the bubble list."""
        return [bubble.md5 for bubble in self.__iterator__()]
    

    def json(self) -> dict:
        """Returns the json of the bubble list."""
        return self.data
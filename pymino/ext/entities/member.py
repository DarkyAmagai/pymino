from typing import Union


class MemberAvatar:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None
    
    def _check_member_avatar(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    @property
    @_check_member_avatar
    def status(self) -> Union[int, None]:
        """Returns the status of the member avatar."""
        return self.data.get("status")
    
    @property
    @_check_member_avatar
    def version(self) -> Union[int, None]:
        """Returns the version of the member avatar."""
        return self.data.get("version")
    
    @property
    @_check_member_avatar
    def resourceUrl(self) -> Union[str, None]:
        """Returns the resource URL of the member avatar."""
        return self.data.get("resourceUrl")
    
    @property
    @_check_member_avatar
    def name(self) -> Union[str, None]:
        """Returns the name of the member avatar."""
        return self.data.get("name")
    
    @property
    @_check_member_avatar
    def icon(self) -> Union[str, None]:
        """Returns the icon of the member avatar."""
        return self.data.get("icon")
    
    @property
    @_check_member_avatar
    def frameType(self) -> Union[int, None]:
        """Returns the frame type of the member avatar."""
        return self.data.get("frameType")
    
    @property
    @_check_member_avatar
    def frameId(self) -> Union[str, None]:
        """Returns the frame ID of the member avatar."""
        return self.data.get("frameId")


class Member:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None
        
    def _check_member(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    
    @property
    @_check_member
    def uid(self) -> Union[str, None]:
        """Returns the uid of the member."""
        return self.data.get("uid")
    
    @property
    @_check_member
    def userId(self) -> Union[str, None]:
        """Returns the userId of the member."""
        return self.uid
    
    @property
    @_check_member
    def status(self) -> Union[int, None]:
        """Returns the status of the member."""
        return self.data.get("status")
    
    @property
    @_check_member
    def icon(self) -> Union[str, None]:
        """Returns the icon of the member."""
        return self.data.get("icon")
    
    @property
    @_check_member
    def reputation(self) -> Union[int, None]:
        """Returns the reputation of the member."""
        return self.data.get("reputation")
    
    @property
    @_check_member
    def role(self) -> Union[int, None]:
        """Returns the role of the member."""
        return self.data.get("role")
    
    @property
    @_check_member
    def nickname(self) -> Union[str, None]:
        """Returns the nickname of the member."""
        return self.data.get("nickname")
    
    @property
    @_check_member
    def level(self) -> Union[int, None]:
        """Returns the level of the member."""
        return self.data.get("level")
    
    @property
    @_check_member
    def membership_status(self) -> Union[int, None]:
        """Returns the accountMembershipStatus of the member."""
        return self.data.get("accountMembershipStatus")
    
    @property
    @_check_member
    def avatar(self) -> Union[MemberAvatar, None]:
        """Returns the avatar of the member."""
        return MemberAvatar(self.data.get("avatarFrame"))
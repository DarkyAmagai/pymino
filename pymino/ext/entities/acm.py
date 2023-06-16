from typing import List, Union


class CommunityStats:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data.get("communityStats", data)
        except AttributeError:
            self.data = None    

    @property
    def daily_active_members(self) -> Union[int, None]:
        """Returns the daily active members of the community."""
        return self.data.get("dailyActiveMembers")
    
    @property
    def monthly_active_members(self) -> Union[int, None]:
        """Returns the monthly active members of the community."""
        return self.data.get("monthlyActiveMembers")
    
    @property
    def total_time_spent(self) -> Union[int, None]:
        """Returns the total time spent in the community."""
        return self.data.get("totalTimeSpent")
    
    @property
    def total_posts_created(self) -> Union[int, None]:
        """Returns the total posts created in the community."""
        return self.data.get("totalPostsCreated")
    
    @property
    def new_members_today(self) -> Union[int, None]:
        """Returns the new members today in the community."""
        return self.data.get("newMembersToday")
    
    @property
    def total_members(self) -> Union[int, None]:
        """Returns the total members in the community."""
        return self.data.get("totalMembers")
    

class Applicant:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data.get("applicant", data)
        except AttributeError:
            self.data = None

    @property
    def status(self) -> Union[int, None]:
        """Returns the status of the applicant."""
        return self.data.get("status")
    
    @property
    def uid(self) -> Union[str, None]:
        """Returns the uid of the applicant."""
        return self.data.get("uid")
    
    @property
    def is_global(self) -> Union[bool, None]:
        """Returns whether the applicant is global."""
        return self.data.get("isGlobal")
    
    @property
    def role(self) -> Union[int, None]:
        """Returns the role of the applicant."""
        return self.data.get("role")
    
    @property
    def is_staff(self) -> Union[bool, None]:
        """Returns whether the applicant is staff."""
        return self.data.get("isStaff")
    
    @property
    def nickname(self) -> Union[str, None]:
        """Returns the nickname of the applicant."""
        return self.data.get("nickname")
    
    @property
    def icon(self) -> Union[str, None]:
        """Returns the icon of the applicant."""
        return self.data.get("icon")


class ApplicantList:
    def __init__(self, data: list) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    @property
    def status(self) -> Union[int, None]:
        """Returns the status of the applicant."""
        return [applicant.get("status") for applicant in self.data]
    
    @property
    def uid(self) -> Union[str, None]:
        """Returns the uid of the applicant."""
        return [applicant.get("uid") for applicant in self.data]
    
    @property
    def is_global(self) -> Union[bool, None]:
        """Returns whether the applicant is global."""
        return [applicant.get("isGlobal") for applicant in self.data]
    
    @property
    def role(self) -> Union[int, None]:
        """Returns the role of the applicant."""
        return [applicant.get("role") for applicant in self.data]
    
    @property
    def is_staff(self) -> Union[bool, None]:
        """Returns whether the applicant is staff."""
        return [applicant.get("isStaff") for applicant in self.data]
    
    @property
    def nickname(self) -> Union[str, None]:
        """Returns the nickname of the applicant."""
        return [applicant.get("nickname") for applicant in self.data]
    
    @property
    def icon(self) -> Union[str, None]:
        """Returns the icon of the applicant."""
        return [applicant.get("icon") for applicant in self.data]


class CommunityMembershipRequest:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    @property
    def status(self) -> Union[int, None]:
        """Returns the status of the community membership request."""
        return self.data.get("status")
    
    @property
    def request_id(self) -> Union[str, None]:
        """Returns the request id of the community membership request."""
        return self.data.get("requestId")
    
    @property
    def modified_time(self) -> Union[str, None]:
        """Returns the modified time of the community membership request."""
        return self.data.get("modifiedTime")
    
    @property
    def ndc_id(self) -> Union[int, None]:
        """Returns the ndc id of the community membership request."""
        return self.data.get("ndcId")
    
    @property
    def created_time(self) -> Union[str, None]:
        """Returns the created time of the community membership request."""
        return self.data.get("createdTime")
    
    @property
    def message(self) -> Union[str, None]:
        """Returns the message of the community membership request."""
        return self.data.get("message")
    
    @property
    def applicant(self) -> Union[Applicant, None]:
        """Returns the applicant of the community membership request."""
        return Applicant(self.data.get("applicant"))
    
    @property
    def uid(self) -> Union[str, None]:
        """Returns the uid of the community membership request."""
        return self.data.get("uid")


class CommunityMembershipRequestList:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data.get("communityMembershipRequestList", data)
        except AttributeError:
            self.data = None

    @property
    def parser(self) -> CommunityMembershipRequest:
        """Returns the parser of the community membership request list."""
        return CommunityMembershipRequest(self.data)
    
    @property
    def status(self) -> List[Union[int, None]]:
        """Returns the status of the community membership request list."""
        return [x.get("status") for x in self.data]
    
    @property
    def request_id(self) -> List[Union[str, None]]:
        """Returns the request id of the community membership request list."""
        return [x.get("requestId") for x in self.data]
    
    @property
    def modified_time(self) -> List[Union[str, None]]:
        """Returns the modified time of the community membership request list."""
        return [x.get("modifiedTime") for x in self.data]
    
    @property
    def comId(self) -> List[Union[int, None]]:
        """Returns the ndc id of the community membership request list."""
        return [x.get("ndcId") for x in self.data]
    
    @property
    def created_time(self) -> List[Union[str, None]]:
        """Returns the created time of the community membership request list."""
        return [x.get("createdTime") for x in self.data]
    
    @property
    def message(self) -> List[Union[str, None]]:
        """Returns the message of the community membership request list."""
        return [x.get("message") for x in self.data]
    
    @property
    def applicant(self) -> ApplicantList:
        """Returns the applicant of the community membership request list."""
        return ApplicantList([x.get("applicant") for x in self.data])
    
    @property
    def uid(self) -> List[Union[str, None]]:
        """Returns the uid of the community membership request list."""
        return [x.get("uid") for x in self.data]
    
    @property
    def userId(self) -> List[Union[str, None]]:
        """Returns the user id of the community membership request list."""
        return self.uid
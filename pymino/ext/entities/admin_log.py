from typing import Any, Dict, List, Optional

__all__ = (
    "AdminLog",
    "AdminLogList",
    "ExtData",
    "ExtDataList",
)


class ExtData:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def value(self) -> Dict[str, Any]:
        """Returns the value of the ext data"""
        return self.data.get("value") or {}

    @property
    def note(self) -> Optional[str]:
        """Returns the note the moderator/admin left on the request"""
        return self.data.get("note")

    def json(self) -> Dict[str, Any]:
        """Returns the raw json data"""
        return self.data


class ExtDataList:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = data

    @property
    def value(self) -> List[Dict[str, Any]]:
        """Returns a list of values of the ext data"""
        return [data.get("value") or {} for data in self.data]

    @property
    def note(self) -> List[Optional[str]]:
        """Returns a list of notes the moderator/admin left on the request"""
        return [note.get("note") for note in self.data]

    def json(self) -> List[Dict[str, Any]]:
        """Returns the raw json data"""
        return self.data


class AdminLog:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def operation_name(self) -> str:
        """Returns the name of the operation"""
        return self.data.get("operationName", "")

    @property
    def comId(self) -> int:
        """Returns the comId of the community the operation was performed on"""
        return self.data.get("ndcId", 0)

    @property
    def refer_ticket_id(self) -> int:
        """Returns the ticket id of the operation"""
        return self.data.get("referTicketId", 0)

    @property
    def object_url(self) -> Optional[str]:
        """Returns the url of the object the operation was performed on"""
        return self.data.get("objectUrl")

    @property
    def created_time(self) -> str:
        """Returns the time the operation was performed"""
        return self.data.get("createdTime", "")

    @property
    def ext_data(self) -> ExtData:
        """Returns the ext data of the operation"""
        return ExtData(self.data.get("extData") or {})

    @property
    def operation_level(self) -> int:
        """Returns the level of the operation"""
        return self.data.get("operationLevel", 0)

    @property
    def operation_id(self) -> int:
        """Returns the id of the operation"""
        return self.data.get("operation", 0)

    @property
    def object_type(self) -> int:
        """Returns the type of the object the operation was performed on"""
        return self.data.get("objectType", 0)

    @property
    def operation_details(self) -> Optional[str]:
        """Returns the details of the operation"""
        return self.data.get("operationDetail")

    @property
    def log_id(self) -> int:
        """Returns the log id of the operation"""
        return self.data.get("logId", 0)

    @property
    def moderation_level(self) -> int:
        """Returns the moderation level of the operation"""
        return self.data.get("moderationLevel", 0)

    @property
    def objectId(self) -> int:
        """Returns the object id of the operation"""
        return self.data.get("objectId", 0)

    @property
    def moderator(self) -> Dict[str, Any]:
        """Returns the moderator of the operation"""
        return self.data.get("author") or {}

    @property
    def moderator_username(self) -> str:
        """Returns the username of the moderator of the operation"""
        return self.moderator.get("nickname", "")

    @property
    def moderator_uid(self) -> str:
        """Returns the uid of the moderator of the operation"""
        return self.moderator.get("uid", "")

    @property
    def moderator_icon(self) -> Optional[str]:
        """Returns the icon of the moderator of the operation"""
        return self.moderator.get("icon")

    def json(self) -> Dict[str, Any]:
        """Returns the raw json data"""
        return self.data


class AdminLogList:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def parser(self) -> List[AdminLog]:
        """Returns a list of AdminLog objects"""
        adminLogList: List[Dict[str, Any]] = self.data.get("adminLogList") or []
        return [AdminLog(i) for i in adminLogList]

    @property
    def paging(self) -> Dict[str, Any]:
        """Returns the paging data"""
        return self.data.get("paging") or {}

    @property
    def next_page_token(self) -> Optional[str]:
        """Returns the next page token"""
        return self.paging.get("nextPageToken")

    @property
    def prev_page_token(self) -> Optional[str]:
        """Returns the previous page token"""
        return self.paging.get("prevPageToken")

    @property
    def operation_name(self) -> List[str]:
        """Returns a list of operation names"""
        return [i.operation_name for i in self.parser()]

    @property
    def comId(self) -> List[int]:
        """Returns a list of comIds"""
        return [i.comId for i in self.parser()]

    @property
    def refer_ticket_id(self) -> List[int]:
        """Returns a list of ticket ids"""
        return [i.refer_ticket_id for i in self.parser()]

    @property
    def object_url(self) -> List[Optional[str]]:
        """Returns a list of object urls"""
        return [i.object_url for i in self.parser()]

    @property
    def created_time(self) -> List[str]:
        """Returns a list of created times"""
        return [i.created_time for i in self.parser()]

    @property
    def ext_data(self) -> ExtDataList:
        """Returns a list of ExtData objects"""
        return ExtDataList([i.ext_data.json() for i in self.parser()])

    @property
    def operation_level(self) -> List[int]:
        """Returns a list of operation levels"""
        return [i.operation_level for i in self.parser()]

    @property
    def operation_id(self) -> List[int]:
        """Returns a list of operation ids"""
        return [i.operation_id for i in self.parser()]

    @property
    def object_type(self) -> List[int]:
        """Returns a list of object types"""
        return [i.object_type for i in self.parser()]

    @property
    def operation_details(self) -> List[Optional[str]]:
        """Returns a list of operation details"""
        return [i.operation_details for i in self.parser()]

    @property
    def log_id(self) -> List[int]:
        """Returns a list of log ids"""
        return [i.log_id for i in self.parser()]

    @property
    def moderation_level(self) -> List[int]:
        """Returns a list of moderation levels"""
        return [i.moderation_level for i in self.parser()]

    @property
    def objectId(self) -> List[int]:
        """Returns a list of object ids"""
        return [i.objectId for i in self.parser()]

    @property
    def moderator(self) -> List[Dict[str, Any]]:
        """Returns a list of moderators"""
        return [i.moderator for i in self.parser()]

    @property
    def moderator_username(self) -> List[str]:
        """Returns a list of moderator usernames"""
        return [i.moderator_username for i in self.parser()]

    @property
    def moderator_uid(self) -> List[str]:
        """Returns a list of moderator uids"""
        return [i.moderator_uid for i in self.parser()]

    @property
    def moderator_icon(self) -> List[Optional[str]]:
        """Returns a list of moderator icons"""
        return [i.moderator_icon for i in self.parser()]

    def json(self) -> Dict[str, Any]:
        """Returns the raw json data"""
        return self.data

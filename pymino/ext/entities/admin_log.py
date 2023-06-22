from typing import List


class ExtData:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    def _check_ext_data(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper

    @property
    @_check_ext_data
    def value(self) -> dict:
        """Returns the value of the ext data"""
        return self.data.get("value")   

    @property
    @_check_ext_data
    def note(self) -> int:
        """Returns the note the moderator/admin left on the request"""
        return self.data.get("note")
    
    def json(self) -> dict:
        """Returns the raw json data"""
        return self.data
    

class ExtDataList:
    def __init__(self, data: list) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    def _check_ext_data_list(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper

    @property
    @_check_ext_data_list
    def value(self) -> List[dict]:
        """Returns a list of values of the ext data"""
        return [data.get("value") if data is not None else None for data in self.data]

    @property
    @_check_ext_data_list
    def note(self) -> List[str]:
        """Returns a list of notes the moderator/admin left on the request"""
        return [str(note.get("note")) if note is not None else None for note in self.data]
    
    def json(self) -> List[dict]:
        """Returns the raw json data"""
        return self.data


class AdminLog:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    def _check_admin_log(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper

    @property
    @_check_admin_log
    def operation_name(self) -> str:
        """Returns the name of the operation"""
        return self.data.get("operationName")

    @property
    @_check_admin_log
    def comId(self) -> int:
        """Returns the comId of the community the operation was performed on"""
        return self.data.get("comId")

    @property
    @_check_admin_log
    def refer_ticket_id(self) -> int:
        """Returns the ticket id of the operation"""
        return self.data.get("referTicketId")

    @property
    @_check_admin_log
    def object_url(self) -> str:
        """Returns the url of the object the operation was performed on"""
        return self.data.get("objectUrl")

    @property
    @_check_admin_log
    def created_time(self) -> str:
        """Returns the time the operation was performed"""
        return self.data.get("createdTime")

    @property
    @_check_admin_log
    def ext_data(self) -> ExtData:
        """Returns the ext data of the operation"""
        return ExtData(self.data.get("extData"))

    @property
    @_check_admin_log
    def operation_level(self) -> int:
        """Returns the level of the operation"""
        return self.data.get("operationLevel")

    @property
    @_check_admin_log
    def operation_id(self) -> int:
        """Returns the id of the operation"""
        return self.data.get("operation")

    @property
    @_check_admin_log
    def object_type(self) -> int:
        """Returns the type of the object the operation was performed on"""
        return self.data.get("objectType")

    @property
    @_check_admin_log
    def operation_details(self) -> str:
        """Returns the details of the operation"""
        return self.data.get("operationDetail")

    @property
    @_check_admin_log
    def log_id(self) -> int:
        """Returns the log id of the operation"""
        return self.data.get("logId")

    @property
    @_check_admin_log
    def moderation_level(self) -> int:
        """Returns the moderation level of the operation"""
        return self.data.get("moderationLevel")

    @property
    @_check_admin_log
    def objectId(self) -> int:
        """Returns the object id of the operation"""
        return self.data.get("objectId")

    @property
    @_check_admin_log
    def moderator(self) -> dict:
        """Returns the moderator of the operation"""
        return self.data.get("author")

    @property
    @_check_admin_log
    def moderator_username(self) -> str:
        """Returns the username of the moderator of the operation"""
        return None if self.moderator is None else self.moderator.get("nickname")

    @property
    @_check_admin_log
    def moderator_uid(self) -> str:
        """Returns the uid of the moderator of the operation"""
        return None if self.moderator is None else self.moderator.get("uid")

    @property
    @_check_admin_log
    def moderator_icon(self) -> str:
        """Returns the icon of the moderator of the operation"""
        return None if self.moderator is None else self.moderator.get("icon")

    def json(self) -> dict:
        """Returns the raw json data"""
        return self.data
    

class AdminLogList:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    def parser(self) -> List[AdminLog]:
        """Returns a list of AdminLog objects"""
        return [AdminLog(i) for i in self.data.get("adminLogList")]
    
    @property
    def paging(self) -> dict:
        """Returns the paging data"""
        return self.data.get("paging")
    
    @property
    def next_page_token(self) -> int:
        """Returns the next page token"""
        return self.paging.get("nextPageToken")
    
    @property
    def prev_page_token(self) -> int:
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
    def object_url(self) -> List[str]:
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
    def operation_details(self) -> List[str]:
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
    def moderator(self) -> List[dict]:
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
    def moderator_icon(self) -> str:
        """Returns a list of moderator icons"""
        return [i.moderator_icon for i in self.parser()]

    def json(self) -> dict:
        """Returns the raw json data"""
        return self.data
from typing import List


class ChatThreadExtensions:
    def __init__(self, data: dict):
        try:
            self.data = data.get("extensions", data)
        except AttributeError:
            self.data = None

    
    def _check_extensions(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper
    

    @property
    @_check_extensions
    def is_view_only(self) -> bool:
        """Returns whether the chat is view only"""
        return self.data.get("viewOnly")

    @property
    @_check_extensions
    def coHosts(self) -> List[str]:
        """Returns a list of co-host uids"""
        return self.data.get("coHost")
    
    @property
    @_check_extensions
    def coHost(self) -> str:
        #NOTE: This will be removed in the future
        """Returns the co-host uid"""
        return self.data.get("coHost")

    @property
    @_check_extensions
    def language(self) -> str:
        """Returns the language of the chat"""
        return self.data.get("language")
    
    @property
    @_check_extensions
    def is_members_can_invite(self) -> bool:
        """Returns whether members can invite others"""
        return self.data.get("membersCanInvite")
    
    @property
    @_check_extensions
    def screening_room_permission(self) -> dict:
        """Returns the screening room permission"""
        return self.data.get("screeningRoomPermission")
    
    @property
    @_check_extensions
    def background(self) -> str:
        """Returns the background of the chat"""
        try:
            return self.data.get("bm")[1]
        except IndexError:
            return None

    @property
    @_check_extensions
    def avchat_member_user_id_list(self) -> List[str]:
        """Returns a list of avchat member uids"""
        return self.data.get("avchatMemberUidList")

    @property
    @_check_extensions
    def screening_room_host_user_id(self) -> str:
        """Returns the screening room host uid"""
        return self.data.get("screeningRoomHostUid")

    @property
    @_check_extensions
    def visibility(self) -> int:
        """Returns the visibility of the chat"""
        return self.data.get("visibility")

    @property
    @_check_extensions
    def banned_user_ids(self) -> List[str]:
        """Returns a list of banned member uids"""
        return self.data.get("bannedMemberUidList")

    @property
    @_check_extensions
    def last_message_time(self) -> int:
        """Returns the last members summary update time"""
        return self.data.get("lastMembersSummaryUpdateTime")

    @property
    @_check_extensions
    def is_fans_only(self) -> bool:
        """Returns whether the chat is fans only"""
        return self.data.get("fansOnly")

    @property
    @_check_extensions
    def announcement(self) -> str:
        """Returns the announcement of the chat"""
        return self.data.get("announcement")

    @property
    @_check_extensions
    def last_update_time(self) -> int:
        """Returns the channel type last created time"""
        return self.data.get("channelTypeLastCreatedTime")
    
    @property
    @_check_extensions
    def avchatId(self) -> str:
        """Returns the avchat id"""
        return self.data.get("avchatId")
    
    @property
    @_check_extensions
    def channel_type(self) -> int:
        """Returns the channel type"""
        return self.data.get("channelType")
    
    @property
    @_check_extensions
    def is_announcement_pinned(self) -> bool:
        """Returns whether the chat announcement is pinned"""
        return self.data.get("pinAnnouncement")
    
    @property
    @_check_extensions
    def voice_chat_join_type(self) -> int:
        """Returns the vv chat join type"""
        return self.data.get("vvChatJoinType")
    
    @property
    @_check_extensions
    def tipping_perm_status(self) -> int:
        """Returns the tipping permission status"""
        return self.data.get("tippingPermStatus")
    
    @_check_extensions
    def json(self) -> dict:
        """Returns the json data"""
        return self.data


class ChatThreadExtensionsList:
    def __init__(self, data: list):
        try:
            self.data = data
        except AttributeError:
            self.data = None

    @property
    def is_view_only(self) -> List[bool]:
        """Returns a list of whether the chat is view only"""
        return [i.get("viewOnly") if i else None for i in self.data]
    
    @property
    def co_host_user_ids(self) -> List[List[str]]:
        """Returns a list of co-host uids"""
        return [i.get("coHost") if i else None for i in self.data]
    
    @property
    def language(self) -> List[str]:
        """Returns a list of the language of the chat"""
        return [i.get("language") if i else None for i in self.data]
    
    @property
    def is_members_can_invite(self) -> List[bool]:
        """Returns a list of whether members can invite others"""
        return [i.get("membersCanInvite") if i else None for i in self.data]
    
    @property
    def screening_room_permission(self) -> List[dict]:
        """Returns a list of the screening room permission"""
        return [i.get("screeningRoomPermission") if i else None for i in self.data]
    
    @property
    def background(self) -> List[str]:
        """Returns a list of the background of the chat"""
        return [i.get("bm")[1] if i and isinstance(i.get("bm"), list) else None for i in self.data]
    
    @property
    def avchat_member_user_id_list(self) -> List[List[str]]:
        """Returns a list of avchat member uids"""
        return [i.get("avchatMemberUidList") if i else None for i in self.data]
    
    @property
    def screening_room_host_user_id(self) -> List[str]:
        """Returns a list of the screening room host uid"""
        return [i.get("screeningRoomHostUid") if i else None for i in self.data]
    
    @property
    def visibility(self) -> List[int]:
        """Returns a list of the visibility of the chat"""
        return [i.get("visibility") if i else None for i in self.data]
    
    @property
    def banned_user_ids(self) -> List[List[str]]:
        """Returns a list of banned member uids"""
        return [i.get("bannedMemberUidList") if i else None for i in self.data]
    
    @property
    def last_message_time(self) -> List[int]:
        """Returns a list of the last members summary update time"""
        return [i.get("lastMembersSummaryUpdateTime") if i else None for i in self.data]
    
    @property
    def is_fans_only(self) -> List[bool]:
        """Returns a list of whether the chat is fans only"""
        return [i.get("fansOnly") if i else None for i in self.data]
    
    @property
    def announcement(self) -> List[str]:
        """Returns the announcement of the chat"""
        return [i.get("announcement") if i else None for i in self.data]

    @property
    def last_update_time(self) -> List[int]:
        """Returns the channel type last created time"""
        return [i.get("channelTypeLastCreatedTime") if i else None for i in self.data]
    
    @property
    def avchatId(self) -> List[str]:
        """Returns the avchat id"""
        return [i.get("avchatId") if i else None for i in self.data]
    
    @property
    def channel_type(self) -> List[int]:
        """Returns the channel type"""
        return [i.get("channelType") if i else None for i in self.data]
    
    @property
    def is_announcement_pinned(self) -> List[bool]:
        """Returns whether the chat announcement is pinned"""
        return [i.get("pinAnnouncement") if i else None for i in self.data]
    
    @property
    def voice_chat_join_type(self) -> List[int]:
        """Returns the vv chat join type"""
        return [i.get("vvChatJoinType") if i else None for i in self.data]
    
    @property
    def tipping_perm_status(self) -> List[int]:
        """Returns the tipping permission status"""
        return [i.get("tippingPermStatus") if i else None for i in self.data]
    
    def json(self) -> dict:
        """Returns the json data"""
        return self.data


class MemberSummary:
    def __init__(self, data: dict):
        try:
            self.data = data.get("membersSummary", data)
        except AttributeError:
            self.data = None


    def _check_memberSummary(F):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else F(*args, **kwargs)
        return wrapper


    @property
    @_check_memberSummary
    def status(self) -> List[int]:
        """Returns a list of member statuses"""
        return [i.get("status") for i in self.data]

    @property
    @_check_memberSummary
    def uid(self) -> List[str]:
        """Returns a list of member uids"""
        return [i.get("uid") for i in self.data]
    
    @property
    @_check_memberSummary
    def userId(self) -> List[str]:
        """Returns a list of member user ids"""
        return self.uid

    @property
    @_check_memberSummary
    def membership_status(self) -> List[int]:
        """Returns a list of member membership statuses"""
        return [i.get("membershipStatus") for i in self.data]

    @property
    @_check_memberSummary
    def role(self) -> List[int]:
        """Returns a list of member roles"""
        return [i.get("role") for i in self.data]

    @property
    @_check_memberSummary
    def nickname(self) -> List[str]:
        """Returns a list of member nicknames"""
        return [i.get("nickname") for i in self.data]
    
    @property
    @_check_memberSummary
    def username(self) -> List[str]:
        """Returns a list of member usernames"""
        return self.nickname

    @property
    @_check_memberSummary
    def icon(self) -> List[str]:
        """Returns a list of member icons"""
        return [i.get("icon") for i in self.data]
    
    @property
    @_check_memberSummary
    def avatar(self) -> List[str]:
        """Returns a list of member avatars"""
        return self.icon

    @_check_memberSummary
    def json(self) -> List[dict]:
        """Returns a list of member summaries"""
        return self.data


class MemberSummaryList:
    def __init__(self, data: list):
        try:
            self.data = data
        except AttributeError:
            self.data = None
    
    @property
    def status(self) -> List[List[int]]:
        """Returns a list of member statuses"""
        return [[x.get("status") for x in y] for y in self.data]
    
    @property
    def uid(self) -> List[str]:
        """Returns a list of member uids"""
        return [[x.get("uid") for x in y] for y in self.data]
    
    @property
    def userId(self) -> List[str]:
        """Returns a list of member user ids"""
        return self.uid
    
    @property
    def membershipStatus(self) -> List[int]:
        """Returns a list of member membership statuses"""
        return [[x.get("membershipStatus") for x in y] for y in self.data]
    
    @property
    def role(self) -> List[int]:
        """Returns a list of member roles"""
        return [[x.get("role") for x in y] for y in self.data]
    
    @property
    def nickname(self) -> List[str]:
        """Returns a list of member nicknames"""
        return [[x.get("nickname") for x in y] for y in self.data]
    
    @property
    def username(self) -> List[str]:
        """Returns a list of member usernames"""
        return self.nickname
    
    @property
    def icon(self) -> List[str]:
        """Returns a list of member icons"""
        return [[x.get("icon") for x in y] for y in self.data]
    
    @property
    def avatar(self) -> List[str]:
        """Returns a list of member avatars"""
        return self.icon
    
    def json(self) -> List[dict]:
        """Returns a list of member summaries"""
        return self.data


class ChatThread: 
    def __init__(self, data: dict):
        try:
            self.data = data.get("thread", data)
        except AttributeError:
            self.data = None

    
    @property
    def user_added_topic_list(self) -> List[str]:
        """Returns a list of user added topics"""
        return self.data.get("userAddedTopicList")
    
    @property
    def uid(self) -> str:
        """Returns the host user id"""
        return self.data.get("uid")
    
    @property
    def host_user_id(self) -> str:
        """Returns the host user id"""
        return self.uid
    
    @property
    def hostUserId(self) -> str:
        #NOTE: This will be removed in the future
        return self.uid
    
    @property
    def members_quota(self) -> int:
        """Returns the members quota"""
        return self.data.get("membersQuota")
    
    @property
    def members_summary(self) -> MemberSummary:
        """Returns the members summary"""
        return MemberSummary(self.data.get("membersSummary"))
    
    @property
    def threadId(self) -> str:
        """Returns the thread id"""
        return self.data.get("threadId")
    
    @property
    def chatId(self) -> str:
        """Returns the thread id"""
        return self.threadId
    
    @property
    def keywords(self) -> List[str]:
        """Returns a list of keywords"""
        return self.data.get("keywords")
    
    @property
    def members_count(self) -> int:
        """Returns the members count"""
        return self.data.get("membersCount")
    
    @property
    def strategy_info(self) -> dict:
        """Returns the strategy info"""
        return self.data.get("strategyInfo")
    
    @property
    def is_pinned(self) -> bool:
        """Returns whether the chat is pinned"""
        return self.data.get("isPinned")
    
    @property
    def title(self) -> str:
        """Returns the chat title"""
        return self.data.get("title")
    
    @property
    def membership_status(self) -> str:
        """Returns the membership status"""
        return self.data.get("membershipStatus")
    
    @property
    def content(self) -> str:
        """Returns the chat content"""
        return self.data.get("content")
    
    @property
    def is_hidden_required(self) -> bool:
        """Returns whether the chat needs to be hidden"""
        return self.data.get("needHidden")

    @property
    def alert_option(self) -> int:
        """Returns the alert option"""
        return self.data.get("alertOption")
    
    @property
    def last_read_time(self) -> str:
        """Returns the last read time"""
        return self.data.get("lastReadTime")
    
    @property
    def type(self) -> int:
        """Returns the chat type"""
        return self.data.get("type")
    
    @property
    def status(self) -> int:
        """Returns the chat status"""
        return self.data.get("status")
    
    @property
    def is_published_to_global(self) -> bool:
        """Returns whether the chat is published to global"""
        return self.data.get("publishToGlobal")
    
    @property
    def modified_time(self) -> str:
        """Returns the modified time"""
        return self.data.get("modifiedTime")
    
    @property
    def last_message_summary(self) -> dict:
        """Returns the last message summary"""
        return self.data.get("lastMessageSummary")
    
    @property
    def extensions(self) -> ChatThreadExtensions:
        """Returns the chat thread extensions"""
        return ChatThreadExtensions(self.data.get("extensions"))

    def json(self) -> dict:
        """Returns the chat thread json"""
        return self.data


class ChatThreadList:
    def __init__(self, data: dict):
        self.data = data.get("threadList", data)

    def parser(self) -> List[ChatThread]:
        """Returns a list of ChatThread objects"""
        return [ChatThread(x) for x in self.data]
    
    
    @property
    def extensions(self) -> ChatThreadExtensions:
        """Returns the chat thread extensions"""
        return ChatThreadExtensionsList([x.get("extensions") for x in self.data])
    
    @property
    def members_summary(self) -> MemberSummary:
        """Returns the members summary"""
        return MemberSummaryList([x.get("membersSummary") for x in self.data])
    
    @property
    def user_added_topic_list(self) -> List[str]:
        """Returns a list of user added topics"""
        return [x.user_added_topic_list for x in self.parser()]
    
    @property
    def uid(self) -> List[str]:
        """Returns a list of host user ids"""
        return [x.uid for x in self.parser()]
    
    @property
    def host_user_id(self) -> List[str]:
        """Returns a list of host user ids"""
        return self.uid
    
    @property
    def members_quota(self) -> List[int]:
        """Returns a list of members quotas"""
        return [x.members_quota for x in self.parser()]
    
    @property
    def threadId(self) -> List[str]:
        """Returns a list of thread ids"""
        return [x.threadId for x in self.parser()]
    
    @property
    def chatId(self) -> List[str]:
        """Returns a list of thread ids"""
        return self.threadId
    
    @property
    def keywords(self) -> List[List[str]]:
        """Returns a list of keywords"""
        return [x.keywords for x in self.parser()]
    
    @property
    def members_count(self) -> List[int]:
        """Returns a list of members counts"""
        return [x.members_count for x in self.parser()]
    
    @property
    def strategy_info(self) -> List[dict]:
        """Returns a list of strategy info"""
        return [x.strategy_info for x in self.parser()]
    
    @property
    def is_pinned(self) -> List[bool]:
        """Returns a list of whether the chat is pinned"""
        return [x.is_pinned for x in self.parser()]
    
    @property
    def title(self) -> List[str]:
        """Returns a list of chat titles"""
        return [x.title for x in self.parser()]
    
    @property
    def membership_status(self) -> List[str]:
        """Returns a list of membership statuses"""
        return [x.membership_status for x in self.parser()]
    
    @property
    def content(self) -> List[str]:
        """Returns a list of chat contents"""
        return [x.content for x in self.parser()]
    
    @property
    def is_hidden_required(self) -> List[bool]:
        """Returns a list of whether the chat needs to be hidden"""
        return [x.is_hidden_required for x in self.parser()]
    
    @property
    def alert_option(self) -> List[int]:
        """Returns a list of alert options"""
        return [x.alert_option for x in self.parser()]
    
    @property
    def last_read_time(self) -> List[str]:
        """Returns a list of last read times"""
        return [x.last_read_time for x in self.parser()]
    
    @property
    def type(self) -> List[int]:
        """Returns a list of chat types"""
        return [x.type for x in self.parser()]
    
    @property
    def status(self) -> List[int]:
        """Returns a list of chat statuses"""
        return [x.status for x in self.parser()]
    
    @property
    def is_published_to_global(self) -> List[bool]:
        """Returns a list of whether the chat is published to global"""
        return [x.is_published_to_global for x in self.parser()]
    
    @property
    def modified_time(self) -> List[str]:
        """Returns a list of modified times"""
        return [x.modified_time for x in self.parser()]
    
    @property
    def last_message_summary(self) -> List[dict]:
        """Returns a list of last message summaries"""
        return [x.last_message_summary for x in self.parser()]
    
    def json(self) -> dict:
        """Returns the chat thread list json"""
        return self.data
    

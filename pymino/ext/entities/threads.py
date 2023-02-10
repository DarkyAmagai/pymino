class CThreadExtensions:
    def __init__(self, data: dict):
        self.data = data
        parser = self.__parser__ if isinstance(self.data, list) else lambda key, default=None: self.data.get(key, default)
        self.coHost:                        list = parser('coHost', None)
        self.language:                      str = parser('language', None)
        self.membersCanInvite:              int = parser('membersCanInvite', None)
        self.background:                    list = parser('bm', None)
        self.creatorUid:                    str = parser('creatorUid', None)
        self.visibility:                    int = parser('visibility', None)
        self.lastMembersSummaryUpdateTime:  dict = parser('lastMembersSummaryUpdateTime', None)
        self.fansOnly:                      bool = parser('fansOnly', None)
        self.channelType:                   int = parser('channelType', None)
        self.vvChatJoinType:                int = parser('vvChatJoinType', None)
        self.avchatMemberUidList:           list = parser('avchatMemberUidList', None)
        self.screeningRoomPermission:       dict = parser('screeningRoomPermission', None)
        self.disabledTime:                  int = parser('__disabledTime__', None)

    def __parser__(self, key: str, default=None): return [i.get(key, default) for i in self.data]

    def json(self): return self.data

class MemberSummary:
    def __init__(self, data: dict):
        self.data = data[0] if isinstance(data[0], list) else data
            
        self.status:            list = [x.get("status") for x in self.data]
        self.uid:               list = [x.get("uid") for x in self.data]
        self.userId:            list = self.uid
        self.membershipStatus:  list = [x.get("membershipStatus") for x in self.data]
        self.role:              list = [x.get("role") for x in self.data]
        self.nickname:          list = [x.get("nickname") for x in self.data]
        self.username:          list = self.nickname
        self.icon:              list = [x.get("icon") for x in self.data]
        self.avatar:            list = self.icon

    def json(self): return self.data

class CThread: 
    def __init__(self, data: dict):
        self.data:                  dict = data.get("thread", data)
        self.userAddedTopicList:    list = self.data.get("userAddedTopicList")
        self.uid:                   str = self.data.get("uid")
        self.hostUserId:            str = self.uid
        self.membersQuota:          int = self.data.get("membersQuota")
        self.membersSummary:        MemberSummary = MemberSummary(self.data.get("membersSummary"))
        self.threadId:              str = self.data.get("threadId")
        self.chatId:                str = self.threadId
        self.keywords:              list = self.data.get("keywords")
        self.membersCount:          int = self.data.get("membersCount")
        self.strategyInfo:          dict = self.data.get("strategyInfo")
        self.isPinned:              bool = self.data.get("isPinned")
        self.title:                 str = self.data.get("title")
        self.membershipStatus:      str = self.data.get("membershipStatus")
        self.content:               str = self.data.get("content")
        self.needHidden:            bool = self.data.get("needHidden")
        self.alertOption:           int = self.data.get("alertOption")
        self.lastReadTime:          str = self.data.get("lastReadTime")
        self.type:                  int = self.data.get("type")
        self.status:                int = self.data.get("status")
        self.publishToGlobal:       bool = self.data.get("publishToGlobal")
        self.modifiedTime:          str = self.data.get("modifiedTime")
        self.lastMessageSummary:    dict = self.data.get("lastMessageSummary")
        self.extensions:            CThreadExtensions = CThreadExtensions(self.data.get("extensions"))

    def json(self): return self.data

class CThreadList:
    def __init__(self, data: dict):
        self.data:                  dict = data.get("threadList", data)
        parser:                     list = [CThread(x) for x in self.data]
        self.extensions:            CThreadExtensions = CThreadExtensions([x.extensions.json() for x in parser])
        self.membersSummary:        MemberSummary = MemberSummary([x.membersSummary.json() for x in parser])
        self.userAddedTopicList:    list = [x.userAddedTopicList for x in parser]
        self.uid:                   list = [x.uid for x in parser]
        self.hostUserId:            list = [x.hostUserId for x in parser]
        self.membersQuota:          list = [x.membersQuota for x in parser]
        self.threadId:              list = [x.threadId for x in parser]
        self.chatId:                list = [x.chatId for x in parser]
        self.keywords:              list = [x.keywords for x in parser]
        self.membersCount:          list = [x.membersCount for x in parser]
        self.strategyInfo:          list = [x.strategyInfo for x in parser]
        self.isPinned:              list = [x.isPinned for x in parser]
        self.title:                 list = [x.title for x in parser]
        self.membershipStatus:      list = [x.membershipStatus for x in parser]
        self.content:               list = [x.content for x in parser]
        self.needHidden:            list = [x.needHidden for x in parser]
        self.alertOption:           list = [x.alertOption for x in parser]
        self.lastReadTime:          list = [x.lastReadTime for x in parser]
        self.type:                  list = [x.type for x in parser]
        self.status:                list = [x.status for x in parser]
        self.publishToGlobal:       list = [x.publishToGlobal for x in parser]
        self.modifiedTime:          list = [x.modifiedTime for x in parser]
        self.lastMessageSummary:    list = [x.lastMessageSummary for x in parser]

    def json(self): return self.data

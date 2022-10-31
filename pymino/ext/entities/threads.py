class CThreadExtensions:
    def __init__(self, data: dict):
        self.data = data
        parser = self.__parser__ if isinstance(self.data, list) else self.data.get
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
            
        self.status:            list = [x.get("status", None) for x in self.data]
        self.uid:               list = [x.get("uid", None) for x in self.data]
        self.userId:            list = self.uid
        self.membershipStatus:  list = [x.get("membershipStatus", None) for x in self.data]
        self.role:              list = [x.get("role", None) for x in self.data]
        self.nickname:          list = [x.get("nickname", None) for x in self.data]
        self.username:          list = self.nickname
        self.icon:              list = [x.get("icon", None) for x in self.data]
        self.avatar:            list = self.icon

    def json(self): return self.data

class CThread: 
    def __init__(self, data: dict):
        self.data:                  dict = data.get("thread", data)
        self.userAddedTopicList:    list = self.data.get("userAddedTopicList", None)
        self.uid:                   str = self.data.get("uid", None)
        self.hostUserId:            str = self.uid
        self.membersQuota:          int = self.data.get("membersQuota", None)
        self.membersSummary:        MemberSummary = MemberSummary(self.data.get("membersSummary", None))
        self.threadId:              str = self.data.get("threadId", None)
        self.chatId:                str = self.threadId
        self.keywords:              list = self.data.get("keywords", None)
        self.membersCount:          int = self.data.get("membersCount", None)
        self.strategyInfo:          dict = self.data.get("strategyInfo", None)
        self.isPinned:              bool = self.data.get("isPinned", None)
        self.title:                 str = self.data.get("title", None)
        self.membershipStatus:      str = self.data.get("membershipStatus", None)
        self.content:               str = self.data.get("content", None)
        self.needHidden:            bool = self.data.get("needHidden", None)
        self.alertOption:           int = self.data.get("alertOption", None)
        self.lastReadTime:          str = self.data.get("lastReadTime", None)
        self.type:                  int = self.data.get("type", None)
        self.status:                int = self.data.get("status", None)
        self.publishToGlobal:       bool = self.data.get("publishToGlobal", None)
        self.modifiedTime:          str = self.data.get("modifiedTime", None)
        self.lastMessageSummary:    dict = self.data.get("lastMessageSummary", None)
        self.extensions:            CThreadExtensions = CThreadExtensions(self.data.get("extensions", None))

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

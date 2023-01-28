from time import time
from re import findall
from typing import Union

class PrepareMessage:
    def __init__(self, **kwargs) -> None:
        self.base_message = {
            "content": kwargs.get("content", None),
            "mediaType": kwargs.get("mediaType", 0),
            "type": kwargs.get("type", 0),
            "clientRefId": int(time() / 10 % 1000000000),
            "timestamp": int(time() * 1000)
            }
        [self.base_message.update({key: kwargs[key]}) for key in kwargs]

    def json(self): return self.base_message

class MessageAuthor:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data                    = data
        self.uid                     = None
        self.userId                  = None
        self.status                  = None
        self.icon                    = None
        self.avatar                  = None
        self.reputation              = None
        self.role                    = None
        self.nickname                = None
        self.username                = None
        self.level                   = None
        self.accountMembershipStatus = None
        self.avatarFrame             = None

        if isinstance(data, dict):
            self.uid:                       Union[str, None] = self.data.get("uid", self.uid)
            self.userId:                    Union[str, None] = self.uid
            self.status:                    Union[int, None] = self.data.get("status", self.status)
            self.icon:                      Union[str, None] = self.data.get("icon", self.icon)
            self.avatar:                    Union[str, None] = self.icon
            self.reputation:                Union[int, None] = self.data.get("reputation", self.reputation)
            self.role:                      Union[int, None] = self.data.get("role", self.role)
            self.nickname:                  Union[str, None] = self.data.get("nickname", self.nickname)
            self.username:                  Union[str, None] = self.nickname
            self.level:                     Union[int, None] = self.data.get("level", self.level)
            self.accountMembershipStatus:   Union[int, None] = self.data.get("accountMembershipStatus", self.accountMembershipStatus)
            self.avatarFrame:               Union[str, None] = self.data.get("avatarFrame", self.avatarFrame)
        
    def json(self) -> Union[dict, str]:
        return self.data

class CMessage:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.includedInSummary = None
        self.uid               = None
        self.userId            = None
        self.author            = {}
        self.isHidden          = None
        self.messageId         = None
        self.mediaType         = None
        self.content           = None
        self.clientRefId       = None
        self.threadId          = None
        self.chatId            = None
        self.createdTime       = None
        self.extensions        = {}
        self.type              = None
        self.mediaValue        = None

        if isinstance(data, dict):
            self.data:                dict = data.get('result') or data.get('message', self.data)
            self.includedInSummary:   Union[bool, None] = self.data.get('includedInSummary', self.includedInSummary)
            self.uid:                 Union[str, None] = self.data.get('uid', self.uid)
            self.userId:              Union[str, None] = self.uid
            self.author:              Union[dict, None] = self.data.get('author', self.author)
            self.isHidden:            Union[bool, None] = self.data.get('isHidden', self.isHidden)
            self.messageId:           Union[str, None] = self.data.get('messageId', self.messageId)
            self.mediaType:           Union[int, None] = self.data.get('mediaType', self.mediaType)
            self.content:             Union[str, None] = self.data.get('content', self.content)
            self.clientRefId:         Union[int, None] = self.data.get('clientRefId', self.clientRefId)
            self.threadId:            Union[str, None] = self.data.get('threadId', self.threadId)
            self.chatId:              Union[str, None] = self.threadId
            self.createdTime:         Union[str, None] = self.data.get('createdTime', self.createdTime)
            self.extensions:          Union[dict, None] = self.data.get('extensions', self.extensions)
            self.type:                Union[int, None] = self.data.get('type', self.type)
            self.mediaValue:          Union[str, None] = self.data.get('mediaValue', self.mediaValue)

    def json(self) -> Union[dict, str]:
        return self.data

class CMessageAuthorList:
    def __init__(self, data: list) -> None:
        self.data:                    list = data
        self.status:                  list = [i.get('status', None) for i in self.data]
        self.icon:                    list = [i.get('icon', None) for i in self.data]
        self.avatar:                  list = self.icon
        self.reputation:              list = [i.get('reputation', None) for i in self.data]
        self.role:                    list = [i.get('role', None) for i in self.data]
        self.nickname:                list = [i.get('nickname', None) for i in self.data]
        self.username:                list = self.nickname
        self.level:                   list = [i.get('level', None) for i in self.data]
        self.accountMembershipStatus: list = [i.get('accountMembershipStatus', None) for i in self.data]
        self.avatarFrame:             list = [i.get('avatarFrame', None) for i in self.data]

    def json(self) -> Union[dict, str]:
        return self.data

class CMessages:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data              = data
        self.includedInSummary = None
        self.uid               = None
        self.userId            = None
        self.author            = {}
        self.isHidden          = None
        self.messageId         = None
        self.mediaType         = None
        self.content           = None
        self.clientRefId       = None
        self.threadId          = None
        self.chatId            = None
        self.createdTime       = None
        self.extensions        = {}
        self.type              = None
        self.mediaValue        = None

        if isinstance(data, dict):
            self.data:              dict = data.get('result') or data.get('messageList', self.data)
            self.includedInSummary: list = [i.get('includedInSummary', self.includedInSummary) for i in self.data]
            self.uid:               list = [i.get('uid', self.uid) for i in self.data]
            self.userId:            list = self.uid
            self.author:            list = CMessageAuthorList([i.get('author', self.author) for i in self.data])
            self.isHidden:          list = [i.get('isHidden', self.isHidden) for i in self.data]
            self.messageId:         list = [i.get('messageId', self.messageId) for i in self.data]
            self.mediaType:         list = [i.get('mediaType', self.mediaType) for i in self.data]
            self.content:           list = [i.get('content', self.content) for i in self.data]
            self.clientRefId:       list = [i.get('clientRefId', self.clientRefId) for i in self.data]
            self.threadId:          list = [i.get('threadId', self.threadId) for i in self.data]
            self.chatId:            list = self.threadId
            self.createdTime:       list = [i.get('createdTime', self.createdTime) for i in self.data]
            self.extensions:        list = [i.get('extensions', self.extensions) for i in self.data]
            self.type:              list = [i.get('type', self.type) for i in self.data]
            self.mediaValue:        list = [i.get('mediaValue', self.mediaValue) for i in self.data]
        
    def json(self) -> Union[dict, str]:
        return self.data

class Message:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data                   = data
        self.ndcId                  = None
        self.comId                  = None
        self.chatMessage            = {}
        self.author                 = {}
        self.mediaValue             = None
        self.threadId               = None
        self.chatId                 = None
        self.mediaType              = None
        self.content                = None
        self.clientRefId            = None
        self.messageId              = None
        self.uid                    = None
        self.userId                 = None
        self.createdTime            = None
        self.type                   = None
        self.isHidden               = None
        self.includedInSummary      = None
        self.chatBubbleId           = None
        self.chatBubbleVersion      = None
        self.extensions             = {}
        self.mentioned_userids      = []
        self.mentioned_usernames    = []
        self.mentioned_dictionary   = {}
        self.alertOption           = None
        self.membershipStatus      = None

        if isinstance(data, dict):
            self.data:                  dict = data.get("o", self.data)
            self.ndcId:                 Union[int, None] = self.data.get('ndcId', self.ndcId)
            self.comId:                 Union[int, None] = self.ndcId
            self.chatMessage:           Union[dict, None] = self.data.get('chatMessage', self.chatMessage)
            self.author:                MessageAuthor = MessageAuthor(self.chatMessage.get('author', self.author)) if self.chatMessage else self.author
            self.mediaValue:            Union[str, None] = self.chatMessage.get('mediaValue', self.mediaValue)
            self.threadId:              Union[str, None] = self.chatMessage.get('threadId', self.threadId)
            self.chatId:                Union[str, None] = self.threadId
            self.mediaType:             Union[int, None] = self.chatMessage.get('mediaType', self.mediaType)
            self.content:               Union[str, None] = self.chatMessage.get('content', self.content)
            self.clientRefId:           Union[int, None] = self.chatMessage.get('clientRefId', self.clientRefId)
            self.messageId:             Union[str, None] = self.chatMessage.get('messageId', self.messageId)
            self.uid:                   Union[str, None] = self.chatMessage.get('uid', self.uid)
            self.userId:                Union[str, None] = self.uid
            self.createdTime:           Union[str, None] = self.chatMessage.get('createdTime', self.createdTime)
            self.type:                  Union[int, None] = self.chatMessage.get('type', self.type)
            self.isHidden:              Union[bool, None] = self.chatMessage.get('isHidden', self.isHidden)
            self.includedInSummary:     Union[bool, None] = self.chatMessage.get('includedInSummary', self.includedInSummary)
            self.chatBubbleId:          Union[str, None] = self.chatMessage.get('chatBubbleId', self.chatBubbleId)
            self.chatBubbleVersion:     Union[int, None] = self.chatMessage.get('chatBubbleVersion', self.chatBubbleVersion)
            self.extensions:            Union[dict, None] = self.chatMessage.get('extensions', self.extensions)
            self.mentioned_userids:     Union[list, None] = [i.get('uid', None) for i in self.extensions.get('mentionedArray', None)] if self.extensions.get('mentionedArray', None) is not None else None
            self.mentioned_usernames:   Union[list, None] = findall(r'@([^\u202c\u202d]+)', self.content) if self.content is not None else None
            self.mentioned_dictionary:  Union[dict, None] = dict(zip(self.mentioned_userids, self.mentioned_usernames)) if self.mentioned_userids is not None and self.mentioned_usernames is not None else None
            self.alertOption:           Union[int, None] = self.data.get('alertOption', self.alertOption)
            self.membershipStatus:      Union[int, None] = self.data.get('membershipStatus', self.membershipStatus)
        
    def json(self) -> Union[dict, str]:
        return self.data

class Channel:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data            = data
        self.id              = None
        self.channelName     = None
        self.channelKey      = None
        self.channelUid      = None
        self.expiredTime     = None
        self.ndcId           = None
        self.threadId        = None
        self.chatId          = None

        if isinstance(data, dict):
            self.data:              dict = data.get("o", self.data)
            self.id:                Union[str, None] = self.data.get('id', self.id)
            self.channelName:       Union[str, None] = self.data.get('channelName', self.channelName)
            self.channelKey:        Union[str, None] = self.data.get('channelKey', self.channelKey)
            self.channelUid:        Union[int, None] = self.data.get('channelUid', self.channelUid)
            self.expiredTime:       Union[int, None] = self.data.get('expiredTime', self.expiredTime)
            self.ndcId:             Union[int, None] = self.data.get('ndcId', self.ndcId)
            self.threadId:          Union[str, None] = self.data.get('threadId', self.threadId)
            self.chatId:            Union[str, None] = self.threadId
        
    def json(self) -> Union[dict, str]:
        return self.data
from contextlib import suppress
from time import time
from re import findall

class PrepareMessage:
    def __init__(self, **kwargs):
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
    def __init__(self, data: dict):
        self.data = data
        self.uid:                         str = self.data.get("uid", None)
        self.userId:                      str = self.uid
        self.status:                      int = self.data.get("status", None)
        self.icon:                        str = self.data.get("icon", None)
        self.avatar:                      str = self.icon
        self.reputation:                  int = self.data.get("reputation", None)
        self.role:                        int = self.data.get("role", None)
        self.nickname:                    str = self.data.get("nickname", None)
        self.username:                    str = self.nickname
        self.level:                       int = self.data.get("level", None)
        self.accountMembershipStatus:     int = self.data.get("accountMembershipStatus", None)
        self.avatarFrame:                 str = self.data.get("avatarFrame", None)
        
    def json(self): return self.data

class CMessage:
    def __init__(self, data: dict):
        self.data:                dict = data.get('result') or data.get('message')
        self.includedInSummary:   str = self.data.get('includedInSummary', None)
        self.uid:                 str = self.data.get('uid', None)
        self.author:              MessageAuthor = MessageAuthor(self.data.get('author', None))
        self.isHidden:            bool = self.data.get('isHidden', None)
        self.messageId:           str = self.data.get('messageId', None)
        self.mediaType:           int = self.data.get('mediaType', None)
        self.content:             str = self.data.get('content', None)
        self.clientRefId:         int = self.data.get('clientRefId', None)
        self.threadId:            str = self.data.get('threadId', None)
        self.createdTime:         str = self.data.get('createdTime', None)
        self.extensions:          dict = self.data.get('extensions', None)
        self.type:                int = self.data.get('type', None)
        self.mediaValue:          str = self.data.get('mediaValue', None)

    def json(self): return self.data

class CMessageAuthorList:
    def __init__(self, data: list):
        with suppress(Exception):
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

    def json(self): return self.data

class CMessages:
    def __init__(self, data: dict):
        self.data:                   dict = data.get('messageList', data)
        self.includedInSummary:      list = [i.get('includedInSummary', None) for i in self.data]
        self.uid:                    list = [i.get('uid', None) for i in self.data]
        self.userId:                 list = self.uid
        self.author:                 list = CMessageAuthorList([i.get('author', None) for i in self.data])
        self.isHidden:               list = [i.get('isHidden', None) for i in self.data]
        self.messageId:              list = [i.get('messageId', None) for i in self.data]
        self.mediaType:              list = [i.get('mediaType', None) for i in self.data]
        self.content:                list = [i.get('content', None) for i in self.data]
        self.clientRefId:            list = [i.get('clientRefId', None) for i in self.data]
        self.threadId:               list = [i.get('threadId', None) for i in self.data]
        self.chatId:                 list = self.threadId
        self.createdTime:            list = [i.get('createdTime', None) for i in self.data]
        self.extensions:             list = [i.get('extensions', None) for i in self.data]
        self.type:                   list = [i.get('type', None) for i in self.data]
        self.mediaValue:             list = [i.get('mediaValue', None) for i in self.data]
        
    def json(self): return self.data

class Message:
    def __init__(self, data: dict):
        self.data:                 dict = data.get("o", data)
        self.ndcId:                int = self.data.get('ndcId', None)
        self.comId:                int = self.ndcId
        self.chatMessage:          dict = self.data.get('chatMessage', None)
        self.author:               MessageAuthor = MessageAuthor(self.chatMessage.get('author', None)) if self.chatMessage else None
        self.mediaValue:           str = self.chatMessage.get('mediaValue', None)
        self.threadId:             str = self.chatMessage.get('threadId', None)
        self.chatId:               str = self.threadId
        self.mediaType:            int = self.chatMessage.get('mediaType', None)
        self.content:              str = self.chatMessage.get('content', None)
        self.clientRefId:          int = self.chatMessage.get('clientRefId', None)
        self.messageId:            str = self.chatMessage.get('messageId', None)
        self.uid:                  str = self.chatMessage.get('uid', None)
        self.userId:               str = self.uid
        self.createdTime:          str = self.chatMessage.get('createdTime', None)
        self.type:                 int = self.chatMessage.get('type', None)
        self.isHidden:             bool = self.chatMessage.get('isHidden', None)
        self.includedInSummary:    bool = self.chatMessage.get('includedInSummary', None)
        self.chatBubbleId:         str = self.chatMessage.get('chatBubbleId', None)
        self.chatBubbleVersion:    int = self.chatMessage.get('chatBubbleVersion', None)
        self.extensions:           dict = self.chatMessage.get('extensions', None)
        self.mentioned_userids:    list = [i.get('uid', None) for i in self.extensions.get('mentionedArray', None)] if self.extensions.get('mentionedArray', None) is not None else None
        self.mentioned_usernames:  list = findall(r'@([^\u202c\u202d]+)', self.content) if self.content is not None else None
        self.mentioned_dictionary: dict = dict(zip(self.mentioned_userids, self.mentioned_usernames)) if self.mentioned_userids is not None and self.mentioned_usernames is not None else None
        self.alertOption:          int = self.data.get('alertOption', None)
        self.membershipStatus:     int = self.data.get('membershipStatus', None)
        
    def json(self): return self.data

class Channel:
    def __init__(self, data: dict):
        self.data:              dict = data.get("o", data)
        self.id:                str = self.data.get('id', None)
        self.channelName:       str = self.data.get('channelName', None)
        self.channelKey:        str = self.data.get('channelKey', None)
        self.channelUid:        int = self.data.get('channelUid', None)
        self.expiredTime:       int = self.data.get('expiredTime', None)
        self.ndcId:             int = self.data.get('ndcId', None)
        self.threadId:          str = self.data.get('threadId', None)
        self.chatId:            str = self.threadId
        
    def json(self): return self.data
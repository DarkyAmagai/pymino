from time import time

class PrepareMessage:
    def __init__(self, **kwargs):
        self.base_message = {
            "clientRefId": int(time() / 10 % 1000000000),
            "timestamp": int(time() * 1000),
            "type": kwargs.get("type", 0),
            "content": kwargs.get("content", None)
            }
        [self.base_message.update({key: kwargs[key]}) for key in kwargs]

    def json(self): return self.base_message

class MessageAuthor:
    def __init__(self, data: dict):
        self.data = data
        self.uid                         = self.data.get("uid", None)
        self.userId                      = self.uid
        self.status                      = self.data.get("status", None)
        self.icon                        = self.data.get("icon", None)
        self.avatar                      = self.icon
        self.reputation                  = self.data.get("reputation", None)
        self.role                        = self.data.get("role", None)
        self.nickname                    = self.data.get("nickname", None)
        self.username                    = self.nickname
        self.level                       = self.data.get("level", None)
        self.accountMembershipStatus     = self.data.get("accountMembershipStatus", None)
        self.avatarFrame                 = self.data.get("avatarFrame", None)
        
    def json(self): return self.data

class CMessage:
    def __init__(self, data: dict):
        self.data                = data.get('message', data)
        self.includedInSummary   = self.data.get('includedInSummary', None)
        self.uid                 = self.data.get('uid', None)
        self.author              = MessageAuthor(self.data.get('author', None))
        self.isHidden            = self.data.get('isHidden', None)
        self.messageId           = self.data.get('messageId', None)
        self.mediaType           = self.data.get('mediaType', None)
        self.content             = self.data.get('content', None)
        self.clientRefId         = self.data.get('clientRefId', None)
        self.threadId            = self.data.get('threadId', None)
        self.createdTime         = self.data.get('createdTime', None)
        self.extensions          = self.data.get('extensions', None)
        self.type                = self.data.get('type', None)
        self.mediaValue          = self.data.get('mediaValue', None)


    def json(self): return self.data

class CMessageAuthorList:
    def __init__(self, data: dict):
        self.data:                    dict = data
        self.uid:                     list = [i.get('uid', None) for i in self.data]
        self.userId:                  list = self.uid
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
        self.data:              dict = data.get("o", data)
        self.ndcId:             int = self.data.get('ndcId', None)
        self.comId:             int = self.ndcId
        self.chatMessage:       dict = self.data.get('chatMessage', None)
        self.author:            MessageAuthor = MessageAuthor(self.chatMessage.get('author', None))
        self.mediaValue:        str = self.chatMessage.get('mediaValue', None)
        self.threadId:          str = self.chatMessage.get('threadId', None)
        self.chatId:            str = self.threadId
        self.mediaType:         int = self.chatMessage.get('mediaType', None)
        self.content:           str = self.chatMessage.get('content', None)
        self.clientRefId:       int = self.chatMessage.get('clientRefId', None)
        self.messageId:         str = self.chatMessage.get('messageId', None)
        self.uid:               str = self.chatMessage.get('uid', None)
        self.userId:            str = self.uid
        self.createdTime:       str = self.chatMessage.get('createdTime', None)
        self.type:              int = self.chatMessage.get('type', None)
        self.isHidden:          bool = self.chatMessage.get('isHidden', None)
        self.includedInSummary: bool = self.chatMessage.get('includedInSummary', None)
        self.chatBubbleId:      str = self.chatMessage.get('chatBubbleId', None)
        self.chatBubbleVersion: int = self.chatMessage.get('chatBubbleVersion', None)
        self.extensions:        dict = self.chatMessage.get('extensions', None)
        self.alertOption:       int = self.data.get('alertOption', None)
        self.membershipStatus:  int = self.data.get('membershipStatus', None)
        
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
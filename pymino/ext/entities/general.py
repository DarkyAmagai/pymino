from re import findall
from typing import Union

from .exceptions import InvalidLink
from .userprofile import UserProfile, UserProfileList

class ApiResponse:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data       = data
        self.message    = None
        self.statuscode = None
        self.duration   = None
        self.timestamp  = None
        self.mediaValue = None
        
        if isinstance(self.data, dict):
            self.message:       Union[str, None] = self.data.get("api:message", self.message)
            self.statuscode:    Union[int, None] = self.data.get("api:statuscode", self.statuscode)
            self.duration:      Union[str, None] = self.data.get("api:duration", self.duration)
            self.timestamp:     Union[str, None] = self.data.get("api:timestamp", self.timestamp)
            self.mediaValue:    Union[str, None] = self.data.get("mediaValue", self.mediaValue) or self.data.get("result", {}).get("mediaValue", self.mediaValue)
        
    def json(self) -> Union[dict, str]:
        return self.data

class LinkInfo:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data               = data
        self.linkInfoV2         = {}
        self.path               = None
        self.extensions         = {}
        self.objectId           = None
        self.shareURLShortCode  = None
        self.targetCode         = None
        self.ndcId              = None
        self.comId              = None
        self.fullPath           = None
        self.shortCode          = None
        self.objectType         = None

        if isinstance(data, dict):
            self.linkInfoV2:        dict = self.data.get("linkInfoV2", self.linkInfoV2)
            self.path:              Union[str, None] = self.data.get("path", self.path)             or self.linkInfoV2.get("path", self.path)
            self.extensions:        dict = self.data.get("extensions", self.extensions)             or self.linkInfoV2.get("extensions", self.extensions)
            self.objectId:          Union[str, None] = self.data.get("objectId", self.objectId)     or self.extensions.get("linkInfo", {}).get("objectId", self.objectId)
            self.shareURLShortCode: Union[str, None] = self.data.get("shareURLShortCode", self.shareURLShortCode) or self.extensions.get("linkInfo", {}).get("shareURLShortCode", self.shareURLShortCode)
            self.targetCode:        Union[str, None] = self.data.get("targetCode", self.targetCode) or self.extensions.get("linkInfo", {}).get("targetCode", self.targetCode)
            self.ndcId:             Union[int, None] = self.data.get("ndcId", self.ndcId)           or self.extensions.get("linkInfo", {}).get("ndcId", self.ndcId)
            self.comId:             Union[int, None] = self.ndcId
            self.fullPath:          Union[str, None] = self.data.get("fullPath", self.fullPath)     or self.extensions.get("linkInfo", {}).get("fullPath", self.fullPath)
            self.shortCode:         Union[str, None] = self.data.get("shortCode", self.shortCode)   or self.extensions.get("linkInfo", {}).get("shortCode", self.shortCode)
            self.objectType:        Union[str, None] = self.data.get("objectType", self.objectType) or self.extensions.get("linkInfo", {}).get("objectType", self.objectType)

    def json(self) -> Union[dict, str]:
        return self.data

class CommunityInvitation:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data                = data
        self.communityInvitation = {}
        self.status              = None
        self.duration            = None
        self.invitationId        = None
        self.link                = None
        self.modifiedTime        = None
        self.ndcId               = None
        self.createdTime         = None
        self.inviteCode          = None

        if isinstance(data, dict):
            self.communityInvitation:   dict = self.data.get("communityInvitation", self.communityInvitation)
            self.status:                Union[int, None] = self.communityInvitation.get("status", self.status)
            self.duration:              Union[str, None] = self.communityInvitation.get("duration", self.duration)
            self.invitationId:          Union[str, None] = self.communityInvitation.get("invitationId", self.invitationId)
            self.link:                  Union[str, None] = self.communityInvitation.get("link", self.link)
            self.modifiedTime:          Union[str, None] = self.communityInvitation.get("modifiedTime", self.modifiedTime)
            self.ndcId:                 Union[int, None] = self.communityInvitation.get("ndcId", self.ndcId)
            self.createdTime:           Union[str, None] = self.communityInvitation.get("createdTime", self.createdTime)
            self.inviteCode:            Union[str, None] = self.communityInvitation.get("inviteCode", self.inviteCode)

    def json(self) -> Union[dict, str]:
        return self.data

class CheckIn:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.checkInHistory = {}
        self.consecutiveCheckInDays = None
        self.hasCheckInToday = None
        self.hasAnyCheckIn = None
        self.history = {}
        self.userProfile = {}

        if isinstance(data, dict):
            self.checkInHistory:          dict = self.data.get("checkInHistory", self.checkInHistory)
            self.consecutiveCheckInDays:  Union[int, None] = self.checkInHistory.get("consecutiveCheckInDays", self.consecutiveCheckInDays)
            self.hasCheckInToday:         Union[bool, None] = self.checkInHistory.get("hasCheckInToday", self.hasCheckInToday)
            self.hasAnyCheckIn:           Union[bool, None] = self.checkInHistory.get("hasAnyCheckIn", self.hasAnyCheckIn)
            self.history:                 dict = self.checkInHistory.get("history", self.history)
            self.userProfile:             dict = self.data.get("userProfile", self.userProfile)

    def json(self) -> Union[dict, str]:
        return self.data

class InvitationId:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.status = None
        self.duration = None
        self.invitationId = None
        self.link = None
        self.modifiedTime = None
        self.ndcId = None
        self.createdTime = None
        self.inviteCode = None

        if isinstance(data, dict):
            self.status:        Union[int, None] = self.data.get("status", self.status)
            self.duration:      Union[int, None] = self.data.get("duration", self.duration)
            self.invitationId:  Union[str, None] = self.data.get("invitationId", self.invitationId)
            self.link:          Union[str, None] = self.data.get("link", self.link)
            self.modifiedTime:  Union[str, None] = self.data.get("modifiedTime", self.modifiedTime)
            self.ndcId:         Union[int, None] = self.data.get("ndcId", self.ndcId)
            self.createdTime:   Union[str, None] = self.data.get("createdTime", self.createdTime)
            self.inviteCode:    Union[str, None] = self.data.get("inviteCode", self.inviteCode)

    def json(self) -> Union[dict, str]:
        return self.data
    
class CCommunity:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data               = data
        self.keywords           = []
        self.activeInfo         = {}
        self.themePack          = {}
        self.status             = None
        self.probationStatus    = None
        self.updatedTime        = None
        self.primaryLanguage    = None
        self.modifiedTime       = None
        self.membersCount       = None
        self.tagline            = None
        self.name               = None
        self.endpoint           = None
        self.communityHeadList  = []
        self.listedStatus       = None
        self.extensions         = []
        self.mediaList          = []
        self.userAddedTopicList = []
        self.communityHeat      = None
        self.templateId         = None
        self.searchable         = None
        self.createdTime        = None
        self.invitation         = None
        self.ndcId              = None
        self.comId              = None
        self.icon               = None

        if isinstance(data, dict):
            self.data:                  dict = data.get("community", self.data)
            self.keywords:              list = self.data.get("keywords", self.keywords)
            self.activeInfo:            dict = self.data.get("activeInfo", self.activeInfo)
            self.themePack:             dict = self.data.get("themePack", self.themePack)
            self.status:                Union[int, None] = self.data.get("status", self.status)
            self.probationStatus:       Union[int, None] = self.data.get("probationStatus", self.probationStatus)
            self.updatedTime:           Union[str, None] = self.data.get("updatedTime", self.updatedTime)
            self.primaryLanguage:       Union[str, None] = self.data.get("primaryLanguage", self.primaryLanguage)
            self.modifiedTime:          Union[str, None] = self.data.get("modifiedTime", self.modifiedTime)
            self.membersCount:          Union[int, None] = self.data.get("membersCount", self.membersCount)
            self.tagline:               Union[str, None] = self.data.get("tagline", self.tagline)
            self.name:                  Union[str, None] = self.data.get("name", self.name)
            self.endpoint:              Union[str, None] = self.data.get("endpoint", self.endpoint)
            self.communityHeadList:     Union[list, None] = self.data.get("communityHeadList", self.communityHeadList)
            self.listedStatus:          Union[int, None] = self.data.get("listedStatus", self.listedStatus)
            self.extensions:            Union[list, None] = self.data.get("extensions", self.extensions)
            self.mediaList:             Union[list, None] = self.data.get("mediaList", self.mediaList)
            self.userAddedTopicList:    Union[list, None] = self.data.get("userAddedTopicList", self.userAddedTopicList)
            self.communityHeat:         Union[int, None] = self.data.get("communityHeat", self.communityHeat)
            self.templateId:            Union[int, None] = self.data.get("templateId", self.templateId)
            self.searchable:            Union[bool, None] = self.data.get("searchable", self.searchable)
            self.createdTime:           Union[str, None] = self.data.get("createdTime", self.createdTime)
            self.invitation:            InvitationId = InvitationId(self.data.get("invitation", self.invitation))
            
            try:
                self.ndcId:             Union[int, None] = self.data.get("ndcId", self.ndcId) or int(findall(r"\d+", self.data.get("linkInfoV2").get("path"))[0]) 
            except IndexError as error:
                raise InvalidLink from error
            
            self.comId:                 Union[int, None] = self.ndcId
            self.icon:                  Union[str, None] = self.data.get("icon", self.icon)
        
    def json(self) -> Union[dict, str]:
        return self.data

class CCommunityList:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data:                                  dict = data.get("communityList", data)
        parser:                                     list = [CCommunity(x) for x in self.data]
        self.keywords:                              list = [x.keywords for x in parser]
        self.activeInfo:                            list = [x.activeInfo for x in parser]
        self.themePack:                             list = [x.themePack for x in parser]
        self.status:                                list = [x.status for x in parser]
        self.probationStatus:                       list = [x.probationStatus for x in parser]
        self.updatedTime:                           list = [x.updatedTime for x in parser]
        self.primaryLanguage:                       list = [x.primaryLanguage for x in parser]
        self.modifiedTime:                          list = [x.modifiedTime for x in parser]
        self.membersCount:                          list = [x.membersCount for x in parser]
        self.tagline:                               list = [x.tagline for x in parser]
        self.name:                                  list = [x.name for x in parser]
        self.endpoint:                              list = [x.endpoint for x in parser]
        self.communityHeadList:                     list = [x.communityHeadList for x in parser]
        self.listedStatus:                          list = [x.listedStatus for x in parser]
        self.extensions:                            list = [x.extensions for x in parser]
        self.mediaList:                             list = [x.mediaList for x in parser]
        self.userAddedTopicList:                    list = [x.userAddedTopicList for x in parser]
        self.communityHeat:                         list = [x.communityHeat for x in parser]
        self.templateId:                            list = [x.templateId for x in parser]
        self.searchable:                            list = [x.searchable for x in parser]
        self.createdTime:                           list = [x.createdTime for x in parser]
        self.ndcId:                                 list = [x.ndcId for x in parser]
        self.comId:                                 list = [x.comId for x in parser]
        self.icon:                                  list = [x.icon for x in parser]
    
    def json(self) -> Union[dict, str]:
        return self.data

class CBlog:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data                   = data
        self.globalVotesCount       = None
        self.globalVotedValue       = None
        self.votedValue             = None
        self.keywords               = None
        self.mediaList              = []
        self.style                  = {}
        self.totalQuizPlayCount     = None
        self.title                  = None
        self.tipInfo                = {}
        self.contentRating          = None
        self.content                = None
        self.needHidden             = None
        self.guestVotesCount        = None
        self.type                   = None
        self.status                 = None
        self.globalCommentsCount    = None
        self.modifiedTime           = None
        self.widgetDisplayInterval  = None
        self.totalPollVoteCount     = None
        self.blogId                 = None
        self.viewCount              = None
        self.language               = None
        self.author                 = None
        self.extensions             = {}
        self.votesCount             = None
        self.ndcId                  = None
        self.createdTime            = None
        self.endTime                = None
        self.commentsCount          = None

        if isinstance(data, dict):
            self.data:                  dict = data.get("blog", data)
            self.globalVotesCount:      int = self.data.get("globalVotesCount", self.globalVotesCount)
            self.globalVotedValue:      int = self.data.get("globalVotedValue", self.globalVotedValue)
            self.votedValue:            int = self.data.get("votedValue", self.votedValue)
            self.keywords:              str = self.data.get("keywords", self.keywords)
            self.mediaList:             list = self.data.get("mediaList", self.mediaList)
            self.style:                 dict = self.data.get("style", self.style)
            self.totalQuizPlayCount:    int = self.data.get("totalQuizPlayCount", self.totalQuizPlayCount)
            self.title:                 str = self.data.get("title", self.title)
            self.tipInfo:               dict = self.data.get("tipInfo", self.tipInfo)
            self.contentRating:         int = self.data.get("contentRating", self.contentRating)
            self.content:               str = self.data.get("content", self.content)
            self.needHidden:            bool = self.data.get("needHidden", self.needHidden)
            self.guestVotesCount:       int = self.data.get("guestVotesCount", self.guestVotesCount)
            self.type:                  int = self.data.get("type", self.type)
            self.status:                int = self.data.get("status", self.status)
            self.globalCommentsCount:   int = self.data.get("globalCommentsCount", self.globalCommentsCount)
            self.modifiedTime:          str = self.data.get("modifiedTime", self.modifiedTime)
            self.widgetDisplayInterval: str = self.data.get("widgetDisplayInterval", self.widgetDisplayInterval)
            self.totalPollVoteCount:    int = self.data.get("totalPollVoteCount", self.totalPollVoteCount)
            self.blogId:                str = self.data.get("blogId", self.blogId)
            self.viewCount:             int = self.data.get("viewCount", self.viewCount)
            self.language:              str = self.data.get("language", self.language)
            self.author:                UserProfile = UserProfile(data=self.data.get("author", self.author))
            self.extensions:            dict = self.data.get("extensions", self.extensions)
            self.votesCount:            int = self.data.get("votesCount", self.votesCount)
            self.ndcId:                 int = self.data.get("ndcId", self.ndcId)
            self.createdTime:           str = self.data.get("createdTime", self.createdTime)
            self.endTime:               str = self.data.get("endTime", self.endTime)
            self.commentsCount:         int = self.data.get("commentsCount", self.commentsCount)

    def json(self) -> Union[dict, str]:
        return self.data

class CBlogList:
    def __init__(self, data: Union[dict, str]):
        self.data:                   dict = data.get("blogList", data)
        parser:                      list = [CBlog(x) for x in self.data]
        self.author:                 UserProfileList = UserProfileList([x.author.json() for x in parser])
        self.globalVotesCount:       list = [x.globalVotesCount for x in parser]
        self.globalVotedValue:       list = [x.globalVotedValue for x in parser]
        self.votedValue:             list = [x.votedValue for x in parser]
        self.keywords:               list = [x.keywords for x in parser]
        self.mediaList:              list = [x.mediaList for x in parser]
        self.style:                  list = [x.style for x in parser]
        self.totalQuizPlayCount:     list = [x.totalQuizPlayCount for x in parser]
        self.title:                  list = [x.title for x in parser]
        self.tipInfo:                list = [x.tipInfo for x in parser]
        self.contentRating:          list = [x.contentRating for x in parser]
        self.content:                list = [x.content for x in parser]
        self.needHidden:             list = [x.needHidden for x in parser]
        self.guestVotesCount:        list = [x.guestVotesCount for x in parser]
        self.type:                   list = [x.type for x in parser]
        self.status:                 list = [x.status for x in parser]
        self.globalCommentsCount:    list = [x.globalCommentsCount for x in parser]
        self.modifiedTime:           list = [x.modifiedTime for x in parser]
        self.widgetDisplayInterval:  list = [x.widgetDisplayInterval for x in parser]
        self.totalPollVoteCount:     list = [x.totalPollVoteCount for x in parser]
        self.blogId:                 list = [x.blogId for x in parser]
        self.viewCount:              list = [x.viewCount for x in parser]
        self.language:               list = [x.language for x in parser]
        self.extensions:             list = [x.extensions for x in parser]
        self.votesCount:             list = [x.votesCount for x in parser]
        self.ndcId:                  list = [x.ndcId for x in parser]
        self.createdTime:            list = [x.createdTime for x in parser]
        self.endTime:                list = [x.endTime for x in parser]
        self.commentsCount:          list = [x.commentsCount for x in parser]

    def json(self) -> Union[dict, str]:
        return self.data

class Coupon:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data         = data
        self.expiredTime  = None
        self.couponId     = None
        self.scopeDesc    = None
        self.status       = None
        self.modifiedTime = None
        self.couponValue  = None
        self.expiredType  = None
        self.title        = None
        self.couponType   = None
        self.createdTime  = None

        if isinstance(data, dict):
            self.data:          dict = data.get("coupon", data)
            self.expiredTime:   Union[str, None] = self.data.get("expiredTime", self.expiredTime)
            self.couponId:      Union[str, None] = self.data.get("couponId", self.couponId)
            self.scopeDesc:     Union[str, None] = self.data.get("scopeDesc", self.scopeDesc)
            self.status:        Union[int, None] = self.data.get("status", self.status)
            self.modifiedTime:  Union[str, None] = self.data.get("modifiedTime", self.modifiedTime)
            self.couponValue:   Union[int, None] = self.data.get("couponValue", self.couponValue)
            self.expiredType:   Union[int, None] = self.data.get("expiredType", self.expiredType)
            self.title:         Union[str, None] = self.data.get("title", self.title)
            self.couponType:    Union[int, None] = self.data.get("couponType", self.couponType)
            self.createdTime:   Union[str, None] = self.data.get("createdTime", self.createdTime)

    def json(self) -> Union[dict, str]:
        return self.data

class Wallet:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data                    = data
        self.totalCoinsFloat         = None
        self.adsEnabled              = None
        self.adsVideoStats           = {}
        self.adsFlags                = None
        self.totalCoins              = None
        self.businessCoinsEnabled    = None
        self.totalBusinessCoins      = None
        self.totalBusinessCoinsFloat = None

        if isinstance(data, dict):
            self.data:                    dict = data.get("wallet", data)
            self.totalCoinsFloat:         Union[float, None] = self.data.get("totalCoinsFloat", self.totalCoinsFloat)
            self.adsEnabled:              Union[bool, None] = self.data.get("adsEnabled", self.adsEnabled)
            self.adsVideoStats:           Union[dict, None] = self.data.get("adsVideoStats", self.adsVideoStats)
            self.adsFlags:                Union[int, None] = self.data.get("adsFlags", self.adsFlags)
            self.totalCoins:              Union[int, None] = self.data.get("totalCoins", self.totalCoins)
            self.businessCoinsEnabled:    Union[bool, None] = self.data.get("businessCoinsEnabled", self.businessCoinsEnabled)
            self.totalBusinessCoins:      Union[int, None] = self.data.get("totalBusinessCoins", self.totalBusinessCoins)
            self.totalBusinessCoinsFloat: Union[float, None] = self.data.get("totalBusinessCoinsFloat", self.totalBusinessCoinsFloat)

    def json(self) -> Union[dict, str]:
        return self.data

class Themepack:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.themeColor = None
        self.themePackHash = None
        self.themePackRevision = None
        self.themePackUrl = None

        if isinstance(data, dict):
            self.data:                  dict = data
            self.themeColor:            Union[str, None] = self.data.get("themeColor", self.themeColor)
            self.themePackHash:         Union[str, None] = self.data.get("themePackHash", self.themePackHash)
            self.themePackRevision:     Union[int, None] = self.data.get("themePackRevision", self.themePackRevision)
            self.themePackUrl:          Union[str, None] = self.data.get("themePackUrl", self.themePackUrl)

    def json(self) -> Union[dict, str]:
        return self.data

class Notification:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data           = data
        self.parentText     = None
        self.objectId       = None
        self.contextText    = None
        self.type           = None
        self.parentId       = None
        self.operator       = {}
        self.createdTime    = None
        self.parentType     = None
        self.comId          = None
        self.notificationId = None
        self.objectText     = None
        self.contextValue   = None
        self.contextComId   = None
        self.objectType     = None

        if isinstance(data, dict):
            self.parentText:        Union[str, None] = self.data.get("parentText", self.parentText)
            self.objectId:          Union[str, None] = self.data.get("objectId", self.objectId)
            self.contextText:       Union[str, None] = self.data.get("contextText", self.contextText)
            self.type:              Union[int, None] = self.data.get("type", self.type)
            self.parentId:          Union[str, None] = self.data.get("parentId", self.parentId)
            self.operator:          UserProfile = UserProfile(self.data.get("operator", self.operator))
            self.createdTime:       Union[str, None] = self.data.get("createdTime", self.createdTime)
            self.parentType:        Union[int, None] = self.data.get("parentType", self.parentType)
            self.comId:             Union[int, None] = self.data.get("ndcId", self.comId)
            self.notificationId:    Union[str, None] = self.data.get("notificationId", self.notificationId)
            self.objectText:        Union[str, None] = self.data.get("objectText", self.objectText)
            self.contextValue:      Union[str, None] = self.data.get("contextValue", self.contextValue)
            self.contextComId:      Union[int, None] = self.data.get("contextNdcId", self.contextComId)
            self.objectType:        Union[int, None] = self.data.get("objectType", self.objectType)

    def json(self) -> Union[dict, str]:
        return self.data
    
class ResetPassword:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.response = {}
        self.secret = None

        if isinstance(data, dict):
            self.response:  ApiResponse = ApiResponse(self.data, self.response)
            self.secret:    Union[str, None] = self.data.get("secret", self.secret)

    def json(self) -> Union[dict, str]:
        return self.data

class Authenticate:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data    = data
        self.sid     = None
        self.userId  = None
        self.profile = {}
        self.secret  = None

        if isinstance(data, dict):
            self.sid:      Union[str, None] = self.data.get("sid", self.sid)
            self.userId:   Union[str, None] = self.data.get("auid", self.userId)
            self.profile:  UserProfile = UserProfile(self.data.get("userProfile", self.profile))
            self.secret:   Union[str, None] = self.data.get("secret", self.secret)

    def json(self) -> Union[dict, str]:
        return self.data

class CChatMembers:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.members = []

        if isinstance(data, dict):
            self.members: UserProfileList = UserProfileList(self.data.get("memberList", self.members))

    def json(self) -> Union[dict, str]:
        return self.data
    
class CComment:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.modifiedTime = None
        self.ndcId = None
        self.votedValue = None
        self.parentType = None
        self.commentId = None
        self.parentNdcId = None
        self.mediaList = None
        self.votesSum = None
        self.author = {}
        self.extensions = {}
        self.content = None
        self.parentId = None
        self.createdTime = None
        self.subcommentsCount = None
        self.type = None

        if isinstance(data, dict):
            self.modifiedTime:      Union[str, None] = self.data.get("modifiedTime", self.modifiedTime)
            self.ndcId:             Union[int, None] = self.data.get("ndcId", self.ndcId)
            self.votedValue:        Union[int, None] = self.data.get("votedValue", self.votedValue)
            self.parentType:        Union[int, None] = self.data.get("parentType", self.parentType)
            self.commentId:         Union[str, None] = self.data.get("commentId", self.commentId)
            self.parentNdcId:       Union[int, None] = self.data.get("parentNdcId", self.parentNdcId)
            self.mediaList:         Union[None, None] = self.data.get("mediaList", self.mediaList)
            self.votesSum:          Union[int, None] = self.data.get("votesSum", self.votesSum)
            self.author:            UserProfile = UserProfile(self.data.get("author", self.author))
            self.extensions:        CCommentExtensions = CCommentExtensions(self.data.get("extensions", self.extensions))
            self.content:           Union[str, None] = self.data.get("content", self.content)
            self.parentId:          Union[str, None] = self.data.get("parentId", self.parentId)
            self.createdTime:       Union[str, None] = self.data.get("createdTime", self.createdTime)
            self.subcommentsCount:  Union[int, None] = self.data.get("subcommentsCount", self.subcommentsCount)
            self.type:              Union[int, None] = self.data.get("type", self.type)
        
    def json(self) -> Union[dict, str]:
        return self.data

class CCommentList:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data:              dict = data.get("commentList", [])
        parser:                 list = [CComment(x) for x in self.data]
        self.modifiedTime:      list = [x.modifiedTime for x in parser]
        self.ndcId:             list = [x.ndcId for x in parser]
        self.votedValue:        list = [x.votedValue for x in parser]
        self.parentType:        list = [x.parentType for x in parser]
        self.commentId:         list = [x.commentId for x in parser]
        self.parentNdcId:       list = [x.parentNdcId for x in parser]
        self.mediaList:         list = [x.mediaList for x in parser]
        self.votesSum:          list = [x.votesSum for x in parser]
        #self.author:            list = [x.author for x in parser]
        #self.extensions:        list = [x.extensions for x in parser]
        self.content:           list = [x.content for x in parser]
        self.parentId:          list = [x.parentId for x in parser]
        self.createdTime:       list = [x.createdTime for x in parser]
        self.subcommentsCount:  list = [x.subcommentsCount for x in parser]
        self.type:              list = [x.type for x in parser]

    def json(self) -> Union[dict, str]:
        return self.data

class CCommentExtensions:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data
        self.status = None
        self.iconV2 = None
        self.name = None
        self.stickerId = None
        self.smallIconV2 = None
        self.smallIcon = None
        self.stickerCollectionId = None
        self.mediumIcon = None
        self.stickerCollectionSummary = {}
        self.extensions = None
        self.usedCount = None
        self.mediumIconV2 = None
        self.createdTime = None
        self.icon = None

        if isinstance(data, dict):
            self.data:                      Union[dict, None] = self.data.get("sticker", self.data)
            self.status:                    Union[int, None] = self.data.get("status", self.status)
            self.iconV2:                    Union[str, None] = self.data.get("iconV2", self.iconV2)
            self.name:                      Union[str, None] = self.data.get("name", self.name)
            self.stickerId:                 Union[str, None] = self.data.get("stickerId", self.stickerId)
            self.smallIconV2:               Union[str, None] = self.data.get("smallIconV2", self.smallIconV2)
            self.smallIcon:                 Union[str, None] = self.data.get("smallIcon", self.smallIcon)
            self.stickerCollectionId:       Union[str, None] = self.data.get("stickerCollectionId", self.stickerCollectionId)
            self.mediumIcon:                Union[str, None] = self.data.get("mediumIcon", self.mediumIcon)
            self.stickerCollectionSummary:  Union[dict, None] = self.data.get("stickerCollectionSummary", self.stickerCollectionSummary)
            self.extensions:                Union[None, None] = self.data.get("extensions", self.extensions)
            self.usedCount:                 Union[int, None] = self.data.get("usedCount", self.usedCount)
            self.mediumIconV2:              Union[str, None] = self.data.get("mediumIconV2", self.mediumIconV2)
            self.createdTime:               Union[None, None] = self.data.get("createdTime", self.createdTime)
            self.icon:                      Union[str, None] = self.data.get("icon", self.icon)

    def json(self) -> Union[dict, str]:
        return self.data

class FeaturedBlog:
    def __init__(self, data: Union[dict, str]):
        self.data           = data

    def return_none(func):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else func(*args, **kwargs)
        return wrapper
    
    @property
    @return_none
    def ref_object_type(self) -> Union[int, None]:
        return self.data.get('refObjectType')    
    
    @property
    @return_none
    def ref_object_id(self) -> Union[str, None]:
        return self.data.get('refObjectId')
    
    @property
    @return_none
    def expired_time(self) -> Union[str, None]:
        return self.data.get('expiredTime')
    
    @property
    @return_none
    def featured_type(self) -> Union[int, None]:
        return self.data.get('featuredType')
    
    @property
    @return_none
    def created_time(self) -> Union[str, None]:
        return self.data.get('createdTime')
    
    @property
    @return_none
    def ref_object(self) -> Union[dict, None]:
        return self.data.get('refObject')
    
    @property
    @return_none
    def global_votes_count(self) -> Union[int, None]:
        return self.ref_object.get('globalVotesCount')
    
    @property
    @return_none
    def global_voted_count(self) -> Union[int, None]:
        return self.ref_object.get('globalVotedCount')
    
    @property
    @return_none
    def voted_value(self) -> Union[int, None]:
        return self.ref_object.get('votedValue')
    
    @property
    @return_none
    def keywords(self) -> Union[str, None]:
        return self.ref_object.get('keywords')
    
    @property
    @return_none
    def strategy_info(self) -> Union[str, None]:
        return self.ref_object.get('strategyInfo')
    
    @property
    @return_none
    def media_list(self) -> Union[list, None]:
        return self.ref_object.get('mediaList')
    
    @property
    @return_none
    def style(self) -> Union[dict, None]:
        return self.ref_object.get('style')
    
    @property
    @return_none
    def total_quiz_play_count(self) -> Union[int, None]:
        return self.ref_object.get('totalQuizPlayCount')
    
    @property
    @return_none
    def title(self) -> Union[str, None]:
        return self.ref_object.get('title')
    
    @property
    @return_none
    def tip_info(self) -> Union[dict, None]:
        return self.ref_object.get('tipInfo')
    
    @property
    @return_none
    def content(self) -> Union[str, None]:
        return self.ref_object.get('content')
    
    @property
    @return_none
    def content_rating(self) -> Union[str, None]:
        return self.ref_object.get('contentRating')
    
    @property
    @return_none
    def need_hidden(self) -> Union[bool, None]:
        return self.ref_object.get('needHidden')
    
    @property
    @return_none
    def guest_votes_count(self) -> Union[int, None]:
        return self.ref_object.get('guestVotesCount')
    
    @property
    @return_none
    def global_comments_count(self) -> Union[int, None]:
        return self.ref_object.get('globalCommentsCount')
    
    @property
    @return_none
    def modified_time(self) -> Union[str, None]:
        return self.ref_object.get('modifiedTime')
    
    @property
    @return_none
    def widget_display_interval(self) -> Union[int, None]:
        return self.ref_object.get('widgetDisplayInterval')
    
    @property
    @return_none
    def total_poll_vote_count(self) -> Union[int, None]:
        return self.ref_object.get('totalPollVoteCount')
    
    @property
    @return_none
    def blogId(self) -> Union[str, None]:
        return self.ref_object.get('blogId')
    
    @property
    @return_none
    def view_count(self) -> Union[int, None]:
        return self.ref_object.get('viewCount')
    
    @property
    @return_none
    def ref_object_type(self) -> Union[int, None]:
        return self.ref_object.get('refObjectType')
    
    @property
    @return_none
    def ref_object_id(self) -> Union[str, None]:
        return self.ref_object.get('refObjectId')
    
    @property
    @return_none
    def author(self) -> UserProfile:
        return UserProfile(self.ref_object.get('author'))

    def json(self) -> Union[dict, None]:
        return self.data

class FeaturedBlogs:
    def __init__(self, data: dict):
        self.data:                      dict = data.get("featuredList", data)
        parser:                         list = [FeaturedBlog(x) for x in self.data]
        self.ref_object_type:           list = [x.ref_object_type for x in parser]
        self.ref_object_id:             list = [x.ref_object_id for x in parser]
        self.expired_time:              list = [x.expired_time for x in parser]
        self.featured_type:             list = [x.featured_type for x in parser]
        self.created_time:              list = [x.created_time for x in parser]
        self.ref_object:                list = [x.ref_object for x in parser]
        self.global_votes_count:        list = [x.global_votes_count for x in parser]
        self.global_voted_count:        list = [x.global_voted_count for x in parser]
        self.voted_value:               list = [x.voted_value for x in parser]
        self.keywords:                  list = [x.keywords for x in parser]
        self.strategy_info:             list = [x.strategy_info for x in parser]
        self.media_list:                list = [x.media_list for x in parser]
        self.style:                     list = [x.style for x in parser]
        self.total_quiz_play_count:     list = [x.total_quiz_play_count for x in parser]
        self.title:                     list = [x.title for x in parser]
        self.tip_info:                  list = [x.tip_info for x in parser]
        self.content:                   list = [x.content for x in parser]
        self.content_rating:            list = [x.content_rating for x in parser]
        self.need_hidden:               list = [x.need_hidden for x in parser]
        self.guest_votes_count:         list = [x.guest_votes_count for x in parser]
        self.global_comments_count:     list = [x.global_comments_count for x in parser]
        self.modified_time:             list = [x.modified_time for x in parser]
        self.widget_display_interval:   list = [x.widget_display_interval for x in parser]
        self.total_poll_vote_count:     list = [x.total_poll_vote_count for x in parser]
        self.blogId:                    list = [x.blogId for x in parser]
        self.view_count:                list = [x.view_count for x in parser]
        self.ref_object_type:           list = [x.ref_object_type for x in parser]
        self.ref_object_id:             list = [x.ref_object_id for x in parser]
        self.author:                    UserProfileList = UserProfileList([x.author.json() for x in parser])

    def json(self) -> Union[dict, None]:
        return self.data
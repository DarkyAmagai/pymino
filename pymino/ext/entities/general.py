from re import findall
from .userprofile import UserProfile, UserProfileList

class ApiResponse:
    def __init__(self, data: dict):
        self.data = data
        self.message:            str = self.data.get('api:message', None)
        self.statuscode:         int = self.data.get('api:statuscode', None)
        self.duration:           str = self.data.get('api:duration', None)
        self.timestamp:          str = self.data.get('api:timestamp', None)
        self.mediaValue:         str = self.data.get('mediaValue', None) or self.data.get('result', {}).get('mediaValue', None)

    def json(self): return self.data

class LinkInfo:
    def __init__(self, data: dict):
        self.data:               dict = data
        self.linkInfoV2:         dict = self.data.get('linkInfoV2', None) 
        self.path:               str = self.data.get('path', None) or self.linkInfoV2.get('path', None)
        self.extensions:         dict = self.data.get('extensions', None) or self.linkInfoV2.get('extensions', None)
        self.objectId:           str = self.data.get('objectId', None) or self.extensions.get('linkInfo', {}).get('objectId', None)
        self.targetCode:         str = self.data.get('targetCode', None) or self.extensions.get('linkInfo', {}).get('targetCode', None)
        self.ndcId:              int = self.data.get('ndcId', None) or self.extensions.get('linkInfo', {}).get('ndcId', None)
        self.comId:              int = self.ndcId 
        self.fullPath:           str = self.data.get('fullPath', None) or self.extensions.get('linkInfo', {}).get('fullPath', None)
        self.shortCode:          str = self.data.get('shortCode', None) or self.extensions.get('linkInfo', {}).get('shortCode', None)
        self.objectType:         int = self.data.get('objectType', None) or self.extensions.get('linkInfo', {}).get('objectType', None)

    def json(self): return self.data

class CommunityInvitation:
    def __init__(self, data: dict):
        self.data:                      dict = data
        self.communityInvitation:       dict = self.data['communityInvitation']
        self.status:                    int = self.communityInvitation.get('status', None)
        self.duration:                  str = self.communityInvitation.get('duration', None)
        self.invitationId:              str = self.communityInvitation.get('invitationId', None)
        self.link:                      str = self.communityInvitation.get('link', None)
        self.modifiedTime:              str = self.communityInvitation.get('modifiedTime', None)
        self.ndcId:                     int = self.communityInvitation.get('ndcId', None)
        self.createdTime:               str = self.communityInvitation.get('createdTime', None)
        self.inviteCode:                str = self.communityInvitation.get('inviteCode', None)

    def json(self): return self.data

class CheckIn:
    def __init__(self, data: dict):
        self.data:                      dict = data
        self.checkInHistory:            dict = self.data.get('checkInHistory', None)
        self.consecutiveCheckInDays:    bool = self.checkInHistory.get('consecutiveCheckInDays', None)
        self.hasCheckInToday:           bool = self.checkInHistory.get('hasCheckInToday', None)
        self.hasAnyCheckIn:             bool = self.checkInHistory.get('hasAnyCheckIn', None)
        self.history:                   dict = self.checkInHistory.get('history', None)
        self.userProfile:               UserProfile = UserProfile(self.data.get('userProfile', None))

    def json(self): return self.data

class CCommunity:
    def __init__(self, data: dict):
        self.data:                                  dict = data.get("community", data)
        self.isStandaloneAppMonetizationEnabled:    bool = self.data.get("isStandaloneAppMonetizationEnabled", None)
        self.keywords:                              list = self.data.get("keywords", None)
        self.isStandaloneAppDeprecated:             bool = self.data.get("isStandaloneAppDeprecated", None)
        self.activeInfo:                            dict = self.data.get("activeInfo", None)
        self.promotionalMediaList:                  list = self.data.get("promotionalMediaList", None)
        self.themePack:                             dict = self.data.get("themePack", None)
        self.status:                                int = self.data.get("status", None)
        self.probationStatus:                       int = self.data.get("probationStatus", None)
        self.updatedTime:                           str = self.data.get("updatedTime", None)
        self.primaryLanguage:                       str = self.data.get("primaryLanguage", None)
        self.modifiedTime:                          str = self.data.get("modifiedTime", None)
        self.membersCount:                          int = self.data.get("membersCount", None)
        self.tagline:                               str = self.data.get("tagline", None)
        self.name:                                  str = self.data.get("name", None)
        self.endpoint:                              str = self.data.get("endpoint", None)
        self.communityHeadList:                     list = self.data.get("communityHeadList", None)
        self.listedStatus:                          int = self.data.get("listedStatus", None)
        self.extensions:                            list = self.data.get("extensions", None)
        self.mediaList:                             list = self.data.get("mediaList", None)
        self.userAddedTopicList:                    list = self.data.get("userAddedTopicList", None)
        self.communityHeat:                         int = self.data.get("communityHeat", None)
        self.templateId:                            int = self.data.get("templateId", None)
        self.searchable:                            bool = self.data.get("searchable", None)
        self.createdTime:                           str = self.data.get("createdTime")
        self.ndcId:                                 int = self.data.get("ndcId") or int(findall(r'\d+', self.data.get("linkInfoV2").get("path"))[0])
        self.comId:                                 int = self.ndcId
        self.icon:                                  str = self.data.get("icon", None)
        
    def json(self) -> dict: return self.data

class CCommunityList:
    def __init__(self, data: dict):
        self.data:                                  dict = data.get("communityList", data)
        parser:                                     list = [CCommunity(x) for x in self.data]
        self.isStandaloneAppMonetizationEnabled:    list = [x.isStandaloneAppMonetizationEnabled for x in parser]
        self.keywords:                              list = [x.keywords for x in parser]
        self.isStandaloneAppDeprecated:             list = [x.isStandaloneAppDeprecated for x in parser]
        self.activeInfo:                            list = [x.activeInfo for x in parser]
        self.promotionalMediaList:                  list = [x.promotionalMediaList for x in parser]
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
    
    def json(self) -> dict: return self.data

class CBlog:
    def __init__(self, data: dict):
        self.data:                                  dict = data.get("blog", data)
        self.globalVotesCount:                      int = self.data.get("globalVotesCount", None)
        self.globalVotedValue:                      int = self.data.get("globalVotedValue", None)
        self.votedValue:                            int = self.data.get("votedValue", None)
        self.keywords:                              str = self.data.get("keywords", None)
        self.mediaList:                             list = self.data.get("mediaList", None)
        self.style:                                 dict = self.data.get("style", None)
        self.totalQuizPlayCount:                    int = self.data.get("totalQuizPlayCount", None)
        self.title:                                 str = self.data.get("title", None)
        self.tipInfo:                               dict = self.data.get("tipInfo", None)
        self.contentRating:                         int = self.data.get("contentRating", None)
        self.content:                               str = self.data.get("content", None)
        self.needHidden:                            bool = self.data.get("needHidden", None)
        self.guestVotesCount:                       int = self.data.get("guestVotesCount", None)
        self.type:                                  int = self.data.get("type", None)
        self.status:                                int = self.data.get("status", None)
        self.globalCommentsCount:                   int = self.data.get("globalCommentsCount", None)
        self.modifiedTime:                          str = self.data.get("modifiedTime", None)
        self.widgetDisplayInterval:                 str = self.data.get("widgetDisplayInterval", None)
        self.totalPollVoteCount:                    int = self.data.get("totalPollVoteCount", None)
        self.blogId:                                str = self.data.get("blogId", None)
        self.viewCount:                             int = self.data.get("viewCount", None)
        self.language:                              str = self.data.get("language", None)
        self.author:                                UserProfile = UserProfile(data=self.data.get("author", None))
        self.extensions:                            dict = self.data.get("extensions", None)
        self.votesCount:                            int = self.data.get("votesCount", None)
        self.ndcId:                                 int = self.data.get("ndcId", None)
        self.createdTime:                           str = self.data.get("createdTime", None)
        self.endTime:                               str = self.data.get("endTime", None)
        self.commentsCount:                         int = self.data.get("commentsCount", None)

    def json(self) -> dict: return self.data

class CBlogList:
    def __init__(self, data: dict):
        self.data:                   dict = data.get("blogList", None)
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

    def json(self): return self.data

class Coupon:
    def __init__(self, data: dict):
        self.data:          dict = data.get("coupon", data)
        self.expiredTime:   str = self.data.get("expiredTime", None)
        self.couponId:      str = self.data.get("couponId", None)
        self.scopeDesc:     str = self.data.get("scopeDesc", None)
        self.status:        int = self.data.get("status", None)
        self.modifiedTime:  str = self.data.get("modifiedTime", None)
        self.couponValue:   int = self.data.get("couponValue", None)
        self.expiredType:   int = self.data.get("expiredType", None)
        self.title:         str = self.data.get("title", None)
        self.couponType:    int = self.data.get("couponType", None)
        self.createdTime:   str = self.data.get("createdTime", None)

    def json(self) -> dict: return self.data

class Wallet:
    def __init__(self, data: dict):
        self.data:                  dict = data.get("wallet", data)
        self.totalCoinsFloat:       float = self.data.get("totalCoinsFloat", None)
        self.adsEnabled:            bool = self.data.get("adsEnabled", None)
        self.adsVideoStats:         dict = self.data.get("adsVideoStats", None)
        self.adsFlags:              int = self.data.get("adsFlags", None)
        self.totalCoins:            int = self.data.get("totalCoins", None)
        self.businessCoinsEnabled:  bool = self.data.get("businessCoinsEnabled", None)
        self.totalBusinessCoins:    int = self.data.get("totalBusinessCoins", None)
        self.totalBusinessCoinsFloat: float = self.data.get("totalBusinessCoinsFloat", None)

    def json(self) -> dict: return self.data

class Themepack:
    def __init__(self, data: dict):
        self.data:                  dict = data
        self.themeColor:            str = self.data.get("themeColor", None)
        self.themePackHash:         str = self.data.get("themePackHash", None)
        self.themePackRevision:     int = self.data.get("themePackRevision", None)
        self.themePackUrl:          str = self.data.get("themePackUrl", None)

    def json(self) -> dict: return self.data

class Notification:
    def __init__(self, data: dict):
        self.data:              dict = data
        self.parentText:        str = self.data.get("parentText", None)
        self.objectId:          str = self.data.get("objectId", None)
        self.contextText:       str = self.data.get("contextText", None)
        self.type:              int = self.data.get("type", None)
        self.parentId:          str = self.data.get("parentId", None)
        self.operator:          UserProfile = UserProfile(self.data.get("operator", None))
        self.createdTime:       str = self.data.get("createdTime", None)
        self.parentType:        int = self.data.get("parentType", None)
        self.comId:             int = self.data.get("ndcId", None)
        self.notificationId:    str = self.data.get("notificationId", None)
        self.objectText:        str = self.data.get("objectText", None)
        self.contextValue:      str = self.data.get("contextValue", None)
        self.contextComId:      int = self.data.get("contextNdcId", None)
        self.objectType:        int = self.data.get("objectType", None)

    def json(self) -> dict: return self.data

class ResetPassword:
    def __init__(self, data: dict):
        self.data:      dict = data
        self.response:  ApiResponse = ApiResponse(self.data)
        self.secret:    str = self.data.get("secret", None)

    def json(self) -> dict: return self.data

class Authenticate:
    def __init__(self, data: dict):
        self.data:      dict = data
        self.sid:       str = self.data.get("sid", None)
        self.userId:    str = self.data.get("auid", None)
        self.profile:   UserProfile = UserProfile(self.data.get("userProfile", None))
        self.secret:    str = self.data.get("secret", None)

    def json(self) -> dict: return self.data

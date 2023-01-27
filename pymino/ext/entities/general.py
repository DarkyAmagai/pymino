from re import findall
from .userprofile import UserProfile, UserProfileList

class ApiResponse:
    def __init__(self, data: dict):
        self.data = data
        self.message:            str = self.data.get('api:message')
        self.statuscode:         int = self.data.get('api:statuscode')
        self.duration:           str = self.data.get('api:duration')
        self.timestamp:          str = self.data.get('api:timestamp')
        self.mediaValue:         str = self.data.get('mediaValue') or self.data.get('result', {}).get('mediaValue')

    def json(self): return self.data

class LinkInfo:
    def __init__(self, data: dict):
        self.data:               dict = data
        self.linkInfoV2:         dict = self.data.get('linkInfoV2') 
        self.path:               str = self.data.get('path') or self.linkInfoV2.get('path')
        self.extensions:         dict = self.data.get('extensions') or self.linkInfoV2.get('extensions')
        self.objectId:           str = self.data.get('objectId') or self.extensions.get('linkInfo', {}).get('objectId')
        self.targetCode:         str = self.data.get('targetCode') or self.extensions.get('linkInfo', {}).get('targetCode')
        self.ndcId:              int = self.data.get('ndcId') or self.extensions.get('linkInfo', {}).get('ndcId')
        self.comId:              int = self.ndcId 
        self.fullPath:           str = self.data.get('fullPath') or self.extensions.get('linkInfo', {}).get('fullPath')
        self.shortCode:          str = self.data.get('shortCode') or self.extensions.get('linkInfo', {}).get('shortCode')
        self.objectType:         int = self.data.get('objectType') or self.extensions.get('linkInfo', {}).get('objectType')

    def json(self): return self.data

class CommunityInvitation:
    def __init__(self, data: dict):
        self.data:                      dict = data
        self.communityInvitation:       dict = self.data['communityInvitation']
        self.status:                    int = self.communityInvitation.get('status')
        self.duration:                  str = self.communityInvitation.get('duration')
        self.invitationId:              str = self.communityInvitation.get('invitationId')
        self.link:                      str = self.communityInvitation.get('link')
        self.modifiedTime:              str = self.communityInvitation.get('modifiedTime')
        self.ndcId:                     int = self.communityInvitation.get('ndcId')
        self.createdTime:               str = self.communityInvitation.get('createdTime')
        self.inviteCode:                str = self.communityInvitation.get('inviteCode')

    def json(self): return self.data

class CheckIn:
    def __init__(self, data: dict):
        self.data:                      dict = data
        self.checkInHistory:            dict = self.data.get('checkInHistory')
        self.consecutiveCheckInDays:    bool = self.checkInHistory.get('consecutiveCheckInDays')
        self.hasCheckInToday:           bool = self.checkInHistory.get('hasCheckInToday')
        self.hasAnyCheckIn:             bool = self.checkInHistory.get('hasAnyCheckIn')
        self.history:                   dict = self.checkInHistory.get('history')
        self.userProfile:               UserProfile = UserProfile(self.data.get('userProfile'))

    def json(self): return self.data

class CCommunity:
    def __init__(self, data: dict):
        self.data:                                  dict = data.get("community", data)
        self.isStandaloneAppMonetizationEnabled:    bool = self.data.get("isStandaloneAppMonetizationEnabled")
        self.keywords:                              list = self.data.get("keywords")
        self.isStandaloneAppDeprecated:             bool = self.data.get("isStandaloneAppDeprecated")
        self.activeInfo:                            dict = self.data.get("activeInfo")
        self.promotionalMediaList:                  list = self.data.get("promotionalMediaList")
        self.themePack:                             dict = self.data.get("themePack")
        self.status:                                int = self.data.get("status")
        self.probationStatus:                       int = self.data.get("probationStatus")
        self.updatedTime:                           str = self.data.get("updatedTime")
        self.primaryLanguage:                       str = self.data.get("primaryLanguage")
        self.modifiedTime:                          str = self.data.get("modifiedTime")
        self.membersCount:                          int = self.data.get("membersCount")
        self.tagline:                               str = self.data.get("tagline")
        self.name:                                  str = self.data.get("name")
        self.endpoint:                              str = self.data.get("endpoint")
        self.communityHeadList:                     list = self.data.get("communityHeadList")
        self.listedStatus:                          int = self.data.get("listedStatus")
        self.extensions:                            list = self.data.get("extensions")
        self.mediaList:                             list = self.data.get("mediaList")
        self.userAddedTopicList:                    list = self.data.get("userAddedTopicList")
        self.communityHeat:                         int = self.data.get("communityHeat")
        self.templateId:                            int = self.data.get("templateId")
        self.searchable:                            bool = self.data.get("searchable")
        self.createdTime:                           str = self.data.get("createdTime")
        self.ndcId:                                 int = self.data.get("ndcId") or int(findall(r'\d+', self.data.get("linkInfoV2").get("path"))[0])
        self.comId:                                 int = self.ndcId
        self.icon:                                  str = self.data.get("icon")
        
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
        self.globalVotesCount:                      int = self.data.get("globalVotesCount")
        self.globalVotedValue:                      int = self.data.get("globalVotedValue")
        self.votedValue:                            int = self.data.get("votedValue")
        self.keywords:                              str = self.data.get("keywords")
        self.mediaList:                             list = self.data.get("mediaList")
        self.style:                                 dict = self.data.get("style")
        self.totalQuizPlayCount:                    int = self.data.get("totalQuizPlayCount")
        self.title:                                 str = self.data.get("title")
        self.tipInfo:                               dict = self.data.get("tipInfo")
        self.contentRating:                         int = self.data.get("contentRating")
        self.content:                               str = self.data.get("content")
        self.needHidden:                            bool = self.data.get("needHidden")
        self.guestVotesCount:                       int = self.data.get("guestVotesCount")
        self.type:                                  int = self.data.get("type")
        self.status:                                int = self.data.get("status")
        self.globalCommentsCount:                   int = self.data.get("globalCommentsCount")
        self.modifiedTime:                          str = self.data.get("modifiedTime")
        self.widgetDisplayInterval:                 str = self.data.get("widgetDisplayInterval")
        self.totalPollVoteCount:                    int = self.data.get("totalPollVoteCount")
        self.blogId:                                str = self.data.get("blogId")
        self.viewCount:                             int = self.data.get("viewCount")
        self.language:                              str = self.data.get("language")
        self.author:                                UserProfile = UserProfile(data=self.data.get("author"))
        self.extensions:                            dict = self.data.get("extensions")
        self.votesCount:                            int = self.data.get("votesCount")
        self.ndcId:                                 int = self.data.get("ndcId")
        self.createdTime:                           str = self.data.get("createdTime")
        self.endTime:                               str = self.data.get("endTime")
        self.commentsCount:                         int = self.data.get("commentsCount")

    def json(self) -> dict: return self.data

class CBlogList:
    def __init__(self, data: dict):
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

    def json(self): return self.data

class Coupon:
    def __init__(self, data: dict):
        self.data:          dict = data.get("coupon", data)
        self.expiredTime:   str = self.data.get("expiredTime")
        self.couponId:      str = self.data.get("couponId")
        self.scopeDesc:     str = self.data.get("scopeDesc")
        self.status:        int = self.data.get("status")
        self.modifiedTime:  str = self.data.get("modifiedTime")
        self.couponValue:   int = self.data.get("couponValue")
        self.expiredType:   int = self.data.get("expiredType")
        self.title:         str = self.data.get("title")
        self.couponType:    int = self.data.get("couponType")
        self.createdTime:   str = self.data.get("createdTime")

    def json(self) -> dict: return self.data

class Wallet:
    def __init__(self, data: dict):
        self.data:                  dict = data.get("wallet", data)
        self.totalCoinsFloat:       float = self.data.get("totalCoinsFloat")
        self.adsEnabled:            bool = self.data.get("adsEnabled")
        self.adsVideoStats:         dict = self.data.get("adsVideoStats")
        self.adsFlags:              int = self.data.get("adsFlags")
        self.totalCoins:            int = self.data.get("totalCoins")
        self.businessCoinsEnabled:  bool = self.data.get("businessCoinsEnabled")
        self.totalBusinessCoins:    int = self.data.get("totalBusinessCoins")
        self.totalBusinessCoinsFloat: float = self.data.get("totalBusinessCoinsFloat")

    def json(self) -> dict: return self.data

class Themepack:
    def __init__(self, data: dict):
        self.data:                  dict = data
        self.themeColor:            str = self.data.get("themeColor")
        self.themePackHash:         str = self.data.get("themePackHash")
        self.themePackRevision:     int = self.data.get("themePackRevision")
        self.themePackUrl:          str = self.data.get("themePackUrl")

    def json(self) -> dict: return self.data

class Notification:
    def __init__(self, data: dict):
        self.data:              dict = data
        self.parentText:        str = self.data.get("parentText")
        self.objectId:          str = self.data.get("objectId")
        self.contextText:       str = self.data.get("contextText")
        self.type:              int = self.data.get("type")
        self.parentId:          str = self.data.get("parentId")
        self.operator:          UserProfile = UserProfile(self.data.get("operator"))
        self.createdTime:       str = self.data.get("createdTime")
        self.parentType:        int = self.data.get("parentType")
        self.comId:             int = self.data.get("ndcId")
        self.notificationId:    str = self.data.get("notificationId")
        self.objectText:        str = self.data.get("objectText")
        self.contextValue:      str = self.data.get("contextValue")
        self.contextComId:      int = self.data.get("contextNdcId")
        self.objectType:        int = self.data.get("objectType")

    def json(self) -> dict: return self.data

class ResetPassword:
    def __init__(self, data: dict):
        self.data:      dict = data
        self.response:  ApiResponse = ApiResponse(self.data)
        self.secret:    str = self.data.get("secret")

    def json(self) -> dict: return self.data

class Authenticate:
    def __init__(self, data: dict):
        self.data:      dict = data
        self.sid:       str = self.data.get("sid")
        self.userId:    str = self.data.get("auid")
        self.profile:   UserProfile = UserProfile(self.data.get("userProfile"))
        self.secret:    str = self.data.get("secret")

    def json(self) -> dict: return self.data

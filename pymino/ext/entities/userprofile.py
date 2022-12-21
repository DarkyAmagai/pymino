class UserProfile:
    def __init__(self, data: dict):
        self.data:                      dict = data.get('userProfile', data)
        self.status:                    int = self.data.get('status', None)
        self.moodSticker:               str = self.data.get('moodSticker', None)
        self.itemsCount:                int = self.data.get('itemsCount', None)
        self.consecutiveCheckInDays:    int = self.data.get('consecutiveCheckInDays', None)
        self.uid:                       str = self.data.get('uid', None)
        self.userId:                    str = self.uid
        self.aminoId:                   str = self.data.get('aminoId', None)
        self.modifiedTime:              str = self.data.get('modifiedTime', None)
        self.followingStatus:           int = self.data.get('followingStatus', None)
        self.onlineStatus:              int = self.data.get('onlineStatus', None)
        self.accountMembershipStatus:   int = self.data.get('accountMembershipStatus', None)
        self.isGlobal:                  bool = self.data.get('isGlobal', None)
        self.avatarFrameId:             str = self.data.get('avatarFrameId', None)
        self.fanClubList:               list = self.data.get('fanClubList', None)
        self.reputation:                int = self.data.get('reputation', None)
        self.postsCount:                int = self.data.get('postsCount', None)
        self.avatarFrame:               dict = self.data.get('avatarFrame', None)
        self.followers:                 int = self.data.get('membersCount', None)
        self.nickname:                  str = self.data.get('nickname', None)
        self.username:                  str = self.nickname
        self.mediaList:                 list = self.data.get('mediaList', None)
        self.icon:                      str = self.data.get('icon', None)
        self.avatar:                    str = self.icon 
        self.isNicknameVerified:        bool = self.data.get('isNicknameVerified', None)
        self.mood:                      str = self.data.get('mood', None)
        self.level:                     int = self.data.get('level', None)
        self.pushEnabled:               bool = self.data.get('pushEnabled', None)
        self.membershipStatus:          int = self.data.get('membershipStatus', None)
        self.influencerInfo:            dict = self.data.get('influencerInfo', None)
        self.content:                   str = self.data.get('content', None)
        self.following:                 int = self.data.get('following', None)
        self.role:                      int = self.data.get('role', None)
        self.commentsCount:             int = self.data.get('commentsCount', None)
        self.ndcId:                     int = self.data.get('ndcId', None)
        self.comId:                     int = self.ndcId
        self.createdTime:               str = self.data.get('createdTime', None)
        self.extensions:                dict = self.data.get('extensions', None)
        self.visitPrivacy:              int = self.data.get('visitPrivacy', None)
        self.storiesCount:              int = self.data.get('storiesCount', None)
        self.blogsCount:                int = self.data.get('blogsCount', None)

    def json(self): return self.data

class UserProfileList:
	def __init__(self, data: dict):
		self.data = data.get("userProfileList", data) if isinstance(data, dict) else data

		parser:                            list = [UserProfile(x) for x in self.data]
		self.status:                       list = [x.status for x in parser]
		self.moodSticker:                  list = [x.moodSticker for x in parser]
		self.itemsCount:                   list = [x.itemsCount for x in parser]
		self.consecutiveCheckInDays:       list = [x.consecutiveCheckInDays for x in parser]
		self.uid:                          list = [x.uid for x in parser]
		self.userId:                       list = self.uid
		self.modifiedTime:                 list = [x.modifiedTime for x in parser]
		self.followingStatus:              list = [x.followingStatus for x in parser]
		self.onlineStatus:                 list = [x.onlineStatus for x in parser]
		self.accountMembershipStatus:      list = [x.accountMembershipStatus for x in parser]
		self.isGlobal:                     list = [x.isGlobal for x in parser]
		self.avatarFrameId:                list = [x.avatarFrameId for x in parser]
		self.fanClubList:                  list = [x.fanClubList for x in parser]
		self.reputation:                   list = [x.reputation for x in parser]
		self.postsCount:                   list = [x.postsCount for x in parser]
		self.avatarFrame:                  list = [x.avatarFrame for x in parser]
		self.followers:                    list = [x.followers for x in parser]
		self.nickname:                     list = [x.nickname for x in parser]
		self.username:                     list = self.nickname
		self.mediaList:                    list = [x.mediaList for x in parser]
		self.icon:                         list = [x.icon for x in parser]
		self.avatar:                       list = self.icon
		self.isNicknameVerified:           list = [x.isNicknameVerified for x in parser]
		self.mood:                         list = [x.mood for x in parser]
		self.level:                        list = [x.level for x in parser]
		self.pushEnabled:                  list = [x.pushEnabled for x in parser]
		self.membershipStatus:             list = [x.membershipStatus for x in parser]
		self.influencerInfo:               list = [x.influencerInfo for x in parser]
		self.content:                      list = [x.content for x in parser]
		self.following:                    list = [x.following for x in parser]
		self.role:                         list = [x.role for x in parser]
		self.commentsCount:                list = [x.commentsCount for x in parser]
		self.ndcId:                        list = [x.ndcId for x in parser]
		self.comId:                        list = self.ndcId
		self.createdTime:                  list = [x.createdTime for x in parser]
		self.extensions:                   list = [x.extensions for x in parser]
		self.visitPrivacy:                 list = [x.visitPrivacy for x in parser]
		self.storiesCount:                 list = [x.storiesCount for x in parser]
		self.blogsCount:                   list = [x.blogsCount for x in parser]

class OnlineMembers:
	def __init__(self, data: dict):
		self.data: dict                    = data.get('o', data)
		self.topic                         = self.data.get('topic', None)
		self.ndcId                         = self.data.get('ndcId', None)
		self.comId                         = self.ndcId
		self.usersOnline                   = self.data.get('userProfileCount', None)
		self._user: dict                   = self.data.get('userProfileList', None)[0]
		self.isGuest                       = self._user.get('isGuest', None)
		self.uid                           = self._user.get('uid', None)
		self.userId                        = self.uid
		self.status                        = self._user.get('status', None)
		self.icon                          = self._user.get('icon', None)
		self.avatar                        = self.icon
		self.reputation                    = self._user.get('reputation', None)
		self.role                          = self._user.get('role', None)
		self.nickname                      = self._user.get('nickname', None)
		self.username                      = self.nickname
		self.level                         = self._user.get('level', None)
		self.extensions                    = self._user.get('extensions', None)
		self.accountMembershipStatus       = self._user.get('accountMembershipStatus', None)
		self.avatarFrameId                 = self._user.get('avatarFrameId', None)
		self.avatarFrame                   = self._user.get('avatarFrame', None)
		self.isNicknameVerified            = self._user.get('isNicknameVerified', None)

	def json(self): return self.data
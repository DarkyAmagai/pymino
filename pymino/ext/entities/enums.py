from enum import IntEnum, Enum

class ObjectTypes(IntEnum):
    USER = 0
    BLOG = 1
    WIKI = 2
    CHAT = 12

class ChatTypes(Enum):
    LATEST = "latest"
    POPULAR = "popular"
    RECOMMENDED = "recommended"

class LeaderboardTypes(IntEnum):
    ACTIVE24H = 1
    ACTIVE7D = 2
    HALL_OF_FAME = 3
    CHECK_IN = 4
    QUIZ = 5

class UserTypes(Enum):
    LEADERS = "leaders"
    CURATORS = "curators"       
    RECENT = "recent"
    FEATURED = "featured"    
    BANNED = "banned"

class FlagTypes(IntEnum):
    AGGRESSION =  0
    SPAM = 2
    OFFTOPIC = 4
    VIOLENCE = 106
    INTOLERANCE = 107
    SUICIDE = 108
    TROLLING = 109
    PORNOGRAPHY = 110

class OnlineTypes(IntEnum):
    ONLINE = 1
    OFFLINE = 2
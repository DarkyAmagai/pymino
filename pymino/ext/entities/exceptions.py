from ujson import loads
from contextlib import suppress

class UnsupportedService(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class FileTooLarge(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidRequest(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidSession(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AccessDenied(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class UnexistentData(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ActionNotAllowed(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ServiceUnderMaintenance(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class MessageNeeded(Exception):
    def __init__(self, response: str):
        super().__init__(response)
        
class InvalidAccountOrPassword(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AccountDisabled(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class EmailAlreadyTaken(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AccountDoesNotExist(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidDevice(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AccountLimitReached(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CantFollowYourself(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class UserUnavailable(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class YouAreBanned(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class UserNotMemberOfCommunity(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class RequestRejected(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ActivateAccount(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CantLeaveCommunity(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ReachedTitleLength(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class EmailFlaggedAsSpam(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AccountDeleted(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ReachedMaxTitles(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class VerificationRequired(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class UserBannedByTeamAmino(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class BadImage(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class RequestedNoLongerExists(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InsufficientLevel(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class WallCommentingDisabled(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CommunityNoLongerExists(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidCodeOrLink(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CommunityNameAlreadyTaken(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CommunityCreateLimitReached(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CommunityDisabled(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CommunityDeleted(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class TooManyInviteUsers(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ChatInvitesDisabled(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class RemovedFromChat(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class UserNotJoined(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class LevelFiveRequiredToEnableProps(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ChatViewOnly(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class ChatMessageTooBig(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InviteCodeNotFound(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AlreadyRequestedJoinCommunity(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AlreadyCheckedIn(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AlreadyUsedMonthlyRepair(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AccountAlreadyRestored(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class IncorrectVerificationCode(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class NotOwnerOfChatBubble(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class NotEnoughCoins(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AlreadyPlayedLottery(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class CannotSendCoins(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class AminoIDAlreadyChanged(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidAminoID(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidName(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class YouHaveBlockedThisUser(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class NoLongerExists(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class API_ERROR(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class BlockedByOrganizer(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class YouAreBlockedByThisUser(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class UserHasBeenDeleted(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class APIException(Exception):
    def __init__(self, response: str):
        self.exception_map = {
            100: UnsupportedService,
            102: FileTooLarge,
            103: InvalidRequest,
            105: InvalidSession,
            106: AccessDenied,
            107: UnexistentData,
            110: ActionNotAllowed,
            111: ServiceUnderMaintenance,
            113: MessageNeeded,
            200: InvalidAccountOrPassword,
            210: AccountDisabled,
            215: EmailAlreadyTaken,
            216: AccountDoesNotExist,
            218: InvalidDevice,
            219: AccountLimitReached,
            221: CantFollowYourself,
            225: UserUnavailable,
            229: YouAreBanned,
            230: UserNotMemberOfCommunity,
            235: RequestRejected,
            238: ActivateAccount,
            239: CantLeaveCommunity,
            240: ReachedTitleLength,
            241: EmailFlaggedAsSpam,
            245: UserHasBeenDeleted,
            246: AccountDeleted,
            262: ReachedMaxTitles,
            270: VerificationRequired,
            293: UserBannedByTeamAmino,
            300: BadImage,
            500: RequestedNoLongerExists,
            551: InsufficientLevel,
            603: YouAreBlockedByThisUser,
            604: YouHaveBlockedThisUser,
            606: BlockedByOrganizer,
            700: NoLongerExists,
            702: WallCommentingDisabled,
            801: CommunityNoLongerExists,
            802: InvalidCodeOrLink,
            805: CommunityNameAlreadyTaken,
            806: CommunityCreateLimitReached,
            814: CommunityDisabled,
            833: CommunityDeleted,
            1606: TooManyInviteUsers,
            1611: ChatInvitesDisabled,
            1612: RemovedFromChat,
            1613: UserNotJoined,
            1661: LevelFiveRequiredToEnableProps,
            1663: ChatViewOnly,
            1664: ChatMessageTooBig,
            1900: InviteCodeNotFound,
            2001: AlreadyRequestedJoinCommunity,
            2601: AlreadyCheckedIn,
            2611: AlreadyUsedMonthlyRepair,
            2800: AccountAlreadyRestored,
            3102: IncorrectVerificationCode,
            3905: NotOwnerOfChatBubble,
            4300: NotEnoughCoins,
            4400: AlreadyPlayedLottery,
            4500: CannotSendCoins,
            6001: AminoIDAlreadyChanged,
            6002: InvalidAminoID,
            99001: InvalidName
        }
    
        self.url = None
        self.message = None
        self.status_code = None

        with suppress(Exception):
            json_response: dict = loads(response)
            self.status_code: int = json_response.get("api:statuscode", response)
            self.message: str = json_response.get("api:message", response)
            self.url: str = json_response.get("url", response)
        
        if any([
            not isinstance(self.status_code, int),
            self.status_code not in self.exception_map
        ]):
            raise API_ERROR(response)
        
        exception = self.exception_map.get(self.status_code)
        if self.exception_map.get(self.status_code):
            if self.url is not None:
                self.message = f"{self.message} ({self.url})"

            raise exception(self.message)
            
class MissingCommunityId(Exception):
    def __init__(self):
        super().__init__(
            "Please provide a community id to the bot before running it or add it to the function call."
            )

class VerifyCommunityIdIsCorrect(Exception):
    def __init__(self):
        super().__init__(
            "Check your community id! It should be an integer.\nIf you're using a community link, use `fetch_community_id` instead."
            )
        
class MissingEmailPasswordOrSid(Exception):
    def __init__(self):
        super().__init__(
            "Please provide an email, password or sid to the bot.run() function before running it."
            )
        
class LoginFailed(Exception):
    def __init__(self):
        super().__init__(
            "Login failed. Please check your email and password."
            )
        
class FailedToFetchWebsocketUrl(Exception):
    def __init__(self):
        super().__init__(
            "Failed to fetch websocket url. Please try again later."
            )
        
class LoginRequired(Exception):
    def __init__(self):
        super().__init__(
            "Please login before using this function."
            )
        
class InvalidImage(Exception):
    def __init__(self):
        super().__init__(
            "Invalid image. Please check the image you are trying to upload. It should be a file path or a url."
            )
        
class MissingTimers(Exception):
    def __init__(self):
        super().__init__(
            "You are missing the start and end timers. Please provide them."
            )
        
class NoDataProvided(Exception):
    def __init__(self):
        super().__init__(
            "No data provided. Please provide data to the function."
            )
        
class NotLoggedIn(Exception):
    def __init__(self):
        super().__init__(
            "You are not logged in. Please login before using this function."
            )
        
class Forbidden(Exception):
    def __init__(self):
        super().__init__(
            "403 Forbidden. Possible IP ban. Please try again later."
            "\nIf this error persists, change your IP address.\n"
            )
        
class ServiceUnavailable(Exception):
    def __init__(self):
        super().__init__(
            "Amino is currently down or having issues. Please try again later."
            "\nThis has nothing to do with the bot or your internet connection.\n"
            )
        
class BadGateway(Exception):
    def __init__(self):
        super().__init__(
            "Amino is currently down or having issues. Please try again later."
            "\nThis has nothing to do with the bot or your internet connection.\n"
            )
        
class InvalidLink(Exception):
    def __init__(self):
        super().__init__(
            "Invalid link. Please check the link you are trying to use."
            )
        
class MustRunInContext(Exception):
    def __init__(self):
        super().__init__(
            "This function must be run in a context."
            )
        
class WrongWebSocketPackage(Exception):
    def __init__(self):
        super().__init__(
            "Wrong websocket package was installed. We corrected it for you."
            "\nPlease restart your bot.\n"
            )
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

class DataNoLongerExists(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InternalServerError(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidEmail(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidPassword(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class WhoaCooldown(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidThemepack(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class InvalidVoiceNote(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class PostedTooRecently(Exception):
    def __init__(self, response: str):
        super().__init__(response)

class APIException(Exception):
    def __init__(self, response: dict):
        exception_map = {
            100: UnsupportedService,
            101: InternalServerError,
            102: FileTooLarge,
            103: InvalidRequest,
            104: InvalidRequest,
            105: InvalidSession,
            106: AccessDenied,
            107: UnexistentData,
            110: ActionNotAllowed,
            111: ServiceUnderMaintenance,
            113: MessageNeeded,
            200: InvalidAccountOrPassword,
            210: AccountDisabled,
            213: InvalidEmail,
            214: InvalidPassword,
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
            291: WhoaCooldown,
            293: UserBannedByTeamAmino,
            300: BadImage,
            313: InvalidThemepack,
            314: InvalidVoiceNote,
            500: RequestedNoLongerExists,
            503: PostedTooRecently,
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
            826: CommunityCreateLimitReached,
            833: CommunityDeleted,
            1600: DataNoLongerExists,
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

        status_code = response.get("api:statuscode")
        message = response.get("api:message")
        url = response.get("url")

        if status_code in exception_map:
            exception = exception_map.get(status_code)

            if url is not None:
                message = f"{message} ({url})"

            if exception:
                raise exception(message)

        raise API_ERROR(response)

            
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
        
class NullResponse(Exception):
    def __init__(self):
        super().__init__(
            "Server returned a null response. Possible crash content in the requested data."
            )
        
class PingFailed(Exception):
    def __init__(self):
        super().__init__(
            "Ping failed. Please make sure you are logged in and try again."
            )
        
class IntentsNotEnabled(Exception):
    def __init__(self):
        super().__init__(
            "Intents are not enabled. Please enable them in your Bot instance and try again."
            )

class InvalidCommandPrefix(Exception):
    def __init__(self):
        super().__init__(
            "Invalid command prefix. Please provide a valid command prefix."
            )
        
class MissingAwaitError(Exception):
    def __init__(self):
        super().__init__(
            "Missing await error. Please add `await` before your function call."
            )
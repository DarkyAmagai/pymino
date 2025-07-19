from typing import Any, NoReturn, cast

__all__ = (
    "APIException",
    "API_ERROR",
    "AccessDenied",
    "AccountAlreadyRestored",
    "AccountDeleted",
    "AccountDisabled",
    "AccountDoesNotExist",
    "AccountLimitReached",
    "AccountLoginRatelimited",
    "ActionNotAllowed",
    "ActivateAccount",
    "AlreadyCheckedIn",
    "AlreadyPlayedLottery",
    "AlreadyRequestedJoinCommunity",
    "AlreadyUsedMonthlyRepair",
    "AminoIDAlreadyChanged",
    "BadGateway",
    "BadImage",
    "BlockedByOrganizer",
    "CannotSendCoins",
    "CantFollowYourself",
    "CantLeaveCommunity",
    "ChatInvitesDisabled",
    "ChatMessageTooBig",
    "ChatViewOnly",
    "CommunityCreateLimitReached",
    "CommunityDeleted",
    "CommunityDisabled",
    "CommunityNameAlreadyTaken",
    "CommunityNoLongerExists",
    "DataNoLongerExists",
    "EmailAlreadyTaken",
    "EmailFlaggedAsSpam",
    "FailedToFetchWebsocketUrl",
    "FileTooLarge",
    "Forbidden",
    "IncorrectVerificationCode",
    "InsufficientLevel",
    "IntentsNotEnabled",
    "InternalServerError",
    "InvalidAccountOrPassword",
    "InvalidAminoID",
    "InvalidCodeOrLink",
    "InvalidCommandPrefix",
    "InvalidDevice",
    "InvalidEmail",
    "InvalidImage",
    "InvalidLink",
    "InvalidName",
    "InvalidPassword",
    "InvalidRequest",
    "InvalidSession",
    "InvalidThemepack",
    "InvalidVoiceNote",
    "InviteCodeNotFound",
    "LevelFiveRequiredToEnableProps",
    "LoginFailed",
    "LoginRequired",
    "MessageNeeded",
    "MissingAwaitError",
    "MissingCommunityId",
    "MissingDeviceKeyOrSignatureKey",
    "MissingEmailPasswordOrSid",
    "MissingServiceKey",
    "MissingTimers",
    "MustRunInContext",
    "NoDataProvided",
    "NoLongerExists",
    "NotEnoughCoins",
    "NotLoggedIn",
    "NotOwnerOfChatBubble",
    "NullResponse",
    "PingFailed",
    "PostedTooRecently",
    "PyminoException",
    "ReachedMaxTitles",
    "ReachedTitleLength",
    "RemovedFromChat",
    "RequestRejected",
    "RequestedNoLongerExists",
    "ServiceUnavailable",
    "ServiceUnderMaintenance",
    "TooManyInviteUsers",
    "UnexistentData",
    "UnsupportedService",
    "UserBannedByTeamAmino",
    "UserHasBeenDeleted",
    "UserNotJoined",
    "UserNotMemberOfCommunity",
    "UserUnavailable",
    "VerificationRequired",
    "VerifyCommunityIdIsCorrect",
    "WallCommentingDisabled",
    "WhoaCooldown",
    "WrongWebSocketPackage",
    "YouAreBanned",
    "YouAreBlockedByThisUser",
    "YouHaveBlockedThisUser",
)


class PyminoException(Exception): ...


class UnsupportedService(PyminoException): ...


class FileTooLarge(PyminoException): ...


class InvalidRequest(PyminoException): ...


class InvalidSession(PyminoException): ...


class AccessDenied(PyminoException): ...


class UnexistentData(PyminoException): ...


class ActionNotAllowed(PyminoException): ...


class ServiceUnderMaintenance(PyminoException): ...


class MessageNeeded(PyminoException): ...


class InvalidAccountOrPassword(PyminoException): ...


class AccountDisabled(PyminoException): ...


class EmailAlreadyTaken(PyminoException): ...


class AccountDoesNotExist(PyminoException): ...


class InvalidDevice(PyminoException): ...


class AccountLimitReached(PyminoException): ...


class CantFollowYourself(PyminoException): ...


class UserUnavailable(PyminoException): ...


class YouAreBanned(PyminoException): ...


class UserNotMemberOfCommunity(PyminoException): ...


class RequestRejected(PyminoException): ...


class ActivateAccount(PyminoException): ...


class CantLeaveCommunity(PyminoException): ...


class ReachedTitleLength(PyminoException): ...


class EmailFlaggedAsSpam(PyminoException): ...


class AccountDeleted(PyminoException): ...


class ReachedMaxTitles(PyminoException): ...


class VerificationRequired(PyminoException): ...


class UserBannedByTeamAmino(PyminoException): ...


class BadImage(PyminoException): ...


class RequestedNoLongerExists(PyminoException): ...


class InsufficientLevel(PyminoException): ...


class WallCommentingDisabled(PyminoException): ...


class CommunityNoLongerExists(PyminoException): ...


class InvalidCodeOrLink(PyminoException): ...


class CommunityNameAlreadyTaken(PyminoException): ...


class CommunityCreateLimitReached(PyminoException): ...


class CommunityDisabled(PyminoException): ...


class CommunityDeleted(PyminoException): ...


class TooManyInviteUsers(PyminoException): ...


class ChatInvitesDisabled(PyminoException): ...


class RemovedFromChat(PyminoException): ...


class UserNotJoined(PyminoException): ...


class LevelFiveRequiredToEnableProps(PyminoException): ...


class ChatViewOnly(PyminoException): ...


class ChatMessageTooBig(PyminoException): ...


class InviteCodeNotFound(PyminoException): ...


class AlreadyRequestedJoinCommunity(PyminoException): ...


class AlreadyCheckedIn(PyminoException): ...


class AlreadyUsedMonthlyRepair(PyminoException): ...


class AccountAlreadyRestored(PyminoException): ...


class IncorrectVerificationCode(PyminoException): ...


class NotOwnerOfChatBubble(PyminoException): ...


class NotEnoughCoins(PyminoException): ...


class AlreadyPlayedLottery(PyminoException): ...


class CannotSendCoins(PyminoException): ...


class AminoIDAlreadyChanged(PyminoException): ...


class InvalidAminoID(PyminoException): ...


class InvalidName(PyminoException): ...


class YouHaveBlockedThisUser(PyminoException): ...


class NoLongerExists(PyminoException): ...


class API_ERROR(PyminoException): ...


class BlockedByOrganizer(PyminoException): ...


class YouAreBlockedByThisUser(PyminoException): ...


class UserHasBeenDeleted(PyminoException): ...


class DataNoLongerExists(PyminoException): ...


class InternalServerError(PyminoException): ...


class InvalidEmail(PyminoException): ...


class InvalidPassword(PyminoException): ...


class WhoaCooldown(PyminoException): ...


class InvalidThemepack(PyminoException): ...


class InvalidVoiceNote(PyminoException): ...


class PostedTooRecently(PyminoException): ...


def APIException(response: dict[str, Any]) -> NoReturn:
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
        99001: InvalidName,
    }
    status_code = response.get("api:statuscode")
    message = response.get("api:message")
    url = response.get("url")
    if isinstance(status_code, int) and status_code in exception_map:
        exception = exception_map[status_code]
        if url is not None:
            message = f"{message} ({url})"
        raise exception(cast(str, message))
    raise API_ERROR(response)


class AccountLoginRatelimited(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Account login ratelimited by Amino, wait 3 minutes and try again."
        )


class MissingCommunityId(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Please provide a community id to the bot before running it or add it to the function call."
        )


class VerifyCommunityIdIsCorrect(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Check your community id! It should be an integer.\nIf you're using a community link, use `fetch_community_id` instead."
        )


class MissingEmailPasswordOrSid(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Please provide an email, password or sid to the bot.run() function before running it."
        )


class LoginFailed(PyminoException):
    def __init__(self) -> None:
        super().__init__("Login failed. Please check your email and password.")


class FailedToFetchWebsocketUrl(PyminoException):
    def __init__(self) -> None:
        super().__init__("Failed to fetch websocket url. Please try again later.")


class LoginRequired(PyminoException):
    def __init__(self) -> None:
        super().__init__("Please login before using this function.")


class InvalidImage(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Invalid image. Please check the image you are trying to upload. It should be a file path or a url."
        )


class MissingTimers(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "You are missing the start and end timers. Please provide them."
        )


class NoDataProvided(PyminoException):
    def __init__(self) -> None:
        super().__init__("No data provided. Please provide data to the function.")


class NotLoggedIn(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "You are not logged in. Please login before using this function."
        )


class Forbidden(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "403 Forbidden. Possible IP ban. Please try again later. If this error persists, change your IP address."
        )


class ServiceUnavailable(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Amino is currently down or having issues. Please try again later. This has nothing to do with the bot or your internet connection."
        )


class BadGateway(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Amino is currently down or having issues. Please try again later. This has nothing to do with the bot or your internet connection."
        )


class InvalidLink(PyminoException):
    def __init__(self) -> None:
        super().__init__("Invalid link. Please check the link you are trying to use.")


class MustRunInContext(PyminoException):
    def __init__(self) -> None:
        super().__init__("This function must be run in a context.")


class WrongWebSocketPackage(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Wrong websocket package was installed. We corrected it for you. Please restart your bot."
        )


class NullResponse(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Server returned a null response. Possible crash content in the requested data."
        )


class PingFailed(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Ping failed. Please make sure you are logged in and try again."
        )


class IntentsNotEnabled(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Intents are not enabled. Please enable them in your Bot instance and try again."
        )


class InvalidCommandPrefix(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Invalid command prefix. Please provide a valid command prefix."
        )


class MissingAwaitError(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Missing await error. Please add `await` before your function call."
        )


class MissingDeviceKeyOrSignatureKey(PyminoException):
    def __init__(self) -> None:
        super().__init__(
            "Missing signature and or device key. Please provide a signature or device key."
        )


class MissingServiceKey(PyminoException):
    def __init__(self):
        super().__init__(
            "It appears you are missing a required service key. This key is essential for accessing the service. To obtain the key, please visit the official Discord server. The Server provides support and resources related to the service. https://discord.gg/3HRdkVNets"
        )

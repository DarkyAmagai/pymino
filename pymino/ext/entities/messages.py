import re
import time
from typing import Any, Optional, cast

from pymino.ext.entities import userprofile

__all__ = (
    "CMessage",
    "CMessageAuthorList",
    "CMessageExtensions",
    "CMessages",
    "Channel",
    "Message",
    "MessageAuthor",
    "PrepareMessage",
    "ReplyMessage",
)


class PrepareMessage:
    def __init__(
        self,
        content: Optional[str] = None,
        mediaType: int = 0,
        type: int = 0,
        **kwargs: Any,
    ) -> None:
        self.base_message: dict[str, Any] = {
            "content": content,
            "mediaType": mediaType,
            "type": type,
            "clientRefId": int(time.time() / 10 % 1000000000),
            "timestamp": int(time.time() * 1000),
        }
        self.base_message.update(kwargs)

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.base_message


class MessageAuthor:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return bool(self.uid)

    @property
    def uid(self) -> str:
        """Returns the user id of the author."""
        return self.data.get("uid", "")

    @property
    def userId(self) -> str:
        """Returns the user id of the author."""
        return self.uid

    @property
    def status(self) -> int:
        """Returns the status of the author."""
        return self.data.get("status", 0)

    @property
    def icon(self) -> Optional[str]:
        """Returns the icon of the author."""
        return self.data.get("icon")

    @property
    def avatar(self) -> Optional[str]:
        """Returns the icon of the author."""
        return self.icon

    @property
    def reputation(self) -> int:
        """Returns the reputation of the author."""
        return self.data.get("reputation", 0)

    @property
    def role(self) -> int:
        """Returns the role of the author."""
        return self.data.get("role", 0)

    @property
    def nickname(self) -> str:
        """Returns the nickname of the author."""
        return self.data.get("nickname", "")

    @property
    def username(self) -> str:
        """Returns the nickname of the author."""
        return self.nickname

    @property
    def level(self) -> int:
        """Returns the level of the author."""
        return self.data.get("level", 0)

    @property
    def accountMembershipStatus(self) -> int:
        """Returns the account membership status of the author."""
        return self.data.get("accountMembershipStatus", 0)

    @property
    def avatarFrame(self) -> dict[str, Any]:
        """Returns the avatar frame of the author."""
        return self.data.get("avatarFrame") or {}

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.data


class CMessage:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("result") or data.get("message", data)

    @property
    def includedInSummary(self) -> bool:
        """Returns if the message is included in the summary."""
        return self.data.get("includedInSummary", False)

    @property
    def uid(self) -> str:
        """Returns the user id of the author."""
        return self.data.get("uid", "")

    @property
    def userId(self) -> str:
        """Returns the user id of the author."""
        return self.uid

    @property
    def author(self) -> dict[str, Any]:
        """Returns the author object of the message."""
        return self.data.get("author") or {}

    @property
    def isHidden(self) -> bool:
        """Returns if the message is hidden."""
        return self.data.get("isHidden", False)

    @property
    def messageId(self) -> str:
        """Returns the message id."""
        return self.data.get("messageId", "")

    @property
    def mediaType(self) -> Optional[int]:
        """Returns the media type of the message."""
        return self.data.get("mediaType")

    @property
    def content(self) -> Optional[str]:
        """Returns the content of the message."""
        return self.data.get("content")

    @property
    def clientRefId(self) -> int:
        """Returns the client reference id of the message."""
        return self.data.get("clientRefId", 0)

    @property
    def threadId(self) -> str:
        """Returns the thread id of the message."""
        return self.data.get("threadId", "")

    @property
    def chatId(self) -> str:
        """Returns the chat id of the message."""
        return self.threadId

    @property
    def createdTime(self) -> str:
        """Returns the created time of the message."""
        return self.data.get("createdTime", "")

    @property
    def extensions(self) -> dict[str, Any]:
        """Returns the extensions of the message."""
        return self.data.get("extensions") or {}

    @property
    def type(self) -> int:
        """Returns the type of the message."""
        return self.data.get("type", 0)

    @property
    def mediaValue(self) -> Optional[str]:
        """Returns the media value of the message."""
        return self.data.get("mediaValue")

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.data


class ReplyMessage:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def includedInSummary(self) -> bool:
        """Is a boolean value that determines whether the message is included in the summary of the chat."""
        return self.data.get("includedInSummary", False)

    @property
    def uid(self) -> str:
        """Is the user id of the user who sent the message that was replied to.

        THIS IS NOT THE BOT'S USER ID.

        """
        return self.data.get("uid", "")

    @property
    def userId(self) -> str:
        """Is the user id of the user who sent the message that was replied to.

        THIS IS NOT THE BOT'S USER ID.

        """
        return self.uid

    @property
    def author(self) -> userprofile.UserProfile:
        """Is the user profile of the user who sent the message that was replied to.

        THIS IS NOT THE BOT'S USER PROFILE.

        """
        return userprofile.UserProfile(self.data.get("author") or {})

    @property
    def isHidden(self) -> bool:
        """Is a boolean value that determines whether the message that was replied to is hidden."""
        return self.data.get("isHidden", False)

    @property
    def messageId(self) -> str:
        """Is the message id of the message that was replied to.
        THIS IS NOT THE BOT'S MESSAGE ID.

        """
        return self.data.get("messageId", "")

    @property
    def mediaType(self) -> Optional[int]:
        """Is the media type of the message that was replied to."""
        # TODO: Add media types
        return self.data.get("mediaType")

    @property
    def content(self) -> Optional[str]:
        """Is the content of the message that was replied to.

        THIS IS NOT THE BOT'S MESSAGE CONTENT.

        """
        return self.data.get("content")

    @property
    def clientRefId(self) -> int:
        """Is the client reference id of the message that was replied to.

        THIS IS NOT THE BOT'S CLIENT REFERENCE ID.

        """
        return self.data.get("clientRefId", 0)

    @property
    def threadId(self) -> str:
        """Is the thread / chat id that the message that was replied to was sent in."""
        return self.data.get("threadId", "")

    @property
    def chatId(self) -> str:
        """Is the thread / chat id that the message that was replied to was sent in."""
        return self.threadId

    @property
    def createdTime(self) -> str:
        """Is the time that the message that was replied to was sent."""
        return self.data.get("createdTime", "")

    @property
    def type(self) -> int:
        """Is the type of the message that was replied to."""
        return self.data.get("type", 0)

    @property
    def mediaValue(self) -> Optional[str]:
        """Is the media value of the message that was replied to."""
        return self.data.get("mediaValue")

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.data


class CMessageExtensions:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def messageId(self) -> Optional[str]:
        """Is the message id of the message that was replied to.

        THIS IS NOT THE BOT'S MESSAGE ID.

        """
        return self.data.get("replyMessageId")

    @property
    def message(self) -> ReplyMessage:
        """Is the message that was replied to.

        THIS IS NOT THE BOT'S MESSAGE.

        """
        return ReplyMessage(self.data.get("replyMessage") or {})

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.data


class CMessageAuthorList:
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.data = data

    @property
    def status(self) -> list[int]:
        """Returns a list of the status of the users in the chat."""
        return [i.get("status", 0) for i in self.data]

    @property
    def icon(self) -> list[Optional[str]]:
        """Returns a list of the icon of the users in the chat."""
        return [i.get("icon") for i in self.data]

    @property
    def avatar(self) -> list[Optional[str]]:
        """Returns a list of the avatar of the users in the chat."""
        return self.icon

    @property
    def reputation(self) -> list[int]:
        """Returns a list of the reputation of the users in the chat."""
        return [i.get("reputation", 0) for i in self.data]

    @property
    def role(self) -> list[int]:
        """Returns a list of the role of the users in the chat."""
        return [i.get("role", 0) for i in self.data]

    @property
    def nickname(self) -> list[str]:
        """Returns a list of the nickname of the users in the chat."""
        return [i.get("nickname", "") for i in self.data]

    @property
    def username(self) -> list[str]:
        """Returns a list of the username of the users in the chat."""
        return self.nickname

    @property
    def level(self) -> list[int]:
        """Returns a list of the level of the users in the chat."""
        return [i.get("level", 0) for i in self.data]

    @property
    def accountMembershipStatus(self) -> list[int]:
        """Returns a list of the account membership status of the users in the chat."""
        return [i.get("accountMembershipStatus", 0) for i in self.data]

    @property
    def avatarFrame(self) -> list[dict[str, Any]]:
        """Returns a list of the avatar frame of the users in the chat."""
        return [i.get("avatarFrame") or {} for i in self.data]

    def json(self) -> list[dict[str, Any]]:
        """`JSON` - returns the raw data."""
        return self.data


class CMessages:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: list[dict[str, Any]] = (
            data.get("result") or data.get("messageList") or []
        )

    @property
    def includedInSummary(self) -> list[bool]:
        """Returns a list of the included in summary of the messages in the chat."""
        return [i.get("includedInSummary", False) for i in self.data]

    @property
    def uid(self) -> list[str]:
        """Returns a list of the uid of the messages in the chat."""
        return [i.get("uid", "") for i in self.data]

    @property
    def userId(self) -> list[str]:
        """Returns a list of the user id of the messages in the chat."""
        return self.uid

    @property
    def author(self) -> CMessageAuthorList:
        """Returns a list of the author of the messages in the chat."""
        return CMessageAuthorList([i.get("author") or {} for i in self.data])

    @property
    def isHidden(self) -> list[bool]:
        """Returns a list of the is hidden of the messages in the chat."""
        return [i.get("isHidden", False) for i in self.data]

    @property
    def messageId(self) -> list[str]:
        """Returns a list of the message id of the messages in the chat."""
        return [i.get("messageId", "") for i in self.data]

    @property
    def mediaType(self) -> list[Optional[int]]:
        """Returns a list of the media type of the messages in the chat."""
        return [i.get("mediaType") for i in self.data]

    @property
    def content(self) -> list[Optional[str]]:
        """Returns a list of the content of the messages in the chat."""
        return [i.get("content") for i in self.data]

    @property
    def clientRefId(self) -> list[int]:
        """Returns a list of the client ref id of the messages in the chat."""
        return [i.get("clientRefId", 0) for i in self.data]

    @property
    def threadId(self) -> list[str]:
        """Returns a list of the thread id of the messages in the chat."""
        return [i.get("threadId", "") for i in self.data]

    @property
    def chatId(self) -> list[str]:
        """Returns a list of the chat id of the messages in the chat."""
        return self.threadId

    @property
    def createdTime(self) -> list[str]:
        """Returns a list of the created time of the messages in the chat."""
        return [i.get("createdTime", "") for i in self.data]

    @property
    def extensions(self) -> list[dict[str, Any]]:
        """Returns a list of the extensions of the messages in the chat."""
        return [i.get("extensions") or {} for i in self.data]

    @property
    def type(self) -> list[int]:
        """Returns a list of the type of the messages in the chat."""
        return [i.get("type", 0) for i in self.data]

    @property
    def mediaValue(self) -> list[Optional[str]]:
        """Returns a list of the media value of the messages in the chat."""
        return [i.get("mediaValue") for i in self.data]

    def json(self) -> list[dict[str, Any]]:
        """Returns the raw data."""
        return self.data


class Message:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("o", data)

    @property
    def ndcId(self) -> int:
        """Is the community id that the message was sent in."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        """Is the community id that the message was sent in."""
        return self.ndcId

    @property
    def chatMessage(self) -> dict[str, Any]:
        """Is the message that was sent."""
        return self.data.get("chatMessage") or {}

    @property
    def author(self) -> MessageAuthor:
        """Is the author of the message."""
        return MessageAuthor(self.chatMessage.get("author") or {})

    @property
    def mediaValue(self) -> Optional[str]:
        """Is the media value of the message."""
        return self.chatMessage.get("mediaValue")

    @property
    def threadId(self) -> str:
        """Is the thread id the message was sent in."""
        return self.chatMessage.get("threadId", "")

    @property
    def chatId(self) -> str:
        """Is the thread id the message was sent in."""
        return self.threadId

    @property
    def mediaType(self) -> Optional[int]:
        """Is the media type of the message."""
        return self.chatMessage.get("mediaType")

    @property
    def content(self) -> str:
        """Is the content of the message."""
        return self.chatMessage.get("content") or ""

    @property
    def clientRefId(self) -> int:
        """Is the client reference id of the message."""
        return self.chatMessage.get("clientRefId", 0)

    @property
    def messageId(self) -> str:
        """Is the message id of the message."""
        return self.chatMessage.get("messageId", "")

    @property
    def uid(self) -> str:
        return self.chatMessage.get("uid", "")

    @property
    def userId(self) -> str:
        return self.uid

    @property
    def createdTime(self) -> str:
        return self.chatMessage.get("createdTime", "")

    @property
    def type(self) -> int:
        """Is the type of the message."""
        return self.chatMessage.get("type", 0)

    @property
    def isHidden(self) -> bool:
        """Is whether the message is hidden or not."""
        return self.chatMessage.get("isHidden", False)

    @property
    def includedInSummary(self) -> bool:
        """Is whether the message is included in the summary or not."""
        return self.chatMessage.get("includedInSummary", False)

    @property
    def chatBubbleId(self) -> Optional[str]:
        """Is the chat bubble id of the message."""
        return self.chatMessage.get("chatBubbleId")

    @property
    def chatBubbleVersion(self) -> Optional[int]:
        """Is the chat bubble version of the message."""
        return self.chatMessage.get("chatBubbleVersion")

    @property
    def replied(self) -> CMessageExtensions:
        """Returns the replied message if there was one."""
        return CMessageExtensions(self.chatMessage.get("extensions") or {})

    @property
    def extensions(self) -> dict[str, Any]:
        """Returns the extensions of the message."""
        return self.chatMessage.get("extensions") or {}

    @property
    def mentioned_user_ids(self) -> list[str]:
        """Returns a list of the mentioned user ids."""
        return [
            i["uid"]
            for i in cast(list[Any], self.extensions.get("mentionedArray") or [])
        ]

    @property
    def mentioned_user_names(self) -> list[str]:
        """Returns a list of the mentioned user names."""
        return re.findall(r"@([^\u202c\u202d]+)", self.content or "")

    @property
    def mentioned_dictionary(self) -> dict[str, str]:
        """Returns a dictionary of the mentioned {userid: username}."""
        return dict(zip(self.mentioned_user_ids, self.mentioned_user_names))

    @property
    def alertOption(self) -> int:
        """Is the alert option of the message."""
        return self.chatMessage.get("alertOption", 0)

    @property
    def membershipStatus(self) -> int:
        """Is the membership status of the message."""
        return self.chatMessage.get("membershipStatus", 0)

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.data


class Channel:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data.get("o", data)

    @property
    def id(self) -> str:
        """Is the id of the channel."""
        return self.data.get("id", "")

    @property
    def channelName(self) -> str:
        """Is the channel name of the channel."""
        return self.data.get("channelName", "")

    @property
    def channelKey(self) -> str:
        """Is the channel key of the channel."""
        return self.data.get("channelKey", "")

    @property
    def channelUid(self) -> int:
        """Is the channel uid of the channel."""
        return self.data.get("channelUid", 0)

    @property
    def expiredTime(self) -> Optional[str]:
        """Is the expired time of the channel."""
        return self.data.get("expiredTime")

    @property
    def ndcId(self) -> int:
        """Is the community id that the channel is in."""
        return self.data.get("ndcId", 0)

    @property
    def comId(self) -> int:
        """Is the community id that the channel is in."""
        return self.ndcId

    @property
    def threadId(self) -> str:
        """Is the thread id of the channel."""
        return self.data.get("threadId", "")

    @property
    def chatId(self) -> str:
        """Is the chat id of the channel."""
        return self.threadId

    def json(self) -> dict[str, Any]:
        """Returns the raw data."""
        return self.data

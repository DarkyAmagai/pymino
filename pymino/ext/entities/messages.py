from time import time
from re import findall
from typing import Union

from . import UserProfile

class PrepareMessage:
    def __init__(self, **kwargs) -> None:
        self.base_message = {
            "content": kwargs.get("content", None),
            "mediaType": kwargs.get("mediaType", 0),
            "type": kwargs.get("type", 0),
            "clientRefId": int(time() / 10 % 1000000000),
            "timestamp": int(time() * 1000)
            }
        [self.base_message.update({key: kwargs[key]}) for key in kwargs]

    def json(self):
        """`JSON` - returns the raw data."""
        return self.base_message


class MessageAuthor:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data

    @property
    def uid(self) -> Union[str, None]:
        """
        `uid` - returns the user id of the author.
            - `str` - The user id of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("uid")
    
    @property
    def userId(self) -> Union[str, None]:
        """
        `userId` - returns the user id of the author.
            - `str` - The user id of the author.
            - `None` - If the data is `None`.

        """
        return self.uid
    
    @property
    def status(self) -> Union[int, None]:
        """
        `status` - returns the status of the author.
            - `int` - The status of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("status")
    
    @property
    def icon(self) -> Union[str, None]:
        """
        `icon` - returns the icon of the author.
            - `str` - The icon of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("icon")
    
    @property
    def avatar(self) -> Union[str, None]:
        """
        `avatar` - returns the icon of the author.
            - `str` - The icon of the author.
            - `None` - If the data is `None`.

        """
        return self.icon
    
    @property
    def reputation(self) -> Union[int, None]:
        """
        `reputation` - returns the reputation of the author.
            - `int` - The reputation of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("reputation")
    
    @property
    def role(self) -> Union[int, None]:
        """
        `role` - returns the role of the author.
            - `int` - The role of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("role")
    
    @property
    def nickname(self) -> Union[str, None]:
        """
        `nickname` - returns the nickname of the author.
            - `str` - The nickname of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("nickname")
    
    @property
    def username(self) -> Union[str, None]:
        """
        `username` - returns the nickname of the author.
            - `str` - The nickname of the author.
            - `None` - If the data is `None`.

        """
        return self.nickname
    
    @property
    def level(self) -> Union[int, None]:
        """
        `level` - returns the level of the author.
            - `int` - The level of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("level")
    
    @property
    def accountMembershipStatus(self) -> Union[int, None]:
        """
        `accountMembershipStatus` - returns the account membership status of the author.
            - `int` - The account membership status of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("accountMembershipStatus")
    
    @property
    def avatarFrame(self) -> Union[str, None]:
        """
        `avatarFrame` - returns the avatar frame of the author.
            - `str` - The avatar frame of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("avatarFrame")
        
    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data


class CMessage:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data: dict = data.get('result') or data.get('message', data)

    def return_none(func):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else func(*args, **kwargs)
        return wrapper
    
    @property
    @return_none
    def includedInSummary(self) -> Union[bool, None]:
        """
        `includedInSummary` - returns if the message is included in the summary.
            - `bool` - If the message is included in the summary.
            - `None` - If the data is `None`.

        """
        return self.data.get("includedInSummary")
    
    @property
    @return_none
    def uid(self) -> Union[str, None]:
        """
        `uid` - returns the user id of the author.
            - `str` - The user id of the author.
            - `None` - If the data is `None`.

        """
        return self.data.get("uid")
    
    @property
    @return_none
    def userId(self) -> Union[str, None]:
        """
        `userId` - returns the user id of the author.
            - `str` - The user id of the author.
            - `None` - If the data is `None`.

        """
        return self.uid
    
    @property
    @return_none
    def author(self) -> Union[dict, None]:
        """
        `author` - returns the author object of the message.
            - `dict` - The author of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("author")
    
    @property
    @return_none
    def isHidden(self) -> Union[bool, None]:
        """
        `isHidden` - returns if the message is hidden.
            - `bool` - If the message is hidden.
            - `None` - If the data is `None`.

        """
        return self.data.get("isHidden")
    
    @property
    @return_none
    def messageId(self) -> Union[str, None]:
        """
        `messageId` - returns the message id.
            - `str` - The message id.
            - `None` - If the data is `None`.

        """
        return self.data.get("messageId")
    
    @property
    @return_none
    def mediaType(self) -> Union[int, None]:
        """
        `mediaType` - returns the media type of the message.
            - `int` - The media type of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("mediaType")
    
    @property
    @return_none
    def content(self) -> Union[str, None]:
        """
        `content` - returns the content of the message.
            - `str` - The content of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("content")
    
    @property
    @return_none
    def clientRefId(self) -> Union[str, None]:
        """
        `clientRefId` - returns the client reference id of the message.
            - `str` - The client reference id of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("clientRefId")
    
    @property
    @return_none
    def threadId(self) -> Union[str, None]:
        """
        `threadId` - returns the thread id of the message.
            - `str` - The thread id of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("threadId")
    
    @property
    @return_none
    def chatId(self) -> Union[str, None]:
        """
        `chatId` - returns the chat id of the message.
            - `str` - The chat id of the message.
            - `None` - If the data is `None`.

        """
        return self.threadId
    
    @property
    @return_none
    def createdTime(self) -> Union[str, None]:
        """
        `createdTime` - returns the created time of the message.
            - `str` - The created time of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("createdTime")
    
    @property
    @return_none
    def extensions(self) -> Union[dict, None]:
        """
        `extensions` - returns the extensions of the message.
            - `dict` - The extensions of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("extensions")
    
    @property
    @return_none
    def type(self) -> Union[int, None]:
        """
        `type` - returns the type of the message.
            - `int` - The type of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("type")
    
    @property
    @return_none
    def mediaValue(self) -> Union[str, None]:
        """
        `mediaValue` - returns the media value of the message.
            - `str` - The media value of the message.
            - `None` - If the data is `None`.

        """
        return self.data.get("mediaValue")

    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data
    
class ReplyMessage:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data

    def return_none(func):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else func(*args, **kwargs)
        return wrapper
    
    @property
    @return_none
    def includedInSummary(self) -> Union[bool, None]:
        """
        `Included in summary` - is a boolean value that determines whether the message is included in the summary of the chat.

        - `True` means that the message is included in the summary of the chat.
        - `False` means that the message is not included in the summary of the chat.
        - `None` means that there was an error while trying to get the value.

        """
        return self.data.get('includedInSummary')
    
    @property
    @return_none
    def uid(self) -> Union[str, None]:
        """
        `UID` - is the user id of the user who sent the message that was replied to.

         THIS IS NOT THE BOT'S USER ID.
            - `str` means that the user id was successfully retrieved.
            - `None` means that there was an error while trying to get the user id.

        """
        return self.data.get('uid')
    
    @property
    @return_none
    def userId(self) -> Union[str, None]:
        """
        `User ID` - is the user id of the user who sent the message that was replied to.

         THIS IS NOT THE BOT'S USER ID.
            - `str` means that the user id was successfully retrieved.
            - `None` means that there was an error while trying to get the user id.

        """
        return self.uid
    
    @property
    @return_none
    def author(self) -> Union[UserProfile, None]:
        """
        `Author` - is the user profile of the user who sent the message that was replied to.

         THIS IS NOT THE BOT'S USER PROFILE.
            - `UserProfile` means that the user profile was successfully retrieved.
            - `None` means that there was an error while trying to get the user profile.

        """
        try:
            return UserProfile(self.data.get('author'))
        except Exception:
            return None
    
    @property
    @return_none
    def isHidden(self) -> Union[bool, None]:
        """
        `Is Hidden` - is a boolean value that determines whether the message that was replied to is hidden.

        - `True` means that the message is hidden.
        - `False` means that the message is not hidden.
        - `None` means that there was an error while trying to get the value.

        """
        return self.data.get('isHidden')
    
    @property
    @return_none
    def messageId(self) -> Union[str, None]:
        """
        `Message ID` - is the message id of the message that was replied to.

        THIS IS NOT THE BOT'S MESSAGE ID.
            - `str` means that the message id was successfully retrieved.
            - `None` means that there was an error while trying to get the message id.

        """
        return self.data.get('messageId')
    
    @property
    @return_none
    def mediaType(self) -> Union[int, None]:
        """
        `Media Type` - is the media type of the message that was replied to.
        #TODO: Add media types
        """
        return self.data.get('mediaType')
    
    @property
    @return_none
    def content(self) -> Union[str, None]:
        """
        `Content` - is the content of the message that was replied to.

        THIS IS NOT THE BOT'S MESSAGE CONTENT.
            - `str` means that the message content was successfully retrieved.
            - `None` means that there was an error while trying to get the message content.

        """
        return self.data.get('content')
    
    @property
    @return_none
    def clientRefId(self) -> Union[int, None]:
        """
        `Client Ref ID` - is the client reference id of the message that was replied to.

        THIS IS NOT THE BOT'S CLIENT REFERENCE ID.
            - `int` means that the client reference id was successfully retrieved.
            - `None` means that there was an error while trying to get the client reference id.

        """
        return self.data.get('clientRefId')
    
    @property
    @return_none
    def threadId(self) -> Union[str, None]:
        """
        `Thread ID` - is the thread / chat id that the message that was replied to was sent in.

            - `str` means that the thread id was successfully retrieved.
            - `None` means that there was an error while trying to get the thread id.

        """
        return self.data.get('threadId')
    
    @property
    @return_none
    def chatId(self) -> Union[str, None]:
        """
        `Chat ID` - is the thread / chat id that the message that was replied to was sent in.

            - `str` means that the thread id was successfully retrieved.
            - `None` means that there was an error while trying to get the thread id.

        """
        return self.threadId
    
    @property
    @return_none
    def createdTime(self) -> Union[str, None]:
        """
        `Created Time` - is the time that the message that was replied to was sent.

            - `str` means that the time was successfully retrieved.
            - `None` means that there was an error while trying to get the time.

        """
        return self.data.get('createdTime')
    
    @property
    @return_none
    def type(self) -> Union[str, None]:
        """
        `Type` - is the type of the message that was replied to.

            - `str` means that the type was successfully retrieved.
            - `None` means that there was an error while trying to get the type.

        """
        return self.data.get('type')
    
    @property
    @return_none
    def mediaValue(self) -> Union[str, None]:
        """
        `Media Value` - is the media value of the message that was replied to.

            - `str` means that the media value was successfully retrieved.
            - `None` means that there was an error while trying to get the media value.

        """
        return self.data.get('mediaValue')
    
    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data

class CMessageExtensions:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data

    @property
    def messageId(self) -> Union[str, None]:
        """
        `Message ID` - is the message id of the message that was replied to.
        
        THIS IS NOT THE BOT'S MESSAGE ID.
            - `str` means that the message id was successfully retrieved.
            - `None` means that there was an error while trying to get the message id.
            
        """
        return self.data.get('replyMessageId')
        
    @property
    def message(self) -> ReplyMessage:
        """
        `Message` - is the message that was replied to.
        
        THIS IS NOT THE BOT'S MESSAGE.
            - `ReplyMessage` means that the message was successfully retrieved.
            - `None` means that there was an error while trying to get the message.
        
        """
        return ReplyMessage(self.data.get('replyMessage'))
    
    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data

class CMessageAuthorList:
    def __init__(self, data: list) -> None:
        self.data = data

    def return_none(func):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else func(*args, **kwargs)
        return wrapper
    
    @property
    @return_none
    def status(self) -> Union[str, None]:
        """
        `status` - Returns a list of the status of the users in the chat.
            - `str` means that the status was successfully retrieved.
            - `None` means that there was an error while trying to get the status.

        """
        return [i.get('status') for i in self.data]
    
    @property
    @return_none
    def icon(self) -> Union[str, None]:
        """
        `icon` - Returns a list of the icon of the users in the chat.
            - `str` means that the icon was successfully retrieved.
            - `None` means that there was an error while trying to get the icon.

        """
        return [i.get('icon') for i in self.data]
    
    @property
    @return_none
    def avatar(self) -> Union[str, None]:
        """
        `avatar` - Returns a list of the avatar of the users in the chat.
            - `str` means that the avatar was successfully retrieved.
            - `None` means that there was an error while trying to get the avatar.

        """
        return self.icon
    
    @property
    @return_none
    def reputation(self) -> Union[str, None]:
        """
        `reputation` - Returns a list of the reputation of the users in the chat.
            - `str` means that the reputation was successfully retrieved.
            - `None` means that there was an error while trying to get the reputation.

        """
        return [i.get('reputation') for i in self.data]
    
    @property
    @return_none
    def role(self) -> Union[str, None]:
        """
        `role` - Returns a list of the role of the users in the chat.
            - `str` means that the role was successfully retrieved.
            - `None` means that there was an error while trying to get the role.

        """
        return [i.get('role') for i in self.data]
    
    @property
    @return_none
    def nickname(self) -> Union[str, None]:
        """
        `nickname` - Returns a list of the nickname of the users in the chat.
            - `str` means that the nickname was successfully retrieved.
            - `None` means that there was an error while trying to get the nickname.

        """
        return [i.get('nickname') for i in self.data]
    
    @property
    @return_none
    def username(self) -> Union[str, None]:
        """
        `username` - Returns a list of the username of the users in the chat.
            - `str` means that the username was successfully retrieved.
            - `None` means that there was an error while trying to get the username.

        """
        return self.nickname
    
    @property
    @return_none
    def level(self) -> Union[str, None]:
        """
        `level` - Returns a list of the level of the users in the chat.
            - `str` means that the level was successfully retrieved.
            - `None` means that there was an error while trying to get the level.

        """
        return [i.get('level') for i in self.data]
    
    @property
    @return_none
    def accountMembershipStatus(self) -> Union[str, None]:
        """
        `accountMembershipStatus` - Returns a list of the account membership status of the users in the chat.
            - `str` means that the account membership status was successfully retrieved.
            - `None` means that there was an error while trying to get the account membership status.

        """
        return [i.get('accountMembershipStatus') for i in self.data]
    
    @property
    @return_none
    def avatarFrame(self) -> Union[str, None]:
        """
        `avatarFrame` - Returns a list of the avatar frame of the users in the chat.
            - `str` means that the avatar frame was successfully retrieved.
            - `None` means that there was an error while trying to get the avatar frame.

        """
        return [i.get('avatarFrame') for i in self.data]

    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data

class CMessages:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data.get('result') or data.get('messageList', data)

    def return_none(func):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else func(*args, **kwargs)
        return wrapper
    
    @property
    @return_none
    def includedInSummary(self) -> Union[bool, None]:
        """
        `includedInSummary` - Returns a list of the included in summary of the messages in the chat.
            - `bool` means that the included in summary was successfully retrieved.
            - `None` means that there was an error while trying to get the included in summary.

        """
        return [i.get('includedInSummary') for i in self.data]
    
    @property
    @return_none
    def uid(self) -> Union[str, None]:
        """
        `uid` - Returns a list of the uid of the messages in the chat.
            - `str` means that the uid was successfully retrieved.
            - `None` means that there was an error while trying to get the uid.

        """
        return [i.get('uid') for i in self.data]
    
    @property
    @return_none
    def userId(self) -> Union[str, None]:
        """
        `userId` - Returns a list of the user id of the messages in the chat.
            - `str` means that the user id was successfully retrieved.
            - `None` means that there was an error while trying to get the user id.

        """
        return self.uid
    
    @property
    @return_none
    def author(self) -> Union[CMessageAuthorList, None]:
        """
        `author` - Returns a list of the author of the messages in the chat.
            - `CMessageAuthorList` means that the author was successfully retrieved.
            - `None` means that there was an error while trying to get the author.

        """
        return CMessageAuthorList([i.get('author') for i in self.data])
    
    @property
    @return_none
    def isHidden(self) -> Union[bool, None]:
        """
        `isHidden` - Returns a list of the is hidden of the messages in the chat.
            - `bool` means that the is hidden was successfully retrieved.
            - `None` means that there was an error while trying to get the is hidden.

        """
        return [i.get('isHidden') for i in self.data]
    
    @property
    @return_none
    def messageId(self) -> Union[str, None]:
        """
        `messageId` - Returns a list of the message id of the messages in the chat.
            - `str` means that the message id was successfully retrieved.
            - `None` means that there was an error while trying to get the message id.

        """
        return [i.get('messageId') for i in self.data]
    
    @property
    @return_none
    def mediaType(self) -> Union[str, None]:
        """
        `mediaType` - Returns a list of the media type of the messages in the chat.
            - `str` means that the media type was successfully retrieved.
            - `None` means that there was an error while trying to get the media type.

        """
        return [i.get('mediaType') for i in self.data]
    
    @property
    @return_none
    def content(self) -> Union[str, None]:
        """
        `content` - Returns a list of the content of the messages in the chat.
            - `str` means that the content was successfully retrieved.
            - `None` means that there was an error while trying to get the content.

        """
        return [i.get('content') for i in self.data]
    
    @property
    @return_none
    def clientRefId(self) -> Union[str, None]:
        """
        `clientRefId` - Returns a list of the client ref id of the messages in the chat.
            - `str` means that the client ref id was successfully retrieved.
            - `None` means that there was an error while trying to get the client ref id.

        """
        return [i.get('clientRefId') for i in self.data]
    
    @property
    @return_none
    def threadId(self) -> Union[str, None]:
        """
        `threadId` - Returns a list of the thread id of the messages in the chat.
            - `str` means that the thread id was successfully retrieved.
            - `None` means that there was an error while trying to get the thread id.

        """
        return [i.get('threadId') for i in self.data]
    
    @property
    @return_none
    def chatId(self) -> Union[str, None]:
        """
        `chatId` - Returns a list of the chat id of the messages in the chat.
            - `str` means that the chat id was successfully retrieved.
            - `None` means that there was an error while trying to get the chat id.

        """
        return self.threadId
    
    @property
    @return_none
    def createdTime(self) -> Union[int, None]:
        """
        `createdTime` - Returns a list of the created time of the messages in the chat.
            - `int` means that the created time was successfully retrieved.
            - `None` means that there was an error while trying to get the created time.

        """
        return [i.get('createdTime') for i in self.data]
    
    @property
    @return_none
    def extensions(self) -> Union[dict, None]:
        """
        `extensions` - Returns a list of the extensions of the messages in the chat.
            - `dict` means that the extensions was successfully retrieved.
            - `None` means that there was an error while trying to get the extensions.

        """
        return [i.get('extensions') for i in self.data]
    
    @property
    @return_none
    def type(self) -> Union[str, None]:
        """
        `type` - Returns a list of the type of the messages in the chat.
            - `str` means that the type was successfully retrieved.
            - `None` means that there was an error while trying to get the type.

        """
        return [i.get('type') for i in self.data]
    
    @property
    @return_none
    def mediaValue(self) -> Union[str, None]:
        """
        `mediaValue` - Returns a list of the media value of the messages in the chat.
            - `str` means that the media value was successfully retrieved.
            - `None` means that there was an error while trying to get the media value.

        """
        return [i.get('mediaValue') for i in self.data]
        
    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data

class Message:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data: dict = data.get("o", data)

    @property
    def ndcId(self) -> Union[int, None]:
        """
        `ndcId` - is the community id that the message was sent in.
        
            - `int` means that the ndcId was successfully retrieved.
            - `None` means that there was an error while trying to get the ndcId.
        
        """
        return self.data.get('ndcId')
    
    @property
    def comId(self) -> Union[int, None]:
        """
        `comId` - is the community id that the message was sent in.
        
            - `int` means that the comId was successfully retrieved.
            - `None` means that there was an error while trying to get the comId.
            
        """
        return self.ndcId
    
    @property
    def chatMessage(self) -> Union[dict, None]:
        """
        `chatMessage` - is the message that was sent.

            Contains all the information about the message.
            - `dict` means that the chatMessage was successfully retrieved.
            - `None` means that there was an error while trying to get the chatMessage.

        """
        return self.data.get('chatMessage')
    
    @property
    def author(self) -> Union[MessageAuthor, None]:
        """
        `author` - is the author of the message.
        
            - `MessageAuthor` means that the author was successfully retrieved.
            - `None` means that there was an error while trying to get the author.
            
        """
        return MessageAuthor(self.chatMessage.get('author')) if self.chatMessage else None
    
    @property
    def mediaValue(self) -> Union[str, None]:
        """
        `mediaValue` - is the media value of the message.
        
            - `str` means that the mediaValue was successfully retrieved.
            - `None` means that there was an error while trying to get the mediaValue.
            
        """
        return self.chatMessage.get('mediaValue')
    
    @property
    def threadId(self) -> Union[str, None]:
        """
        `threadId` - is the thread id the message was sent in.
        
            - `str` means that the threadId was successfully retrieved.
            - `None` means that there was an error while trying to get the threadId.
            
        """
        return self.chatMessage.get('threadId')
    
    @property
    def chatId(self) -> Union[str, None]:
        """
        `chatId` - is the thread id the message was sent in.
        
            - `str` means that the chatId was successfully retrieved.
            - `None` means that there was an error while trying to get the chatId.
        
        """
        return self.threadId
    
    @property
    def mediaType(self) -> Union[int, None]:
        """
        `mediaType` - is the media type of the message.
        
            - `int` means that the mediaType was successfully retrieved.
            - `None` means that there was an error while trying to get the mediaType.
            
        """
        return self.chatMessage.get('mediaType')
    
    @property
    def content(self) -> Union[str, None]:
        """
        `content` - is the content of the message.
        
            - `str` means that the content was successfully retrieved.
            - `None` means that there was an error while trying to get the content.
        
        """
        return self.chatMessage.get('content')
    
    @property
    def clientRefId(self) -> Union[int, None]:
        """
        `clientRefId` - is the client reference id of the message.
        
            - `int` means that the clientRefId was successfully retrieved.
            - `None` means that there was an error while trying to get the clientRefId.
        
        """
        return self.chatMessage.get('clientRefId')
    
    @property
    def messageId(self) -> Union[str, None]:
        """
        `messageId` - is the message id of the message.
        
            - `str` means that the messageId was successfully retrieved.
            - `None` means that there was an error while trying to get the messageId.
            
        """
        return self.chatMessage.get('messageId')
    
    @property
    def uid(self) -> Union[str, None]:
        """
        `uid` - is the user id of the user who sent the message.
        
            - `str` means that the uid was successfully retrieved.
            - `None` means that there was an error while trying to get the uid.
            
        """
        return self.chatMessage.get('uid')
    
    @property
    def userId(self) -> Union[str, None]:
        """
        `userId` - is the user id of the user who sent the message.
        
            - `str` means that the userId was successfully retrieved.
            - `None` means that there was an error while trying to get the userId.
        
        """
        return self.uid
    
    @property
    def createdTime(self) -> Union[str, None]:
        """
        `createdTime` - is the time the message was sent.
        
            - `str` means that the createdTime was successfully retrieved.
            - `None` means that there was an error while trying to get the createdTime.
        
        """
        return self.chatMessage.get('createdTime')
    
    @property
    def type(self) -> Union[int, None]:
        """
        `type` - is the type of the message.
        
            - `int` means that the type was successfully retrieved.
            - `None` means that there was an error while trying to get the type.
        
        """
        return self.chatMessage.get('type')
    
    @property
    def isHidden(self) -> Union[bool, None]:
        """
        `isHidden` - is whether the message is hidden or not.

            - `bool` means that the isHidden was successfully retrieved.
            - `None` means that there was an error while trying to get the isHidden.

        """
        return self.chatMessage.get('isHidden')
    
    @property
    def includedInSummary(self) -> Union[bool, None]:
        """
        `includedInSummary` - is whether the message is included in the summary or not.
        
            - `bool` means that the includedInSummary was successfully retrieved.
            - `None` means that there was an error while trying to get the includedInSummary.
            
        """
        return self.chatMessage.get('includedInSummary')
    
    @property
    def chatBubbleId(self) -> Union[str, None]:
        """
        `chatBubbleId` - is the chat bubble id of the message.
        
            - `str` means that the chatBubbleId was successfully retrieved.
            - `None` means that there was an error while trying to get the chatBubbleId.
            
        """
        return self.chatMessage.get('chatBubbleId')
    
    @property
    def chatBubbleVersion(self) -> Union[int, None]:
        """
        `chatBubbleVersion` - is the chat bubble version of the message.
        
            - `int` means that the chatBubbleVersion was successfully retrieved.
            - `None` means that there was an error while trying to get the chatBubbleVersion.
            
        """
        return self.chatMessage.get('chatBubbleVersion')

    @property
    def replied(self) -> CMessageExtensions:
        """
        `replied` - Returns the replied message if there was one.
        
            - `CMessageExtensions` means there was a reply.
            - `None` means there was no reply.
            
        """
        return CMessageExtensions(self.chatMessage.get('extensions')) if self.chatMessage.get('extensions') != {} else None
    
    @property
    def extensions(self) -> Union[dict, None]:
        """
        `extensions` - Returns the extensions of the message.
        
            - `dict` means that the extensions was successfully retrieved.
            - `None` means that there was an error while trying to get the extensions.
            
        """
        return self.chatMessage.get('extensions')
    
    @property
    def mentioned_user_ids(self) -> Union[list, None]:
        """
        `mentioned_user_ids` - Returns a list of the mentioned user ids.
        
            - `list` means there were mentioned user ids.
            - `None` means there were no mentioned user ids.
            
        """
        return [
            i.get('uid', None) for i in self.extensions.get('mentionedArray')
            ] if self.extensions.get('mentionedArray') is not None else None
    
    @property
    def mentioned_user_names(self) -> Union[list, None]:
        """
        `mentioned_user_names` - Returns a list of the mentioned user names.
        
            - `list` means there were mentioned user names.
            - `None` means there were no mentioned user names.
            
        """
        return findall(r'@([^\u202c\u202d]+)', self.content) if self.content is not None else None
    
    @property
    def mentioned_dictionary(self) -> Union[dict, None]:
        """
        `mentioned_dictionary` - Returns a dictionary of the mentioned {userid: username}.

            - `dict` means there was a mentioned dictionary.
            - `None` means there was no mentioned dictionary.
        
        """
        return dict(zip(
            self.mentioned_user_ids, self.mentioned_user_names
            )) if self.mentioned_user_ids is not None and self.mentioned_user_names is not None else None

    @property
    def alertOption(self) -> Union[int, None]:
        """
        `alertOption` - is the alert option of the message.
        
            - `int` means that the alertOption was successfully retrieved.
            - `None` means that there was an error while trying to get the alertOption.
            
        """
        return self.chatMessage.get('alertOption')
    
    @property
    def membershipStatus(self) -> Union[int, None]:
        """
        `membershipStatus` - is the membership status of the message.
        
            - `int` means that the membershipStatus was successfully retrieved.
            - `None` means that there was an error while trying to get the membershipStatus.
            
        """
        return self.chatMessage.get('membershipStatus')
        
    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data

class Channel:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data = data.get("o", data)

    def return_none(func):
        def wrapper(*args, **kwargs):
            return None if args[0].data is None else func(*args, **kwargs)
        return wrapper
    
    @property
    @return_none
    def id(self) -> Union[str, None]:
        """
        `id` - is the id of the channel.

            - `str` means that the id was successfully retrieved.
            - `None` means that there was an error while trying to get the id.

        """
        return self.data.get('id')
    
    @property
    @return_none
    def channelName(self) -> Union[str, None]:
        """
        `channelName` - is the channel name of the channel.

            - `str` means that the channelName was successfully retrieved.
            - `None` means that there was an error while trying to get the channelName.

        """
        return self.data.get('channelName')
    
    @property
    @return_none
    def channelKey(self) -> Union[str, None]:
        """
        `channelKey` - is the channel key of the channel.

            - `str` means that the channelKey was successfully retrieved.
            - `None` means that there was an error while trying to get the channelKey.

        """
        return self.data.get('channelKey')
    
    @property
    @return_none
    def channelUid(self) -> Union[int, None]:
        """
        `channelUid` - is the channel uid of the channel.

            - `int` means that the channelUid was successfully retrieved.
            - `None` means that there was an error while trying to get the channelUid.

        """
        return self.data.get('channelUid')
    
    @property
    @return_none
    def expiredTime(self) -> Union[int, None]:
        """
        `expiredTime` - is the expired time of the channel.

            - `int` means that the expiredTime was successfully retrieved.
            - `None` means that there was an error while trying to get the expiredTime.

        """
        return self.data.get('expiredTime')
    
    @property
    @return_none
    def ndcId(self) -> Union[int, None]:
        """
        `ndcId` - is the community id that the channel is in.

            - `int` means that the ndcId was successfully retrieved.
            - `None` means that there was an error while trying to get the ndcId.

        """
        return self.data.get('ndcId')
    
    @property
    @return_none
    def comId(self) -> Union[int, None]:
        """
        `comId` - is the community id that the channel is in.

            - `int` means that the comId was successfully retrieved.
            - `None` means that there was an error while trying to get the comId.

        """
        return self.ndcId
    
    @property
    @return_none
    def threadId(self) -> Union[str, None]:
        """
        `threadId` - is the thread id of the channel.

            - `str` means that the threadId was successfully retrieved.
            - `None` means that there was an error while trying to get the threadId.

        """
        return self.data.get('threadId')
    
    @property
    @return_none
    def chatId(self) -> Union[str, None]:
        """
        `chatId` - is the chat id of the channel.

            - `str` means that the chatId was successfully retrieved.
            - `None` means that there was an error while trying to get the chatId.

        """
        return self.threadId
    
    def json(self) -> Union[dict, str]:
        """`JSON` - returns the raw data."""
        return self.data



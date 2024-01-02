from .entities import *
from .utilities.generate import *
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])

class Global:
    def __init__(self) -> None:
        pass


    def authenticated(func: F) -> F:
        """
        A decorator that checks if the client is authenticated.
        
        :param func: The function to decorate.
        :type func: F
        :return: The decorated function.
        :rtype: F
        
        This decorator is used to check if the client is authenticated.
        If the client is not authenticated, a `LoginRequired` exception
        will be raised.
        """
        def wrapper(*args, **kwargs) -> Any:
            try:
                if not args[0].is_authenticated:
                    raise LoginRequired
                return func(*args, **kwargs)
            except AttributeError:
                raise LoginRequired
        return wrapper


    def make_request(self, method: str, url: str, data: dict = None, is_login_required: bool = True) -> dict:
        """
        Makes a request to the API.
        
        :param method: The HTTP method to use.
        :type method: str
        :param url: The URL to make the request to.
        :type url: str
        :param data: The data to send with the request.
        :type data: dict
        :return: The response from the request.
        :rtype: dict
        :param is_login_required: Whether the request requires the client to be logged in.
        :type is_login_required: bool
        
        This method is used to make requests to the API.
        
        Example usage:
        
        >>> client.make_request(
            ...     method = "GET",
            ...     url = "/g/s/user-profile/0000-000000-000000-0000-000000"
            ...     is_login_required = True
            ... )
            
        This will make a GET request to the URL `/g/s/user-profile/0000-000000-000000-0000-000000`.
        """
        return self.request.handler(
            method = method,
            url = url,
            data = data,
            is_login_required = is_login_required
        )


    def fetch_user(self, userId: str) -> UserProfile:
        """
        Fetches a user's profile.
        
        :param userId: The ID of the user to fetch.
        :type userId: str
        :return: The user's profile.
        :rtype: UserProfile
        
        This method is used to fetch a user's profile.
        
        Example usage:
        
        >>> x = client.fetch_user("0000-000000-000000-0000-000000")
        >>> print(x.nickname)
        "Example"
        >>> print(x.content)
        "This is an example profile."
        >>> print(x.icon)
        """
        return UserProfile(self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}"
        ))
    

    def edit_profile(
        self,
        nickname: str = None,
        content: str = None,
        icon: str = None,
        backgroundColor: str = None,
        backgroundImage: str = None,
        defaultBubbleId: str = None
        ) -> UserProfile:
        """
        Edits the user's profile.

        :param nickname: The new nickname for the user.
        :type nickname: str
        :param content: The new content for the user's profile.
        :type content: str
        :param icon: The new icon image file for the user.
        :type icon: str
        :param backgroundColor: The new background color for the user's profile.
        :type backgroundColor: str
        :param backgroundImage: The new background image file for the user's profile.
        :type backgroundImage: str
        :param defaultBubbleId: The ID of the default bubble for the user's profile.
        :type defaultBubbleId: str
        :return: The response from the account's `edit_profile` method.
        :rtype: Response

        This method allows the authenticated user to edit their profile settings. Different aspects of the profile can be modified,
        such as the nickname, content, icon, background color, background image, and default bubble. Only the specified parameters will
        be updated. The `userId` parameter is set to the authenticated user's ID automatically.

        **Example usage:**

        To change the nickname and icon for the user:

        >>> response = client.edit_profile(nickname="New Nickname", icon="path/to/icon.jpg")
        ... if response.status == 200:
        ...     print("Profile edited successfully!")
        ... else:
        ...     print("Failed to edit profile.")
        """
        data = {
                "address": None,
                "latitude": 0,
                "longitude": 0,
                "mediaList": None,
                "eventSource": "UserProfileView",
                "timestamp": int(time() * 1000),
        }

        if nickname: data['nickname'] = nickname
        if icon: data['icon'] = self.upload_image(icon)
        if content: data['content'] = content
        if backgroundColor:
            data["extensions"] = {
                "style": {
                    "backgroundColor": backgroundColor
                    if backgroundColor.startswith("#")
                    else f"#{backgroundColor}"
                }
            }

        if backgroundImage:
            data["extensions"] = {
                "style": {
                    "backgroundMediaList": [
                        [100, self.upload_image(backgroundImage), None, None, None]
                    ]
                }
            }
        if defaultBubbleId:
            data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        return UserProfile(self.make_request(
            method = "POST",
            url = f"/g/s/user-profile/{self.userId}",
            data = data
        ))


    @authenticated
    def send_message(self, content: str, chatId: str, **kwargs) -> CMessage:
        """
        Sends a message to a chat thread.

        :param content: The content of the message.
        :type content: str
        :param chatId: The ID of the chat thread to send the message to.
        :type chatId: str
        :param **kwargs: Additional parameters for the message.
        :return: A `CMessage` object containing the details of the sent message.
        :rtype: CMessage

        This method sends a message to a chat thread. The content and chat ID parameters are required. Additional parameters
        can be passed as keyword arguments. The method calls the `PrepareMessage` object's `json` method to prepare the message
        data. The result is a `CMessage` object containing the details of the sent message.
        """
        return CMessage(self.make_request(
            method="POST",
            url=f"/g/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content, **kwargs).json()
            ))


    @authenticated
    def edit_profile(
        self,
        nickname: str = None,
        content: str = None,
        icon: str = None,
        backgroundColor: str = None,
        backgroundImage: str = None,
        defaultBubbleId: str = None
        ) -> UserProfile:
        """
        Edits the user's profile.

        :param nickname: The new nickname for the user.
        :type nickname: str
        :param content: The new content for the user's profile.
        :type content: str
        :param icon: The new icon image file for the user.
        :type icon: str
        :param backgroundColor: The new background color for the user's profile.
        :type backgroundColor: str
        :param backgroundImage: The new background image file for the user's profile.
        :type backgroundImage: str
        :param defaultBubbleId: The ID of the default bubble for the user's profile.
        :type defaultBubbleId: str
        :return: The response from the account's `edit_profile` method.
        :rtype: Response

        This method allows the authenticated user to edit their profile settings. Different aspects of the profile can be modified,
        such as the nickname, content, icon, background color, background image, and default bubble. Only the specified parameters will
        be updated. The `userId` parameter is set to the authenticated user's ID automatically.

        **Example usage:**

        To change the nickname and icon for the user:

        >>> response = client.edit_profile(nickname="New Nickname", icon="path/to/icon.jpg")
        ... if response.status == 200:
        ...     print("Profile edited successfully!")
        ... else:
        ...     print("Failed to edit profile.")
        """
        data = {
                "address": None,
                "latitude": 0,
                "longitude": 0,
                "mediaList": None,
                "eventSource": "UserProfileView",
                "timestamp": int(time() * 1000),
        }

        if nickname: data['nickname'] = nickname
        if icon: data['icon'] = self.upload_image(icon)
        if content: data['content'] = content
        if backgroundColor:
            data["extensions"] = {
                "style": {
                    "backgroundColor": backgroundColor
                    if backgroundColor.startswith("#")
                    else f"#{backgroundColor}"
                }
            }

        if backgroundImage:
            data["extensions"] = {
                "style": {
                    "backgroundMediaList": [
                        [100, self.upload_image(backgroundImage), None, None, None]
                    ]
                }
            }
        if defaultBubbleId:
            data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        return UserProfile(self.make_request(
            method = "POST", url = f"/g/s/user-profile/{self.userId}",
            data = data
        ))


    @authenticated
    def start_chat(
        self,
        userId: Union[str, list],
        message: str,
        title: str = None,
        content: str = None,
        isGlobal: bool = False,
        publishToGlobal: bool = False
        ) -> ChatThread:
        """
        Starts a chat thread.
        :param userId: The ID or list of IDs of the users to invite to the chat.
        :type userId: Union[str, list]
        :param message: The initial message content.
        :type message: str
        :param title: The title of the chat thread (optional).
        :type title: str, optional
        :param content: Additional content for the message (optional).
        :type content: str, optional
        :param isGlobal: Indicates if the chat is global (optional, default: False).
        :type isGlobal: bool, optional
        :param publishToGlobal: Indicates if the chat should be published globally (optional, default: False).
        :type publishToGlobal: bool, optional
        :return: A `ChatThread` object representing the created chat thread.
        :rtype: ChatThread
        """
        try:
            userIds = [userId] if isinstance(userId, str) else userId
        except Exception as e:
            raise ValueError("Incorrect type for userId. <--- userId can be only a string or a list.") from e

        data = dict(
            title = title,
            inviteeUids = userIds,
            initialMessageContent = message,
            content = content,
            timestamp = int(time() * 1000),
            publishToGlobal = 0
        )

        if isGlobal: data.update({"type": 2, "eventSource": "GlobalComposeMenu"})
        else: data["type"] = 0

        if publishToGlobal: data["publishToGlobal"] = 1

        return ChatThread(
            self.make_request(method="POST", url="/g/s/chat/thread", data=data)
        )


    @authenticated
    def blocker_users(self, start: int = 0, size: int = 25) -> List[str]:
        """
        Retrieves a list of users what are blocking the logged account.
        :param start: The index to start retrieving the list from (optional, default: 0).
        :type start: int, optional
        :param size: The number of users to retrieve (optional, default: 25).
        :type size: int, optional
        :return: A list of user IDs representing the blocker users.
        :rtype: list
        """
        return self.make_request(
            method = "GET",
            url = f"/g/s/block/full-list?start={start}&size={size}"
        )["blockerUidList"]


    def fetch_wall_comments(self, userId: str, sorting: str = "newest", start: int = 0, size: int = 25) -> CommentList:
        """
        Fetches wall comments for a user.

        :param userId: The ID of the user whose wall comments will be fetched.
        :type userId: str
        :param sorting: The sorting method for the comments. Options: "newest" (default), "oldest", "top".
        :type sorting: str, optional
        :param start: The starting index of the comments to fetch (pagination). Default is 0.
        :type start: int, optional
        :param size: The number of comments to fetch (pagination). Default is 25.
        :type size: int, optional
        :return: The list of wall comments for the specified user.
        :rtype: CommentList
        :raises ValueError: If an incorrect sorting method is provided.

        This method retrieves wall comments for a specific user. The comments can be sorted by "newest" (default), "oldest", or "top".
        The `start` parameter specifies the index of the first comment to fetch, while the `size` parameter determines the number of
        comments to retrieve. The comments are returned as a `CommentList` object.

        **Example usage:**

        To fetch the newest 25 wall comments for a user:

        >>> comments = client.fetch_wall_comments(userId="00000000-0000-0000-0000-000000000000")
        >>> for comment in comments:
        ...     print(comment.content)
        """
        if sorting.lower() == "newest": sorting = "newest"
        elif sorting.lower() == "oldest": sorting = "oldest"
        elif sorting.lower() == "top": sorting = "vote"
        else: raise ValueError("Incorrect sorting method.")

        return CommentList(self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}"
        ))


    @authenticated
    def delete_message(self, chatId: str, messageId: str) -> ApiResponse:
        """
        Deletes a message in a chat thread.

        :param chatId: The ID of the chat thread where the message is located.
        :type chatId: str
        :param messageId: The ID of the message to delete.
        :type messageId: str
        :return: The API response indicating the success or failure of the deletion.
        :rtype: ApiResponse

        This method allows the authenticated user to delete a specific message in a chat thread. The `chatId` parameter identifies the
        chat thread, while the `messageId` parameter specifies the ID of the message to be deleted.

        **Note:** Only authorized users can delete messages in a chat thread. If the deletion is successful, the API response will indicate
        a successful deletion. Otherwise, an error message will be returned.

        **Example usage:**

        To delete a message with the ID "00000000-0000-0000-0000-000000000000" in a chat thread with the ID "00000000-0000-0000-0000-000000000000":

        >>> response = client.delete_message(chatId="00000000-0000-0000-0000-000000000000", messageId="00000000-0000-0000-0000-000000000000")
        >>> if response.success:
        ...     print("Message deleted successfully!")
        ... else:
        ...     print("Failed to delete message.")
        """
        return ApiResponse(self.make_request(
            method = "DELETE",
            url = f"/g/s/chat/thread/{chatId}/message/{messageId}"
        ))


    @authenticated
    def edit_chat(
        self,
        chatId: str,
        doNotDisturb: bool = None,
        pinChat: bool = None,
        title: str = None,
        icon: str = None,
        backgroundImage: str = None,
        content: str = None,
        announcement: str = None,
        coHosts: list = None,
        keywords: list = None,
        pinAnnouncement: bool = None,
        publishToGlobal: bool = None,
        canTip: bool = None,
        viewOnly: bool = None,
        canInvite: bool = None,
        fansOnly: bool = None
        ) -> list:
        """
        Edits the settings of a chat.

        :param chatId: The ID of the chat to be edited.
        :type chatId: str
        :param doNotDisturb: Set to True to enable "Do Not Disturb" mode for the chat, False to disable it. Default is None.
        :type doNotDisturb: bool, optional
        :param pinChat: Set to True to pin the chat, False to unpin it. Default is None.
        :type pinChat: bool, optional
        :param title: The new title for the chat.
        :type title: str, optional
        :param icon: The new icon image file for the chat.
        :type icon: str, optional
        :param backgroundImage: The new background image file for the chat.
        :type backgroundImage: str, optional
        :param content: The new content for the chat.
        :type content: str, optional
        :param announcement: The new announcement for the chat.
        :type announcement: str, optional
        :param coHosts: A list of user IDs to set as co-hosts for the chat.
        :type coHosts: list, optional
        :param keywords: A list of keywords to associate with the chat.
        :type keywords: list, optional
        :param pinAnnouncement: Set to True to pin the announcement, False to unpin it. Default is None.
        :type pinAnnouncement: bool, optional
        :param publishToGlobal: Set to True to publish the chat to the global feed, False to unpublish it. Default is None.
        :type publishToGlobal: bool, optional
        :param canTip: Set to True to enable tipping permissions for the chat, False to disable it. Default is None.
        :type canTip: bool, optional
        :param viewOnly: Set to True to enable view-only mode for the chat, False to disable it. Default is None.
        :type viewOnly: bool, optional
        :param canInvite: Set to True to allow members to invite others to the chat, False to disable it. Default is None.
        :type canInvite: bool, optional
        :param fansOnly: Set to True to enable "Fans Only" mode for the chat, False to disable it. Default is None.
        :type fansOnly: bool, optional
        :return: A list of HTTP status codes for each operation performed during the chat edit.
        :rtype: list

        This method allows the authenticated user to edit various settings of a chat, such as "Do Not Disturb" mode, pinning,
        title, icon, background image, content, announcement, co-hosts, keywords, pinning the announcement, publishing to the
        global feed, tipping permissions, view-only mode, allowing members to invite others, and "Fans Only" mode. Only the
        specified parameters will be updated.

        The function returns a list of HTTP status codes for each operation performed during the chat edit.

        **Example usage:**

        To edit the title and pin the chat:

        >>> response_codes = client.edit_chat(chatId="chat123", title="New Chat Title", pinChat=True)
        >>> if all(code == 200 for code in response_codes):
        ...     print("Chat edited successfully!")
        ... else:
        ...     print("Failed to edit chat.")
        """
        data = {"timestamp": int(time() * 1000)}

        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = self.upload_image(icon)
        if keywords: data["keywords"] = keywords
        if announcement: data["extensions"] = {"announcement": announcement}
        if pinAnnouncement: data["extensions"] = {"pinAnnouncement": pinAnnouncement}
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if publishToGlobal: data["publishToGlobal"] = 0
        if not publishToGlobal: data["publishToGlobal"] = 1

        responses = []

        if doNotDisturb is not None:
            responses.append(ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/member/{self.userId}/alert",
                data = {
                    "alertOption": 2 if doNotDisturb else 1,
                    "timestamp": int(time() * 1000)
                }
            )).status_code)
        
        if pinChat is not None:
            responses.append(ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/{'pin' if pinChat else 'unpin'}"
            )).status_code)
        
        if backgroundImage is not None:
            responses.append(ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/member/{self.userId}/background",
                data = {
                    "media": [100, self.upload_image(backgroundImage), None],
                    "timestamp": int(time() * 1000)
                }
            )).status_code)
        
        if coHosts is not None:
            responses.append(ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/co-host",
                data = {
                    "uidList": coHosts,
                    "timestamp": int(time() * 1000)
                }
            )).status_code)
        
        if viewOnly is not None:
            responses.append(ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/view-only/{'enable' if viewOnly else 'disable'}"
            )).status_code)
        
        if canInvite is not None:
            responses.append(ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/members-can-invite/{'enable' if canInvite else 'disable'}"
            )).status_code)
        
        if canTip is not None:
            responses.append(ApiResponse(
                method = "POST",
                url = f"/g/s/chat/thread/{chatId}/tipping-perm-status/{'enable' if canTip else 'disable'}"
            ).status_code)
        
        responses.append(ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/chat/thread/{chatId}",
            data = data
        )).status_code)

        return responses


    @authenticated
    def follow(self, userId: Union[str, list]) -> ApiResponse:
        """
        Follows a user or a list of users.

        :param userId: The ID of the user or a list of user IDs to follow.
        :type userId: Union[str, list]
        :return: The status code of the API response.
        :rtype: int

        This method allows the authenticated user to follow another user or a list of users. The `userId` parameter can be a single
        user ID (string) or a list of user IDs. If a single user ID is provided, the method will follow that user. If a list of user IDs
        is provided, the method will follow all the users in the list.

        If a single user ID is provided, the function will make a POST request to "/g/s/user-profile/{userId}/member" to follow the user.
        If a list of user IDs is provided, the function will make a POST request to "/g/s/user-profile/{self.userId}/joined" with the
        `targetUidList` parameter set to the list of user IDs and the `timestamp` parameter set to the current timestamp.

        The function returns the status code of the API response.

        **Example usage:**

        To follow a single user:

        >>> response_code = client.follow(userId="user123")
        >>> if response_code == 200:
        ...     print("User followed successfully!")
        ... else:
        ...     print("Failed to follow user.")

        To follow multiple users:

        >>> user_ids = ["user123", "user456", "user789"]
        >>> response_code = client.follow(userId=user_ids)
        >>> if response_code == 200:
        ...     print("Users followed successfully!")
        ... else:
        ...     print("Failed to follow users.")
        """
        if isinstance(userId, str):
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/user-profile/{userId}/member"
            ))
        if isinstance(userId, list):
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/user-profile/{self.userId}/joined",
                data = {
                    "targetUidList": userId,
                    "timestamp": int(time() * 1000)
                }
            ))


    @authenticated
    def fetch_chats(self, start: int = 0, size: int = 25) -> ChatThreadList:
        """
        Fetches the chat threads for the authenticated user.

        :param start: The starting index of the chat threads to fetch. (Default: 0)
        :type start: int, optional
        :param size: The number of chat threads to fetch. (Default: 25)
        :type size: int, optional
        :return: A `ChatThreadList` object containing the fetched chat threads.
        :rtype: ChatThreadList

        This function sends a GET request to the API to fetch the chat threads that the authenticated user has joined.

        `ChatThreadList` represents a list of chat threads.

        **Example usage:**

        >>> threads = client.fetch_chats(start=0, size=10)
        ... for thread in threads:
        ...     print(thread.title)
        """
        return ChatThreadList(self.make_request(
            method = "GET",
            url = f"/g/s/chat/thread?type=joined-me&start={start}&size={size}"
        ))


    @authenticated
    def fetch_chat(self, chatId: str) -> ChatThread:
        """
        Fetches a chat thread by its ID.

        :param chatId: The ID of the chat thread to fetch.
        :type chatId: str
        :return: A `ChatThread` object representing the fetched chat thread.
        :rtype: ChatThread

        This function sends a GET request to the API to fetch a chat thread based on its ID.

        `ChatThread` represents a thread of messages in a chat.

        **Example usage:**

        >>> chat = client.fetch_chat("123456789")
        ... print(chat.thread_id)
        ... print(chat.messages)
        """
        return ChatThread(self.make_request(
            method = "GET",
            url = f"/g/s/chat/thread/{chatId}"
        ))


    @authenticated
    def fetch_chat_users(self, chatId: str, start: int = 0, size: int = 25) -> CChatMembers:
        """
        Fetches the users in a chat.

        :param chatId: The ID of the chat.
        :type chatId: str
        :param start: The start index for fetching the users. (Default: 0)
        :type start: int, optional
        :param size: The number of users to fetch. (Default: 25)
        :type size: int, optional
        :return: A `CChatMembers` object containing the chat members.
        :rtype: CChatMembers

        This function retrieves the users who are members of the specified chat.

        `CChatMembers` represents the members of a chat.

        **Example usage:**

        >>> chat_members = client.fetch_chat_users("chat123")
        ... for member in chat_members.nickname:
        ...     print(member)
        """
        return CChatMembers(self.make_request(
            method = "GET",
            url = f"/g/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2"
        ))


    @authenticated
    def invite_to_chat(self, chatId: str, userId: Union[str, list]) -> ApiResponse:
        """
        Invites user(s) to a chat.

        :param chatId: The ID of the chat to invite users to.
        :type chatId: str
        :param userId: The ID(s) of the user(s) to invite. It can be a string or a list of strings.
        :type userId: Union[str, list]
        :return: An `ApiResponse` object representing the response of the invitation request.
        :rtype: ApiResponse
        :raises TypeError: If userId is neither a string nor a list of strings.

        This function sends a POST request to invite user(s) to a chat.

        The user(s) specified by userId will be invited to join the chat identified by chatId.

        `ApiResponse` represents the response of an API request.

        **Example usage:**

        >>> response = client.invite_to_chat("chat123", "user456")
        ... print(response.status_code)
        """
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list): userIds = userId
        else: raise TypeError("UserId must be a string or a list of strings.")

        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/chat/thread/{chatId}/member/invite",
            data = {
                "timestamp": int(time() * 1000),
                "uids": userIds
            }
        ))


    @authenticated
    def kick(self, chatId: str, userId: str, allowRejoin: bool = True) -> ApiResponse:
        """
        Kicks a user from a chat.

        :param chatId: The ID of the chat.
        :type chatId: str
        :param userId: The ID of the user to be kicked.
        :type userId: str
        :param allowRejoin: Whether to allow the user to rejoin the chat. (Default: True)
        :type allowRejoin: bool, optional
        :return: An `ApiResponse` object representing the API response.
        :rtype: ApiResponse

        This function sends a DELETE request to the API to kick the specified user from the chat.

        `ApiResponse` represents the response from the API.

        **Example usage:**

        >>> response = client.kick("chat123", "user456")
        ... print(response.status_code)
        ... print(response.json())
        """
        return ApiResponse(self.make_request(
            method = "DELETE",
            url = f"/g/s/chat/thread/{chatId}/member/{userId}?allowRejoin={allowRejoin}"
        ))


    @authenticated
    def fetch_messages(self, chatId: str, size: int = 25, pageToken: str = None) -> CMessages:
        """
        Fetches messages from a chat.

        :param chatId: The ID of the chat to fetch messages from.
        :type chatId: str
        :param size: The number of messages to fetch. (Default: 25)
        :type size: int, optional
        :param pageToken: The page token for pagination. (Optional)
        :type pageToken: str, optional
        :return: A `CMessages` object representing the fetched messages.
        :rtype: CMessages

        This function retrieves messages from the specified chat using the provided parameters.

        `CMessages` represents a collection of messages in the chat.

        **Example usage:**

        >>> messages = client.fetch_messages("chat123", size=50, pageToken="token123")
        ... for message in messages:
        ...     print(message.text)
        """
        if pageToken is not None:
            return CMessages(self.make_request(
                method = "GET",
                url = f"/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&pageToken={pageToken}&size={size}"
            ))
        return CMessages(self.make_request(
            method = "GET",
            url = f"/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"
        ))


    @authenticated
    def fetch_message(self, chatId: str, messageId: str) -> Message:
        """
        Fetches a specific message from a chat thread.

        :param chatId: The ID of the chat thread.
        :type chatId: str
        :param messageId: The ID of the message to fetch.
        :type messageId: str
        :return: A `Message` object representing the fetched message.
        :rtype: Message

        This function retrieves a specific message with the given `messageId` from the chat thread specified by `chatId`.

        `Message` represents a message in a chat thread.

        **Example usage:**

        >>> message = client.fetch_message("chat123", "message456")
        ... print(message.text)
        ... print(message.timestamp)
        """
        return Message(self.make_request(
            method = "GET",
            url = f"/g/s/chat/thread/{chatId}/message/{messageId}"
        ))


    @authenticated
    def search_community(self, aminoId: str) -> dict:
        """
        Search for a community by Amino ID or link.

        :param aminoId: The Amino ID or link of the community to search for.
        :type aminoId: str
        :return: A dictionary containing the search results.
        :rtype: dict

        This function sends a GET request to search for a community using the specified Amino ID or link.

        **Example usage:**

        >>> search_results = client.search_community("example_community").title
        ... print(search_results)
        """
        return self.make_request(
            method = "GET",
            url = f"/g/s/search/amino-id-and-link?q={aminoId}"
        )


    @authenticated
    def fetch_followers(self, userId: str, start: int = 0, size: int = 25) -> UserProfileList:
        """
        Fetches the followers of a user.

        :param userId: The ID of the user to fetch the followers for.
        :type userId: str
        :param start: The starting index of the followers list. (Default: 0)
        :type start: int, optional
        :param size: The number of followers to fetch. (Default: 25)
        :type size: int, optional
        :return: A `UserProfileList` object containing the fetched followers.
        :rtype: UserProfileList

        This function sends a GET request to the API to fetch the followers of a user.

        `UserProfileList` represents a list of user profiles.

        **Example usage:**

        >>> followers = client.fetch_followers("user123", start=0, size=10)
        ... for follower in followers.userId:
        ...     print(follower)
        """
        return UserProfileList(self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/member?start={start}&size={size}"
        ))


    def fetch_following(self, userId: str, start: int = 0, size: int = 25) -> UserProfileList:
        """
        Fetches the user profiles of the users that the specified user is following.

        :param userId: The ID of the user.
        :type userId: str
        :param start: The index to start fetching from. (Default: 0)
        :type start: int, optional
        :param size: The number of user profiles to fetch. (Default: 25)
        :type size: int, optional
        :return: A `UserProfileList` object containing the user profiles.
        :rtype: UserProfileList

        This function sends a GET request to the API to fetch the user profiles of the users that the specified user is following.

        `UserProfileList` represents a list of user profiles.

        **Example usage:**

        >>> following = client.fetch_following("user123")
        ... for profile in following.userId:
        ...     print(profile)
        """
        
        return UserProfileList(self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/joined?start={start}&size={size}"
        ))

    def large_fetch_following(self, userId: str, size: int = 25, pageToken: str = None, ignoreMembership: bool = True) -> FollowerList:
        """
        Fetches the user profiles of the users that the specified user is following.
        :param userId: The ID of the user.
        :type userId: str
        :param size: The number of user profiles to fetch. (Default: 25)
        :type size: int, optional
        :param pageToken: The page token to fetch from. (Default: None)
        :type pageToken: str, optional
        :param ignoreMembership: Whether to ignore membership. (Default: True)
        :type ignoreMembership: bool, optional
        :return: A `FollowerList` object containing the user profiles.
        :rtype: FollowerList
        
        This function sends a GET request to the API to fetch the user profiles of the users that the specified user is following.
        
        `FollowerList` represents a list of user profiles.
        
        **Example usage:**
    
        >>> following = client.large_fetch_following("user123")
        ... for userId in following.members.userId:
        ...     print(userId)
        """
        if pageToken:
            return FollowerList(self.make_request(
                method = "GET",
                url = f"/g/s/user-profile/{userId}/joined?size={size}&pageToken={pageToken}&pagingType=t&ignoreMembership={1 if ignoreMembership else 0}"
            ))

        return FollowerList(self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/joined?pagingType=t&size={size}&ignoreMembership={1 if ignoreMembership else 0}"
        ))

    def fetch_visitors(self, userId: str, start: int = 0, size: int = 25) -> UserProfileList:
        """
        Fetches the visitors of a user profile.

        :param userId: The ID of the user profile to fetch visitors for.
        :type userId: str
        :param start: The index of the first visitor to retrieve. (Default: 0)
        :type start: int, optional
        :param size: The maximum number of visitors to retrieve. (Default: 25)
        :type size: int, optional
        :return: A `UserProfileList` object containing the retrieved user profiles.
        :rtype: UserProfileList

        This function sends a GET request to the API to fetch the visitors of a user profile.

        `UserProfileList` represents a list of user profiles.

        **Example usage:**

        >>> visitors = client.fetch_visitors("123456", start=0, size=10)
        ... for visitor in visitors.userId:
        ...     print(visitor)
        """
        return UserProfileList(self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/visitors?start={start}&size={size}"
        ))


    @authenticated
    def blocked_users(self, start: int = 0, size: int = 25):
        """
        Retrieves a list of blocked users.

        :param start: The index of the first blocked user to retrieve. (Default: 0)
        :type start: int, optional
        :param size: The maximum number of blocked users to retrieve. (Default: 25)
        :type size: int, optional
        :return: A `UserProfileList` object containing the list of blocked users.
        :rtype: UserProfileList

        This function sends a GET request to the API to retrieve a list of blocked users.

        `UserProfileList` represents a list of user profiles.

        **Example usage:**

        >>> blocked_users = client.blocked_users(start=0, size=10)
        ... for user in blocked_users.userId:
        ...     print(user)
        """
        return UserProfileList(self.make_request(
            method = "GET",
            url = f"/g/s/block?start={start}&size={size}"
        ))


    @authenticated
    def mark_as_read(self, chatId: str, messageId: str) -> ApiResponse:
        """
        Marks a message as read.
        
        :param chatId: The ID of the chat to mark the message as read in.
        :type chatId: str
        :param messageId: The ID of the message to mark as read.
        :type messageId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to mark a message as read.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.mark_as_read("000000-0000-0000-000000", "000000-0000-0000-000000")
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/chat/thread/{chatId}/mark-as-read",
            data = {
                "messageId": messageId,
                "timestamp": int(time() * 1000)
            }
        ))


    @authenticated
    def visit(self, userId: str) -> ApiResponse:
        """
        Visits a user profile.
        
        :param userId: The ID of the user profile to visit.
        :type userId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to visit a user profile.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.visit("000000-0000-0000-000000")
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/user-profile/{userId}?action=visit"
        ))


    @authenticated
    def block(self, userId: str) -> ApiResponse:
        """
        Blocks a user.
        
        :param userId: The ID of the user to block.
        :type userId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to block a user.

        `ApiResponse` represents a response from the API.

        **Example usage:**

        >>> x = client.block("000000-0000-0000-000000")
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/block/{userId}"
        ))


    @authenticated
    def unblock(self, userId: str) -> ApiResponse:
        """
        Unblocks a user.
        
        :param userId: The ID of the user to unblock.
        :type userId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a DELETE request to the API to unblock a user.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.unblock("000000-0000-0000-000000")
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "DELETE",
            url = f"/g/s/block/{userId}"
        ))


    @authenticated
    def join_request(self, comId: str, message: str = None):
        """
        Sends a join request to a community.
        
        :param comId: The ID of the community to send the join request to.
        :type comId: str
        :param message: The message to send with the join request.
        :type message: str, optional
        
        This function sends a POST request to the API to send a join request to a community.

        `ApiResponse` represents a response from the API.

        **Example usage:**

        >>> x = client.join_request("000000-0000-0000-000000", "Hello! I would like to join this community.")
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/x{comId}/s/community/membership-request",
            data = {
                "message": message,
                "timestamp": int(time() * 1000)
            }
        ))


    @authenticated
    def flag_community(
        self,
        comId: str,
        reason: str,
        flagType: FlagTypes = FlagTypes.OFFTOPIC,
        isGuest: bool = False
        ) -> ApiResponse:
        """
        Flags a community.
        
        :param comId: The ID of the community to flag.
        :type comId: str
        :param reason: The reason for flagging the community.
        :type reason: str
        :param flagType: The type of flag to send.
        :type flagType: FlagTypes, optional
        :param isGuest: Whether or not the flag is from a guest account.
        :type isGuest: bool, optional
        
        This function sends a POST request to the API to flag a community.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.flag_community("000000-0000-0000-000000", "This community is offensive.", 1)
        ... print(x.status_code)
        """
        if reason is None: raise ValueError("Reason must be specified.")
        if flagType is None: raise ValueError("Flag type must be specified.")

        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/x{comId}/s/item-flag",
            data = {
                "flagType": flagType.value if isinstance(flagType, FlagTypes) else flagType,
                "reason": reason,
                "timestamp": int(time() * 1000),
                "isGuest": "g-flag" if isGuest else "flag"
            }
        ))


    def fetch_linked_communities(self, userId: str) -> list:
        """
        Fetches a user's linked communities.
        
        :param userId: The ID of the user to fetch the linked communities of.
        :type userId: str
        :return: A list of linked communities.
        :rtype: list
        
        This function sends a GET request to the API to fetch a user's linked communities.
        
        **Example usage:**
        
        >>> x = client.fetch_linked_communities("000000-0000-0000-000000")
        ... print(x)
        """
        return self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/linked-community"
        )["linkedCommunityList"]


    def fetch_unlinked_communities(self, userId: str) -> list:
        """
        Fetches a user's unlinked communities.
        
        :param userId: The ID of the user to fetch the unlinked communities of.
        :type userId: str
        :return: A list of unlinked communities.
        :rtype: list
        
        This function sends a GET request to the API to fetch a user's unlinked communities.
        
        **Example usage:**
        
        >>> x = client.fetch_unlinked_communities("000000-0000-0000-000000")
        ... print(x)
        """
        return self.make_request(
            method = "GET",
            url = f"/g/s/user-profile/{userId}/unlinked-community"
        )["unlinkedCommunityList"]


    @authenticated
    def reorder_linked_communities(self, comIds: List[int]) -> ApiResponse:
        """
        Reorders a user's linked communities.
        
        :param comIds: A list of community IDs to reorder.
        :type comIds: List[int]
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to reorder a user's linked communities.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.reorder_linked_communities([3, 2, 1])
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/user-profile/{self.userId}/linked-community/reorder",
            data = {
                "timestamp": int(time() * 1000),
                "comIds": comIds
            }
        ))


    @authenticated
    def add_linked_community(self, comId: int) -> ApiResponse:
        """
        Adds a linked community to a user's profile.
        
        :param comId: The ID of the community to add.
        :type comId: int
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to add a linked community to a user's profile.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.add_linked_community(3)
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "POST",
            url = f"/g/s/user-profile/{self.userId}/linked-community/{comId}"
        ))


    @authenticated
    def remove_linked_community(self, comId: int) -> ApiResponse:
        """
        Removes a linked community from a user's profile.
        
        :param comId: The ID of the community to remove.
        :type comId: int
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a DELETE request to the API to remove a linked community from a user's profile.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.remove_linked_community(1)
        ... print(x.status_code)
        """
        return ApiResponse(self.make_request(
            method = "DELETE",
            url = f"/g/s/user-profile/{self.userId}/linked-community/{comId}"
        ))


    @authenticated
    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None) -> ApiResponse:
        """
        Comments on a user's profile, blog, or wiki.
        
        :param message: The message to comment.
        :type message: str
        :param userId: The ID of the user to comment on.
        :type userId: str
        :param blogId: The ID of the blog to comment on.
        :type blogId: str
        :param wikiId: The ID of the wiki to comment on.
        :type wikiId: str
        :param replyTo: The ID of the comment to reply to.
        :type replyTo: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to comment on a user's profile, blog, or wiki.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.comment("Hello, world!", userId = "000000-0000-0000-000000")
        ... print(x.status_code)
        """
        if message is None: raise ValueError("Message must be specified.")

        data = {
            "content": message,
            "stickerId": None,
            "type": 0,
            "timestamp": int(time() * 1000)
        }

        if replyTo: data["respondTo"] = replyTo

        if userId:
            data["eventSource"] = "UserProfileView"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/user-profile/{userId}/g-comment",
                data = data
            ))

        elif blogId:
            data["eventSource"] = "PostDetailView"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/blog/{blogId}/g-comment",
                data = data
            ))
        
        elif wikiId:
            data["eventSource"] = "PostDetailView"
            url = f"/g/s/item/{wikiId}/g-comment"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/item/{wikiId}/g-comment"
            ))
        
        else:
            raise ValueError("Either userId, blogId or wikiId must be specified.")


    @authenticated
    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None) -> ApiResponse:
        """
        Deletes a comment on a user's profile, blog, or wiki.
        
        :param commentId: The ID of the comment to delete.
        :type commentId: str
        :param userId: The ID of the user to delete the comment from.
        :type userId: str
        :param blogId: The ID of the blog to delete the comment from.
        :type blogId: str
        :param wikiId: The ID of the wiki to delete the comment from.
        :type wikiId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a DELETE request to the API to delete a comment on a user's profile, blog, or wiki."""
        if userId:
            return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/user-profile/{userId}/g-comment/{commentId}"
            ))
        elif blogId:
            return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/blog/{blogId}/g-comment/{commentId}"
            ))
        elif wikiId:
            return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/item/{wikiId}/g-comment/{commentId}"
            ))
        else:
            raise ValueError("Either userId, blogId or wikiId must be specified.")


    @authenticated
    def like_blog(self, blogId: Union[str, list] = None, wikiId: str = None) -> ApiResponse:
        """
        Likes a blog or wiki.
        
        :param blogId: The ID of the blog to like.
        :type blogId: Union[str, list]
        :param wikiId: The ID of the wiki to like.
        :type wikiId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to like a blog or wiki.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.like_blog("000000-0000-0000-000000")
        ... print(x.status_code)
        """
        data = {"value": 4, "timestamp": int(time() * 1000)}

        if blogId:
            if isinstance(blogId, str):
                data["eventSource"] = "UserProfileView",
                return ApiResponse(self.make_request(
                    method = "POST",
                    url = f"/g/s/blog/{blogId}/g-vote?cv=1.2",
                    data = data
                ))
            elif isinstance(blogId, list):
                data["targetIdList"] = blogId,
                return ApiResponse(
                    self.make_request(
                        method = "POST", url="/g/s/feed/g-vote",
                        data = data
                    )
                )
            else: raise TypeError("blogId must be a string or a list.")

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/item/{wikiId}/g-vote?cv=1.2",
                data = data
            ))
        else:
            raise ValueError("Either blogId or wikiId must be specified.")


    @authenticated
    def unlike_blog(self, blogId: str = None, wikiId: str = None) -> ApiResponse:
        """
        Unlikes a blog or wiki.
        
        :param blogId: The ID of the blog to unlike.
        :type blogId: str
        :param wikiId: The ID of the wiki to unlike.
        :type wikiId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a DELETE request to the API to unlike a blog or wiki.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.unlike_blog("000000-0000-0000-000000")
        ... print(x.status_code)
        """
        
        if blogId: return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"{self.api}/g/s/blog/{blogId}/g-vote?eventSource=UserProfileView"
            ))
        elif wikiId: return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/item/{wikiId}/g-vote?eventSource=PostDetailView"
            ))
        else:
            raise ValueError("Either blogId or wikiId must be specified.")


    @authenticated
    def like_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None) -> ApiResponse:
        """
        Likes a comment on a user's profile, blog, or wiki.
        
        :param commentId: The ID of the comment to like.
        :type commentId: str
        :param userId: The ID of the user to like the comment on.
        :type userId: str
        :param blogId: The ID of the blog to like the comment on.
        :type blogId: str
        :param wikiId: The ID of the wiki to like the comment on.
        :type wikiId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse

        This function sends a POST request to the API to like a comment on a user's profile, blog, or wiki.

        `ApiResponse` represents a response from the API.

        **Example usage:**

        >>> x = client.like_comment("000000-0000-0000-000000", userId="000000-0000-0000-000000")
        ... print(x.status_code)
        """
        data = {"value": 4, "timestamp": int(time() * 1000)}

        if userId:
            data["eventSource"] = "UserProfileView"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/user-profile/{userId}/comment/{commentId}/g-vote?cv=1.2&value=1",
                data = data
                ))
        
        elif blogId:
            data["eventSource"] = "PostDetailView"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/blog/{blogId}/comment/{commentId}/g-vote?cv=1.2&value=1",
                data = data
            ))
        
        elif wikiId:
            data["eventSource"] = "PostDetailView"
            return ApiResponse(self.make_request(
                method = "POST",
                url = f"/g/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1",
                data = data
            ))
        
        else: raise ValueError("Either userId, blogId or wikiId must be specified.")


    @authenticated
    def unlike_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None) -> ApiResponse:
        """
        Unlikes a comment on a user's profile, blog, or wiki.
        
        :param commentId: The ID of the comment to unlike.
        :type commentId: str
        :param userId: The ID of the user to unlike the comment on.
        :type userId: str
        :param blogId: The ID of the blog to unlike the comment on.
        :type blogId: str
        :param wikiId: The ID of the wiki to unlike the comment on.
        :type wikiId: str
        :return: An `ApiResponse` object containing the response from the API.
        :rtype: ApiResponse
        
        This function sends a DELETE request to the API to unlike a comment on a user's profile, blog, or wiki.
        
        `ApiResponse` represents a response from the API.
        
        **Example usage:**
        
        >>> x = client.unlike_comment("000000-0000-0000-000000", userId="000000-0000-0000-000000")
        ... print(x.status_code)
        """
        if userId:
            return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView"
            ))
        elif blogId:
            return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
            ))
        elif wikiId:
            return ApiResponse(self.make_request(
                method = "DELETE",
                url = f"/g/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
            ))
        else: raise ValueError("Either userId, blogId or wikiId must be specified.")


    def fetch_supported_languages(self) -> List[str]:
        """
        Fetches a list of supported languages for the API.
        
        :return: A list of supported languages.
        :rtype: List[str]
        
        This function sends a GET request to the API to fetch a list of supported languages.
        
        **Example usage:**
        
        >>> x = client.fetch_supported_languages()
        ... print(x)
        """
        return self.make_request(
            method="GET",
            url="/g/s/community-collection/supported-languages?start=0&size=100",
        )["supportedLanguages"]


    @authenticated
    def fetch_ta_announcement(self, language: str = "en", start: int = 0, size: int = 25) -> dict:
        """
        Fetches the latest announcements from the API.

        :param language: The language to fetch the announcements in.
        :type language: str
        :param start: The index to start fetching announcements from.
        :type start: int
        :param size: The number of announcements to fetch.
        :type size: int
        :return: A dictionary containing the announcements.
        :rtype: dict

        This function sends a GET request to the API to fetch the latest announcements.

        **Example usage:**

        >>> x = client.fetch_ta_announcement()
        ... print(x)
        """
        if language not in self.fetch_supported_languages():
            raise ValueError("Invalid language.")
        
        return self.make_request(
            method = "GET",
            url = f"/g/s/announcement?language={language}&start={start}&size={size}"
        )


    @authenticated
    def join_chat(self, chatId: str) -> ApiResponse:
        """
        Joins the authenticated user to a chat thread.

        :param chatId: The ID of the chat thread to join.
        :type chatId: str
        :return: The API response.
        :rtype: ApiResponse

        This method joins the authenticated user to a chat thread. The user must be a member of the community that the chat
        thread belongs to in order to join the thread.

        **Note:** This method requires authentication. If the client is not authenticated, a `LoginRequired` exception will
        be raised.
        """
        return ApiResponse(self.make_request(
            method="POST",
            url=f"/g/s/chat/thread/{chatId}/member/{self.userId}"
            ))


    @authenticated
    def leave_chat(self, chatId: Union[str, List[str]]) -> ApiResponse:
        """
        Removes the authenticated user from a chat thread.

        :param chatId: A list of chat thread IDs to leave or a single chat thread ID to leave.
        :type chatId: Union[str, List[str]]
        :return: The API response.
        :rtype: ApiResponse

        This method removes the authenticated user from a chat thread. The user must be a member of the chat thread in order
        to leave it.

        **Note:** This method requires authentication. If the client is not authenticated, a `LoginRequired` exception will
        be raised.
        """
        return ApiResponse(self.make_request(
            method="DELETE",
            url = f"/g/s/chat/thread/leave?threadIds={','.join(chatId) if isinstance(chatId, list) else chatId}"
            ))


    @authenticated
    def join_community(self, community_id: int, invitationId = None) -> ApiResponse:
        """
        Joins the user to a community with the provided community ID.

        :param community_id: The ID of the community to join.
        :type community_id: int
        :param invitationId: The ID of the invitation link.
        :type invitationId: str
        :return: An ApiResponse object containing the server response.
        :rtype: ApiResponse
        :raises LoginRequired: If the user is not logged in.

        This function first checks if the client is logged in by checking for a valid session ID. If not, it raises a
        LoginRequired exception.

        If the client is logged in, the function sends a POST request to the server to join the specified community.
        The request includes the client's session ID and the ID of the community to join.

        The function returns an ApiResponse object containing the server response.

        **Note:** This function can be used to join the user to a community with the provided community ID. Once joined,
        the user can make API calls related to the community, such as posting or retrieving posts.
        """
        data = {"timestamp": int(time() * 1000)}
        if invitationId:
            data["invitationId"] = invitationId

        return ApiResponse(
            self.make_request(
                method="POST",
                url=f"/x{community_id}/s/community/join",
                data = data
        ))


    @authenticated
    def leave_community(self, community_id: int) -> ApiResponse:
        """
        Leaves the user from a community with the provided community ID.

        :param community_id: The ID of the community to leave.
        :type community_id: int
        :return: An ApiResponse object containing the server response.
        :rtype: ApiResponse
        :raises LoginRequired: If the user is not logged in.

        This function first checks if the client is logged in by checking for a valid session ID. If not, it raises a
        LoginRequired exception.

        If the client is logged in, the function sends a POST request to the server to leave the specified community.
        The request includes the client's session ID and the ID of the community to leave.

        The function returns an ApiResponse object containing the server response.

        **Note:** This function can be used to leave the user from a community with the provided community ID. Once left,
        the user will no longer have access to the community and will not be able to make API calls related to the community.
        """
        return ApiResponse(self.make_request(
            method="POST",
            url=f"/x{community_id}/s/community/leave"
            ))
    

    def fetch_community(self, community_id: int) -> CCommunity:
        """
        Fetches the community information for the community with the provided community ID.

        :param community_id: The ID of the community to fetch.
        :type community_id: int
        :return: A CCommunity object representing the community information.
        :rtype: CCommunity

        This function sends a GET request to the server to fetch the community information for the community with the
        provided community ID. The request includes the ID of the community to fetch.

        The function returns a CCommunity object representing the community information. The CCommunity object contains
        attributes such as the members count, the community's layout, and other community information.

        **Note:** This function can be used to fetch the community information for a community on Amino. The community
        information can be used to display information about the community such as the community's name, description, and
        other information.
        """
        return CCommunity(self.make_request(
            method="GET",
            url=f"/g/s-x{community_id}/community/info"
            ))
    

    @authenticated
    def joined_communities(self) -> CCommunityList:
        """
        Retrieves the list of communities that the authenticated user has joined.

        :return: The list of communities.
        :rtype: CCommunityList

        This method returns the list of communities that the authenticated user has joined. The list includes information
        such as the community ID, name, description, and theme.

        **Note:** This method requires authentication. If the client is not authenticated, a `LoginRequired` exception will
        be raised.
        """
        return CCommunityList(self.make_request(
            method="GET",
            url="/g/s/community/joined"
            ))


    def fetch_object_id(self, link: str) -> str:
        """
        Fetches the object ID given a link to the object.

        :param link: The link to the object.
        :type link: str
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: The ID of the object.
        :rtype: str

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        The method caches the object ID for faster access in future calls.

        **Example usage:**

        >>> object_id = client.community.fetch_object_id(link="https://aminoapps.com/p/w2Fs6H")
        >>> print(object_id)
        """

        KEY = str((link, "OBJECT_ID"))
        if not self.cache.get(KEY):
            self.cache.set(KEY, self.make_request(
                method = "GET",
                url = f"/g/s/link-resolution?q={link}"
                ))
        return LinkInfo(self.cache.get(KEY)).objectId


    def fetch_object_info(self, link: str) -> LinkInfo:
        """
        Fetches information about an object given its link.

        :param link: The link to the object.
        :type link: str
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: A LinkInfo object containing information about the object.
        :rtype: LinkInfo

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        The method caches the object information for faster access in future calls.

        `LinkInfo`:

        - `data`: The raw response data from the API.
        - `linkInfoV2`: The link information data.
        - `path`: The path of the object.
        - `extensions`: The extensions data.
        - `objectId`: The ID of the object.
        - `shareURLShortCode`: The short code of the share URL.
        - `targetCode`: The target code.
        - `ndcId`: The NDC ID.
        - `comId`: The community ID.
        - `fullPath`: The full path of the object.
        - `shortCode`: The short code of the object.
        - `objectType`: The type of the object.

        **Example usage:**

        >>> object_info = client.community.fetch_object_info(link="https://aminoapps.com/p/w2Fs6H")
        >>> print(object_info.objectId)
        """

        KEY = str((link, "OBJECT_INFO"))
        if not self.cache.get(KEY):
            self.cache.set(KEY, self.make_request(
                method = "GET",
                url = f"/g/s/link-resolution?q={link}"
                ))
        return LinkInfo(self.cache.get(KEY))

    def fetch_public_communities(self, type: str = "discover") -> CCommunityList:
        """
        Fetches a list of public communities.

        This method retrieves a list of public communities based on the specified parameters.

        :param type: The type of communities to fetch (default is "discover").
        :type type: str
        :return: A `CCommunityList` object containing the list of public communities.
        :rtype: CCommunityList
        
        **example usage:**
        
        >>> communities = client.fetch_public_communities()
        >>> for community in communities.name:
        >>>     print(community)
        """
        return CCommunityList(self.make_request(
            method = "GET",
            url = f"/g/s/topic/0/feed/community?type={type}&categoryKey=recommendation&moduleId=0c56a709-1f96-474d-ae2f-4225d0e998e5"
        ))
    
    def fetch_available_communities(self, start: int = 0, size: int = 25, language: str = "en") -> CCommunityList:
        """
        Fetches a list of available communities.

        This method retrieves a list of communities that are available for exploration.

        :param start: The starting index of the communities to fetch (default is 0).
        :type start: int
        :param size: The number of communities to fetch in a single request (default is 25).
        :type size: int
        :param language: The language code used for filtering communities (default is "en").
        :type language: str
        :return: A CCommunityList object containing information about the available communities.
        :rtype: CCommunityList
        :raises: Any exceptions raised during the API request process.

        The `CCommunityList` object provides access to information about multiple communities:

        - `json`: The raw response data from the API.
        - `comId`: The list of community Ids.
        - `name`: The list of community names.

        **Example usage:**

        >>> community_list = client.community.fetch_available_communities(start=0, size=10, language="en")
        >>> for name, comId in zip(community_list.name, community_list.comId):
        >>>     print(name, comId])
        """
        return CCommunityList(self.make_request(
            method = "GET",
            url = f"/g/s/topic/0/feed/community?language={language}&type=web-explore&categoryKey=recommendation&start={start}&size={size}&pagingType=t"
        ))

    @authenticated
    def unfollow(self, userId: str) -> ApiResponse:
        """
        Unfollows a user.
        :param userId: The ID of the user to unfollow.
        :type userId: str
        :return: An ApiResponse object containing the response data from the API.
        :rtype: ApiResponse
        This function allows the logged-in user to unfollow another user specified by their ID.
        After successful execution, the user will no longer be following the specified user.
        **Example usage:**
        >>> response = client.unfollow(userId="user123")
        >>> print(response.status_code)
        """
        return ApiResponse(self.make_request(
            method = "DELETE",
            url = f"/g/s/user-profile/{userId}/member/{self.userId}"
        ))
    
    @authenticated
    def fetch_notifications(self, start: int = 0, size: int = 25):
        """
        Fetches the notifications for the authenticated user.
        :param start: The starting index of the notifications to fetch (default is 0).
        :type start: int
        :param size: The number of notifications to fetch in a single request (default is 25).
        :type size: int
        :return: A list of notifications.
        :rtype: list
        This function allows the logged-in user to fetch their notifications.
        **Example usage:**
        >>> notifications = client.fetch_notifications(start=0, size=25)
        >>> for notification in notifications:
        >>>     print(notification)
        """
        return GlobalNotificationList(self.make_request(
            method = "GET",
            url = f"/g/s/notification?start={start}&size={size}"
        ))
    
    
    @authenticated
    def delete_notification(self, notificationId: str) -> ApiResponse:
        """
        Deletes a notification.
        :param notificationId: The ID of the notification to delete.
        :type notificationId: str
        :return: An ApiResponse object containing the response data from the API.
        :rtype: ApiResponse
        This function allows the logged-in user to delete a notification.
        **Example usage:**
        >>> response = client.delete_notification(notificationId="notification123")
        >>> print(response.status_code)
        """
        return ApiResponse(self.make_request(
            method = "DELETE",
            url = f"/g/s/notification/{notificationId}"
        ))
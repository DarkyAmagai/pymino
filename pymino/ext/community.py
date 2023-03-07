from uuid import uuid4
from io import BytesIO
from requests import get
from random import randint
from diskcache import Cache
from base64 import b64encode
from time import time, timezone
from typing import BinaryIO, Callable, List, Optional, Union, TypeVar, Any


from .entities.enums import *
from .entities.threads import CThread, CThreadList
from .entities.userprofile import UserProfile, UserProfileList

from .entities.messages import (
    CMessage, CMessages, PrepareMessage
    )
from .entities.exceptions import (
    InvalidImage, MissingCommunityId,
    MissingTimers, NoDataProvided, NotLoggedIn
    )
from .entities.general import (
    ApiResponse, CBlog, CBlogList, CChatMembers,
    CComment, CCommentList, CCommunity, CCommunityList,
    CheckIn, CommunityInvitation, Coupon, FeaturedBlogs,
    InvitationId, LinkInfo, NotificationList, QuizRankingList
    )

F = TypeVar("F", bound=Callable[..., Any])

class Community:
    """
    The `Community` class handles community related actions.

    **Parameters:**

    - `bot` or `client` (`Bot` or `Client`): The client instance that this object belongs to.
    - `session` (`requests.Session`): The session object used to make requests.
    - `community_id` (`int`, optional): The community ID to use for the methods. If not provided, the default community ID
      set in the `Community` instance will be used.

    ------------------------
    ## NotLoggedIn Error

    If you get a `NotLoggedIn` error, you need to log in to the client before using the specific method.

    ------------------------
    ## MissingCommunityId Error

    If you get a `MissingCommunityId` error, you need to pass the community ID to the method or set the community ID in
    the `Community` class.

    ```
    # Set community ID (recommended for single-community bots)

    client = Client()

    # To fetch the community ID from a link
    client.fetch_community_id(community_link="https://aminoapps.com/c/your-community-link")

    # To manually set the community ID
    client.set_community_id(community_id=123456789)

    # Pass community ID to method (recommended for multi-community bots)
    client.community.join_community(comId=123456789)
    ```

    ------------------------
    ## Object IDs

    To get the ID of an object (e.g. a chat, blog, or user), use the `fetch_object_id` method.

    ```
    # Get object ID (chat, blog, user) from link 

    client = Client()

    object_id = client.community.fetch_object_id(link="https://aminoapps.com/p/w2Fs6H")
    print(object_id) # Output: the object ID from the link.
    ```

    ------------------------
    ## Sending Messages and Images to Chats

    To send a message to a chat, use the `send_message` method.

    ```
    # Send message to chat

    client = Client()

    client.community.send_message(
        chatId="000000-0000-0000-000000",
        content="Hello, world!",
        comId=123456789 # We need to pass the community ID because we didn't set it in the `Community` instance.
    )
    ```

    To send an image to a chat, use the `send_image` method. You'll need either the image URL or path to the image.

    ```
    # Send image to chat

    client = Client()

    client.community.send_image(
        chatId="000000-0000-0000-000000",
        image="https://i.imgur.com/your-image.png", # or image="path/to/image.png"
        comId=123456789 # We need to pass the community ID because we didn't set it in the `Community` instance.
    )
    ```

    """

    def __init__(self, bot, session, community_id: Union[str, int] = None) -> None:
        self.bot = bot
        self.session = session
        self.cache = Cache("cache")
        self.community_id: Union[str, int] = community_id
        self.userId: Optional[str] = None
        if self.userId is None: return


    def community(func: F) -> F:
        """
        A decorator that ensures the user is logged in and a community ID is present before running the decorated function.

        :param func: The function to be decorated.
        :type func: Callable
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: The result of calling the decorated function.
        :rtype: Any

        Before using this decorator, you must initialize a `Community` instance with either a `community_id` or by setting it 
        after fetching the community ID with `fetch_community_id` method.

        **Example usage:**

        >>> client = Bot()
        >>> client.fetch_community_id(community_link="https://aminoapps.com/c/your-community-link")
        >>> client.community_id = 123456789

        >>> @community
        >>> def my_function(self, comId: str):
        >>>     # Function code
        """
        def community_func(*args, **kwargs) -> Any:
            if not args[0].userId:
                raise NotLoggedIn("You are not logged in. Please login before using this function.")
            if not any([args[0].community_id, kwargs.get("comId")]):
                raise MissingCommunityId("Please provide a community id to the bot before running it or add it to the function call.")
            return func(*args, **kwargs)
        community_func.__annotations__ = func.__annotations__
        return community_func


    @community
    def invite_code(self, comId: Union[str, int] = None) -> CommunityInvitation:
        """
        Generates an invite code for the community.

        :param comId: The ID of the community, defaults to None.
        :type comId: Union[str, int], optional
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: A CommunityInvitation object containing the invite code information.
        :rtype: CommunityInvitation

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `CommunityInvitation`:

        - `data`: The raw response data from the API.
        - `communityInvitation`: The invite code information data.
        - `status`: The status of the invite code.
        - `duration`: The duration of the invite code.
        - `invitationId`: The ID of the invite code.
        - `link`: The link to the community with the invite code.
        - `modifiedTime`: The time when the invite code was last modified.
        - `ndcId`: The NDC ID of the community.
        - `createdTime`: The time when the invite code was created.
        - `inviteCode`: The invite code.

        **Example usage:**

        >>> invite_code = client.community.invite_code(comId=123456)
        >>> print(invite_code.inviteCode)
        """
        return CommunityInvitation(self.session.handler(
            method = "POST",
            url = f"/g/s-x{self.community_id if comId is None else comId}/community/invitation",
            data = {"duration": 0, "force": True, "timestamp": int(time() * 1000)}
            ))


    @community
    def fetch_object(
        self,
        objectId: str,
        objectType: ObjectTypes = ObjectTypes.USER,
        comId: Union[str, int] = None,
        **kwargs
        ) -> LinkInfo:
        """
        Fetches the link information of an object given its ID.

        :param objectId: The ID of the object whose link information is to be fetched.
        :type objectId: str
        :param objectType: The type of the object, defaults to ObjectTypes.USER.
        :type objectType: ObjectTypes, optional
        :param comId: The ID of the community, defaults to None.
        :type comId: Union[str, int], optional
        :raises NotLoggedIn: If the user is not logged in.
        :raises MissingCommunityId: If the community ID is missing.
        :return: A LinkInfo object containing the link information of the object.
        :rtype: LinkInfo

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        The method caches the link information for faster access in future calls.

        `ObjectTypes`:

        - `USER`: 0
        - `BLOG`: 1
        - `WIKI`: 2
        - `CHAT`: 12

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

        >>> link_info = client.community.fetch_object(objectId="0000-00000-00000-0000", objectType=ObjectTypes.BLOG, comId=123456)
        >>> print(link_info.fullPath)
        """
        if "object_type" in kwargs: #TODO: Remove this in the near future.
            objectType = kwargs["object_type"]
            print("Warning: The 'object_type' parameter is deprecated. Please use 'objectType' instead.")

        KEY = str((objectId, self.community_id if comId is None else comId))
        if not self.cache.get(KEY):
            self.cache.set(KEY, self.session.handler(
                method = "POST",
                url = f"/g/s-x{self.community_id if comId is None else comId}/link-resolution",
                data = {
                    "objectId": objectId,
                    "targetCode": 1,
                    "objectType": objectType.value if isinstance(objectType, ObjectTypes) else objectType,
                    "timestamp": int(time() * 1000)
                    }
                ))
        return LinkInfo(self.cache.get(KEY))


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
            self.cache.set(KEY, self.session.handler(
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
            self.cache.set(KEY, self.session.handler(
                method = "GET",
                url = f"/g/s/link-resolution?q={link}"
                ))
        return LinkInfo(self.cache.get(KEY))


    def fetch_community(self, comId: Union[str, int] = None) -> CCommunity:
        """
        Fetches information about a community given its ID.

        :param comId: The ID of the community to fetch. If None, the current community ID is used.
        :type comId: Union[str, int], optional
        :raises NotLoggedIn: If the user is not logged in.
        :raises InvalidCommunity: If the community does not exist.
        :return: A CCommunity object containing information about the community.
        :rtype: CCommunity

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        The method caches the community information for faster access in future calls.

        `CCommunity`:

        - `data`: The raw response data from the API.
        - `keywords`: The keywords of the community.
        - `activeInfo`: The active info of the community.
        - `themePack`: The theme pack of the community.
        - `status`: The status of the community.
        - `probationStatus`: The probation status of the community.
        - `updatedTime`: The time the community was last updated.
        - `primaryLanguage`: The primary language of the community.
        - `modifiedTime`: The time the community was last modified.
        - `membersCount`: The number of members in the community.
        - `tagline`: The tagline of the community.
        - `name`: The name of the community.
        - `endpoint`: The endpoint of the community.
        - `communityHeadList`: The community head list.
        - `listedStatus`: The listed status of the community.
        - `extensions`: The extensions data.
        - `mediaList`: The media list of the community.
        - `userAddedTopicList`: The user-added topic list of the community.
        - `communityHeat`: The heat of the community.
        - `templateId`: The template ID of the community.
        - `searchable`: Whether the community is searchable.
        - `createdTime`: The time the community was created.
        - `invitation`: The ID of the invitation for the community.
        - `ndcId`: The NDC ID of the community.
        - `comId`: The ID of the community.
        - `icon`: The icon of the community.

        **Example usage:**

        >>> community_info = client.community.fetch_community(comId="123456")
        >>> print(community_info.name)
        """

        KEY = str((comId, "COMMUNITY_INFO"))
        if not self.cache.get(KEY):
            self.cache.set(KEY, self.session.handler(
                method = "GET",
                url = f"/g/s-x{self.community_id if comId is None else comId}/community/info"
                ))
        return CCommunity(self.cache.get(KEY))


    def joined_communities(self, start: int = 0, size: str = 50) -> CCommunityList:
        """
        Fetches a list of communities the user has joined.
        
        :param start: The index to start fetching from. Defaults to 0.
        :type start: int, optional
        :param size: The number of communities to fetch. Defaults to 50.
        :type size: str, optional
        :raises NotLoggedIn: If the user is not logged in.
        :return: A CCommunityList object containing the list of communities.
        :rtype: CCommunityList
        
        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        
        `CCommunityList`:
        
        - `data`: The raw response data from the API.
        - `keywords`: The keywords of the community.
        - `activeInfo`: The active info of the community.
        - `themePack`: The theme pack of the community.
        - `status`: The status of the community.
        - `probationStatus`: The probation status of the community.
        - `updatedTime`: The time the community was last updated.
        - `primaryLanguage`: The primary language of the community.
        - `modifiedTime`: The time the community was last modified.
        - `membersCount`: The number of members in the community.
        - `tagline`: The tagline of the community.
        - `name`: The name of the community.
        - `endpoint`: The endpoint of the community.
        - `communityHeadList`: The community head list.
        - `listedStatus`: The listed status of the community.
        - `extensions`: The extensions data.
        - `mediaList`: The media list of the community.
        - `userAddedTopicList`: The user-added topic list of the community.
        - `communityHeat`: The heat of the community.
        - `templateId`: The template ID of the community.
        - `searchable`: Whether the community is searchable.
        - `createdTime`: The time the community was created.
        - `invitation`: The ID of the invitation for the community.
        - `ndcId`: The NDC ID of the community.
        - `comId`: The ID of the community.
        - `icon`: The icon of the community.
        
        **Example usage:**
        
        >>> community_list = client.community.joined_communities()
        >>> print(community_list.name)
        """
        return CCommunityList(self.session.handler(
            method = "GET",
            url = f"/g/s/community/joined?v=1&start={start}&size={size}"
            ))


    @community
    def join_community(self, comId: Union[str, int] = None) -> ApiResponse:
        """
        Joins the current or specified community.

        :param comId: The ID of the community to join. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the timestamp as data.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.join_community()
        >>> if api_response.statuscode == 0:
        ...     print("Joined community successfully!")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/community/join", 
            data={"timestamp": int(time() * 1000)}
            ))


    def fetch_invitationId(self, inviteCode: str, **kwargs) -> str:
        """
        Fetches the invitation ID for a given invite code.

        :param inviteCode: The invite code to fetch the invitation ID for.
        :type inviteCode: str
        :return: The invitation ID.
        :rtype: str

        The function sends a GET request to the API with the invite code as a parameter.

        `InvitationId`:

        - `invitationId`: The ID of the invitation.

        **Example usage:**

        >>> invitation_id = client.fetch_invitationId(invite_code="ABCD1234")
        >>> print(invitation_id)
        """
        if "invite_code" in kwargs: #TODO: Remove this in the near future.
            inviteCode = kwargs["invite_code"]
            print("The 'invite_code' parameter has been deprecated. Please use 'inviteCode' instead.")

        return InvitationId(self.session.handler(
            method = "GET",
            url = f"/g/s/community/link-identify?q={inviteCode}"
            )).invitationId


    @community
    def join_community_by_code(self, inviteCode: str, comId: Union[str, int] = None, **kwargs) -> ApiResponse:
        """
        Joins a community using the invite code.

        :param inviteCode: The invite code of the community.
        :type inviteCode: str
        :param comId: The ID of the community to join. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the invitation ID and timestamp as data.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.join_community_by_code(invite_code="ABC123")
        >>> if api_response.statuscode == 0:
        ...     print("Joined community successfully!")
        """
        if "invite_code" in kwargs: #TODO: Remove this in the near future.
            inviteCode = kwargs["invite_code"]
            print("The 'invite_code' parameter has been deprecated. Please use 'inviteCode' instead.")

        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/join",
            data = {
                "invitationId": self.fetch_invitationId(inviteCode=inviteCode),
                "timestamp": int(time() * 1000)
                }
            ))


    @community
    def leave_community(self, comId: Union[str, int] = None) -> ApiResponse:
        """
        Leaves the current or specified community.

        :param comId: The ID of the community to leave. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the timestamp as data.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.leave_community()
        >>> if api_response.statuscode == 0:
        ...     print("Left community successfully!")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/leave", 
            data={"timestamp": int(time() * 1000)}
            ))


    @community
    def request_join(self, message: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Sends a membership request to join the current or specified community.

        :param message: The message to include in the membership request.
        :type message: str
        :param comId: The ID of the community to request membership to. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the message and timestamp as data.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.request_join(message="Please accept my membership request.")
        >>> if api_response.statuscode == 0:
        ...     print("Membership request sent successfully!")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/community/membership-request", 
            data={"message": message, "timestamp": int(time() * 1000)}
            ))


    @community
    def flag_community(self, reason: str, flagType: FlagTypes = FlagTypes.OFFTOPIC, comId: Union[str, int] = None) -> ApiResponse:
        """
        Flags the current or specified community with the given reason and flag type.

        :param reason: The reason for flagging the community.
        :type reason: str
        :param flagType: The flag type to use. Must be a value from the FlagTypes enum.
        :type flagType: FlagTypes
        :param comId: The ID of the community to flag. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the community ID, flag type, reason, and timestamp as data.

        `FlagTypes` enum:

        - `AGGRESSION`: For flagging aggressive content.
        - `SPAM`: For flagging spam content.
        - `OFFTOPIC`: For flagging off-topic content.
        - `VIOLENCE`: For flagging violent content.
        - `INTOLERANCE`: For flagging intolerant content.
        - `SUICIDE`: For flagging content related to suicide or self-harm.
        - `TROLLING`: For flagging trolling behavior.
        - `PORNOGRAPHY`: For flagging pornographic content.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.flag_community(reason="This community contains inappropriate content.", flagType=FlagTypes.PORNOGRAPHY)
        >>> if api_response.statuscode == 0:
        ...     print("Community flagged successfully!")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/flag", 
            data={
            "objectId": self.community_id,
            "objectType": 16,
            "flagType": flagType.value if isinstance(flagType, FlagTypes) else flagType,
            "message": reason,
            "timestamp": int(time() * 1000)
            }))

    @community
    def check_in(self, timezone: Optional[int] = -300, comId: Union[str, int] = None) -> CheckIn:
        """
        Performs a check-in for the current or specified community.

        :param timezone: The timezone offset in minutes. Default is -300 (Eastern Time).
        :type timezone: Optional[int]
        :param comId: The ID of the community to check-in to. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A CheckIn object containing the check-in data.
        :rtype: CheckIn

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the timezone offset and timestamp as data.

        `CheckIn`:

        - `data`: The raw response data from the API.
        - `checkInHistory`: The check-in history data.
        - `consecutiveCheckInDays`: The number of consecutive days the user has checked in.
        - `hasCheckInToday`: Whether the user has checked in today.
        - `hasAnyCheckIn`: Whether the user has checked in at all.
        - `history`: The user's check-in history.
        - `userProfile`: The user's profile data.

        **Example usage:**

        >>> check_in_data = client.community.check_in(timezone=-480)
        >>> if check_in_data.hasCheckInToday:
        ...     print("Check-in successful!")
        """
        return CheckIn(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/check-in",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}
            ))


    @community
    def play_lottery(self, timezone: Optional[int] = -300, comId: Union[str, int] = None) -> ApiResponse:
        """
        Plays the lottery for the current or specified community.

        :param timezone: The timezone offset in minutes. Default is -300 (Eastern Time).
        :type timezone: Optional[int]
        :param comId: The ID of the community to play the lottery in. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the timezone offset and timestamp as data.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.play_lottery(timezone=-480)
        >>> if api_response.statuscode == 0:
        ...     print("Lottery played successfully!")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/check-in/lottery",
            data={"timezone": timezone, "timestamp": int(time() * 1000)}
            ))

    
    @community
    def online_status(
        self,
        onlineStatus: OnlineTypes = OnlineTypes.ONLINE,
        comId: Union[str, int] = None,
        **kwargs
        ) -> ApiResponse:
        """
        Sets the online status of the user in the current or specified community.

        :param onlineStatus: The online status to set. Default is OnlineTypes.ONLINE.
        :type onlineStatus: OnlineTypes
        :param comId: The ID of the community to set the online status in. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: An ApiResponse object containing the API response data.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API with the online status and timestamp as data.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: The message from the API response.
        - `statuscode`: The status code from the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API response.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        >>> api_response = client.community.online_status(status=OnlineTypes.ONLINE)
        >>> if api_response.statuscode == 0:
        ...     print("Online status set successfully!")
        """
        if "status" in kwargs: #TODO: Remove in the near future.
            onlineStatus = kwargs["status"]
            print("The 'status' parameter is deprecated. Please use 'onlineStatus' instead.")

        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{self.userId}/online-status",
            data={"status": onlineStatus.value, "timestamp": int(time() * 1000)}
            ))


    @community
    def fetch_new_user_coupon(self, comId: Union[str, int] = None) -> Coupon:
        """
        Fetches the new user coupon for the current or specified community.

        :param comId: The ID of the community to fetch the new user coupon from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A Coupon object containing information about the new user coupon.
        :rtype: Coupon

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch the new user coupon data.

        `Coupon`:

        - `data`: The raw response data from the API.
        - `expiredTime`: The expiration time of the coupon.
        - `couponId`: The ID of the coupon.
        - `scopeDesc`: The description of the coupon scope.
        - `status`: The status of the coupon.
        - `modifiedTime`: The time the coupon was last modified.
        - `couponValue`: The value of the coupon.
        - `expiredType`: The expiration type of the coupon.
        - `title`: The title of the coupon.
        - `couponType`: The type of the coupon.
        - `createdTime`: The time the coupon was created.

        **Example usage:**

        >>> new_user_coupon = client.community.fetch_new_user_coupon()
        >>> print(new_user_coupon.title)
        """
        return Coupon(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/coupon/new-user-coupon"
            ))


    @community
    def fetch_notifications(self, size: Optional[int] = 25, comId: Union[str, int] = None) -> NotificationList:
        """
        Fetches a list of notifications for the current or specified community.

        :param size: The number of notifications to fetch. Defaults to 25.
        :type size: Optional[int]
        :param comId: The ID of the community to fetch the notifications from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A NotificationList object containing the list of notifications.
        :rtype: NotificationList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch the notifications list data.

        `NotificationList`:

        - `data`: The raw response data from the API.
        - `parentText`: A list of parent text for each notification.
        - `objectId`: A list of object IDs for each notification.
        - `contextText`: A list of context text for each notification.
        - `type`: A list of notification types for each notification.
        - `parentId`: A list of parent IDs for each notification.
        - `author`: A UserProfileList object containing information about the author of each notification.
        - `createdTime`: A list of creation times for each notification.
        - `parentType`: A list of parent types for each notification.
        - `comId`: A list of community IDs for each notification.
        - `notificationId`: A list of notification IDs for each notification.
        - `objectText`: A list of object text for each notification.
        - `contextValue`: A list of context values for each notification.
        - `contextComId`: A list of context community IDs for each notification.
        - `objectType`: A list of object types for each notification.

        **Example usage:**

        >>> notifications = client.community.fetch_notifications(size=10)
        >>> listOfOfObjectIds = notifications.objectId
        """
        return NotificationList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/notification?pagingType=t&size={size}"
            ))


    @community
    def fetch_user(self, userId: str, comId: Union[str, int] = None) -> UserProfile:
        """
        Fetches the user profile of the specified user in the current or specified community.

        :param userId: The ID of the user to fetch the profile for.
        :type userId: str
        :param comId: The ID of the community to fetch the user profile from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `UserProfile` object containing information about the user's profile.
        :rtype: UserProfile

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch the user profile data.

        `UserProfile`:

        - `status`: The status of the request.
        - `mood_sticker`: The mood sticker the user has set.
        - `wiki_count`: The number of wikis the user has created.
        - `consecutive_check_in_days`: The number of consecutive days the user has checked in.
        - `uid`: The user ID of the user.
        - `modified_time`: The time the user profile was last modified.
        - `following_status`: The following status of the user.
        - `online_status`: The online status of the user.
        - `account_membership_status`: The account membership status of the user.
        - `is_global`: Whether the user is a global user.
        - `avatar_frame_id`: The avatar frame ID of the user.
        - `reputation`: The reputation of the user.
        - `posts_count`: The number of posts the user has created.
        - `avatar_frame`: The avatar frame of the user.
        - `members_count`: The number of members the user has.
        - `nickname`: The nickname of the user.
        - `media_list`: The media list of the user.
        - `icon`: The icon of the user.
        - `is_nickname_verified`: Whether the user's nickname is verified.
        - `mood`: The mood of the user.
        - `level`: The level of the user.
        - `notification_subscription_status`: The notification subscription status of the user.
        - `settings`: The settings of the user.
        - `push_enabled`: Whether push is enabled for the user.
        - `membership_status`: The membership status of the user.
        - `influencer_info`: The influencer info of the user.
        - `content`: The user's profile content.
        - `follower_count`: The number of followers the user has.
        - `role`: The role of the user.
        - `comments_count`: The number of comments the user has on their wall.
        - `ndc_id`: The ID of the community the user is in.
        - `created_time`: The time the user was created.
        - `extensions`: The extensions of the user.
        - `stories_count`: The number of stories the user has created.
        - `blogs_count`: The number of blogs the user has created.

        **Example usage:**

        >>> user_profile = client.community.fetch_user(userId='123456')
        >>> print(user_profile.nickname)
        'John Doe'
        """
        return UserProfile(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}"
            ))


    @community
    def fetch_users(
        self,
        userType: UserTypes = UserTypes.RECENT,
        start: Optional[int] = 0,
        size: Optional[int] = 25,
        comId: Union[str, int] = None,
        **kwargs
    ) -> UserProfileList:
        """
        Fetches a list of users in the current or specified community based on the specified user type.
        
        :param userType: The type of users to fetch. Defaults to `UserTypes.RECENT`.
        :type userType: UserTypes
        :param start: The starting point to fetch users from. Defaults to `0`.
        :type start: Optional[int]
        :param size: The amount of users to fetch. Defaults to `25`.
        :type size: Optional[int]
        :param comId: The ID of the community to fetch the users from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `UserProfileList` object containing information about the users.
        :rtype: UserProfileList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of users.

        `UserTypes`:

        - `LEADERS`: Fetches the leaders of the community.
        - `CURATORS`: Fetches the curators of the community.
        - `RECENT`: Fetches the most recent users of the community.
        - `FEATURED`: Fetches the featured users of the community.
        - `BANNED`: Fetches the banned users of the community.

        `UserProfileList`:

        - `status`: The status of the request.
        - `mood_sticker`: The mood sticker the user has set.
        - `wiki_count`: The number of wikis the user has created.
        - `consecutive_check_in_days`: The number of consecutive days the user has checked in.
        - `uid`: The user ID of the user.
        - `modified_time`: The time the user profile was last modified.
        - `following_status`: The following status of the user.
        - `online_status`: The online status of the user.
        - `account_membership_status`: The account membership status of the user.
        - `is_global`: Whether the user is a global user.
        - `avatar_frame_id`: The avatar frame ID of the user.
        - `reputation`: The reputation of the user.
        - `posts_count`: The number of posts the user has created.
        - `avatar_frame`: The avatar frame of the user.
        - `members_count`: The number of members the user has.
        - `nickname`: The nickname of the user.
        - `media_list`: The media list of the user.
        - `icon`: The icon of the user.
        - `is_nickname_verified`: Whether the user's nickname is verified.
        - `mood`: The mood of the user.
        - `level`: The level of the user.
        - `notification_subscription_status`: The notification subscription status of the user.
        - `settings`: The settings of the user.
        - `push_enabled`: Whether push is enabled for the user.
        - `membership_status`: The membership status of the user.
        - `influencer_info`: The influencer info of the user.
        - `content`: The user's profile content.
        - `follower_count`: The number of followers the user has.
        - `role`: The role of the user.
        - `comments_count`: The number of comments the user has on their wall.
        - `ndc_id`: The ID of the community the user is in.
        - `created_time`: The time the user was created.
        - `extensions`: The extensions of the user.
        - `stories_count`: The number of stories the user has created.
        - `blogs_count`: The number of blogs the user has created.

        **Example usage:**

        >>> user_profiles = client.community.fetch_users(userType=UserTypes.CURATORS)
        >>> print(user_profiles[0].nickname) # Prints the nickname of the first user in the list.
        'John Doe'
        """
        if "type" in kwargs: #TODO: Get rid of this in the near future.
            userType = kwargs["type"]
            print("WARNING: The 'type' parameter is deprecated. Please use 'userType' instead.")
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile?type={userType.value if isinstance(userType, UserTypes) else userType}&start={start}&size={size}"
            ))

    @community
    def fetch_online_users(self, start: Optional[int] = 0, size: Optional[int] = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        Fetches a list of online users in the current or specified community.

        :param start: The starting point to fetch users from. Defaults to `0`.
        :type start: Optional[int]
        :param size: The amount of users to fetch. Defaults to `25`.
        :type size: Optional[int]
        :param comId: The ID of the community to fetch the users from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `UserProfileList` object containing information about the online users.
        :rtype: UserProfileList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of online users.

        `UserProfileList`:

        - `status`: The status of the request.
        - `mood_sticker`: The mood sticker the user has set.
        - `wiki_count`: The number of wikis the user has created.
        - `consecutive_check_in_days`: The number of consecutive days the user has checked in.
        - `uid`: The user ID of the user.
        - `modified_time`: The time the user profile was last modified.
        - `following_status`: The following status of the user.
        - `online_status`: The online status of the user.
        - `account_membership_status`: The account membership status of the user.
        - `is_global`: Whether the user is a global user.
        - `avatar_frame_id`: The avatar frame ID of the user.
        - `reputation`: The reputation of the user.
        - `posts_count`: The number of posts the user has created.
        - `avatar_frame`: The avatar frame of the user.
        - `members_count`: The number of members the user has.
        - `nickname`: The nickname of the user.
        - `media_list`: The media list of the user.
        - `icon`: The icon of the user.
        - `is_nickname_verified`: Whether the user's nickname is verified.
        - `mood`: The mood of the user.
        - `level`: The level of the user.
        - `notification_subscription_status`: The notification subscription status of the user.
        - `settings`: The settings of the user.
        - `push_enabled`: Whether push is enabled for the user.
        - `membership_status`: The membership status of the user.
        - `influencer_info`: The influencer info of the user.
        - `content`: The user's profile content.
        - `follower_count`: The number of followers the user has.
        - `role`: The role of the user.
        - `comments_count`: The number of comments the user has on their wall.
        - `ndc_id`: The ID of the community the user is in.
        - `created_time`: The time the user was created.
        - `extensions`: The extensions of the user.
        - `stories_count`: The number of stories the user has created.
        - `blogs_count`: The number of blogs the user has created.

        **Example usage:**

        >>> online_users = client.community.fetch_online_users()
        >>> print(online_users[0].nickname) # Prints the nickname of the first user in the list.
        'John Doe'
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/live-layer?topic=ndtopic:x{self.community_id if comId is None else comId}:online-members&start={start}&size={size}"
            ))

    @community
    def fetch_followers(self, userId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        Fetches a list of followers for a specified user in the current or specified community.

        :param userId: The ID of the user to fetch the followers for.
        :type userId: str
        :param start: The starting point to fetch users from. Defaults to `0`.
        :type start: int
        :param size: The amount of users to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the users from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `UserProfileList` object containing information about the followers.
        :rtype: UserProfileList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of followers for the specified user.

        `UserProfileList`:

        - `status`: The status of the request.
        - `mood_sticker`: The mood sticker the user has set.
        - `wiki_count`: The number of wikis the user has created.
        - `consecutive_check_in_days`: The number of consecutive days the user has checked in.
        - `uid`: The user ID of the user.
        - `modified_time`: The time the user profile was last modified.
        - `following_status`: The following status of the user.
        - `online_status`: The online status of the user.
        - `account_membership_status`: The account membership status of the user.
        - `is_global`: Whether the user is a global user.
        - `avatar_frame_id`: The avatar frame ID of the user.
        - `reputation`: The reputation of the user.
        - `posts_count`: The number of posts the user has created.
        - `avatar_frame`: The avatar frame of the user.
        - `members_count`: The number of members the user has.
        - `nickname`: The nickname of the user.
        - `media_list`: The media list of the user.
        - `icon`: The icon of the user.
        - `is_nickname_verified`: Whether the user's nickname is verified.
        - `mood`: The mood of the user.
        - `level`: The level of the user.
        - `notification_subscription_status`: The notification subscription status of the user.
        - `settings`: The settings of the user.
        - `push_enabled`: Whether push is enabled for the user.
        - `membership_status`: The membership status of the user.
        - `influencer_info`: The influencer info of the user.
        - `content`: The user's profile content.
        - `follower_count`: The number of followers the user has.
        - `role`: The role of the user.
        - `comments_count`: The number of comments the user has on their wall.
        - `ndc_id`: The ID of the community the user is in.
        - `created_time`: The time the user was created.
        - `extensions`: The extensions of the user.
        - `stories_count`: The number of stories the user has created.
        - `blogs_count`: The number of blogs the user has created.

        **Example usage:**

        >>> followers = client.community.fetch_followers(userId = "0000-000000-000000-0000")
        >>> print(followers[0].nickname) # Prints the nickname of the first user in the list.
        'John Doe'
        >>> print(followers.uid) # Prints all the user IDs in the list.
        ['0000-000000-000000-0000', '0000-000000-000000-0001', '0000-000000-000000-0002']
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/member?start={start}&size={size}"
            ))

    @community
    def fetch_following(self, userId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> UserProfileList:
        """
        Fetches a list of users that the specified user is following in the current or specified community.

        :param userId: The ID of the user to fetch the following users for.
        :type userId: str
        :param start: The starting point to fetch users from. Defaults to `0`.
        :type start: int
        :param size: The amount of users to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the users from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `UserProfileList` object containing information about the following users.
        :rtype: UserProfileList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of users that the specified user is following.

        `UserProfileList`:

        - `status`: The status of the request.
        - `mood_sticker`: The mood sticker the user has set.
        - `wiki_count`: The number of wikis the user has created.
        - `consecutive_check_in_days`: The number of consecutive days the user has checked in.
        - `uid`: The user ID of the user.
        - `modified_time`: The time the user profile was last modified.
        - `following_status`: The following status of the user.
        - `online_status`: The online status of the user.
        - `account_membership_status`: The account membership status of the user.
        - `is_global`: Whether the user is a global user.
        - `avatar_frame_id`: The avatar frame ID of the user.
        - `reputation`: The reputation of the user.
        - `posts_count`: The number of posts the user has created.
        - `avatar_frame`: The avatar frame of the user.
        - `members_count`: The number of members the user has.
        - `nickname`: The nickname of the user.
        - `media_list`: The media list of the user.
        - `icon`: The icon of the user.
        - `is_nickname_verified`: Whether the user's nickname is verified.
        - `mood`: The mood of the user.
        - `level`: The level of the user.
        - `notification_subscription_status`: The notification subscription status of the user.
        - `settings`: The settings of the user.
        - `push_enabled`: Whether push is enabled for the user.
        - `membership_status`: The membership status of the user.
        - `influencer_info`: The influencer info of the user.
        - `content`: The user's profile content.
        - `follower_count`: The number of followers the user has.
        - `role`: The role of the user.
        - `comments_count`: The number of comments the user has on their wall.
        - `ndc_id`: The ID of the community the user is in.
        - `created_time`: The time the user was created.
        - `extensions`: The extensions of the user.
        - `stories_count`: The number of stories the user has created.
        - `blogs_count`: The number of blogs the user has created.

        **Example usage:**

        >>> following = client.community.fetch_following(userId = "0000-000000-000000-0000")
        >>> print(following[0].nickname) # Prints the nickname of the first user in the list.
        'John Doe'
        >>> print(following.uid) # Prints all the user IDs in the list.
        ['0000-000000-000000-0000', '0000-000000-000000-0001', '0000-000000-000000-0002']
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/joined?start={start}&size={size}"
            ))

    @community
    def fetch_chat(self, chatId: str, comId: Union[str, int] = None) -> CThread:
        """
        Fetches the chat thread with the specified ID in the current or specified community.

        :param chatId: The ID of the chat thread to fetch.
        :type chatId: str
        :param comId: The ID of the community to fetch the chat thread from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CThread` object containing information about the chat thread.
        :rtype: CThread

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch the chat thread with the specified ID.

        `CThread`:

        - `data`: The raw data of the chat thread.
        - `userAddedTopicList`: A list of topics added by the user.
        - `uid`: The user ID of the thread creator.
        - `hostUserId`: An alias for `uid`.
        - `membersQuota`: The maximum number of members allowed in the chat thread.
        - `membersSummary`: A `MemberSummary` object containing information about the chat thread's members.
        - `threadId`: The ID of the chat thread.
        - `chatId`: An alias for `threadId`.
        - `keywords`: A list of keywords associated with the chat thread.
        - `membersCount`: The number of members currently in the chat thread.
        - `strategyInfo`: The strategy information for the chat thread.
        - `isPinned`: Whether the chat thread is pinned.
        - `title`: The title of the chat thread.
        - `membershipStatus`: The membership status of the user in the chat thread.
        - `content`: The content of the chat thread.
        - `needHidden`: Whether the chat thread needs to be hidden.
        - `alertOption`: The alert option for the chat thread.
        - `lastReadTime`: The last time the chat thread was read.
        - `type`: The type of the chat thread.
        - `status`: The status of the chat thread.
        - `publishToGlobal`: Whether the chat thread is published to the global chat.
        - `modifiedTime`: The time the chat thread was last modified.
        - `lastMessageSummary`: The summary of the last message in the chat thread.
        - `extensions`: The extensions of the chat thread.

        **Example usage:**

        >>> chat_thread = client.community.fetch_chat("0000-000000-000000-0000")
        >>> print(chat_thread.title) # Prints the title of the chat thread.
        'My Chat Thread'
        """
        return CThread(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}"
            ))

    
    @community
    def fetch_chat_mods(self, chatId: str, comId: Union[str, int] = None, moderators: Optional[str] = "all") -> List[str]:
        """
        Fetches a list of moderators for a specified chat thread in the current or specified community.

        :param chatId: The ID of the chat to fetch the moderators for.
        :type chatId: str
        :param comId: The ID of the community that the chat belongs to. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :param moderators: The type of moderators to fetch. Defaults to "all".
            - "all": Returns all moderators of the chat.
            - "co-hosts": Returns only the co-hosts of the chat.
            - "host": Returns only the host of the chat.
        :type moderators: Optional[str]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A list of moderator user IDs.
        :rtype: List[str]
        """
        response: CThread = self.fetch_chat(chatId=chatId, comId=comId)

        return {
            "all": list(response.extensions.coHost) + [response.hostUserId],
            "co-hosts": list(response.extensions.coHost),
            "host": [response.hostUserId]
            }.get(moderators, "all")


    @community
    def fetch_chat_moderators(self, chatId: str, comId: Union[str, int] = None) -> List[str]:
        """
        Fetches a list of all moderators for a specified chat thread in the current or specified community.

        :param chatId: The ID of the chat to fetch the moderators for.
        :type chatId: str
        :param comId: The ID of the community that the chat belongs to. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A list of moderator user IDs.
        :rtype: List[str]
        """
        return self.fetch_chat_mods(chatId=chatId, comId=comId, moderators="all")


    @community
    def fetch_chat_co_hosts(self, chatId: str, comId: Union[str, int] = None) -> List[str]:
        """
        Fetches a list of co-hosts for a specified chat thread in the current or specified community.

        :param chatId: The ID of the chat to fetch the co-hosts for.
        :type chatId: str
        :param comId: The ID of the community that the chat belongs to. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A list of co-host user IDs.
        :rtype: List[str]
        """
        return self.fetch_chat_mods(chatId=chatId, comId=comId, moderators="co-hosts")


    @community
    def fetch_chat_host(self, chatId: str, comId: Union[str, int] = None) -> str:
        """
        Fetches the host of a specified chat thread in the current or specified community.

        :param chatId: The ID of the chat to fetch the host for.
        :type chatId: str
        :param comId: The ID of the community that the chat belongs to. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: The user ID of the chat host.
        :rtype: str
        """
        return self.fetch_chat_mods(chatId=chatId, comId=comId, moderators="host")[0]


    @community
    def fetch_chats(self, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CThreadList:
        """
        Fetches a list of chat threads in the current or specified community that the user has joined.

        :param start: The starting point to fetch chat threads from. Defaults to `0`.
        :type start: int
        :param size: The amount of chat threads to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the chat threads from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CThreadList` object containing information about the chat threads.
        :rtype: CThreadList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of chat threads that the user has joined.

        `CThreadList`:

        - `data`: The raw data of the chat thread list.
        - `extensions`: The extensions of the chat threads in the list.
        - `membersSummary`: The member summary of the chat threads in the list.
        - `userAddedTopicList`: A list of topics added by the user in the chat threads in the list.
        - `uid`: A list of user IDs of the thread creators in the chat threads in the list.
        - `hostUserId`: An alias for `uid`.
        - `membersQuota`: A list of maximum member counts allowed in the chat threads in the list.
        - `threadId`: A list of thread IDs of the chat threads in the list.
        - `chatId`: An alias for `threadId`.
        - `keywords`: A list of keywords associated with the chat threads in the list.
        - `membersCount`: A list of the number of members in the chat threads in the list.
        - `strategyInfo`: The strategy information for the chat threads in the list.
        - `isPinned`: A list of whether the chat threads in the list are pinned.
        - `title`: A list of the titles of the chat threads in the list.
        - `membershipStatus`: A list of the user's membership status in the chat threads in the list.
        - `content`: A list of the contents of the chat threads in the list.
        - `needHidden`: A list of whether the chat threads in the list need to be hidden.
        - `alertOption`: A list of the alert options for the chat threads in the list.
        - `lastReadTime`: A list of the last times the chat threads in the list were read.
        - `type`: A list of the types of the chat threads in the list.
        - `status`: A list of the statuses of the chat threads in the list.
        - `publishToGlobal`: A list of whether the chat threads in the list are published to the global chat.
        - `modifiedTime`: A list of the times the chat threads in the list were last modified.
        - `lastMessageSummary`: A list of the summaries of the last messages in the chat threads in the list.

        **Example usage:**

        >>> chat_threads = client.community.fetch_chats()
        >>> chat_thread_titles = chat_threads.title
        METHOD 1:
        >>> print(chat_thread_titles)
        ['My Chat Thread', 'My Other Chat Thread']
        METHOD 2:
        >>> for chat_thread in chat_threads:
        ...     print(chat_thread.title)
        'My Chat Thread'
        'My Other Chat Thread'
        """
        return CThreadList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread?type=joined-me&start={start}&size={size}"
            ))


    @community
    def fetch_live_chats(self, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CThreadList:
        """
        Fetches a list of live chat threads in the current or specified community that are publicly visible.

        :param start: The starting point to fetch chat threads from. Defaults to `0`.
        :type start: int
        :param size: The amount of chat threads to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the chat threads from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CThreadList` object containing information about the live chat threads.
        :rtype: CThreadList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of publicly visible live chat threads.

        `CThreadList`:

        - `data`: The raw data of the live chat thread list.
        - `extensions`: The extensions of the live chat threads in the list.
        - `membersSummary`: The member summary of the live chat threads in the list.
        - `userAddedTopicList`: A list of topics added by the user in the live chat threads in the list.
        - `uid`: A list of user IDs of the thread creators in the live chat threads in the list.
        - `hostUserId`: An alias for `uid`.
        - `membersQuota`: A list of maximum member counts allowed in the live chat threads in the list.
        - `threadId`: A list of thread IDs of the live chat threads in the list.
        - `chatId`: An alias for `threadId`.
        - `keywords`: A list of keywords associated with the live chat threads in the list.
        - `membersCount`: A list of the number of members in the live chat threads in the list.
        - `strategyInfo`: The strategy information for the live chat threads in the list.
        - `isPinned`: A list of whether the live chat threads in the list are pinned.
        - `title`: A list of the titles of the live chat threads in the list.
        - `membershipStatus`: A list of the user's membership status in the live chat threads in the list.
        - `content`: A list of the contents of the live chat threads in the list.
        - `needHidden`: A list of whether the live chat threads in the list need to be hidden.
        - `alertOption`: A list of the alert options for the live chat threads in the list.
        - `lastReadTime`: A list of the last times the live chat threads in the list were read.
        - `type`: A list of the types of the live chat threads in the list.
        - `status`: A list of the statuses of the live chat threads in the list.
        - `publishToGlobal`: A list of whether the live chat threads in the list are published to the global chat.
        - `modifiedTime`: A list of the times the live chat threads in the list were last modified.
        - `lastMessageSummary`: A list of the summaries of the last messages in the live chat threads in the list.

        **Example usage:**

        >>> live_chat_threads = client.community.fetch_live_chats()
        >>> live_chat_titles = live_chat_threads.title
        METHOD 1:
        >>> print(live_chat_titles)
        ['My Live Chat Thread', 'My Other Live Chat Thread']
        METHOD 2:
        >>> for title in live_chat_titles:
        ...     print(title) # Prints the title of each live chat thread.
        'My Live Chat Thread'
        'My Other Live Chat Thread'
        """
        return CThreadList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/live-layer/public-live-chats?start={start}&size={size}"
            ))


    @community
    def fetch_public_chats(
        self,
        chatType: ChatTypes = ChatTypes.RECOMMENDED,
        start: int = 0,
        size: int = 25,
        comId: Union[str, int] = None,
        **kwargs
        ) -> CThreadList:
        """
        Fetches a list of public chat threads in the current or specified community.

        :param chatType: The type of public chat threads to fetch. Defaults to `ChatTypes.RECOMMENDED`.
        :type chatType: ChatTypes
        :param start: The starting point to fetch chat threads from. Defaults to `0`.
        :type start: int
        :param size: The amount of chat threads to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the chat threads from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CThreadList` object containing information about the public chat threads.
        :rtype: CThreadList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of public chat threads of the specified type.

        `ChatTypes`:

        - `RECOMMENDED`: Fetches a list of recommended public chat threads.
        - `POPULAR`: Fetches a list of popular public chat threads.
        - `LATEST`: Fetches a list of newest public chat threads.

        `CThreadList`:

        - `data`: The raw data of the public chat thread list.
        - `extensions`: The extensions of the public chat threads in the list.
        - `membersSummary`: The member summary of the public chat threads in the list.
        - `userAddedTopicList`: A list of topics added by the user in the public chat threads in the list.
        - `uid`: A list of user IDs of the thread creators in the public chat threads in the list.
        - `hostUserId`: An alias for `uid`.
        - `membersQuota`: A list of maximum member counts allowed in the public chat threads in the list.
        - `threadId`: A list of thread IDs of the public chat threads in the list.
        - `chatId`: An alias for `threadId`.
        - `keywords`: A list of keywords associated with the public chat threads in the list.
        - `membersCount`: A list of the number of members in the public chat threads in the list.
        - `strategyInfo`: The strategy information for the public chat threads in the list.
        - `isPinned`: A list of whether the public chat threads in the list are pinned.
        - `title`: A list of the titles of the public chat threads in the list.
        - `membershipStatus`: A list of the user's membership status in the public chat threads in the list.
        - `content`: A list of the contents of the public chat threads in the list.
        - `needHidden`: A list of whether the public chat threads in the list need to be hidden.
        - `alertOption`: A list of the alert options for the public chat threads in the list.
        - `lastReadTime`: A list of the last times the public chat threads in the list were read.
        - `type`: A list of the types of the public chat threads in the list.
        - `status`: A list of the statuses of the public chat threads in the list.
        - `publishToGlobal`: A list of whether the public chat threads in the list are published to the global chat.
        - `modifiedTime`: A list of the times the public chat threads in the list were last modified
        - `lastMessageSummary`: A list of the summaries of the last messages in the public chat threads in the list.

        **Example usage:**

        >>> public_chat_threads = client.community.fetch_public_chats()
        >>> public_chat_titles = public_chat_threads.title
        METHOD 1:
        >>> print(public_chat_titles)
        ['My Public Chat Thread', 'My Other Public Chat Thread']
        METHOD 2:
        >>> for title in public_chat_titles:
        ...     print(title) # Prints the title of each public chat thread.
        'My Public Chat Thread'
        'My Other Public Chat Thread'
        """
        if "type" in kwargs: #TODO Remove this in the near future.
            chatType = kwargs["type"]
            print("WARNING: The `type` parameter is deprecated. Please use `chatType` instead.")

        return CThreadList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread?type=public-all&filterType={chatType.value if isinstance(chatType, ChatTypes) else chatType}&start={start}&size={size}"
            ))


    @community
    def fetch_chat_members(self, chatId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CChatMembers:
        """
        Fetches a list of members in the specified chat thread in the current or specified community.

        :param chatId: The ID of the chat thread to fetch the members from.
        :type chatId: str
        :param start: The starting point to fetch members from. Defaults to `0`.
        :type start: int
        :param size: The amount of members to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the chat thread from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CChatMembers` object containing information about the chat thread members.
        :rtype: CChatMembers

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of members in the specified chat thread.

        `CChatMembers`:

        - `data`: The raw data of the chat thread members.
        - `members`: A list of `UserProfile` objects representing the members.

        `UserProfile`:

        - `status`: The user's status.
        - `mood_sticker`: The user's mood sticker.
        - `wiki_count`: The number of wikis the user has created.
        - `consecutive_check_in_days`: The number of consecutive days the user has checked in.
        - `uid`: The user's ID.
        - `userId`: An alias for `uid`.
        - `modified_time`: The time the user's profile was last modified.
        - `following_status`: The user's following status.
        - `online_status`: The user's online status.
        - `account_membership_status`: The user's account membership status.
        - `is_global`: Whether the user is a global user.
        - `avatar_frame_id`: The ID of the user's avatar frame.
        - `fan_club_list`: The user's fan clubs.
        - `reputation`: The user's reputation.
        - `posts_count`: The number of posts the user has made.
        - `follower_count`: The number of followers the user has.
        - `nickname`: The user's nickname.
        - `username`: An alias for `nickname`.
        - `media_list`: The user's media list.
        - `icon`: The user's icon.
        - `avatar`: An alias for `icon`.
        - `is_nickname_verified`: Whether the user's nickname is verified.
        - `mood`: The user's mood.
        - `level`: The user's level.
        - `pushEnabled`: Whether the user has push notifications enabled.
        - `membership_status`: The user's membership status in the community.
        - `content`: The user's profile content.
        - `following_count`: The number of users the user is following.
        - `role`: The user's role in the community.
        - `comments_count`: The number of comments the user has made.
        - `ndcId`: The ID of the community the user belongs to.
        - `comId`: An alias for `ndcId`.
        - `created_time`: The time the user's profile was created.
        - `visit_privacy`: The user's visit privacy.
        - `stories_count`: The number of stories the user has created.
        - `blogs_count`: The number of blogs the user has created.

        **Example usage:**

        >>> chat_members = client.community.fetch_chat_members("0000-000000-000000-0000")
        >>> chat_member_usernames = chat_members.members.usernames
        METHOD 1:
        >>> print(chat_member_usernames)
        ['My Username', 'My Other Username']
        METHOD 2:
        >>> for username in chat_member_usernames:
        ...     print(username) # Prints the usernames of each chat member.
        'My Username'
        'My Other Username'
        """
        return CChatMembers(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2"
            ))


    @community
    def fetch_messages(self, chatId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> CMessages:
        """
        Fetches a list of messages in a chat thread with the specified `chatId`.

        :param chatId: The ID of the chat thread to fetch the messages from.
        :type chatId: str
        :param start: The starting point to fetch messages from. Defaults to `0`.
        :type start: int
        :param size: The amount of messages to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the chat thread from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CMessages` object containing information about the chat thread's messages.
        :rtype: CMessages

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of messages in the specified chat thread.

        `CMessages`:

        - `includedInSummary`: A list of booleans indicating whether each message is included in the summary.
        - `uid`: A list of user IDs of the authors of each message.
        - `userId`: An alias for `uid`.
        - `author`: A `CMessageAuthorList` object containing information about the authors of each message.
        - `isHidden`: A list of booleans indicating whether each message is hidden.
        - `messageId`: A list of message IDs of each message.
        - `mediaType`: A list of media types of each message.
        - `content`: A list of contents of each message.
        - `clientRefId`: A list of client reference IDs of each message.
        - `threadId`: A list of thread IDs of each message.
        - `chatId`: An alias for `threadId`.
        - `createdTime`: A list of creation times of each message.
        - `extensions`: A list of extensions of each message.
        - `type`: A list of types of each message.
        - `mediaValue`: A list of media values of each message.

        **Example usage:**

        >>> messages = client.community.fetch_messages(chatId="0000-00000-000000-0000")
        >>> message_content = messages.content
        METHOD 1:
        >>> print(message_content)
        ['Hello, World!', 'How are you?', "I'm doing well, thanks!"]
        METHOD 2:
        >>> for message in message_content:
        ...     print(message) # Prints the content of each message in the chat thread.
        'Hello, World!'
        'How are you?'
        'I'm doing well, thanks!'
        """
        return CMessages(self.session.handler(
            method="GET",
            url=f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message?start={start}&size={size}&type=default"
        ))


    @community
    def fetch_blogs(self, size: int = 25, comId: Union[str, int] = None) -> CBlogList:
        """
        Fetches a list of blogs from the community with the specified `comId`.

        :param size: The number of blogs to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the blogs from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `CBlogList` object containing information about the blogs.
        :rtype: CBlogList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of blogs from the specified community.

        `CBlogList`:

        - `author`: A `UserProfileList` object containing information about the authors of each blog.
        - `globalVotesCount`: A list of global vote counts of each blog.
        - `globalVotedValue`: A list of global vote values of each blog.
        - `votedValue`: A list of vote values of each blog.
        - `keywords`: A list of keywords of each blog.
        - `mediaList`: A list of media objects of each blog.
        - `style`: A list of styles of each blog.
        - `totalQuizPlayCount`: A list of total quiz play counts of each blog.
        - `title`: A list of titles of each blog.
        - `tipInfo`: A list of tip information of each blog.
        - `contentRating`: A list of content ratings of each blog.
        - `content`: A list of contents of each blog.
        - `needHidden`: A list of hidden status of each blog.
        - `guestVotesCount`: A list of guest vote counts of each blog.
        - `type`: A list of types of each blog.
        - `status`: A list of statuses of each blog.
        - `globalCommentsCount`: A list of global comment counts of each blog.
        - `modifiedTime`: A list of modification times of each blog.
        - `widgetDisplayInterval`: A list of widget display intervals of each blog.
        - `totalPollVoteCount`: A list of total poll vote counts of each blog.
        - `blogId`: A list of blog IDs of each blog.
        - `viewCount`: A list of view counts of each blog.
        - `language`: A list of languages of each blog.
        - `extensions`: A list of extensions of each blog.
        - `votesCount`: A list of vote counts of each blog.
        - `ndcId`: A list of NDC IDs of each blog.
        - `createdTime`: A list of creation times of each blog.
        - `endTime`: A list of end times of each blog.
        - `commentsCount`: A list of comment counts of each blog.

        **Example usage:**

        >>> blogs = client.community.fetch_blogs(size=10)
        EXAMPLE 1:
        >>> print(blogs.content)
        ['My first blog post', 'The importance of exercise', 'How to learn a new language', ...]
        EXAMPLE 2:
        >>> for blog in blogs.content:
        ...     print(blog.title) # Prints the title of each blog in the list.
        'My first blog post'
        'The importance of exercise'
        'How to learn a new language'
        ...
        """
        return CBlogList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/feed/blog-all?pagingType=t&size={size}"
            ))
    
    @community
    def fetch_featured_blogs(self, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> FeaturedBlogs:
        """
        Fetches a list of featured blog posts.

        :param start: The starting index of the list. Defaults to `0`.
        :type start: int
        :param size: The number of blog posts to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the featured blog posts from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises NotLoggedIn: If the user is not logged in.
        :return: A `FeaturedBlogs` object containing information about the featured blog posts.
        :rtype: FeaturedBlogs

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch a list of featured blog posts in the specified community.

        `FeaturedBlogs`:

        - `ref_object_type`: A list of reference object types of each featured blog post.
        - `ref_object_id`: A list of reference object IDs of each featured blog post.
        - `expired_time`: A list of expiration times of each featured blog post.
        - `featured_type`: A list of featured types of each featured blog post.
        - `created_time`: A list of creation times of each featured blog post.
        - `ref_object`: A list of reference objects of each featured blog post.
        - `global_votes_count`: A list of global vote counts of each featured blog post.
        - `global_voted_count`: A list of global voted counts of each featured blog post.
        - `voted_value`: A list of voted values of each featured blog post.
        - `keywords`: A list of keywords of each featured blog post.
        - `strategy_info`: A list of strategy information of each featured blog post.
        - `media_list`: A list of media lists of each featured blog post.
        - `style`: A list of styles of each featured blog post.
        - `total_quiz_play_count`: A list of total quiz play counts of each featured blog post.
        - `title`: A list of titles of each featured blog post.
        - `tip_info`: A list of tip information of each featured blog post.
        - `content`: A list of contents of each featured blog post.
        - `content_rating`: A list of content ratings of each featured blog post.
        - `need_hidden`: A list of boolean values indicating whether each featured blog post needs to be hidden.
        - `guest_votes_count`: A list of guest vote counts of each featured blog post.
        - `global_comments_count`: A list of global comment counts of each featured blog post.
        - `modified_time`: A list of modification times of each featured blog post.
        - `widget_display_interval`: A list of widget display intervals of each featured blog post.
        - `total_poll_vote_count`: A list of total poll vote counts of each featured blog post.
        - `blogId`: A list of blog IDs of each featured blog post.
        - `view_count`: A list of view counts of each featured blog post.
        - `author`: A `UserProfileList` object containing information about the authors of each featured blog post.

        **Example usage:**

        >>> featured_blogs = client.community.fetch_featured_blogs(start=0, size=10)
        EXAMPLE 1:
        >>> print(featured_blogs.content)
        ['My first blog post', 'The importance of exercise', 'How to learn a new language', ...]
        EXAMPLE 2:
        >>> for blog in featured_blogs.content:
        ...     print(blog.title)
        'My first blog post'
        'The importance of exercise'
        'How to learn a new language'
        ...
        """
        return FeaturedBlogs(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/feed/featured?start={start}&size={size}"
            ))

    @community
    def fetch_leaderboard(
        self,
        leaderboardType: LeaderboardTypes = LeaderboardTypes.HALL_OF_FAME,
        start: int = 0,
        size: int = 20,
        comId: Union[str, int] = None
        ) -> UserProfileList:
        """
        Fetches the leaderboard for the current community, based on the specified `leaderboardType`.

        :param leaderboardType: The type of leaderboard to fetch. Defaults to `LeaderboardTypes.HALL_OF_FAME`.
        :type leaderboardType: LeaderboardTypes
        :param start: The starting index of the leaderboard to fetch. Defaults to `0`.
        :type start: int
        :param size: The number of users to fetch from the leaderboard. Defaults to `20`.
        :type size: int
        :param comId: The ID of the community to fetch the leaderboard from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `UserProfileList` object containing information about the users in the leaderboard.
        :rtype: UserProfileList
        :raises NotLoggedIn: If the user is not logged in.

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch the leaderboard for the specified community.

        `UserProfileList`:

        - `status`: A list of status of each user in the leaderboard.
        - `mood_sticker`: A list of mood stickers of each user in the leaderboard.
        - `wiki_count`: A list of the wiki count of each user in the leaderboard.
        - `consecutive_check_in_days`: A list of the consecutive check-in days of each user in the leaderboard.
        - `uid`: A list of the user IDs of each user in the leaderboard.
        - `userId`: An alias for `uid`.
        - `modified_time`: A list of the last modified time of each user in the leaderboard.
        - `following_status`: A list of the following status of each user in the leaderboard.
        - `online_status`: A list of the online status of each user in the leaderboard.
        - `account_membership_status`: A list of the account membership status of each user in the leaderboard.
        - `is_global`: A list of booleans indicating whether each user in the leaderboard is global.
        - `avatar_frame_id`: A list of the avatar frame IDs of each user in the leaderboard.
        - `fan_club_list`: A list of fan club lists of each user in the leaderboard.
        - `reputation`: A list of the reputation of each user in the leaderboard.
        - `posts_count`: A list of the number of posts of each user in the leaderboard.
        - `follower_count`: A list of the number of followers of each user in the leaderboard.
        - `nickname`: A list of the nicknames of each user in the leaderboard.
        - `username`: An alias for `nickname`.
        - `media_list`: A list of media lists of each user in the leaderboard.
        - `icon`: A list of icons of each user in the leaderboard.
        - `avatar`: An alias for `icon`.
        - `is_nickname_verified`: A list of booleans indicating whether each user in the leaderboard has a verified nickname.
        - `mood`: A list of moods of each user in the leaderboard.
        - `level`: A list of the levels of each user in the leaderboard.
        - `pushEnabled`: A list of booleans indicating whether push notifications are enabled for each user
        - `membership_status`: A list of the membership status of each user in the leaderboard.
        - `influencer_info`: A list of influencer information of each user in the leaderboard.
        - `content`: A list of contents of each user in the leaderboard.
        - `following_count`: A list of the number of users each user in the leaderboard is following.
        - `role`: A list of the roles of each user in the leaderboard.
        - `comments_count`: A list of the number of comments of each user in the leaderboard.
        - `ndcId`: A list of the NDC IDs of each user in the leaderboard.
        - `comId`: An alias for `ndcId`.
        - `created_time`: A list of the creation times of each user in the leaderboard.
        - `extensions`: A list of extensions of each user in the leaderboard.
        - `visit_privacy`: A list of the visit privacy of each user in the leaderboard.
        - `stories_count`: A list of the number of stories of each user in the leaderboard.
        - `blogs_count`: A list of the number of blogs of each user in the leaderboard.

        **Example usage:**

        >>> leaderboard = client.community.fetch_leaderboard(leaderboardType=LeaderboardTypes.HALL_OF_FAME, start=0, size=10)
        EXAMPLE 1:
        >>> print(leaderboard.content) # Print a list of hall of fame users's bio content.
        ['Been on this app since day 1', 'Top of the leaderboard!', ...]
        EXAMPLE 2:
        >>> for user in leaderboard.nickname:
        ...     print(user)
        'John Doe'
        'Jane Doe'
        ...
        """
        return UserProfileList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/community/leaderboard?rankingType={leaderboardType.value if isinstance(leaderboardType, LeaderboardTypes) else leaderboardType}&start={start}&size={size}"
            ))

    @community
    def fetch_comments(
        self,
        userId: Optional[str] = None,
        blogId: Optional[str] = None,
        wikiId: Optional[str] = None,
        start: int = 0,
        size: int = 25,
        comId: Union[str, int] = None) -> CCommentList:
        """
        Fetches the comments for the specified user, blog, or wiki.

        :param userId: The ID of the user whose comments to fetch. Defaults to `None`.
        :type userId: Optional[str]
        :param blogId: The ID of the blog whose comments to fetch. Defaults to `None`.
        :type blogId: Optional[str]
        :param wikiId: The ID of the wiki whose comments to fetch. Defaults to `None`.
        :type wikiId: Optional[str]
        :param start: The starting index of the comments to fetch. Defaults to `0`.
        :type start: int
        :param size: The number of comments to fetch. Defaults to `25`.
        :type size: int
        :param comId: The ID of the community to fetch the comments from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CCommentList` object containing the comments for the specified user, blog, or wiki.
        :rtype: CCommentList
        :raises NoDataProvided: If none of `userId`, `blogId`, or `wikiId` is provided.

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a GET request to the API to fetch the comments for the specified user, blog, or wiki.

        `CCommentList`:

        - `modifiedTime`: A list of the last modified time of each comment.
        - `ndcId`: A list of the NDC IDs of each comment.
        - `votedValue`: A list of the voted value of each comment.
        - `parentType`: A list of the parent types of each comment.
        - `commentId`: A list of the IDs of each comment.
        - `parentNdcId`: A list of the parent NDC IDs of each comment.
        - `mediaList`: A list of media lists of each comment.
        - `votesSum`: A list of the votes sum of each comment.
        - `content`: A list of the contents of each comment.
        - `parentId`: A list of the parent IDs of each comment.
        - `createdTime`: A list of the creation times of each comment.
        - `subcommentsCount`: A list of the number of subcomments of each comment.
        - `type`: A list of the types of each comment.

        **Example usage:**

        To fetch the comments for a user with ID "0000-0000-0000-0000":

        >>> comments = client.community.fetch_comments(userId="0000-0000-0000-0000")
        EXAMPLE 1:
        >>> print(comments.content) # Print a list of the contents of the comments.
        ['This is a comment!', 'This is another comment!', ...]
        EXAMPLE 2:
        >>> for comment in comments.content:
        ...     print(comment)
        'This is a comment!'
        'This is another comment!'
        ...
        """
        if any([userId, blogId, wikiId]):
            for key, value in {
                "userId": "user-profile/{}",
                "blogId": "blog/{}",
                "wikiId": "item/{}"
            }.items():
                if locals()[key]:
                    return CCommentList(
                        self.session.handler(
                            method="GET",
                            url=f"/x{self.community_id if comId is None else comId}/s/{value.format(locals()[key])}/comment?sort=newest&start={start}&size={size}",
                        )
                    )

        raise NoDataProvided


    @community
    def set_cohost(self, chatId: str, userIds: Union[str, list], comId: Union[str, int] = None) -> ApiResponse:
        """
        Sets the specified user(s) as co-host(s) for the chat with the given `chatId`.

        :param chatId: The ID of the chat to set the co-host(s) for.
        :type chatId: str
        :param userIds: The ID(s) of the user(s) to set as co-host(s). Can be a single user ID or a list of user IDs.
        :type userIds: Union[str, list]
        :param comId: The ID of the community where the chat exists. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the success or failure of the request.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API to set the specified user(s) as co-host(s) for the chat with the given `chatId`.

        `ApiResponse`:

        The response contains the following attributes:

        - `data`: The raw data of the response.
        - `message`: A string message indicating the status of the response.
        - `statuscode`: An integer status code indicating the success or failure of the request.
        - `duration`: The duration of the response.
        - `timestamp`: The timestamp of the response.
        - `mediaValue`: The media value of the response.

        **Example usage:**

        To set a user with ID "0000-0000-0000-0000" as a co-host for a chat with ID "0101-0101-0101-0101":

        >>> response = client.community.set_cohost(chatId="0101-0101-0101-0101", userIds="0000-0000-0000-0000")
        ... if response.message == "OK":
        ...    print("Successfully set user as co-host!")
        ... else:
        ...    print("Failed to set user as co-host.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/cohost",
            data={"userIds": userIds if isinstance(userIds, list) else [userIds]}
            ))

    @community
    def remove_cohost(self, chatId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Removes a co-host from the specified chat.

        :param chatId: The ID of the chat to remove the co-host from.
        :type chatId: str
        :param userId: The ID of the user to remove as a co-host.
        :type userId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object indicating the success or failure of the request.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a DELETE request to the API to remove the specified user as a co-host of the chat.

        `ApiResponse`:

        - `data`: The raw response data from the API.
        - `message`: A message indicating the success or failure of the request.
        - `statuscode`: The HTTP status code of the response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        - `mediaValue`: The media value of the API response.

        **Example usage:**

        To remove a co-host with ID "0000-0000-0000-0000" from a chat with ID "0101-0101-0101-0101":

        >>> response = client.community.remove_cohost(chatId="0101-0101-0101-0101", userId="0000-0000-0000-0000")
        ... if response.message == "OK":
        ...     print("Successfully removed co-host!")
        ... else:
        ...     print("Failed to remove co-host.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/co-host/{userId}"
            ))


    @community
    def follow(self, userId: Union[str, list], comId: Union[str, int] = None) -> ApiResponse:
        """
        Follows the specified user or users.

        :param userId: The ID or IDs of the user or users to follow. Can be a string or a list of strings.
        :type userId: Union[str, list]
        :param comId: The ID of the community to follow the user or users in. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API to follow the specified user or users.

        `ApiResponse`:

        - `message`: The message returned by the API.
        - `statuscode`: The status code returned by the API.
        - `duration`: The duration of the API call.
        - `timestamp`: The timestamp of the API call.
        - `mediaValue`: The media value returned by the API.

        **Example usage:**

        To follow a user with ID "0000-0000-0000-0000":

        >>> response = client.community.follow(userId="0000-0000-0000-0000")
        ... if response.message == "OK":
        ...     print("Successfully followed user!")
        ... else:
        ...     print("Failed to follow user.")
        """
        return ApiResponse(
            self.session.handler(
                method="POST",
                url=f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/{'member' if isinstance(userId, str) else 'joined'}",
                data={
                    "timestamp": int(time()),
                    "targetUidList": userId
                } if isinstance(userId, list) else None
            )
        )

    @community
    def unfollow(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Unfollows the specified user.
        
        :param userId: The ID of the user to unfollow.
        :type userId: str
        :param comId: The ID of the community to unfollow the user in. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request.
        :rtype: ApiResponse
        
        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        
        The function sends a DELETE request to the API to unfollow the specified user.
        
        `ApiResponse`:
        
        - `message`: The message returned by the API.
        - `statuscode`: The status code returned by the API.
        - `duration`: The duration of the API call.
        - `timestamp`: The timestamp of the API call.
        - `mediaValue`: The media value returned by the API.
        
        **Example usage:**
        
        To unfollow a user with ID "0000-0000-0000-0000":
        
        >>> response = client.community.unfollow(userId="0000-0000-0000-0000")
        ... if response.message == "OK":
        ...     print("Successfully unfollowed user.")
        ... else:
        ...     print("Failed to unfollow user.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/member/{self.userId}"
            ))

    @community
    def block(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Blocks a user from the current community.

        :param userId: The ID of the user to block.
        :type userId: str
        :param comId: The ID of the community to block the user from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object representing the response of the API request.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API to block the specified user from the current community.

        **Example usage:**

        To block a user with ID "0000-0000-0000-0000":

        >>> response = client.community.block(userId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Successfully blocked user.")
        ... else:
        ...     print("Failed to block user.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/block/{userId}"
            ))


    @community
    def unblock(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Unblocks a user from the current community.
        
        :param userId: The ID of the user to unblock.
        :type userId: str
        :param comId: The ID of the community to unblock the user from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object representing the response of the API request.
        :rtype: ApiResponse
        
        The `community` decorator is used to ensure that the user is logged in and the community ID is present.
        
        The function sends a DELETE request to the API to unblock the specified user from the current community.
        
        **Example usage:**
        
        To unblock a user with ID "0000-0000-0000-0000":
        
        >>> response = client.community.unblock(userId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Successfully unblocked user.")
        ... else:
        ...     print("Failed to unblock user.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/block/{userId}"
            ))


    @community
    def post_blog(self, title: str, content: str, comId: Union[str, int] = None) -> CBlog: #TODO: ADD DOCSTRING
        return CBlog(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog",
            data = {
                "content": content,
                "title": title,
                "timestamp": int(time() * 1000)
                }))


    @community
    def delete_blog(self, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes the specified blog.

        :param blogId: The ID of the blog to delete.
        :type blogId: str
        :param comId: The ID of the community to delete the blog from. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the result of the deletion.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a DELETE request to the API to delete the specified blog.

        `ApiResponse`:

        - `message`: A message indicating whether the blog was successfully deleted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        - `mediaValue`: The media value of the deleted blog.

        **Example usage:**

        To delete a blog with ID "0000-0000-0000-0000":

        >>> response = client.community.delete_blog(blogId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Blog deleted successfully!")
        ... else:
        ...     print("Blog deletion failed.")
        """
        return ApiResponse(self.session.handler(
            method="DELETE",
            url=f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}"
            ))


    @community
    def post_wiki(self, title: str, content: str, fansOnly: bool=False, comId: Union[str, int] = None) -> ApiResponse:
        """
        Posts a new wiki article in the specified community.

        :param title: The title of the wiki article.
        :type title: str
        :param content: The content of the wiki article.
        :type content: str
        :param fansOnly: Whether the wiki article should be for fans only. Must be either `True` or `False`.
        :type fansOnly: bool
        :param comId: The ID of the community to post the wiki article in. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object representing the response from the server.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a POST request to the API to post a new wiki article with the specified title, content, and fans-only setting.

        The response from the server is returned as an `ApiResponse` object.
        
        `ApiResponse`:

        - `message`: A message indicating whether the blog was successfully deleted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        - `mediaValue`: The media value of the deleted blog.

        **Example usage:**

        To post a new wiki article with the title "My First Wiki Article" and the content "This is my first wiki article.":

        >>> response = client.community.post_wiki(title="My First Wiki Article", content="This is my first wiki article.")
        ... if response.statuscode == 0:
        ...     print("Wiki article successfully posted!")
        ... else:
        ...     print("Wiki article could not be posted.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/item",
            data = {
            "extensions": {"fansOnly": fansOnly},
            "content": content,
            "latitude": 0,
            "longitude": 0,
            "title": title,
            "type": 0,
            "contentLanguage": "en",
            "eventSource": "GlobalComposeMenu",
            "timestamp": int(time() * 1000),
            }))


    @community
    def delete_wiki(self, wikiId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes a wiki item with the given ID.

        :param wikiId: The ID of the wiki item to delete.
        :type wikiId: str
        :param comId: The ID of the community where the wiki item is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        The function sends a DELETE request to the API to delete the specified wiki item.

        `ApiResponse`:

        - `message`: A message indicating whether the blog was successfully deleted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        - `mediaValue`: The media value of the deleted blog.

        **Example usage:**

        To delete a wiki item with ID "0000-0000-0000-0000":

        >>> response = client.community.delete_wiki(wikiId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Wiki item deleted successfully!")
        ... else:
        ...     print("Failed to delete wiki item.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/item/{wikiId}"
            ))

    @community
    def delete_comment(
        self,
        commentId: str,
        userId: Optional[str] = None,
        blogId: Optional[str] = None,
        wikiId: Optional[str] = None,
        comId: Union[str, int] = None
        ) -> ApiResponse:
        """
        Deletes the comment with the given ID.

        :param commentId: The ID of the comment to delete.
        :type commentId: str
        :param userId: The ID of the user who posted the comment (if applicable). Defaults to `None`.
        :type userId: Optional[str]
        :param blogId: The ID of the blog where the comment is located (if applicable). Defaults to `None`.
        :type blogId: Optional[str]
        :param wikiId: The ID of the wiki where the comment is located (if applicable). Defaults to `None`.
        :type wikiId: Optional[str]
        :param comId: The ID of the community where the comment is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        If any of the optional parameters (`userId`, `blogId`, `wikiId`) is provided, the function sends a DELETE request to the API to delete the comment at the specified location. Otherwise, the comment with the specified ID is deleted from the current community.

        `ApiResponse`:

        - `message`: A message indicating whether the comment was successfully deleted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        - `mediaValue`: The media value of the deleted comment.

        **Example usage:**

        To delete a comment with ID "0000-0000-0000-0000":

        >>> response = client.community.delete_comment(commentId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment deleted successfully!")
        ... else:
        ...     print("Failed to delete comment.")
        """
        if any([userId, blogId, wikiId]):
            endpoint={
                "userId": f"/x3/s/user-profile/{userId}/comment/{commentId}" if userId is not None else None,
                "blogId": f"/x3/s/blog/{blogId}/comment/{commentId}" if blogId is not None else None,
                "wikiId": f"/x3/s/item/{wikiId}/comment/{commentId}" if wikiId is not None else None,
                }
            endpoint = endpoint[next(key for key, value in endpoint.items() if value is not None)]

        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment/{commentId}"

        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = endpoint
            ))
    

    @community
    def delete_wiki_comment(self, commentId: str, wikiId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes a comment on a wiki item with the given comment ID and wiki ID.

        :param commentId: The ID of the comment to delete.
        :type commentId: str
        :param wikiId: The ID of the wiki item where the comment is located.
        :type wikiId: str
        :param comId: The ID of the community where the wiki item is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The function calls the `delete_comment` method with `wikiId` and `comId` parameters specified.

        **Example usage:**

        To delete a comment with ID "0000-0000-0000-0000" on a wiki item with ID "1111-1111-1111-1111":

        >>> response = client.community.delete_wiki_comment(commentId="0000-0000-0000-0000", wikiId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Comment deleted successfully!")
        ... else:
        ...     print("Failed to delete comment.")
        """
        return self.delete_comment(commentId = commentId, wikiId = wikiId, comId = comId)


    def delete_profile_comment(self, commentId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes a comment on a user's profile with the given comment ID and user ID.

        :param commentId: The ID of the comment to delete.
        :type commentId: str
        :param userId: The ID of the user whose profile the comment is on.
        :type userId: str
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The function calls the `delete_comment` method with `userId` and `comId` parameters specified.

        **Example usage:**

        To delete a comment with ID "0000-0000-0000-0000" on a user's profile with ID "1111-1111-1111-1111":

        >>> response = client.community.delete_profile_comment(commentId="0000-0000-0000-0000", userId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Comment deleted successfully!")
        ... else:
        ...     print("Failed to delete comment.")
        """
        return self.delete_comment(commentId, userId=userId, comId=comId)


    @community
    def delete_blog_comment(self, commentId: str, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes a comment from a blog post in the current or specified community.

        :param commentId: The ID of the comment to delete.
        :type commentId: str
        :param blogId: The ID of the blog post where the comment is located.
        :type blogId: str
        :param comId: The ID of the community where the blog post is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a DELETE request to the API to delete a comment from a blog post in the specified community.

        `ApiResponse`:

        - `message` (str): A message indicating whether the comment was successfully deleted.
        - `statuscode` (int): The status code of the API response.
        - `duration` (float): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.
        - `mediaValue` (Any): The media value of the deleted comment. Note: the data type of this field may vary depending on the context of the comment.

        **Example usage:**

        To delete a comment with ID "0000-0000-0000-0000" from a blog post with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.delete_blog_comment(commentId="0000-0000-0000-0000", blogId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Comment deleted successfully!")
        ... else:
        ...     print("Failed to delete comment.")
        """
        return self.delete_comment(commentId, blogId=blogId, comId=comId)


    @community
    def comment(
        self,
        content: str,
        userId: Optional[str] = None,
        blogId: Optional[str] = None,
        wikiId: Optional[str] = None,
        image: Optional[str] = None,
        comId: Union[str, int] = None
        ) -> CComment:
        """
        Creates a comment in the current or specified community, at a given location if provided.

        :param content: The text content of the comment.
        :type content: str
        :param userId: The ID of the user profile where the comment should be posted, if applicable. Defaults to `None`.
        :type userId: Optional[str]
        :param blogId: The ID of the blog where the comment should be posted, if applicable. Defaults to `None`.
        :type blogId: Optional[str]
        :param wikiId: The ID of the wiki where the comment should be posted, if applicable. Defaults to `None`.
        :type wikiId: Optional[str]
        :param image: The image to be attached to the comment, if any. Defaults to `None`.
        :type image: Optional[str]
        :param comId: The ID of the community where the comment should be posted. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CComment` object containing information about the newly created comment.
        :rtype: CComment

        This function sends a POST request to the API to create a comment in the specified location or in the current community.

        `CComment`:

        The `CComment` object represents a comment, and has the following attributes:

        - `modifiedTime` (str or None): The time the comment was last modified, or None if not modified.
        - `ndcId` (int or None): The ndc ID of the comment, or None if not available.
        - `votedValue` (int or None): The vote value of the comment, or None if not available.
        - `parentType` (int or None): The parent type of the comment, or None if not available.
        - `commentId` (str or None): The ID of the comment, or None if not available.
        - `parentNdcId` (int or None): The ndc ID of the comment's parent, or None if not available.
        - `mediaList` (None): The media list of the comment, or None if not available.
        - `votesSum` (int or None): The sum of the votes of the comment, or None if not available.
        - `author` (UserProfile): A `UserProfile` object representing the author of the comment.
        - `extensions` (CCommentExtensions): A `CCommentExtensions` object representing the extensions of the comment.
        - `content` (str or None): The text content of the comment, or None if not available.
        - `parentId` (str or None): The ID of the comment's parent, or None if not available.
        - `createdTime` (str or None): The time the comment was created, or None if not available.
        - `subcommentsCount` (int or None): The count of the subcomments of the comment, or None if not available.
        - `type` (int or None): The type of the comment, or None if not available.

        **Example usage:**

        To post a comment with text "Hello world" on a user profile with ID "0000-0000-0000-0000":

        >>> comment = client.community.comment(content="Hello world", userId="0000-0000-0000-0000")
        ... print(comment.content)
        Hello world
        """
        data = {"timestamp": int(time() * 1000), "content": content}

        if any([userId, blogId, wikiId]):
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }
            base_endpoint = "/x{}/s/{}/comment"
            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]))
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment"

        if image:
            data["mediaList"] = [[100,self.__handle_media__(media=image, media_value=True), None, None, None, None]]

        return CComment(self.session.handler(
            method = "POST",
            url = endpoint,
            data = data
            ))


    @community
    def comment_on_blog(self, content: str, blogId: str, image: Optional[str] = None, comId: Union[str, int] = None) -> CComment:
        """
        Creates a comment in the current or specified community, on a blog post with the given ID.

        :param content: The text content of the comment.
        :type content: str
        :param blogId: The ID of the blog where the comment should be posted.
        :type blogId: str
        :param image: The image to be attached to the comment, if any. Defaults to `None`.
        :type image: Optional[str]
        :param comId: The ID of the community where the comment should be posted. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CComment` object containing information about the newly created comment.
        :rtype: CComment

        This function sends a POST request to the API to create a comment in the specified location or in the current community.

        **Example usage:**

        To post a comment with text "Hello world" on a blog post with ID "0000-0000-0000-0000":

        >>> comment = client.community.comment_on_blog(content="Hello world", blogId="0000-0000-0000-0000")
        ... print(comment.content)
        Hello world
        """
        return self.comment(content = content, blogId = blogId, image = image, comId = comId)


    @community
    def comment_on_wiki(self, content: str, wikiId: str, image: Optional[str] = None, comId: Union[str, int] = None) -> CComment:
        """
        Creates a comment in the current or specified community, on a wiki page with the given ID.
        
        :param content: The text content of the comment.
        :type content: str
        :param wikiId: The ID of the wiki page where the comment should be posted.
        :type wikiId: str
        :param image: The image to be attached to the comment, if any. Defaults to `None`.
        :type image: Optional[str]
        :param comId: The ID of the community where the comment should be posted. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CComment` object containing information about the newly created comment.
        :rtype: CComment
        
        This function sends a POST request to the API to create a comment in the specified location or in the current community.
        
        **Example usage:**
        
        To post a comment with text "Hello world" on a wiki page with ID "0000-0000-0000-0000":

        >>> comment = client.community.comment_on_wiki(content="Hello world", wikiId="0000-0000-0000-0000")
        ... print(comment.content)
        Hello world
        """
        return self.comment(content=content, wikiId=wikiId, image=image, comId=comId)


    @community
    def comment_on_profile(self, content: str, userId: str, image: Optional[str] = None, comId: Union[str, int] = None) -> CComment:
        """
        Creates a comment in the current or specified community, on a user profile with the given ID.
        
        :param content: The text content of the comment.
        :type content: str
        :param userId: The ID of the user profile where the comment should be posted.
        :type userId: str
        :param image: The image to be attached to the comment, if any. Defaults to `None`.
        :type image: Optional[str]
        :param comId: The ID of the community where the comment should be posted. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CComment` object containing information about the newly created comment.
        :rtype: CComment
        
        This function sends a POST request to the API to create a comment in the specified location or in the current community.
        
        **Example usage:**
        
        To post a comment with text "Hello world" on a user profile with ID "0000-0000-0000-0000":

        >>> comment = client.community.comment_on_profile(content="Hello world", userId="0000-0000-0000-0000")
        ... print(comment.content)
        Hello world
        """
        return self.comment(content = content, userId = userId, image = image, comId = comId)

   
    @community
    def like_comment(
        self,
        commentId: str,
        userId: Optional[str] = None,
        blogId: Optional[str] = None,
        wikiId: Optional[str] = None,
        comId: Union[str, int] = None
    ) -> ApiResponse:
        """
        Likes the comment with the given ID.

        :param commentId: The ID of the comment to like.
        :type commentId: str
        :param userId: The ID of the user who posted the comment (if applicable). Defaults to `None`.
        :type userId: Optional[str]
        :param blogId: The ID of the blog where the comment is located (if applicable). Defaults to `None`.
        :type blogId: Optional[str]
        :param wikiId: The ID of the wiki where the comment is located (if applicable). Defaults to `None`.
        :type wikiId: Optional[str]
        :param comId: The ID of the community where the comment is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        If any of the optional parameters (`userId`, `blogId`, `wikiId`) is provided, the function sends a POST request to the API to like the comment at the specified location. Otherwise, the comment with the specified ID is liked from the current community.

        `ApiResponse`:

        - `message`: A message indicating whether the comment was successfully liked.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To like a comment with ID "0000-0000-0000-0000":

        >>> response = client.community.like_comment(commentId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment liked successfully!")
        ... else:
        ...     print("Failed to like comment.")
        """
        if any([userId, blogId, wikiId]):
            base_endpoint = "/x{}/s/{}/comment/{}/vote"
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }

            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]), commentId)
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment/{commentId}/vote"

        return ApiResponse(self.session.handler(
            method = "POST",
            url = endpoint,
            data = {
            "value": 1,
            "timestamp": int(time() * 1000),
            "eventSource": "CommentDetailView" if userId is None else "UserProfileView"
            }
            ))


    @community
    def like_wiki_comment(self, commentId: str, wikiId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Likes the comment with the given ID on a wiki page with the given ID.
        
        :param commentId: The ID of the comment to like.
        :type commentId: str
        :param wikiId: The ID of the wiki page where the comment is located.
        :type wikiId: str
        :param comId: The ID of the community where the comment is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to like the comment at the specified location.
        
        `ApiResponse`:
        
        - `message`: A message indicating whether the comment was successfully liked.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        
        **Example usage:**
        
        To like a comment with ID "0000-0000-0000-0000" on a wiki page with ID "0000-0000-0000-0000":

        >>> response = client.community.like_wiki_comment(commentId="0000-0000-0000-0000", wikiId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment liked successfully!")
        ... else:
        ...     print("Failed to like comment.")
        """
        return self.like_comment(commentId = commentId, wikiId = wikiId, comId = comId)


    @community
    def like_blog_comment(self, commentId: str, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Likes the comment with the given ID on a blog page with the given ID.
        
        :param commentId: The ID of the comment to like.
        :type commentId: str
        :param blogId: The ID of the blog page where the comment is located.
        :type blogId: str
        :param comId: The ID of the community where the comment is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to like the comment at the specified location.
        
        `ApiResponse`:
        
        - `message`: A message indicating whether the comment was successfully liked.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        
        **Example usage:**
        
        To like a comment with ID "0000-0000-0000-0000" on a blog page with ID "0000-0000-0000-0000":

        >>> response = client.community.like_blog_comment(commentId="0000-0000-0000-0000", blogId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment liked successfully!")
        ... else:
        ...     print("Failed to like comment.")
        """
        return self.like_comment(commentId = commentId, blogId = blogId, comId = comId)


    @community
    def like_profile_comment(self, commentId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Likes the comment with the given ID on a user profile page with the given ID.
        
        :param commentId: The ID of the comment to like.
        :type commentId: str
        :param userId: The ID of the user profile page where the comment is located.
        :type userId: str
        :param comId: The ID of the community where the comment is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse
        
        This function sends a POST request to the API to like the comment at the specified location.
        
        `ApiResponse`:
        
        - `message`: A message indicating whether the comment was successfully liked.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        
        **Example usage:**
        
        To like a comment with ID "0000-0000-0000-0000" on a user profile page with ID "0000-0000-0000-0000":

        >>> response = client.community.like_profile_comment(commentId="0000-0000-0000-0000", userId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment liked successfully!")
        ... else:
        ...     print("Failed to like comment.")
        """
        return self.like_comment(commentId = commentId, userId = userId, comId = comId)


    @community
    def unlike_comment(
        self,
        commentId: str,
        userId: Optional[str] = None,
        blogId: Optional[str] = None,
        wikiId: Optional[str] = None,
        comId: Union[str, int] = None
        ) -> ApiResponse:
        """
        Removes a like from a comment.

        :param commentId: The ID of the comment to remove the like from.
        :type commentId: str
        :param userId: The ID of the user who liked the comment. If provided, the vote will be removed from the user profile page. Defaults to `None`.
        :type userId: Optional[str]
        :param blogId: The ID of the blog where the comment was made. If provided, the vote will be removed from the blog page. Defaults to `None`.
        :type blogId: Optional[str]
        :param wikiId: The ID of the wiki where the comment was made. If provided, the vote will be removed from the wiki page. Defaults to `None`.
        :type wikiId: Optional[str]
        :param comId: The ID of the community where the comment is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the like was successfully removed from the comment.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To remove a like from a comment with ID "123456":

        >>> response = client.community.unlike_comment(commentId="123456")
        ... if response.statuscode == 0:
        ...     print("Like removed from comment successfully!")
        ... else:
        ...     print("Failed to remove like from comment.")
        """
        if any([userId, blogId, wikiId]):
            base_endpoint = "/x{}/s/{}/comment/{}/vote"
            endpoint_mapping = {
                "userId": "/user-profile/{}",
                "blogId": "/blog/{}",
                "wikiId": "/item/{}"
            }

            for key, value in endpoint_mapping.items():
                if locals()[key]:
                    endpoint = base_endpoint.format(self.community_id if comId is None else comId, value.format(locals()[key]), commentId)
                    break
        else:
            endpoint = f"/x{self.community_id if comId is None else comId}/s/comment/{commentId}/vote"

        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = endpoint
            ))


    @community
    def like_blog(self, blogId: str, userId: Optional[str] = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Likes a blog post.

        :param blogId: The ID of the blog post to like.
        :type blogId: str
        :param userId: The ID of the user who liked the post. If provided, the like will be added to the user profile page. Defaults to `None`.
        :type userId: Optional[str]
        :param comId: The ID of the community where the blog post is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the like was successfully added to the blog post.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To like a blog post with ID "0000-0000-0000-0000":

        >>> response = client.community.like_blog(blogId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Blog post liked successfully!")
        ... else:
        ...     print("Failed to like blog post.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/vote",
            data = {
                "value": 4,
                "timestamp": int(time() * 1000),
                "eventSource": "UserProfileView" if userId is None else "PostDetailView"
                }))


    @community
    def unlike_blog(self, blogId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Removes a like from a blog post.

        :param blogId: The ID of the blog post to remove the like from.
        :type blogId: str
        :param comId: The ID of the community where the blog post is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the like was successfully removed from the blog post.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To remove a like from a blog post with ID "abcdef":

        >>> response = client.community.unlike_blog(blogId="abcdef")
        ... if response.statuscode == 0:
        ...     print("Like removed from blog post successfully!")
        ... else:
        ...     print("Failed to remove like from blog post.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/vote"
            ))


    @community
    def upvote_comment(self, blogId: str, commentId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Upvotes a comment on a blog post.

        :param blogId: The ID of the blog post that contains the comment.
        :type blogId: str
        :param commentId: The ID of the comment to upvote.
        :type commentId: str
        :param comId: The ID of the community where the blog post is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the upvote was successfully added to the comment.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To upvote a comment with ID "0000-0000-0000-0000" on a blog post with ID "1111-1111-1111-1111":

        >>> response = client.community.upvote_comment(blogId="1111-1111-1111-1111", commentId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment upvoted successfully!")
        ... else:
        ...     print("Failed to upvote comment.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/comment/{commentId}/vote",
            data = {
                "value": 1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))


    @community
    def downvote_comment(self, blogId: str, commentId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Downvotes a comment on a blog post.

        :param blogId: The ID of the blog post that contains the comment.
        :type blogId: str
        :param commentId: The ID of the comment to downvote.
        :type commentId: str
        :param comId: The ID of the community where the blog post is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the downvote was successfully added to the comment.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To downvote a comment with ID "0000-0000-0000-0000" on a blog post with ID "1111-1111-1111-1111":

        >>> response = client.community.downvote_comment(blogId="1111-1111-1111-1111", commentId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Comment downvoted successfully!")
        ... else:
        ...     print("Failed to downvote comment.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/comment/{commentId}/vote",
            data = {
                "value": -1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))


    @community
    def fetch_blog(self, blogId: str, comId: Union[str, int] = None) -> CBlog:
        """
        Fetches information about a blog.

        :param blogId: The ID of the blog to fetch.
        :type blogId: str
        :param comId: The ID of the community where the blog is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CBlog` object containing information about the fetched blog.

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `CBlog`:

        A `CBlog` object contains the following attributes:

        - `globalVotesCount`: The total number of votes the blog has received.
        - `globalVotedValue`: The total value of votes the blog has received.
        - `votedValue`: The value of the user's vote, if the user has voted.
        - `keywords`: The keywords associated with the blog.
        - `mediaList`: The media associated with the blog.
        - `style`: The styling of the blog.
        - `totalQuizPlayCount`: The total number of times quizzes associated with the blog have been played.
        - `title`: The title of the blog.
        - `tipInfo`: Information about tips associated with the blog.
        - `contentRating`: The content rating of the blog.
        - `content`: The content of the blog.
        - `needHidden`: Whether the blog is hidden.
        - `guestVotesCount`: The total number of guest votes the blog has received.
        - `type`: The type of the blog.
        - `status`: The status of the blog.
        - `globalCommentsCount`: The total number of comments the blog has received.
        - `modifiedTime`: The time the blog was last modified.
        - `widgetDisplayInterval`: The widget display interval of the blog.
        - `totalPollVoteCount`: The total number of poll votes the blog has received.
        - `blogId`: The ID of the blog.
        - `viewCount`: The total number of views the blog has received.
        - `language`: The language of the blog.
        - `author`: The author of the blog, represented as a `UserProfile` object.
        - `extensions`: Any extensions associated with the blog.
        - `votesCount`: The total number of votes the blog has received.
        - `ndcId`: The ID of the community where the blog is located.
        - `createdTime`: The time the blog was created.
        - `endTime`: The time the blog ends.
        - `commentsCount`: The total number of comments the blog has received.

        **Example usage:**

        To fetch information about a blog with ID "1111-2222-3333-4444":

        >>> blog = client.community.fetch_blog(blogId="1111-2222-3333-4444")
        ... print(f"Blog title: {blog.title}")
        ... print(f"Blog author: {blog.author.nickname}")
        """
        return CBlog(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}"
            ))


    @community
    def fetch_wiki(self, wikiId: str, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add Wiki class
        """
        Fetches information about a wiki.

        :param wikiId: The ID of the wiki to fetch.
        :type wikiId: str
        :param comId: The ID of the community where the wiki is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status and the fetched wiki.

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `data`: A dictionary containing the information about the fetched wiki.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To fetch information about a wiki with ID "1111-2222-3333-4444":

        >>> response = client.community.fetch_wiki(wikiId="1111-2222-3333-4444")
        ... if response.statuscode == 0:
        ...     print("Wiki fetched successfully!")
        ... else:
        ...     print("Failed to fetch wiki.")
        """
        return ApiResponse(self.session.handler(
            method = "GET", url = f"/x{self.community_id if comId is None else comId}/s/item/{wikiId}"))


    @community
    def fetch_quiz(self, quizId: str, start: int = 0, size: int = 10, comId: Union[str, int] = None) -> QuizRankingList:
        """
        Fetches the ranking list for a quiz.

        :param quizId: The ID of the quiz to fetch the ranking list for.
        :type quizId: str
        :param start: The start index of the ranking list (default 0).
        :type start: int
        :param size: The size of the ranking list to fetch (default 10).
        :type size: int
        :param comId: The ID of the community where the quiz is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `QuizRankingList` object containing information about the ranking list.
        :rtype: QuizRankingList

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `QuizRankingList`:

        - `highest_mode`: A list of the highest mode of the quiz.
        - `modified_time`: A list of the last time the quiz was modified.
        - `is_finished`: A list of whether the quiz is finished or not.
        - `hell_is_finished`: A list of whether the quiz is finished in hell mode or not.
        - `highest_score`: A list of the highest score of the quiz.
        - `beat_rate`: A list of the beat rate of the quiz.
        - `last_beat_rate`: A list of the last beat rate of the quiz.
        - `total_times`: A list of the total times the quiz has been played.
        - `latest_score`: A list of the latest score of the quiz.
        - `author`: A list of the author of the quiz.
        - `latest_mode`: A list of the latest mode of the quiz.
        - `created_time`: A list of the time the quiz was created.

        **Example usage:**

        To fetch the ranking list for a quiz with ID "1234-5678-9012" with start index 0 and size 10:

        >>> quiz_ranking_list = client.community.fetch_quiz(quizId="1234-5678-9012", start=0, size=10)
        ... highest_scores = quiz_ranking_list.highest_score
        ... beat_rates = quiz_ranking_list.beat_rate
        ... print(highest_scores)
        ... print(beat_rates)
        """
        return QuizRankingList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{quizId}/quiz/result?start={start}&size={size}"
            ))
    

    @community
    def reply_wall(self, userId: str, commentId: str, message: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Replies to a comment on a user's wall.

        :param userId: The ID of the user whose wall to comment on.
        :type userId: str
        :param commentId: The ID of the comment to reply to.
        :type commentId: str
        :param message: The message to post as a reply.
        :type message: str
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the reply was successfully posted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To reply to a comment with ID "1111-2222-3333-4444" on user "0000-0000-0000-0000"'s wall with message "Thanks for sharing!":

        >>> response = client.community.reply_wall(userId="0000-0000-0000-0000", commentId="1111-2222-3333-4444", message="Thanks for sharing!")
        ... if response.statuscode == 0:
        ...     print("Reply posted successfully!")
        ... else:
        ...     print("Failed to post reply.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/comment",
            data = {
                "content": message,
                "stackedId": None,
                "respondTo": commentId,
                "type": 0,
                "eventSource": "UserProfileView",
                "timestamp": int(time() * 1000)
                }))


    @community
    def vote_poll(self, blogId: str, optionId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Votes for a poll option in the current or specified community.

        :param blogId: The ID of the blog containing the poll.
        :type blogId: str
        :param optionId: The ID of the poll option to vote for.
        :type optionId: str
        :param comId: The ID of the community where the blog is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to vote for a poll option in the specified blog. 

        `ApiResponse`:

        - `message` (str): A message indicating whether the vote was successful.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To vote for poll option with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.vote_poll(blogId="2222-2222-2222-2222", optionId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Voted successfully!")
        ... else:
        ...     print("Failed to vote.")

        To vote for poll option with ID "3333-3333-3333-3333" in a community with ID "123":

        >>> response = client.community.vote_poll(blogId="4444-4444-4444-4444", optionId="3333-3333-3333-3333", comId=123)
        ... if response.statuscode == 0:
        ...     print("Voted successfully!")
        ... else:
        ...     print("Failed to vote.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/poll/option/{optionId}/vote",
            data = {
                "value": 1,
                "eventSource": "PostDetailView",
                "timestamp": int(time() * 1000)
                }))


    @community
    def repost_blog(self, content: str = None, blogId: str = None, wikiId: str = None, comId: Union[str, int] = None) -> CBlog:
        return CBlog(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog",
            data = {
                "content": content,
                "refObjectId": blogId if blogId is not None else wikiId,
                "refObjectType": 1 if blogId is not None else 2,
                "type": 2,
                "timestamp": int(time() * 1000)
                }))


    @community
    def ban(self, userId: str, reason: str, banType: int = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Bans a user in the current or specified community.

        :param userId: The ID of the user to ban.
        :type userId: str
        :param reason: The reason for banning the user.
        :type reason: str
        :param banType: The type of ban to apply. Optional.
        :type banType: int
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to ban a user in the specified community. 

        `ApiResponse`:

        - `message` (str): A message indicating whether the ban was successful.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To ban a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.ban(userId="1111-1111-1111-1111", reason="This user has violated community guidelines.")
        ... if response.statuscode == 0:
        ...     print("User banned successfully!")
        ... else:
        ...     print("Failed to ban user.")

        To ban a user with ID "2222-2222-2222-2222" in a community with ID "123" and apply a ban type:

        >>> response = client.community.ban(userId="2222-2222-2222-2222", reason="This user has been reported for spamming.", banType=2, comId=123)
        ... if response.statuscode == 0:
        ...     print("User banned successfully!")
        ... else:
        ...     print("Failed to ban user.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/ban",
            data = {"reasonType": banType, "note": {"content": reason}, "timestamp": int(time() * 1000)
            }))


    @community
    def unban(self, userId: str, reason: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Unbans a user in the current or specified community.

        :param userId: The ID of the user to unban.
        :type userId: str
        :param reason: The reason for unbanning the user.
        :type reason: str
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to unban a user in the specified community. 

        `ApiResponse`:

        - `message` (str): A message indicating whether the unban was successful.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To unban a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.unban(userId="1111-1111-1111-1111", reason="This user has been unbanned.")
        ... if response.statuscode == 0:
        ...     print("User unbanned successfully!")
        ... else:
        ...     print("Failed to unban user.")

        To unban a user with ID "2222-2222-2222-2222" in a community with ID "123":

        >>> response = client.community.unban(userId="2222-2222-2222-2222", reason="This user has been unbanned.", comId=123)
        ... if response.statuscode == 0:
        ...     print("User unbanned successfully!")
        ... else:
        ...     print("Failed to unban user.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/unban",
            data = {"note": {"content": reason}, "timestamp": int(time() * 1000)
            }))


    @community
    def strike(
        self,
        userId: str,
        amountOfTime: int = 5,
        title: str = None,
        reason: str = None,
        comId: Union[str, int] = None,
        **kwargs
        ) -> ApiResponse:
        """
        Issues a strike against a user in the current or specified community.

        :param userId: The ID of the user to issue a strike to.
        :type userId: str
        :param amountOfTime: The duration of the strike in hours. Can be 1, 2, 3, 4, or 5. Default is 5.
        :type amountOfTime: int
        :param title: An optional title for the strike.
        :type title: str
        :param reason: An optional reason for issuing the strike.
        :type reason: str
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to issue a strike against a user in the specified community. 

        `ApiResponse`:

        - `message` (str): A message indicating whether the strike was successful.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To issue a 5-hour strike against a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.strike(userId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Strike issued successfully!")
        ... else:
        ...     print("Failed to issue strike.")

        To issue a 2-hour strike against a user with ID "2222-2222-2222-2222" in a community with ID "123" with a title and reason:

        >>> response = client.community.strike(userId="2222-2222-2222-2222", amountOfTime=2, title="Second Strike", reason="This is a 2-hour strike.", comId=123)
        ... if response.statuscode == 0:
        ...     print("Strike issued successfully!")
        ... else:
        ...     print("Failed to issue strike.")
        """
        if "amount" in kwargs: #TODO: Remove this in the near future.
            amountOfTime = kwargs["amount"]
            print("Warning: The 'amount' parameter is deprecated. Please use 'amountOfTime' instead.")

        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/notice",
            data = {
                "uid": userId,
                "title": title,
                "content": reason,
                "attachedObject": {"objectId": userId,"objectType": 0},
                "penaltyType": 1,
                "penaltyValue": [3600, 10800, 21600, 43200, 86400][amountOfTime - 1 if amountOfTime in range(1, 6) else 86400],
                "adminOpNote": {},
                "noticeType": 4,
                "timestamp": int(time() * 1000)
                }))


    @community
    def warn(self, userId: str, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Issues a warning to a user in the current or specified community.

        :param userId: The ID of the user to issue a warning to.
        :type userId: str
        :param reason: An optional reason for issuing the warning.
        :type reason: str
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to issue a warning to a user in the specified community. 

        `ApiResponse`:

        - `message` (str): A message indicating whether the warning was successful.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To issue a warning to a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.warn(userId="1111-1111-1111-1111", reason="This is a warning.")
        ... if response.statuscode == 0:
        ...     print("Warning issued successfully!")
        ... else:
        ...     print("Failed to issue warning.")

        To issue a warning to a user with ID "2222-2222-2222-2222" in a community with ID "123" with a reason:

        >>> response = client.community.warn(userId="2222-2222-2222-2222", reason="This is a warning.", comId=123)
        ... if response.statuscode == 0:
        ...     print("Warning issued successfully!")
        ... else:
        ...     print("Failed to issue warning.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/notice",
            data = {
                "uid": userId,
                "title": "Custom",
                "content": reason,
                "attachedObject": {"objectId": userId,"objectType": 0},
                "penaltyType": 0,
                "adminOpNote": {},
                "noticeType": 7,
                "timestamp": int(time() * 1000)
                }))


    @community
    def edit_titles(self, userId: str, titles: list, colors: list, comId: Union[str, int] = None) -> ApiResponse:
        """
        Edits the titles of a user in the current or specified community.

        :param userId: The ID of the user to edit the titles of.
        :type userId: str
        :param titles: A list of titles to set for the user.
        :type titles: list
        :param colors: A list of colors to set for the titles. The length of this list must match the length of the `titles` list.
        :type colors: list
        :param comId: The ID of the community where the user is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to edit the titles of a user in the specified community. 

        `ApiResponse`:

        - `message` (str): A message indicating whether the edit was successful.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To edit the titles of a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.edit_titles(userId="1111-1111-1111-1111", titles=["Title 1", "Title 2"], colors=["#ff0000", "#00ff00"])
        ... if response.statuscode == 0:
        ...     print("Titles edited successfully!")
        ... else:
        ...     print("Failed to edit titles.")

        To edit the titles of a user with ID "2222-2222-2222-2222" in a community with ID "123" with two titles and colors:

        >>> response = client.community.edit_titles(userId="2222-2222-2222-2222", titles=["Title 1", "Title 2"], colors=["#ff0000", "#00ff00"], comId=123)
        ... if response.statuscode == 0:
        ...     print("Titles edited successfully!")
        ... else:
        ...     print("Failed to edit titles.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/admin",
            data = {
                "adminOpName": 207,
                "adminOpValue": {"titles": [{"title": title, "color": color} for title, color in zip(titles, colors)]},
                "timestamp": int(time() * 1000)
                }))


    @community
    def fetch_mod_history(
        self,
        userId: str = None,
        blogId: str = None,
        wikiId: str = None,
        quizId: str = None,
        fileId: str = None,
        size: int = 25,
        comId: Union[str, int] = None
        ) -> ApiResponse:
        """
        Fetches moderation history for a user, blog, wiki, quiz, or file in the current or specified community.

        :param userId: The ID of the user to fetch moderation history for. If not provided, the history of the specified object will be returned.
        :type userId: str
        :param blogId: The ID of the blog to fetch moderation history for.
        :type blogId: str
        :param wikiId: The ID of the wiki to fetch moderation history for.
        :type wikiId: str
        :param quizId: The ID of the quiz to fetch moderation history for.
        :type quizId: str
        :param fileId: The ID of the file to fetch moderation history for.
        :type fileId: str
        :param size: The number of moderation events to return. Default is 25.
        :type size: int
        :param comId: The ID of the community where the object is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing moderation history for the specified object.
        :rtype: ApiResponse

        This function sends a GET request to the API to fetch moderation history for a user, blog, wiki, quiz, or file in the specified community.

        `ApiResponse`:

        - `message` (str): A message indicating whether the moderation history was fetched successfully.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To fetch the moderation history of a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.fetch_mod_history(userId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print(response.json())
        ... else:
        ...     print("Failed to fetch moderation history.")

        To fetch the moderation history of a blog with ID "2222-2222-2222-2222" in a community with ID "123":

        >>> response = client.community.fetch_mod_history(blogId="2222-2222-2222-2222", comId=123)
        ... if response.statuscode == 0:
        ...     print(response.json())
        ... else:
        ...     print("Failed to fetch moderation history.")
        """
        return ApiResponse(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/admin/operation",
            params = {
                "objectId": blogId if blogId is not None else wikiId if wikiId is not None else quizId if quizId is not None else fileId if fileId is not None else userId,
                "objectType": 1 if blogId is not None else 2 if wikiId is not None else 3 if quizId is not None else 109 if fileId is not None else 0,
                "pagingType": "t",
                "size": size
                }))

    @community
    def edit_profile(
        self,
        nickname: str = None,
        content: str = None,
        icon: Union[str, BytesIO] = None,
        backgroundColor: str = None,
        backgroundImage: Union[str, BytesIO] = None,
        cover_image: Union[str, BytesIO] = None,
        comId: Union[str, int] = None,
        **kwargs
        ) -> UserProfile:
        if "background_color" in kwargs: #TODO: Remove in the near future.
            backgroundColor = kwargs["background_color"]
            print("background_color is deprecated, please use backgroundColor instead.")
        if "background_image" in kwargs: #TODO: Remove in the near future.
            backgroundImage = kwargs["background_image"]
            print("background_image is deprecated, please use backgroundImage instead.")

        data: dict = {"timestamp": int(time() * 1000), "extensions": {}}

        [data.update({key: value}) for key, value in {
            "nickname": nickname,
            "content": content,
            "icon": self.__handle_media__(media=icon, media_value=True) if icon is not None else None,
            "mediaList": [[100, self.__handle_media__(media=cover_image, media_value=True), None, None, None, None]] if cover_image is not None else None
            }.items() if value is not None]

        if backgroundColor:
            data["extensions"]["style"] = {"backgroundColor": backgroundColor}

        if backgroundImage:
            data["extensions"]["style"] = {"backgroundMediaList": [[100, self.__handle_media__(media=backgroundImage, media_value=True), None, None, None, None]]}

        return UserProfile(
            self.session.handler(
                method = "POST",
                url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{self.userId}",
                data=data
                ))

    @community
    def fetch_user_blogs(self, userId: str, start: int = 0, size: int = 5, comId: Union[str, int] = None) -> CBlogList:
        """
        Fetches a list of blogs created by a user in the current or specified community.

        :param userId: The ID of the user to fetch blogs for.
        :type userId: str
        :param start: The starting index of the blogs to fetch (default is 0).
        :type start: int
        :param size: The number of blogs to fetch (default is 5).
        :type size: int
        :param comId: The ID of the community where the blogs were created. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CBlogList` object containing information about the fetched blogs.
        :rtype: CBlogList

        This function sends a GET request to the API to fetch a list of blogs created by a user in the specified community.

        `CBlogList`:

        - `data` (list): A list of blogs created by the specified user.
        - `author` (UserProfileList): A list of `UserProfile` objects representing the authors of the fetched blogs.
        - `globalVotesCount` (list): A list of global vote counts for the fetched blogs.
        - `globalVotedValue` (list): A list of global vote values for the fetched blogs.
        - `votedValue` (list): A list of vote values for the fetched blogs.
        - `keywords` (list): A list of keywords associated with the fetched blogs.
        - `mediaList` (list): A list of media items associated with the fetched blogs.
        - `style` (list): A list of style information for the fetched blogs.
        - `totalQuizPlayCount` (list): A list of total quiz play counts for the fetched blogs.
        - `title` (list): A list of titles for the fetched blogs.
        - `tipInfo` (list): A list of tip information for the fetched blogs.
        - `contentRating` (list): A list of content ratings for the fetched blogs.
        - `content` (list): A list of content for the fetched blogs.
        - `needHidden` (list): A list of flags indicating whether the fetched blogs need to be hidden.
        - `guestVotesCount` (list): A list of guest vote counts for the fetched blogs.
        - `type` (list): A list of types for the fetched blogs.
        - `status` (list): A list of statuses for the fetched blogs.
        - `globalCommentsCount` (list): A list of global comment counts for the fetched blogs.
        - `modifiedTime` (list): A list of modification times for the fetched blogs.
        - `widgetDisplayInterval` (list): A list of widget display intervals for the fetched blogs.
        - `totalPollVoteCount` (list): A list of total poll vote counts for the fetched blogs.
        - `blogId` (list): A list of IDs for the fetched blogs.
        - `viewCount` (list): A list of view counts for the fetched blogs.
        - `language` (list): A list of languages for the fetched blogs.
        - `extensions` (list): A list of extensions for the fetched blogs.
        - `votesCount` (list): A list of vote counts for the fetched blogs.
        - `ndcId` (list): A list of NDC IDs for the fetched blogs.
        - `createdTime` (list): A list of creation times for the fetched blogs.
        - `commentsCount` (list): A list of comment counts for the fetched blogs.

        **Example usage:**

        To fetch the first 5 blogs created by a user in the current community:

        >>> blogs = client.fetch_user_blogs(userId="0000-000000-000000-0000")
        ... for blog in blogs.content:
        ...     print(blog)
        "Wow this is a blog!"
        "This is another blog!"
        "This is a third blog!"
        ...
        """
        return CBlogList(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/blog?type=user&q={userId}&start={start}&size={size}"
            ))

    @community
    def fetch_user_wikis(self, userId: str, start: int = 0, size: int = 25, comId: Union[str, int] = None) -> ApiResponse: #TODO: Add WikiList
        """
        Fetches wikis created by a user based on the specified parameters.

        :param userId: The ID of the user to fetch wikis for.
        :type userId: str
        :param start: The index of the first item to fetch. Default is 0.
        :type start: int
        :param size: The number of items to fetch. Default is 25.
        :type size: int
        :param comId: The ID of the community where the wikis were created. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing a list of wikis created by the specified user.
        :rtype: ApiResponse

        This function sends a GET request to the API to fetch a list of wikis created by a user in the specified community.

        `ApiResponse`:

        - `data` (dict): Raw JSON data.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To fetch a list of wikis created by a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.fetch_user_wikis(userId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print(response.json())
        ... else:
        ...     print("Failed to fetch user wikis.")

        To fetch a list of wikis created by a user with ID "2222-2222-2222-2222" in a community with ID "123":

        >>> response = client.community.fetch_user_wikis(userId="2222-2222-2222-2222", comId=123)
        ... if response.statuscode == 0:
        ...     print(response.json())
        ... else:
        ...     print("Failed to fetch user wikis.")
        """
        return ApiResponse(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}"
            ))

    @community
    def fetch_user_check_ins(self, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Fetches a list of check-ins made by a user in the current or specified community.

        :param userId: The ID of the user to fetch check-ins for.
        :type userId: str
        :param comId: The ID of the community where the check-ins were made. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing a list of check-ins made by the specified user.
        :rtype: ApiResponse

        This function sends a GET request to the API to fetch a list of check-ins made by a user in the specified community.

        `ApiResponse`:

        - `data` (list): A list of check-ins made by the specified user.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To fetch a list of check-ins made by a user with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.fetch_user_check_ins(userId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print(response.data)
        ... else:
        ...     print("Failed to fetch user check-ins.")

        To fetch a list of check-ins made by a user with ID "2222-2222-2222-2222" in a community with ID "123":

        >>> response = client.community.fetch_user_check_ins(userId="2222-2222-2222-2222", comId=123)
        ... if response.statuscode == 0:
        ...     print(response.data)
        ... else:
        ...     print("Failed to fetch user check-ins.")
        """
        return ApiResponse(self.session.handler(
            method = "GET",
            url = f"/x{self.community_id if comId is None else comId}/s/check-in/stats/{userId}?timezone=-300"
            ))
            
    @community
    def send_embed(self, chatId: str, title: str, content: str, image: BinaryIO = None, link: Optional[str] = None, comId: Union[str, int] = None) -> CMessage:
        return CMessage(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content = "[c]",
            attachedObject={
                "title": title,
                "content": content,
                "mediaList": [[100, self.__handle_media__(media=image, media_value=True), None]],
                "link": link
                }).json()))

    @community
    def send_link_snippet(self, chatId: str, image: str, message: str = "[c]", link: str = "ndc://user-me", mentioned: list = None, comId: Union[str, int] = None) -> CMessage:
        if mentioned is None:
            mentioned = []

        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=message,
            extensions = {
            "linkSnippetList": [{
                "link": link,
                "mediaType": 100,
                "mediaUploadValue": self.encode_media(
                    self.__handle_media__(
                        media=image,
                        content_type="image/jpg",
                        media_value=False
                    )
                ),
                "mediaUploadValueContentType": "image/png",
                "mentionedArray": [
                {"uid": self.userId}
                ] if isinstance(mentioned, str) else [{"uid": i} for i in mentioned
                ] if isinstance(mentioned, list) else None
            }]
            }).json()))

    @community
    def send_message(self, chatId: str, content: str, comId: Union[str, int] = None) -> CMessage:
        return CMessage(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(content=content).json()
            ))

    @community
    def send_image(self, chatId: str, image: BinaryIO = None, comId: Union[str, int] = None) -> CMessage:
        return CMessage(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                mediaType = 100,
                mediaUploadValue=self.encode_media(
                    self.__handle_media__(
                    media=image,
                    content_type="image/jpg",
                    media_value=False
                )),
                mediaUploadValueContentType = "image/jpg",
                mediaUhqEnabled = True).json()
                ))

    @community
    def send_audio(self, chatId: str, audio: Union[str, BinaryIO] = None, comId: Union[str, int] = None) -> CMessage:
        """
        Sends an audio file to a chat.

        :param chatId: The ID of the chat to send the audio file to.
        :type chatId: str
        :param audio: The path to the audio file or a file-like object containing the audio data.
        :type audio: Union[str, BinaryIO]
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: A `CMessage` object representing the newly sent message.

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        **Example usage:**

        To send an audio file located at "/path/to/audio.aac" to a chat with ID "1111-2222-3333-4444":

        EXAMPLE 1:
        >>> response = client.send_audio(chatId="1111-2222-3333-4444", audio="/path/to/audio.aac")
        ...
        EXAMPLE 2:
        >>> response = client.send_audio(chatId="1111-2222-3333-4444", audio="https://example.com/audio.aac")
        ... 
        """
        return CMessage(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                type=2,
                mediaType=110,
                mediaUploadValue=self.encode_media(
                    self.__handle_media__(
                        media=audio,
                        content_type="audio/aac",
                        media_value=False
            ))).json()))

    @community
    def send_sticker(self, chatId: str, stickerId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Sends a sticker to a chat.

        :param chatId: The ID of the chat to send the sticker to.
        :type chatId: str
        :param stickerId: The ID of the sticker to send.
        :type stickerId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the sticker was successfully sent.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.
        - `messageId`: The ID of the newly sent message.

        **Example usage:**

        To send a sticker with ID "0000-0000-0000-0000" to a chat with ID "1111-2222-3333-4444":

        >>> response = client.community.send_sticker(chatId="1111-2222-3333-4444", stickerId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Sticker sent successfully!")
        ... else:
        ...     print("Failed to send sticker.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message",
            data = PrepareMessage(
                type=3,
                mediaType=113,
                mediaValue=f"ndcsticker://{stickerId}",
                stickerId=stickerId).json()
                ))
    
    def __handle_media__(self, media: str, content_type: str = "image/jpg", media_value: bool = False) -> str:
        """Handles media files."""
        response = None
        
        try:
            if media.startswith("http"):
                response = get(media)
                response.raise_for_status()
                media = response.content
            else:
                media = open(media, "rb").read()
        except Exception as e:
            raise InvalidImage from e

        if media_value:
            return self.upload_media(media=media, content_type=content_type)

        if response and not response.headers.get("content-type").startswith("image"):
            raise InvalidImage

        return media

    def encode_media(self, file: bytes) -> str:
        """Encodes a media file to base64."""
        return b64encode(file).decode()

    def upload_media(self, media: Union[str, BinaryIO], content_type: str = "image/jpg") -> str:
        """Uploads a media file to the server."""
        return ApiResponse(self.session.handler(
            method = "POST",
            url = "/g/s/media/upload",
            data = media,
            content_type = content_type
            )).mediaValue

    @community
    def join_chat(self, chatId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Joins a chat.

        :param chatId: The ID of the chat to join.
        :type chatId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the user successfully joined the chat.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To join a chat with ID "0000-0000-0000-0000":

        >>> response = client.community.join_chat(chatId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Joined chat successfully!")
        ... else:
        ...     print("Failed to join chat.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    @community
    def leave_chat(self, chatId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Leaves a chat.

        :param chatId: The ID of the chat to leave.
        :type chatId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the user successfully left the chat.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To leave a chat with ID "0000-0000-0000-0000" in the current community:

        >>> response = client.community.leave_chat(chatId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Left chat successfully!")
        ... else:
        ...     print("Failed to leave chat.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}"
            ))

    @community
    def kick(self, userId: str, chatId: str, allowRejoin: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        Kicks a user from a chat.

        :param userId: The ID of the user to kick from the chat.
        :type userId: str
        :param chatId: The ID of the chat to kick the user from.
        :type chatId: str
        :param allowRejoin: A boolean indicating whether the user should be allowed to rejoin the chat. Defaults to `True`.
        :type allowRejoin: bool
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the user was successfully kicked from the chat.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To kick a user with ID "0000-0000-0000-0000" from a chat with ID "0000-0000-0000-0000":

        >>> response = client.community.kick(userId="0000-0000-0000-0000", chatId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("User kicked successfully!")
        ... else:
        ...     print("Failed to kick user.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={1 if allowRejoin else 0}"
            ))

    @community
    def delete_chat(self, chatId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes a chat.

        :param chatId: The ID of the chat to delete.
        :type chatId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the chat was successfully deleted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To delete a chat with ID "abcdef":

        >>> response = client.community.delete_chat(chatId="abcdef")
        ... if response.statuscode == 0:
        ...     print("Chat deleted successfully!")
        ... else:
        ...     print("Failed to delete chat.")
        """
        return ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}"
            ))

    @community
    def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Deletes a message in a chat.

        :param chatId: The ID of the chat that contains the message.
        :type chatId: str
        :param messageId: The ID of the message to delete.
        :type messageId: str
        :param asStaff: If `True`, the message is deleted as a staff member. Defaults to `False`.
        :type asStaff: bool
        :param reason: The reason for deleting the message, if being deleted as a staff member. Defaults to `None`.
        :type reason: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the message was successfully deleted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To delete a message with ID `0000-0000-0000-0000` in a chat with ID `0000-0000-0000-0000`:

        >>> response = client.community.delete_message(chatId="0000-0000-0000-0000", messageId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Message deleted successfully!")
        ... else:
        ...     print("Failed to delete message.")
        """
        return ApiResponse(
            self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message/{messageId}/admin",
            data = {
            "adminOpName": 102,
            "adminOpNote": {"content": reason},
            "timestamp": int(time() * 1000)
            }
            )) if asStaff else ApiResponse(self.session.handler(
            method = "DELETE",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/message/{messageId}"
            ))

    @community
    def transfer_host(self, chatId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Requests to transfer chat organizer privileges to another user.

        :param chatId: The ID of the chat where the transfer request will be made.
        :type chatId: str
        :param userId: The ID of the user to transfer organizer privileges to.
        :type userId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the transfer request was successfully made.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To request to transfer chat organizer privileges to another user, use the following code:

        >>> response = client.community.transfer_host(chatId="0000-0000-0000-0000", userId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Transfer request made successfully!")
        ... else:
        ...     print("Failed to make transfer request.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/transfer-organizer",
            data = {
                "uidList": [userId],
                "timestamp": int(time() * 1000)
                }))

    @community
    def accept_host(self, chatId: str, requestId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Accepts a request to transfer chat organizer privileges to the current user.

        :param chatId: The ID of the chat where the transfer request was made.
        :type chatId: str
        :param requestId: The ID of the transfer request to accept.
        :type requestId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the transfer request was successfully accepted.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To accept a request to transfer chat organizer privileges to the current user, use the following code:

        >>> response = client.community.accept_host(chatId="0000-0000-0000-0000", requestId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Transfer request accepted successfully!")
        ... else:
        ...     print("Failed to accept transfer request.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept"
            ))

    @community
    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Subscribes to an influencer's content.

        :param userId: The ID of the influencer to subscribe to.
        :type userId: str
        :param autoRenew: Whether the subscription should auto-renew. Defaults to `False`.
        :type autoRenew: bool
        :param transactionId: A unique ID for the transaction. If not provided, a random UUID is used. Defaults to `None`.
        :type transactionId: str
        :param comId: The ID of the community where the subscription will be made. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the subscription was successfully made.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To subscribe to an influencer with ID "123456":

        >>> response = client.community.subscribe(userId="123456", autoRenew=True)
        ... if response.statuscode == 0:
        ...     print("Subscription created successfully!")
        ... else:
        ...     print("Failed to create subscription.")
        """
        if not transactionId: transactionId = str(uuid4())
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/influencer/{userId}/subscribe",
            data = {
                "paymentContext": {
                    "transactionId": transactionId,
                    "isAutoRenew": autoRenew
                },
                "timestamp": int(time() * 1000)
                }))

    @community
    def thank_props(self, chatId: str, userId: str, comId: Union[str, int] = None) -> ApiResponse:
        """
        Sends a thank-you message to a user who has been tipped in a chat.

        :param chatId: The ID of the chat where the user was tipped.
        :type chatId: str
        :param userId: The ID of the user to send the thank-you message to.
        :type userId: str
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the thank-you message was successfully sent.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To send a thank-you message to user "0000-0000-0000-0000" who was tipped in chat "1111-1111-1111-1111":

        >>> response = client.community.thank_props(chatId="1111-1111-1111-1111", userId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Thank-you message sent successfully!")
        ... else:
        ...     print("Failed to send thank-you message.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank"
            ))

    @community
    def send_active(
        self,
        tz: int = -timezone // 1000,
        start: int = None,
        end: int = None,
        timers: list = None,
        comId: Union[str, int] = None
        ) -> ApiResponse:
        """
        Sends data about user activity to the server.

        :param tz: The timezone offset in seconds from UTC. Defaults to the local timezone.
        :type tz: int
        :param start: The start time of a user activity session, in Unix timestamp format (seconds since 1970-01-01 UTC). Required if `timers` is not provided. Defaults to `None`.
        :type start: int
        :param end: The end time of a user activity session, in Unix timestamp format (seconds since 1970-01-01 UTC). Required if `timers` is not provided. Defaults to `None`.
        :type end: int
        :param timers: A list of user activity sessions, each represented as a dictionary with `start` and `end` keys. Required if `start` and `end` are not provided. Defaults to `None`.
        :type timers: list
        :param comId: The ID of the community where the user activity data will be sent. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :raises MissingTimers: If `start` and `end` are not provided and `timers` is not provided or empty.
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the user activity data was successfully sent.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To send 5 minutes of user activity data:

        >>> start_time = int(time())
        >>> end_time = int(time()) + 300
        >>> response = client.community.send_active(start=start_time, end=end_time)
        ... if response.statuscode == 0:
        ...     print("User activity data sent successfully!")
        ... else:
        ...     print("Failed to send user activity data.")
        """
        if not any([start and end, timers]): raise MissingTimers
        
        data={
            "optInAdsFlags": 2147483647,
            "timezone": tz,
            "timestamp": int(time() * 1000)
        }
        if timers is not None:
            data["userActiveTimeChunkList"] = timers
        else:
            data["userActiveTimeChunkList"] = [{"start": start, "end": end}]

        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/community/stats/user-active-time",
            data=data
            ))

    @community
    def send_coins(
        self,
        coins: int,
        blogId: str = None,
        chatId: str = None,
        wikiId: str = None,
        transactionId: str = None,
        comId: Union[str, int] = None
        ) -> ApiResponse:
        """
        Sends coins to a blog, chat, or wiki item.

        :param coins: The amount of coins to send. Must be a positive integer.
        :type coins: int
        :param blogId: The ID of the blog post to send coins to. If provided, `chatId` and `wikiId` must be `None`. Defaults to `None`.
        :type blogId: str
        :param chatId: The ID of the chat to send coins to. If provided, `blogId` and `wikiId` must be `None`. Defaults to `None`.
        :type chatId: str
        :param wikiId: The ID of the wiki item to send coins to. If provided, `blogId` and `chatId` must be `None`. Defaults to `None`.
        :type wikiId: str
        :param transactionId: A unique ID for the transaction. If not provided, a random UUID is used. Defaults to `None`.
        :type transactionId: str
        :param comId: The ID of the community where the coins will be sent. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the coins were successfully sent.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To send 100 coins to a chat with ID "0000-0000-0000-0000":

        >>> response = client.community.send_coins(coins=100, chatId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("Coins sent successfully!")
        ... else:
        ...     print("Failed to send coins.")
        """
        return ApiResponse(self.session.handler(
            method="POST", url=f'/x{self.community_id if comId is None else comId}/s/{"blog" if blogId else "chat/thread" if chatId else "item"}/{blogId or chatId or wikiId}/tipping',
            data={
                "coins": coins,
                "tippingContext": {"transactionId": transactionId or (str(uuid4()))},
                "timestamp": int(time() * 1000)
            }
        ))


    @community
    def send_chat_props(self, coins: int, chatId: str, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """Refer to `send_coins` for documentation."""
        return self.send_coins(coins=coins, chatId=chatId, transactionId=transactionId, comId=comId)


    @community
    def send_blog_props(self, coins: int, blogId: str, transactionId: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """Refer to `send_coins` for documentation."""
        return self.send_coins(coins=coins, blogId=blogId, transactionId=transactionId, comId=comId)


    @community
    def start_chat(
        self,
        userIds: Union[str, List[str]],
        title: Optional[str] = None,
        message: Optional[str] = None,
        content: Optional[str] = None,
        comId: Optional[Union[str, int]] = None
    ) -> ApiResponse:
        """
        Creates a new chat with the given users.

        :param userIds: A single user ID or a list of user IDs to invite to the chat.
        :type userIds: Union[str, List[str]]
        :param title: The title of the chat. Defaults to `None`.
        :type title: Optional[str]
        :param message: The message to send to the users when inviting them to the chat. Defaults to `None`.
        :type message: Optional[str]
        :param content: The content of the chat. Defaults to `None`.
        :type content: Optional[str]
        :param comId: The ID of the community where the chat will be created. If not provided, the current community ID is used.
        :type comId: Optional[Union[str, int]]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        `ApiResponse`:

        - `message`: A message indicating whether the chat was successfully created.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To create a new chat with users "0000-0000-0000-0000" and "1111-1111-1111-1111":

        >>> response = client.community.start_chat(userIds=["0000-0000-0000-0000", "1111-1111-1111-1111"], title="New chat", message="Join my chat!", content="Hello, world!")
        ... if response.statuscode == 0:
        ...     print("Chat created successfully!")
        ... else:
        ...     print("Failed to create chat.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread",
            data = {
            "title": title,
            "inviteeUids": userIds if isinstance(userIds, list) else [userIds],
            "initialMessageContent": message,
            "content": content,
            "type": 0,
            "publishToGlobal": 0,
            "timestamp": int(time() * 1000)
            }))

    @community
    def invite_chat(self, chatId: str, userIds: Union[str, List[str]], comId: Union[str, int] = None) -> ApiResponse:
        """
        Invites one or more users to join a chat.

        :param chatId: The ID of the chat to invite users to.
        :type chatId: str
        :param userIds: The ID(s) of the user(s) to invite to the chat. Can be a string or a list of strings.
        :type userIds: Union[str, List[str]]
        :param comId: The ID of the community where the chat is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        Sends a POST request to the API to invite the specified user(s) to join the chat with the given ID.

        `ApiResponse`:

        - `message`: A message indicating whether the invitation was successfully sent.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To invite "0101-0101-0101-0101" to join a chat with ID "0000-0000-0000-0000":

        >>> response = client.community.invite_chat(chatId="0000-0000-0000-0000", userIds="0101-0101-0101-0101")
        ... if response.statuscode == 0:
        ...     print("Invitation sent successfully!")
        ... else:
        ...     print("Failed to send invitation.")
        """
        return ApiResponse(self.session.handler(
            method = "POST", url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/invite",
            data = {
            "uids": userIds if isinstance(userIds, list) else [userIds],
            "timestamp": int(time() * 1000)
            }))


    @community
    def set_view_only(self, chatId: str, viewOnly: bool = True, comId: Union[str, int] = None) -> ApiResponse:
        """
        Set the view-only mode for a chat thread.

        :param chatId: The ID of the chat thread to modify.
        :type chatId: str
        :param viewOnly: Whether to enable or disable view-only mode. Defaults to `True`.
        :type viewOnly: bool
        :param comId: The ID of the community where the chat thread is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        The `community` decorator is used to ensure that the user is logged in and the community ID is present.

        If `viewOnly` is `True`, the function sends a POST request to the API to enable view-only mode for the chat thread with the specified ID. Otherwise, view-only mode is disabled.

        `ApiResponse`:

        - `message`: A message indicating whether view-only mode was successfully enabled or disabled.
        - `statuscode`: The status code of the API response.
        - `duration`: The duration of the API request.
        - `timestamp`: The timestamp of the API request.

        **Example usage:**

        To enable view-only mode for a chat thread with ID "0000-0000-0000-0000":

        >>> response = client.community.set_view_only(chatId="0000-0000-0000-0000", viewOnly=True)
        ... if response.statuscode == 0:
        ...     print("View-only mode enabled successfully!")
        ... else:
        ...     print("Failed to enable view-only mode.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/view-only/enable" if viewOnly else f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/view-only/disable"
            ))


    @community
    def set_members_can_invite(self, chatId: str, canInvite: bool = True, comId: Union[str, int] = None, **kwargs) -> ApiResponse:
        """
        Sets whether members of a chat thread in the current or specified community can invite other members.

        :param chatId: The ID of the chat thread to set the members can invite status for.
        :type chatId: str
        :param canInvite: Whether members of the chat thread can invite other members. Defaults to True.
        :type canInvite: bool
        :param comId: The ID of the community where the chat thread is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to enable or disable the ability for members of a chat thread to invite other members in the specified community.

        `ApiResponse`:

        - `message` (str): A message indicating whether the setting was successfully changed.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To allow members of a chat thread with ID "1111-1111-1111-1111" to invite other members in the current community:

        >>> response = client.community.set_members_can_invite(chatId="1111-1111-1111-1111", canInvite=True)
        ... if response.statuscode == 0:
        ...     print("Members can invite status set successfully!")
        ... else:
        ...     print("Failed to set members can invite status.")

        To disable the ability for members of a chat thread with ID "2222-2222-2222-2222" to invite other members in a community with ID "3333":

        >>> response = client.community.set_members_can_invite(chatId="2222-2222-2222-2222", canInvite=False, comId=3333)
        ... if response.statuscode == 0:
        ...     print("Members can invite status disabled successfully!")
        ... else:
        ...     print("Failed to disable members can invite status.")
        """
        if "can_invite" in kwargs: #TODO: Remove in the near future.
            canInvite = kwargs["can_invite"]
            print("The 'can_invite' parameter is deprecated. Please use 'canInvite' instead.")

        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/members-can-invite/enable" if canInvite else f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/members-can-invite/disable"
            ))


    @community
    def change_chat_background(self, chatId: str, backgroundImage: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Changes the background image of a chat thread in the current or specified community.

        :param chatId: The ID of the chat thread to change the background image for.
        :type chatId: str
        :param backgroundImage: The URL or file path of the image to set as the background image of the chat thread. If None, the background image will be cleared.
        :type backgroundImage: str
        :param comId: The ID of the community where the chat thread is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to change the background image of a chat thread in the specified community. If no `backgroundImage` is provided, the background image will be cleared.

        `ApiResponse`:

        - `message` (str): A message indicating whether the background image was successfully changed.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To change the background image of a chat thread with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.change_chat_background(chatId="1111-1111-1111-1111", backgroundImage="https://example.com/background.jpg")
        ... if response.statuscode == 0:
        ...     print("Chat background changed successfully!")
        ... else:
        ...     print("Failed to change chat background.")

        To clear the background image of a chat thread with ID "2222-2222-2222-2222" in a community with ID "123":

        >>> response = client.community.change_chat_background(chatId="2222-2222-2222-2222", backgroundImage=None, comId=123)
        ... if response.statuscode == 0:
        ...     print("Chat background cleared successfully!")
        ... else:
        ...     print("Failed to clear chat background.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/member/{self.userId}/background",
            data = {
            "media": [[100, self.__handle_media__(media=backgroundImage, media_value=True), None]],
            "timestamp": int(time() * 1000)
            }))


    @community
    def solve_quiz(self, quizId: str, quizAnswers: Union[dict, list], hellMode: bool = False, comId: Union[str, int] = None) -> ApiResponse:
        """
        Submits answers to a quiz in the current or specified community.

        :param quizId: The ID of the quiz to solve.
        :type quizId: str
        :param quizAnswers: A dictionary or list of dictionaries containing the quiz answers. Each dictionary should have the keys "questionId" (str) and "answer" (str).
        :type quizAnswers: Union[dict, list]
        :param hellMode: Whether to solve the quiz in hell mode. Defaults to False.
        :type hellMode: bool
        :param comId: The ID of the community where the quiz is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to submit answers to a quiz in the specified community. The quiz answers should be provided as a dictionary or list of dictionaries with the keys "questionId" (str) and "answer" (str).

        If `hellMode` is True, the quiz will be solved in hell mode.

        `ApiResponse`:

        - `message` (str): A message indicating whether the quiz was successfully solved.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.
        - `mediaValue` (dict): The result of the quiz, including the user's score, rank, and prizes.

        **Example usage:**

        To solve a quiz with ID "1111-1111-1111-1111" in the current community:

        >>> answers = [{"questionId": "q1", "answer": "a1"}, {"questionId": "q2", "answer": "a2"}]
        >>> response = client.community.solve_quiz(quizId="1111-1111-1111-1111", quizAnswers=answers)
        ... if response.statuscode == 0:
        ...     print("Quiz solved successfully!")
        ... else:
        ...     print("Failed to solve quiz.")

        To solve a quiz with ID "2222-2222-2222-2222" in a community with ID "1234" in hell mode:

        >>> answers = {"questionId": "q1", "answer": "a1"}
        >>> response = client.community.solve_quiz(quizId="2222-2222-2222-2222", quizAnswers=answers, hellMode=True, comId=1234)
        ... if response.statuscode == 0:
        ...     print("Quiz solved successfully!")
        ... else:
        ...     print("Failed to solve quiz.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{quizId}/quiz/result",
            data = {
            "quizAnswerList": quizAnswers if isinstance(quizAnswers, list) else [quizAnswers],
            "mode": 1 if hellMode else 0,
            "timestamp": int(time() * 1000)
            }))


    @community
    def set_channel(self, chatId: str, comId: Union[str, int] = None) -> None:
        for i in range(2):
            self.bot.send_websocket_message({
                "o": {
                    "ndcId": self.community_id if comId is None else comId,
                    "threadId": chatId,
                    "joinRole": 1 if i == 0 else None,
                    "id": randint(0, 100)
                },
                "t": 112 if i == 0 else 200
                })

    @community
    def start_vc(self, chatId: str, comId: Union[str, int] = None) -> None:
        for i in range(2):
            self.bot.send_websocket_message({
                "o": {
                    "ndcId": self.community_id if comId is None else comId,
                    "threadId": chatId,
                    "joinRole": 1 if i == 0 else None,
                    "channelType": 1 if i == 1 else None,
                    "id": randint(0, 100)
                },
                "t": 112 if i == 0 else 108
            })


    @community
    def stop_vc(self, chatId: str, comId: Union[str, int] = None) -> None:
        self.bot.send_websocket_message({
            "o": {
                "ndcId": self.community_id if comId is None else comId,
                "threadId": chatId,
                "joinRole": 2,
                "id": randint(0, 100)
            },
            "t": 112
        })


    @community
    def disable_chat(self, chatId: str, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Disables a chat thread in the current or specified community.

        :param chatId: The ID of the chat thread to disable.
        :type chatId: str
        :param reason: An optional reason for disabling the chat thread.
        :type reason: str
        :param comId: The ID of the community where the chat thread is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to disable a chat thread in the specified community. If a reason is provided, the reason is included in the request data.

        `ApiResponse`:

        - `message` (str): A message indicating whether the chat thread was successfully disabled.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To disable a chat thread with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.disable_chat(chatId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Chat thread disabled successfully!")
        ... else:
        ...     print("Failed to disable chat thread.")

        To disable a chat thread with ID "2222-2222-2222-2222" in a community with ID "1234" and provide a reason:

        >>> response = client.community.disable_chat(chatId="2222-2222-2222-2222", reason="This chat thread violates community guidelines.", comId=1234)
        ... if response.statuscode == 0:
        ...     print("Chat thread disabled successfully!")
        ... else:
        ...     print("Failed to disable chat thread.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/chat/thread/{chatId}/admin",
            data = {
            "adminOpName": 110,
            "adminOpValue": 9,
            "timestamp": int(time() * 1000)
            } if reason is None else {
            "adminOpNote": {"content": reason},
            "adminOpName": 110,
            "adminOpValue": 9,
            "timestamp": int(time() * 1000)
            }))


    @community
    def disable_blog(self, blogId: str, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Disables a blog in the current or specified community.

        :param blogId: The ID of the blog to disable.
        :type blogId: str
        :param reason: An optional reason for disabling the blog.
        :type reason: str
        :param comId: The ID of the community where the blog is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to disable a blog in the specified community. If a reason is provided, the reason is included in the request data.

        `ApiResponse`:

        - `message` (str): A message indicating whether the blog was successfully disabled.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To disable a blog with ID "1111-1111-1111-1111" in the current community:

        >>> response = client.community.disable_blog(blogId="1111-1111-1111-1111")
        ... if response.statuscode == 0:
        ...     print("Blog disabled successfully!")
        ... else:
        ...     print("Failed to disable blog.")

        To disable a blog with ID "2222-2222-2222-2222" in a community with ID "123" and provide a reason:

        >>> response = client.community.disable_blog(blogId="2222-2222-2222-2222", reason="This blog violates community guidelines.", comId=123)
        ... if response.statuscode == 0:
        ...     print("Blog disabled successfully!")
        ... else:
        ...     print("Failed to disable blog.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/blog/{blogId}/admin",
            data = {
            "adminOpName": 110,
            "adminOpValue": 9,
            "timestamp": int(time() * 1000)
            } if reason is None else {
            "adminOpNote": {"content": reason},
            "adminOpName": 110,
            "adminOpValue": 9,
            "timestamp": int(time() * 1000)
            }))


    @community
    def hide_user(self, userId: str, reason: str = None, comId: Union[str, int] = None) -> ApiResponse:
        """
        Hides a user profile in the current or specified community.

        :param userId: The ID of the user to hide.
        :type userId: str
        :param reason: An optional reason for hiding the user.
        :type reason: str
        :param comId: The ID of the community where the user profile is located. If not provided, the current community ID is used.
        :type comId: Union[str, int]
        :return: An `ApiResponse` object containing information about the request status.
        :rtype: ApiResponse

        This function sends a POST request to the API to hide a user profile in the specified community. If a reason is provided, the reason is included in the request data.

        `ApiResponse`:

        - `message` (str): A message indicating whether the user was successfully hidden.
        - `statuscode` (int): The status code of the API response.
        - `duration` (str): The duration of the API request.
        - `timestamp` (str): The timestamp of the API request.

        **Example usage:**

        To hide a user with ID "0000-0000-0000-0000" in the current community:

        >>> response = client.community.hide_user(userId="0000-0000-0000-0000")
        ... if response.statuscode == 0:
        ...     print("User hidden successfully!")
        ... else:
        ...     print("Failed to hide user.")

        To hide a user with ID "1111-1111-1111-1111" in a community with ID "123" and provide a reason:

        >>> response = client.community.hide_user(userId="1111-1111-1111-1111", reason="This user violated community guidelines.", comId=123)
        ... if response.statuscode == 0:
        ...     print("User hidden successfully!")
        ... else:
        ...     print("Failed to hide user.")
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url = f"/x{self.community_id if comId is None else comId}/s/user-profile/{userId}/admin",
            data = {
            "adminOpName": 18,
            "timestamp": int(time() * 1000)
            } if reason is None else {
            "adminOpNote": {"content": reason},
            "adminOpName": 18,
            "timestamp": int(time() * 1000)
            }))
    
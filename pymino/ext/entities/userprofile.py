from typing import List, Union

class AvatarFrameNotFound:
	"""`AvatarFrameNotFound` - Class representing a avatar frame not found."""
	def __init__(self):
		pass

class AvatarFrame:
	"""
	`AvatarFrame` - Class representing a avatar frame.

	`Attributes`:
	- `_data` - The data containing the avatar frame.
	
	`Properties`:
	- `status` - The status of the request.
	- `ownership_status` - The ownership status of the avatar frame.
	- `version` - The version of the avatar frame.
	- `resource_url` - The resource url of the avatar frame.
	- `name` - The name of the avatar frame.
	- `icon` - The icon of the avatar frame.
	- `frame_type` - The frame type of the avatar frame.
	- `frame_id` - The frame id of the avatar frame.
	"""
	def __init__(self, data: dict):
		self._data = data

	@property
	def status(self) -> int:
		"""
		`status` - The status of the request.
		
		`Returns`:
		- `int` - The status of the request.
		"""
		return self._data.get('status')

	@property
	def ownership_status(self) -> str:
		"""
		`ownership_status` - The ownership status of the avatar frame.

		`Returns`:
		- `str` - The ownership status of the avatar frame.
		"""
		return self._data.get('ownershipStatus')

	@property
	def version(self) -> int:
		"""
		`version` - The version of the avatar frame.

		`Returns`:
		- `int` - The version of the avatar frame.
		"""
		return self._data.get('version')
		
	@property
	def resource_url(self) -> str:
		"""
		`resource_url` - The resource url of the avatar frame.

		`Returns`:
		- `str` - The resource url of the avatar frame.
		"""
		return self._data.get('resourceUrl')

	@property
	def name(self) -> str:
		"""
		`name` - The name of the avatar frame.

		`Returns`:
		- `str` - The name of the avatar frame.
		"""
		return self._data.get('name')

	@property
	def icon(self) -> str:
		"""
		`icon` - The icon of the avatar frame.
		
		`Returns`:
		- `str` - The icon of the avatar frame.
		"""
		return self._data.get('icon')

	@property
	def frame_type(self) -> int:
		"""
		`frame_type` - The frame type of the avatar frame.
		
		`Returns`:
		- `int` - The frame type of the avatar frame.
		"""
		return self._data.get('frameType')
		
	@property
	def frame_id(self) -> str:
		"""
		`frame_id` - The frame id of the avatar frame.
		
		`Returns`:
		- `str` - The frame id of the avatar frame.
		"""
		return self._data.get('frameId')

class InfluencerInfoNotFound:
	"""`InfluencerInfoNotFound` - Class representing a influencer info not found."""
	def __init__(self):
		pass

class InfluencerInfo:
	"""
	`InfluencerInfo` - Class representing a influencer info.

	`Attributes`:
	- `_data` - The data containing the influencer info.

	`Properties`:
	- `pinned` - The pinned status of the influencer info.
	- `created_time` - The created time of the influencer info.
	- `fans_count` - The fans count of the influencer info.
	- `monthly_fee` - The monthly fee of the influencer info.
	"""
	def __init__(self, data: dict):
		self._data = data

	@property
	def pinned(self) -> bool:
		"""
		`pinned` - The pinned status of the influencer.

		`Returns`:
		- `bool` - The pinned status of the influencer info.
		"""
		return self._data.get('pinned')

	@property
	def created_time(self) -> int:
		"""
		`created_time` - The influencer created time.

		`Returns`:
		- `int` - The created time of the influencer.
		"""
		return self._data.get('createdTime')

	@property
	def fans_count(self) -> int:
		"""
		`fans_count` - The fans count of the of the influencer.

		`Returns`:
		- `int` - The fans count of the influencer.
		"""
		return self._data.get('fansCount')

	@property
	def monthly_fee(self) -> int:
		"""
		`monthly_fee` - The monthly fee of the influencer.

		`Returns`:
		- `int` - The monthly fee of the influencer.
		"""
		return self._data.get('monthlyFee')

class CustomTitle:
    def __init__(self, data: dict):
        self._data = data

    @property
    def color(self) -> str:
        return self._data.get('color')

    @property
    def title(self) -> str:
        return self._data.get('title')

class UserExtensionsNotFound:
	"""`UserExtensionsNotFound` - Class representing a user extensions not found."""
	def __init__(self):
		pass		

class UserExtensions:
	def __init__(self, data: dict):
		self._data = data

	@property
	def privilege_of_comment_on_user_profile(self) -> int:
		return self._data.get('privilegeOfCommentOnUserProfile')
		
	@property
	def style(self) -> str:
		return self._data.get('style')
		
	@property
	def title_names(self) -> List[str]:
		titles_found = self._data.get('customTitles')
		return [title['title'] for title in titles_found] if titles_found else []

	@property
	def title_colors(self) -> List[str]:
		titles_found = self._data.get('customTitles')
		return [title['color'] for title in titles_found] if titles_found else []

	@property
	def titles(self) -> List[dict]:
		return self._data.get('customTitles', [])

	@property
	def privilege_of_chat_invite_request(self) -> int:
		return self._data.get('privilegeOfChatInviteRequest')

class MoodStickerNotFound:
	"""`MoodStickerNotFound` - Class representing a mood sticker not found."""
	def __init__(self):
		pass

class MoodSticker:
	"""
	`mood_sticker` - Mood sticker the user has set.

	`Returns:` MoodSticker | MoodStickerNotFound

	`Example`:
	```py
	>>> user = bot.community.fetch_user(0000-0000-0000-0000)
	>>> if isinstance(user.mood_sticker, MoodSticker):
	...	 print(user.mood_sticker.name)
	... else:
	...	 print('This user has no mood sticker set.')
	```
	"""
	def __init__(self, data: dict):
		self._data = data

	@property
	def status(self) -> int:
		"""
		`status` - is the status of request.

		`Returns`:
		- `int` - is the status of request.
		"""
		return self._data.get('status')

	@property
	def icon_v2(self) -> str:
		"""
		`icon_v2` - The icon v2 of the mood sticker.

		`Returns`:
		- `str` - The icon v2 of the mood sticker.
		"""
		return self._data.get('iconV2')

	@property
	def name(self) -> str:
		"""
		`name` - The name of the mood sticker.

		`Returns`:
		- `str` - The name of the mood sticker.
		"""
		return self._data.get('name')

	@property
	def sticker_id(self) -> int:
		"""
		`sticker_id` - The sticker id of the mood sticker.

		`Returns`:
		- `int` - The sticker id of the mood sticker.
		"""
		return self._data.get('stickerId')

	@property
	def small_icon_v2(self) -> str:
		"""
		`small_icon_v2` - The small icon v2 of the mood sticker.

		`Returns`:
		- `str` - The small icon v2 of the mood sticker.
		"""
		return self._data.get('smallIconV2')

	@property
	def small_icon(self) -> str:
		"""
		`small_icon` - The small icon of the mood sticker.

		`Returns`:
		- `str` - The small icon of the mood sticker.
		"""
		return self._data.get('smallIcon')

	@property
	def sticker_collection_id(self) -> int:
		"""
		`sticker_collection_id` - The sticker collection id of the mood sticker.

		`Returns`:
		- `int` - The sticker collection id of the mood sticker.
		"""
		return self._data.get('stickerCollectionId')

	@property
	def medium_icon(self) -> str:
		"""
		`medium_icon` - The medium icon of the mood sticker.

		`Returns`:
		- `str` - The medium icon of the mood sticker.
		"""
		return self._data.get('mediumIcon')

	@property
	def extensions(self) -> str:
		"""
		`extensions` - The extensions of the mood sticker.

		`Returns`:
		- `str` - The extensions of the mood sticker.
		"""
		return self._data.get('extensions')

	@property
	def used_count(self) -> int:
		"""
		`used_count` - The used count of the mood sticker.

		`Returns`:
		- `int` - The used count of the mood sticker.
		"""
		return self._data.get('usedCount')

	@property
	def medium_icon_v2(self) -> str:
		"""
		`medium_icon_v2` - The medium icon v2 of the mood sticker.

		`Returns`:
		- `str` - The medium icon v2 of the mood sticker.
		"""
		return self._data.get('mediumIconV2')

	@property
	def created_time(self) -> int:
		"""
		`created_time` - The created time of the mood sticker.

		`Returns`:
		- `int` - The created time of the mood sticker.
		"""
		return self._data.get('createdTime')

	@property
	def icon(self) -> str:
		"""
		`icon` - The icon of the mood sticker.

		`Returns`:
		- `str` - The icon of the mood sticker.
		"""
		return self._data.get('icon')

class UserProfile:
	"""
	`UserProfile` - Class representing a user profile.

	`Attributes`:
	- `_data` - The data containing the user profile.
	
	`Properties`:
	- `status` - is the status of request.
	- `mood_sticker` - Mood sticker the user has set.
	- `wiki_count` - The amount of wiki the user has created.
	- `consecutive_check_in_days` - The amount of consecutive days the user has checked in.
	- `uid` - The user id of the user.
	- `modified_time` - The time the user profile was last modified.
	- `following_status` - The following status of the user.
	- `online_status` - The online status of the user.
	- `account_membership_status` - The account membership status of the user.
	- `is_global` - Is the user a global user.
	- `avatar_frame_id` - The avatar frame id of the user.
	- `reputation` - The reputation of the user.
	- `posts_count` - The amount of posts the user has created.
	- `avatar_frame` - The avatar frame of the user.
	- `members_count` - The amount of members the user has.
	- `nickname` - The nickname of the user.
	- `media_list` - The media list of the user.
	- `icon` - The icon of the user.
	- `is_nickname_verified` - Is the nickname of the user verified.
	- `mood` - The mood of the user.
	- `level` - The level of the user.
	- `notification_subscription_status` - The notification subscription status of the user.
	- `settings` - The settings of the user.
	- `push_enabled` - Is the push enabled of the user.
	- `membership_status` - The membership status of the user.
	- `influencer_info` - The influencer info of the user.
	- `content` - The user's profile content.
	- `follower_count` - The amount of followers the user has.
	- `role` - The role of the user.
	- `comments_count` - The amount of comments the user has on their wall.
	- `ndc_id` - The community id the user is in.
	- `created_time` - The time the user was created.
	- `extensions` - The extensions of the user.
	- `stories_count` - The amount of stories the user has created.
	- `blogs_count` - The amount of blogs the user has created.
	"""
	def __init__(self, data: dict):
		self._data = data.get('userProfile', data)
	
	@property
	def status(self) -> int:
		"""
		`status` - is the status of request.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.status)
		```
		"""
		return self._data.get('status', None)

	@property
	def mood_sticker(self) -> Union[MoodSticker, MoodStickerNotFound]:
		"""
		`mood_sticker` - Mood sticker the user has set.

		`Returns:` MoodSticker | MoodStickerNotFound

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> if isinstance(user.mood_sticker, MoodSticker):
		...	 print(user.mood_sticker.name)
		... else:
		...	 print('This user has no mood sticker set.')
		```
		"""
		moodSticker = self._data.get('moodSticker')
		return MoodSticker(moodSticker) if moodSticker else MoodStickerNotFound()
		
	@property
	def wiki_count(self) -> int:
		"""
		`wiki_count` - The amount of wiki the user has created.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.wiki_count)
		```
		"""
		return self._data.get('itemsCount', None)

	@property
	def consecutive_check_in_days(self) -> int:
		"""
		`consecutiveCheckInDays` - The amount of consecutive days the user has checked in.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.consecutive_check_in_days)
		```
		"""
		return self._data.get('consecutiveCheckInDays', None)

	@property
	def uid(self) -> str:
		"""
		`uid` - The user's uid.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.uid)
		```
		"""
		return self._data.get('uid', None)

	@property
	def userId(self) -> str:
		"""
		`userId` - The user's uid.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.userId)
		```
		"""
		return self.uid

	@property
	def aminoId(self) -> str:
		"""
		`aminoId` - The user's amino id.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.aminoId)
		```
		"""
		return self._data.get('aminoId', None)

	@property
	def modified_time(self) -> str:
		"""
		`modifiedTime` - The time the user's profile was last modified.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.modified_time)
		```
		"""
		return self._data.get('modifiedTime', None)

	@property
	def following_status(self) -> int:
		"""
		`followingStatus` - Whether the user is following the current user.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.following_status)
		```
		"""
		return self._data.get('followingStatus', None)

	@property
	def online_status(self) -> int:
		"""
		`onlineStatus` - The user's online status.
		
		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.online_status)
		```
		"""
		return self._data.get('onlineStatus', None)

	@property
	def account_membership_status(self) -> int:
		"""
		`account_membership_status` - The user's account membership status.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.account_membership_status)
		```
		"""
		return self._data.get('accountMembershipStatus', None)

	@property
	def is_global(self) -> bool:
		"""
		`is_global` - Whether the user is a global user.

		`Returns:` bool | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.is_global)
		```
		"""
		return self._data.get('isGlobal', None)

	@property
	def avatar_frame_id(self) -> str:
		"""
		`avatar_frame_id` - The user's avatar frame id.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.avatar_frame_id)
		```
		"""
		return self._data.get('avatarFrameId', None)

	@property
	def fan_club_list(self) -> list:
		"""
		`fan_club_list` - The user's fan club list.

		`Returns:` list | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.fan_club_list)
		```
		"""
		return self._data.get('fanClubList', None)

	@property
	def reputation(self) -> int:
		"""
		`reputation` - The user's reputation.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.reputation)
		```
		"""
		return self._data.get('reputation', None)

	@property
	def posts_count(self) -> int:
		"""
		`posts_count` - The amount of posts the user has created.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.posts_count)
		```
		"""
		return self._data.get('postsCount', None)

	@property
	def avatar_frame(self) -> Union[AvatarFrame, AvatarFrameNotFound]:
		"""
		`avatar_frame` - The user's avatar frame.
		
		`Returns:` dict | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> if isinstance(user.avatar_frame, AvatarFrame):
		...     print(user.avatar_frame.name)
		... else:
		...     print('Avatar frame not found.')
		```
		"""
		return AvatarFrame(self._data.get('avatarFrame', None))

	@property
	def follower_count(self) -> int:
		"""
		`follower_count` - The amount of followers the user has.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.follower_count)
		```
		"""
		return self._data.get('membersCount', None)	

	@property
	def nickname(self) -> str:
		"""
		`nickname` - The user's nickname.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.nickname)
		```
		"""
		return self._data.get('nickname', None)

	@property
	def username(self) -> str:
		"""
		`username` - The user's username.
		
		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.username)
		```
		"""
		return self.nickname

	@property
	def media_list(self) -> list:
		"""
		`mediaList` - The user's media list.

		`Returns:` list | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.media_list)
		```
		"""
		return self._data.get('mediaList', None)

	@property
	def icon(self) -> str:
		"""
		`icon` - The user's icon.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.icon)
		```
		"""
		return self._data.get('icon', None)

	@property
	def avatar(self) -> str:
		"""
		`avatar` - The user's avatar.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.avatar)
		```
		"""
		return self.icon

	@property
	def is_nickname_verified(self) -> bool:
		"""
		`isNicknameVerified` - The user's nickname verification status.

		`Returns:` bool | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.is_nickname_verified)
		```
		"""
		return self._data.get('isNicknameVerified', None)

	@property
	def mood(self) -> str:
		"""
		`mood` - The user's mood.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.mood)
		```
		"""
		return self._data.get('mood', None)

	@property
	def level(self) -> int:
		"""
		`level` - The user's level.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.level)
		```
		"""
		return self._data.get('level', None)

	@property
	def push_enabled(self) -> bool:
		"""
		`pushEnabled` - The user's push notification status.

		`Returns:` bool | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.push_enabled)
		```
		"""
		return self._data.get('pushEnabled', None)

	@property
	def membership_status(self) -> int:
		"""
		`membershipStatus` - The user's membership status.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.membership_status)
		```
		"""
		return self._data.get('membershipStatus', None)

	@property
	def influencer_info(self) -> Union[InfluencerInfo, InfluencerInfoNotFound]:
		"""
		`influencerInfo` - The user's influencer info.

		`Returns:` dict | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> if isinstance(user.influencer_info, InfluencerInfo):
		...     print(user.influencer_info)
		... else:
		...     print("User influencer info not found.")
		```
		"""
		return InfluencerInfo(self._data.get('influencerInfo', None))

	@property
	def content(self) -> str:
		"""
		`content` - The user's profile content.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.content)
		```
		"""
		return self._data.get('content', None)

	@property
	def following_count(self) -> int:
		"""
		`followingCount` - The amount of users the user is following.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.following_count)
		```
		"""
		return self._data.get('membersCount', None)

	@property
	def role(self) -> int:
		"""
		`role` - The user's role.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.role)
		```
		"""
		return self._data.get('role', None)

	@property
	def comments_count(self) -> int:
		"""
		`commentsCount` - The amount of comments the user has on their wall.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.comments_count)
		```
		"""
		return self._data.get('commentsCount', None)

	@property
	def ndcId(self) -> int:
		"""
		`ndcId` - The community the user is in.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.ndcId)
		```
		"""
		return self._data.get('ndcId', None)

	@property
	def comId(self) -> int:
		"""
		`comId` - The community the user is in.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.comId)
		```
		"""
		return self._data.get('ndcId', None)

	@property
	def created_time(self) -> str:
		"""
		`createdTime` - The time the user was created.

		`Returns:` str | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.created_time)
		```
		"""
		return self._data.get('createdTime', None)

	@property
	def extensions(self) -> Union[UserExtensions, UserExtensionsNotFound]:
		"""
		`extensions` - The user's extensions.

		`Returns:` dict | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> if isinstance(user.extensions, UserExtensions):
		...     print(user.extensions)
		... else:
		...     print("No extensions found.")
		```
		"""
		return UserExtensions(self._data.get('extensions', None))

	@property
	def visit_privacy(self) -> int:
		"""
		`visitPrivacy` - The user's visit privacy.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.visit_privacy)
		```
		"""
		return self._data.get('visitPrivacy', None)

	@property
	def stories_count(self) -> int:
		"""
		`storiesCount` - The amount of stories the user has.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.stories_count)
		```
		"""
		return self._data.get('storiesCount', None)

	@property
	def blogs_count(self) -> int:
		"""
		`blogsCount` - The amount of blogs the user has.

		`Returns:` int | None

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.blogs_count)
		```
		"""
		return self._data.get('blogsCount', None)

	def json(self) -> dict:
		"""
		`json` - The json response from the api.
		
		`Returns:` dict

		`Example`:
		```py
		>>> user = bot.community.fetch_user(0000-0000-0000-0000)
		>>> print(user.json())
		```
		"""
		return self._data

class OnlineMembers:
	"""
	`OnlineMembers` - The online members of a community.
	
	`Attributes`:
	- `_data` - The json response from the api.
	- `_user` - The user's data.

	`Properties`:
	- `topic` - The community's topic.
	- `ndcId` - The community's id.
	- `comId` - The community's id.
	- `users_online` - The amount of users online.
	- `is_guest` - If the user is a guest.
	- `uid` - The user's id.
	- `userId` - The user's id.
	- `status` - The user's status.
	- `icon` - The user's icon.
	- `avatar` - The user's icon.
	- `reputation` - The user's reputation.
	- `role` - The user's role.
	- `nickname` - The user's nickname.
	- `username` - The user's nickname.
	- `level` - The user's level.
	- `extensions` - The user's extensions.
	- `account_membership_status` - The user's account membership status.
	- `avatar_frame_id` - The user's avatar frame id.
	- `avatar_frame` - The user's avatar frame.
	- `is_nickname_verified` - If the user's nickname is verified.
	- `json` - The json response from the api.
	"""
	def __init__(self, data: dict):
		self._data = data.get('o', data)
		self._user: dict = self._data.get('userProfileList', None)[0]

	@property
	def topic(self) -> str:
		"""
		`topic` - The community's topic.
		
		`Returns:` str | None
		"""
		return self._data.get('topic', None)
	
	@property
	def ndcId(self) -> str:
		"""
		`ndcId` - The community's id.

		`Returns:` str | None
		"""
		return self._data.get('ndcId', None)

	@property
	def comId(self) -> str:
		"""
		`comId` - The community's id.
		
		`Returns:` str | None
		"""
		return self.ndcId

	@property
	def users_online(self) -> int:
		"""
		`usersOnline` - The amount of users online.
		
		`Returns:` int | None
		"""
		return self._data.get('userProfileCount', None)

	@property
	def is_guest(self) -> bool:
		"""
		`isGuest` - If the user is a guest.
		
		`Returns:` bool | None
		"""
		return self._user.get('isGuest', None)

	@property
	def uid(self) -> str:
		"""
		`uid` - The user's id.
		
		`Returns:` str | None
		"""
		return self._user.get('uid', None)

	@property
	def userId(self) -> str:
		"""
		`userId` - The user's id.
		
		`Returns:` str | None
		"""
		return self.uid

	@property
	def status(self) -> str:
		"""
		`status` - The user's status.
		
		`Returns:` str | None
		"""
		return self._user.get('status', None)

	@property
	def icon(self) -> str:
		"""
		`icon` - The user's icon.
		
		`Returns:` str | None
		"""
		return self._user.get('icon', None)

	@property
	def avatar(self) -> str:
		"""
		`avatar` - The user's icon.
		
		`Returns:` str | None
		"""
		return self.icon

	@property
	def reputation(self) -> int:
		"""
		`reputation` - The user's reputation.
		
		`Returns:` int | None
		"""
		return self._user.get('reputation', None)

	@property
	def role(self) -> str:
		"""
		`role` - The user's role.
		
		`Returns:` str | None
		"""
		return self._user.get('role', None)

	@property
	def nickname(self) -> str:
		"""
		`nickname` - The user's nickname.
		
		`Returns:` str | None
		"""
		return self._user.get('nickname', None)

	@property
	def username(self) -> str:
		"""
		`username` - The user's nickname.
		
		`Returns:` str | None
		"""
		return self.nickname

	@property
	def level(self) -> int:
		"""
		`level` - The user's level.
		
		`Returns:` int | None
		"""
		return self._user.get('level', None)

	@property
	def extensions(self) -> UserExtensions:
		"""
		`extensions` - The user's extensions.
		
		`Returns:` UserExtensions | None
		
		`Example:`
		```py
		>>> user = OnlineUser(...)
		>>> if isinstance(user.extensions, UserExtensions):
		...     print(user.extensions.(...))
		... else:
		...     print('No extensions')
		```
		"""
		return UserExtensions(self._user.get('extensions', None))

	@property
	def account_membership_status(self) -> str:
		"""
		`accountMembershipStatus` - The user's account membership status.

		`Returns:` str | None
		"""
		return self._user.get('accountMembershipStatus', None)

	@property
	def avatar_frame_id(self) -> str:
		"""
		`avatarFrameId` - The user's avatar frame id.

		`Returns:` str | None
		"""
		return self._user.get('avatarFrameId', None)

	@property
	def avatar_frame(self) -> AvatarFrame:
		"""
		`avatarFrame` - The user's avatar frame.

		`Returns:` AvatarFrame | None

		`Example:`
		```py
		>>> user = OnlineUser(...)
		>>> if isinstance(user.avatar_frame, AvatarFrame):
		...     print(user.avatar_frame.(...))
		... else:
		...     print('No avatar frame')
		```
		"""
		return AvatarFrame(self._user.get('avatarFrame', None))

	@property
	def is_nickname_verified(self) -> bool:
		"""
		`isNicknameVerified` - If the user's nickname is verified.

		`Returns:` bool | None
		"""
		return self._user.get('isNicknameVerified', None)

	def json(self):
		"""
		`Returns:`
		- Api response in json format.
		"""
		return self._data

class UserProfileList:
	def __init__(self, data: dict):
		self._data = data.get("userProfileList", data) if isinstance(data, dict) else data

		parser:							list = [UserProfile(x) for x in self._data]
		self.status:					list = [x.status for x in parser]
		self.mood_sticker:				list = [x.mood_sticker for x in parser]
		self.wiki_count:				list = [x.wiki_count for x in parser]
		self.consecutive_check_in_days:	list = [x.consecutive_check_in_days for x in parser]
		self.uid:						list = [x.uid for x in parser]
		self.userId:					list = self.uid
		self.modified_time:				list = [x.modified_time for x in parser]
		self.following_status:			list = [x.following_status for x in parser]
		self.online_status:				list = [x.online_status for x in parser]
		self.account_membership_status:	list = [x.account_membership_status for x in parser]
		self.is_global:					list = [x.is_global for x in parser]
		self.avatar_frame_id:			list = [x.avatar_frame_id for x in parser]
		self.fan_club_list:				list = [x.fan_club_list for x in parser]
		self.reputation:				list = [x.reputation for x in parser]
		self.posts_count:				list = [x.posts_count for x in parser]
		#self.avatar_frame:				list = [x.avatar_frame for x in parser]
		self.follower_count:			list = [x.follower_count for x in parser]
		self.nickname:					list = [x.nickname for x in parser]
		self.username:					list = self.nickname
		self.media_list:				list = [x.media_list for x in parser]
		self.icon:						list = [x.icon for x in parser]
		self.avatar:					list = self.icon
		self.is_nickname_verified:		list = [x.is_nickname_verified for x in parser]
		self.mood:						list = [x.mood for x in parser]
		self.level:						list = [x.level for x in parser]
		self.pushEnabled:				list = [x.push_enabled for x in parser]
		self.membership_status:			list = [x.membership_status for x in parser]
		#self.influencer_info:			list = [x.influencer_info for x in parser]
		self.content:					list = [x.content for x in parser]
		self.following_count:			list = [x.following_count for x in parser]
		self.role:						list = [x.role for x in parser]
		self.comments_count:			list = [x.comments_count for x in parser]
		self.ndcId:						list = [x.ndcId for x in parser]
		self.comId:						list = self.ndcId
		self.created_time:				list = [x.created_time for x in parser]
		#self.extensions:				list = [x.extensions for x in parser]
		self.visit_privacy:				list = [x.visit_privacy for x in parser]
		self.stories_count:				list = [x.stories_count for x in parser]
		self.blogs_count:				list = [x.blogs_count for x in parser]
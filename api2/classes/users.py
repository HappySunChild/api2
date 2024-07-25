# https://friends.roblox.com/docs/index.html
# https://users.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse

from .base import BaseData
from .badges import UserBadge
from ..enums import AssetType, UserThumbnailSize, UserThumbnailType, OutfitType
from ..utility.fetcher import PageIterator, SortOrder

if TYPE_CHECKING:
	from ..client import Client
	from ..types import UserOrId

class FriendRequest(BaseData):
	def __init__(self, client: Client, data: dict) -> None:
		friend_request_data = data['friendRequest']
		
		self.client = client
		
		self.id = friend_request_data.get('senderId')
		self.source_universe_id = friend_request_data.get('sourceUniverseId')
		self.origin_source_type = friend_request_data.get('originSourceType')
		self.contact_name = friend_request_data.get('contactName')
		self.sent_at = parse(friend_request_data['sentAt']).timestamp()
		
		self.origin_user = User(client, data) # why does friend request contain the same information as a user who knows
	
	def accept(self):
		client = self.client
		client.fetcher.post(
			url=client.url_generator.get_url('friends', f'v1/users/{self.id}/accept-friend-request')
		)
	
	def decline(self):
		client = self.client
		client.fetcher.post(
			url=client.url_generator.get_url('friends', f'v1/users/{self.id}/decline-friend-request')
		)
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.origin_user.fullname}>'

class BaseUser(BaseData):
	def get_presence(self):
		presences = self.client.presence.get_user_presences([self.id])
		
		try:
			return presences[0]
		except IndexError:
			return None
	
	
	def get_friends(self) -> list[Friend]:
		client = self.client
		
		friends_json, _ = client.fetcher.get(
			url=client.url_generator.get_url('friends', f'v1/users/{self.id}/friends')
		)
		
		friends_data = None
		
		try:
			friends_data = friends_json['data']
		except:
			friends_data = []
		
		return [Friend(client, data) for data in friends_data]
	
	def get_mutuals_with(self, other: UserOrId):
		if isinstance(other, int):
			other = BaseUser(self.client, other)
		
		mutuals = []
		
		friends = self.get_friends()
		other_friends = other.get_friends()
		
		mutuals = [friend if friend in other_friends else None for friend in friends]
		
		for _ in range(mutuals.count(None)):
			mutuals.remove(None)
		
		return mutuals
	
	
	def get_currency(self):
		return self.client.economy.get_user_currency(self.id)
	
	
	def get_badges(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Descending):
		client = self.client
		
		return PageIterator(
			fetcher=client.fetcher,
			url=client.url_generator.get_url('badges', f'v1/users/{self.id}/badges'),
			sort_order=sort_order,
			page_size=page_size,
			handler=lambda data: UserBadge(client, data)
		)
	
	def get_games(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending):
		from .universes import Universe
		
		client = self.client
		
		return PageIterator(
			fetcher=client.fetcher,
			url=client.url_generator.get_url('games', f'v2/users/{self.id}/games'),
			page_size=page_size,
			sort_order=sort_order,
			handler=lambda data: Universe(client, data)
		)
	
	def get_inventory(self, asset_type: AssetType, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending):
		client = self.client
		
		return client.inventory.get_user_inventory(
			user_id=self.id,
			asset_type=asset_type,
			page_size=page_size,
			sort_order=sort_order
		)
	
	
	def get_thumbnail(self, type: UserThumbnailType = UserThumbnailType.Bust, size: UserThumbnailSize = UserThumbnailSize.Medium, is_circular: bool = False):
		return self.client.thumbnails.get_user_thumbnails([self.id], type=type, size=size, is_circular=is_circular)[0]
	
	
	def get_outfits(self, outfit_type: OutfitType = OutfitType.Avatar, page_size: int = 25, is_editable: bool = True):
		return self.client.avatar.get_user_outfits(self.id, outfit_type=outfit_type, page_size=page_size, is_editable=is_editable)
	
	def get_avatar_details(self):
		return self.client.avatar.get_user_avatar_details(self.id)
	
	def get_avatar_asset_ids(self) -> list[int]:
		return self.client.avatar.get_user_currently_wearing(self.id)
	
	@property
	def can_view_inventory(self):
		return self.client.inventory.can_view_inventory(self.id)
	
	@property
	def has_premium(self):
		has_premium = self.client.economy.get_user_has_premium(self.id)
		
		return has_premium
	
	@property
	def link(self):
		return f'https://www.roblox.com/users/{self.id}/profile'
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.id}>'


class PartialUser(BaseUser):
	def __init__(self, client: Client, data: dict):
		super().__init__(client, data.get('userId', data.get('id')))
		
		self.raw = data
		
		self.name = data.get('username', data.get('name'))
		self.display_name = data.get('displayName')
	
	@property
	def fullname(self):
		return f'{self.display_name} @{self.name}'
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.fullname}>'

class User(PartialUser):
	def __init__(self, client: Client, data: dict):
		super().__init__(client, data)
		
		self.description = data.get('description')
		
		self.is_banned = data.get('isBanned')
		self.has_verified_badge = data.get('hasVerifiedBadge')
		
		if data.get('created'):
			self.created = parse(data.get('created')).timestamp()
	
	def update_info(self):
		client = self.client
		
		user_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('users', f'v1/users/{self.id}')
		)
		
		self.__init__(client, user_data)


class AuthenticatedUser(User):
	def __init__(self, client: Client, data: dict):
		super().__init__(client, data)
	
	def follow_user(self, target_id: int):
		client = self.client
		_, res = client.fetcher.post(
			url=client.url_generator.get_url('friends', f'v1/users/{target_id}/follow')
		)
		
		return res
	
	def unfollow_user(self, target_id: int):
		client = self.client
		_, res = client.fetcher.post(
			url=client.url_generator.get_url('friends', f'v1/users/{target_id}/unfollow')
		)
		
		return res
	
	
	def get_friend_requets(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Descending):
		client = self.client
		
		return PageIterator(
			fetcher=client.fetcher,
			url=client.url_generator.get_url('friends', 'v1/my/friends/requests'),
			page_size=page_size,
			sort_order=sort_order,
			handler=lambda data: FriendRequest(client, data)
		)
	
	def send_friend_request(self, target_id: int):
		client = self.client
		_, res = client.fetcher.post(
			url=client.url_generator.get_url('friends', f'v1/users/{target_id}/request-friendship')
		)
		
		return res
	
	def unfriend_user(self, target_id: int):
		client = self.client
		client.fetcher.post(
			url=client.url_generator.get_url('friends', f'v1/users/{target_id}/unfriend')
		)

class Friend(User):
	def __init__(self, client: Client, data: dict):
		super().__init__(client, data)
		
		self.is_online = data.get('isOnline')
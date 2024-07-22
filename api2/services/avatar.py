# https://avatar.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseprovider import BaseProvider
from ..enums import AvatarType, OutfitType
from ..utility.fetcher import PageIterator
from ..classes.badges import BaseData

if TYPE_CHECKING:
	from ..types import UserOrId
	from ..client import Client

class AvatarScales:
	def __init__(self, scale_data: dict) -> None:
		self.body_type = scale_data.get('bodyType')
		self.propertion = scale_data.get('proportion')
		
		self.height_scale = scale_data.get('height')
		self.width_scale = scale_data.get('width')
		self.head_scale = scale_data.get('head')
		self.depth_scale = scale_data.get('depth')

class AvatarBodyColors:
	def __init__(self, color_data: dict) -> None:
		self.head_color = color_data['headColor3']
		self.torso_color = color_data['torsoColor3']
		self.right_arm_color = color_data['rightArmColor3']
		self.left_arm_color = color_data['leftArmColor3']
		self.right_leg_color = color_data['rightLegColor3']
		self.left_leg_color = color_data['leftLegColor3']

class AvatarDetails:
	def __init__(self, data: dict) -> None:
		self.avatar_type = AvatarType(data['playerAvatarType'])
		
		self.scales = AvatarScales(data['scales'])
		self.body_colors = AvatarBodyColors(data['bodyColor3s'])
		
		self.default_shirt_applied = data['defaultShirtApplied']
		self.default_pants_applied = data['defaultPantsApplied']
		
		self.assets = data['assets']
		self.emotes = data['emotes']

class Outfit(BaseData):
	def __init__(self, client: Client, outfit_data: dict) -> None:
		super().__init__(client, outfit_data['id'])
		
		self.name = outfit_data['name']
		self.is_editable = outfit_data['isEditable']
	
	def get_thumbnail(self):
		return self.client.thumbnails.get_outfit_thumbnails([self.id])[0]
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.name} {self.id}>'

class AvatarProvider(BaseProvider):
	def get_user_outfits(self, user: UserOrId, outfit_type: OutfitType = OutfitType.Avatar, page_size: int = 25, is_editable: bool = True):
		client = self.client
		
		return PageIterator(
			fetcher=client.fetcher,
			url=client.url_generator.get_url('avatar', f'v2/avatar/users/{int(user)}/outfits'),
			page_size=page_size,
			handler=lambda data: Outfit(client, data),
			
			itemsPerPage = page_size,
			outfitType = outfit_type,
			isEditable = is_editable
		)
	
	def get_user_currently_wearing(self, user: UserOrId):
		client = self.client
		
		avatar_json, _ = client.fetcher.get(
			url=client.url_generator.get_url('avatar', f'v1/users/{int(user)}/currently-wearing')
		)
		
		asset_ids = None
		
		try:
			asset_ids = avatar_json['assetIds']
		except:
			asset_ids = []
		
		return asset_ids
	
	def get_user_avatar_details(self, user: UserOrId):
		client = self.client
		
		avatar_details_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('avatar', f'v2/avatar/users/{int(user)}/avatar')
		)
		
		return AvatarDetails(avatar_details_data)
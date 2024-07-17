# https://thumbnails.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from ..enums import UniverseThumbnailSize, ThumbnailFormat, ThumbnailState, UserThumbnailSize, UserThumbnailType, PlaceThumbnailPolicy, PlaceThumbnailSize

if TYPE_CHECKING:
	from ..types import UserOrId, PlaceOrId, UniverseOrId, BadgeOrId
	from ..client import Client

class Thumbnail:
	def __init__(self, thumbnail_data: dict) -> None:
		self.image_url = thumbnail_data['imageUrl']
		self.target_id = thumbnail_data['targetId']
		
		self.version = thumbnail_data['version']
		self.state = ThumbnailState(thumbnail_data['state'])
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.image_url!r}>'

class UniverseThumbnails:
	def __init__(self, universe_thumbnail_data: dict) -> None:
		self.universe_id = universe_thumbnail_data['universeId']
		self.thumbnails = [
			Thumbnail(thumbnail_data)
			for thumbnail_data in universe_thumbnail_data['thumbnails']
		]

class ThumbnailProvider:
	def __init__(self, client: Client) -> None:
		self.client = client
	
	def get_badge_icons(
			self,
			badges: list[BadgeOrId],
			is_circular: bool = False,
			format: ThumbnailFormat = ThumbnailFormat.Png
		):
		
		client = self.client
		
		thumbnail_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('thumbnails', 'v1/badges/icons'),
			params={
				'badgeIds': list(map(int, badges)),
				'size': '150x150',
				'isCircular': is_circular,
				'format': format.value
			}
		)
		
		return [
			Thumbnail(data)
			for data in thumbnail_data['data']
		]
	
	def get_places_icons(
			self,
			places: list[PlaceOrId],
			size: PlaceThumbnailSize = PlaceThumbnailSize.Medium,
			policy: PlaceThumbnailPolicy = PlaceThumbnailPolicy.Placeholder,
			is_circular: bool = False,
			format: ThumbnailFormat = ThumbnailFormat.Png
		):
		
		client = self.client
		
		thumbnail_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('thumbnails', 'v1/places/gameicons'),
			params={
				'placeIds': list(map(int, places)),
				'isCircular': is_circular,
				'returnPolicy': policy.value,
				'size': size.value,
				'format': format.value
			}
		)
		
		return [
			Thumbnail(data)
			for data in thumbnail_data['data']
		]
	
	def get_user_thumbnails(
			self,
			users: list[UserOrId],
			type: UserThumbnailType = UserThumbnailType.FullBody,
			size: UserThumbnailSize = UserThumbnailSize.Medium,
			is_circular: bool = False,
			format: ThumbnailFormat = ThumbnailFormat.Png
		):
		
		client = self.client
		
		thumbnail_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('thumbnails', f'v1/users/{type.value}'),
			params={
				'userIds': users,
				'isCircular': is_circular,
				'size': size.value,
				'format': format.value
			}
		)
		
		return [
			Thumbnail(data)
			for data in thumbnail_data['data']
		]
	
	def get_universe_thumbnails(
			self,
			universes: list[UniverseOrId],
			size: UniverseThumbnailSize = UniverseThumbnailSize.Medium,
			is_circular: bool = False,
			count_per_universe: int = 1,
			defaults: bool = True,
			format: ThumbnailFormat = ThumbnailFormat.Png
		):
		
		client = self.client
		
		thumbnail_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('thumbnails', 'v1/games/multiget/thumbnails'),
			params={
				'universeIds': list(map(int, universes)),
				'countPerUniverse': count_per_universe,
				'defaults': defaults,
				'isCircular': is_circular,
				'size': size.value,
				'format': format.value
			}
		)
		
		return [
			UniverseThumbnails(data)
			for data in thumbnail_data['data']
		]
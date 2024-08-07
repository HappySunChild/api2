from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse

from .base import BaseData
from .places import BasePlace
from ..utility.fetcher import PageIterator
from ..enums import UniverseThumbnailSize

if TYPE_CHECKING:
	from ..client import Client

class BaseUniverse(BaseData):
	def get_thumbnail_container(self, size: UniverseThumbnailSize = UniverseThumbnailSize.Medium, count: int = 1, is_circular: bool = False):
		return self.client.thumbnails.get_universe_thumbnails([self.id], size=size, count_per_universe=count, is_circular=is_circular)[0]
	
	def get_thumbnails(self, size: UniverseThumbnailSize = UniverseThumbnailSize.Medium, count: int = 1, is_circular: bool = False):
		return self.get_thumbnail_container(size=size, count=count, is_circular=is_circular).thumbnails
	
	def get_badges(self, page_size: int = 10):
		from .badges import Badge
		
		client = self.client
		
		return PageIterator(
			fetcher=client.fetcher,
			url=client.url_generator.get_url('badges', f'v1/universes/{self.id}/badges'),
			page_size=page_size,
			handler=lambda data: Badge(client, data)
		)
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.id}>'

class PartialUniverse(BaseUniverse):
	def __init__(self, client: Client, data: dict):
		super().__init__(client, data['id'])
		
		self.name = data.get('name')
		
		place_id = None
		
		if data.get('rootPlace'):
			place_id = data['rootPlace']['id']
		else:
			place_id = data.get('rootPlaceId')
		
		self.root_place = BasePlace(client, place_id)
	
	@property
	def link(self):
		return self.root_place.link

class Universe(PartialUniverse):
	def __init__(self, client: Client, data: dict):
		super().__init__(client, data)
		
		self.raw = data
		
		self.description = data.get('description')
		
		self.playing = data.get('playing')
		self.visits = data.get('visits')
		self.max_players = data.get('maxPlayers')
		
		self.is_favorited = data.get('isFavoritedByUser')
		self.favorited_count = data.get('favoritedCount')
		
		self.is_genre_enforced = data.get('isGenreEnforced')
		self.genre = data.get('genre')
		self.price = data.get('price')
		self.copying_allowed = data.get('copyingAllowed')
		
		self.created = parse(data.get('created')).timestamp()
		self.updated = parse(data.get('updated')).timestamp()
		
		creator_data = data.get('creator')
		
		if creator_data:
			creator_type = creator_data.get('type')
			creator_id = creator_data.get('id')
			
			new_creator = None
			
			if creator_type == 'User':
				from .users import BaseUser
				
				new_creator = BaseUser(client, creator_id)
			elif creator_type == 'Group':
				from .groups import BaseGroup
				
				new_creator = BaseGroup(client, creator_id)
			
			self.creator = new_creator
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.name}>'
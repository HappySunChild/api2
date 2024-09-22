# https://presence.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse

from .baseprovider import BaseProvider
from ..classes.users import BaseUser
from ..classes.universes import BaseUniverse
from ..classes.places import BasePlace
from ..enums import PresenceType

if TYPE_CHECKING:
	from ..types import UserOrId
	from ..client import Client

PRESENCE_NAMES = [
	'Offline',
	'Online',
	'In Game',
	'Studio',
	'Invisible'
]

PRESENCE_COLORS = [
	0x3B3B3B,
	0x5883F2,
	0x52DE4B,
	0xDDAE4A,
	0xE04646
]

class Presence:
	def __init__(self, client: Client, data: dict) -> None:
		self.presence_type = PresenceType(data['userPresenceType'])
		
		self.last_online = parse(data['lastOnline']).timestamp()
		self.last_location = data['lastLocation']
		
		self.job_id = data['gameId']
		self.root_place_id = data['rootPlaceId']
		self.universe_id = data['universeId']
		self.user_id = data['userId']
		
		self.user = BaseUser(client, data['userId'])
		
		root_place = None
		universe = None
		
		if self.universe_id:
			universe = BaseUniverse(client, self.universe_id)
		
		if self.root_place_id:
			root_place = BasePlace(client, self.root_place_id)
		
		self.root_place = root_place
		self.universe = universe
	
	@property
	def color(self):
		return PRESENCE_COLORS[self.presence_type.value]
	
	@property
	def location_name(self):
		return PRESENCE_NAMES[self.presence_type.value]
	
	@property
	def game_link(self):
		if not self.root_place:
			return 'no game link'
		
		return self.root_place.link
	
	@property
	def join_link(self):
		if not self.root_place or not self.job_id:
			return 'no join link'
		
		return f'roblox://experiences/start?placeId={self.root_place_id}&gameInstanceId={self.job_id}'
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.last_location!r}>'
	
	def __eq__(self, value: object) -> bool:
		if not isinstance(value, self.__class__):
			return False
		
		return self.last_location == value.last_location and self.presence_type == value.presence_type

class PresenceProvider(BaseProvider):
	def get_user_presences(self, users: list[UserOrId]) -> list[Presence]:
		client = self.client
		
		presence_data, _ = client.fetcher.post(
			url=client.url_generator.get_url('presence', 'v1/presence/users'),
			payload={
				"userIds": list(map(int, users))
			}
		)
		
		return [Presence(client, data) for data in presence_data['userPresences']]
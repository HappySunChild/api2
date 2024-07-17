# https://presence.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse
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
		
		user = None
		root_place = None
		universe = None
		
		if client.config.allow_partials:
			user = BaseUser(client, data['userId'])
			universe = BaseUniverse(client, data['universeId'])
			root_place = BasePlace(client, data['rootPlaceId'])
		else:
			user = client.get_User(data['userId'])
			universe = client.get_Universe(data['universeId'])
			root_place = client.get_Place(data['rootPlaceId'])
		
		self.root_place = root_place
		self.universe = universe
		self.user = user
	
	@property
	def color(self):
		return PRESENCE_COLORS[self.presence_type.value]
	
	@property
	def location_name(self):
		return PRESENCE_NAMES[self.presence_type.value]
	
	@property
	def game_link(self):
		return self.root_place.link
	
	@property
	def join_link(self):
		return f'roblox://experiences/start?placeId={self.place_id}&gameInstanceId={self.job_id}'
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.last_location!r}>'

class PresenceProvider:
	def __init__(self, client: Client) -> None:
		self.client = client
	
	def get_user_presences(self, users: list[UserOrId]) -> list[Presence]:
		client = self.client
		
		presence_data, _ = client.fetcher.post(
			url=client.url_generator.get_url('presence', 'v1/presence/users'),
			json={
				"userIds": list(map(int, users))
			}
		)
		
		return [Presence(client, data) for data in presence_data['userPresences']]
# https://presence.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse
from ..classes.universes import BaseUniverse
from ..classes.places import BasePlace
from ..enums import PresenceType

if TYPE_CHECKING:
	from ..client import Client

presence_names = [
	'Offline',
	'Online',
	'In Game',
	'Studio',
	'Invisible'
]

presence_colors = [
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
		
		self.job_id = data.get('gameId')
		
		root_place = None
		universe = None
		
		if client.config.allow_partials:
			universe = BaseUniverse(client, data['universeId'])
			root_place = BasePlace(client, data['rootPlaceId'])
		else:
			universe = client.get_Universe(data['universeId'])
			root_place = client.get_Place(data['rootPlaceId'])
		
		self.root_place = root_place
		self.universe = universe
	
	@property
	def color(self):
		return presence_colors[self.presence_type.value]
	
	@property
	def location_name(self):
		return presence_names[self.presence_type.value]
	
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
	
	def get_user_presences(self, users: list):
		client = self.client
		
		presence_data, _ = client.fetcher.post(
			url=client.url_generator.get_url('presence', 'v1/presence/users'),
			json={
				"userIds": users
			}
		)
		
		return [Presence(client, data) for data in presence_data['userPresences']]
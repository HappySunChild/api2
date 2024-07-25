from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse

from .base import BaseData
from ..classes.universes import PartialUniverse
from ..classes.places import BasePlace

if TYPE_CHECKING:
	from ..client import Client

class BadgeStatistics:
	def __init__(self, statistic_data: dict) -> None:
		self.past_day_awarded_count = statistic_data.get('pastDayAwardedCount')
		self.awarded_count = statistic_data.get('awardedCount')
		self.win_rate_percentage = statistic_data.get('winRatePercentage')

class BaseBadge(BaseData):
	def get_icon(self, is_circular: bool = False):
		return self.client.thumbnails.get_badge_icons([self.id], is_circular=is_circular)[0]
	
	@property
	def link(self):
		return f'https://www.roblox.com/badges/{self.id}/badge'
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.id}>'

class PartialBadge(BaseBadge):
	def __init__(self, client: Client, data: dict) -> None:
		super().__init__(client, data['id'])
		
		self.raw = data
		
		self.name = data['name']
		self.description = data['description']
		self.enabled = data['enabled']
		
		self.created = parse(data['created']).timestamp()
		self.updated = parse(data['updated']).timestamp()
		
		self.statistics = BadgeStatistics(data['statistics'])
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self.name}>'

class UserBadge(PartialBadge):
	def __init__(self, client: Client, data: dict) -> None:
		super().__init__(client, data)
		
		self.awarder = BasePlace(client=client, id=data['awarder']['id'])

class Badge(PartialBadge):
	def __init__(self, client: Client, data: dict) -> None:
		super().__init__(client, data)
		
		self.awarding_universe = PartialUniverse(client=client, data=data['awardingUniverse'])
from __future__ import annotations
from typing import TYPE_CHECKING

from dateutil.parser import parse

from .base import BaseData

if TYPE_CHECKING:
	from ..client import Client

class BaseAsset(BaseData):
	def __init__(self, client: Client, id: int) -> None:
		super().__init__(client, id)

class Asset(BaseAsset):
	def __init__(self, client: Client, data: dict) -> None:
		self.id = data.get('assetId')
		
		super().__init__(client, self.id)
		
		self.created = parse(data['created']).timestamp()
		self.updated = parse(data['updated']).timestamp()
		
		owner = None
		
		if client.config.allow_partials:
			from ..classes.users import PartialUser
			
			owner = PartialUser(client, data['owner'])
		else:
			owner = client.get_User(data['owner']['userId'])
		
		self.owner = owner
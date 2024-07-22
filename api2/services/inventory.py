# https://inventory.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional

from ..enums import AssetType
from ..classes.assets import Asset
from ..utility.fetcher import PageIterator, SortOrder

if TYPE_CHECKING:
	from ..client import Client

class InventoryProvider:
	def __init__(self, client: Client) -> None:
		self.client = client
	
	def can_view_inventory(self, user_id: int):
		client = self.client
		
		inventory_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('inventory', f'v1/users/{user_id}/can-view-inventory')
		)
		
		return inventory_data['canView']
	
	def get_user_inventory(self, user_id: int, asset_type: AssetType, page_size: int = 10, sort_order: SortOrder = SortOrder.Descending, handler: Optional[Callable] = None):
		client = self.client
		
		if handler is None:
			handler = lambda data: Asset(client, data)
		
		return PageIterator(
			fetcher=client.fetcher,
			url=client.url_generator.get_url('inventory', f'v2/users/{user_id}/inventory/{asset_type.value}'),
			page_size=page_size,
			sort_order=sort_order,
			handler=handler
		)
# https://economy.roblox.com/docs/index.html
# https://premiumfeatures.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..client import Client

class EconomyProvider:
	def __init__(self, client: Client) -> None:
		self.client = client
	
	def get_user_has_premium(self, user_id: int):
		client = self.client
		
		has_premium, _ = client.fetcher.get(
			url=client.url_generator.get_url('premiumfeatures', f'v1/users/{user_id}/validate-membership')
		)
		
		return has_premium
	
	def get_user_currency(self, user_id: int):
		client = self.client
		
		currency_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('economy', f'v1/users/{user_id}/currency')
		)
		
		return currency_data['robux']
# https://economy.roblox.com/docs/index.html
# https://premiumfeatures.roblox.com/docs/index.html

from baseprovider import BaseProvider

class EconomyProvider(BaseProvider):
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
		
		try:
			return currency_data['robux']
		except:
			return -1
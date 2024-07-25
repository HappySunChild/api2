# https://users.roblox.com/docs/index.html

from ..classes.users import User, BaseUser, PartialUser, AuthenticatedUser

from .baseprovider import BaseProvider

class UserProvider(BaseProvider):
	def multiget_users_usernames(self, usernames: list[str], exclude_banned: bool = True) -> list[PartialUser]:
		client = self.client
		
		users_data, _ = client.fetcher.post(
			url=client.url_generator.get_url('users', 'v1/usernames/users'),
			payload={
				'usernames': usernames,
				'excludeBannedUsers': exclude_banned
			}
		)
		
		return [
			PartialUser(client=client, data=data)
			for data in users_data['data']
		]
	
	def multiget_users_ids(self, user_ids: list[int], exclude_banned: bool = True) -> list[PartialUser]:
		client = self.client
		
		users_data, _ = client.fetcher.post(
			url=client.url_generator.get_url('users', 'v1/users'),
			payload={
				'userIds': user_ids,
				'excludeBannedUsers': exclude_banned
			}
		)
		
		return [
			PartialUser(client=client, data=data)
			for data in users_data['data']
		]
	
	def get_base_user(self, user_id: int) -> BaseUser:
		return BaseUser(client=self.client, id=user_id)
	
	def get_user(self, user_id: int) -> User:
		client = self.client
		
		user_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('users', f'v1/users/{user_id}')
		)
		
		return User(client=client, data=user_data)
	
	def get_authenticated_user(self, full: bool = True):
		client = self.client
		
		user_data, _ = client.fetcher.get(
			url=client.url_generator.get_url('users', 'v1/users/authenticated')
		)
		
		if full:
			authenticated_user = AuthenticatedUser(client, user_data)
			authenticated_user.update_info()
			
			return authenticated_user
		
		return BaseUser(client, user_data['id'])
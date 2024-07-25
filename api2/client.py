from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

from .utility.fetcher import Fetcher
from .utility.url import URLGenerator

from .services.presence import PresenceProvider
from .services.economy import EconomyProvider
from .services.inventory import InventoryProvider
from .services.thumbnail import ThumbnailProvider
from .services.avatar import AvatarProvider
from .services.users import UserProvider

from .classes.groups import Group, BaseGroup
from .classes.users import User, BaseUser, AuthenticatedUser
from .classes.places import Place, BasePlace
from .classes.universes import Universe, BaseUniverse
from .classes.badges import Badge

if TYPE_CHECKING:
	from .types import UserOrId, PlaceOrId, UniverseOrId

class ClientConfig:
	def __init__(self,
			do_caching: bool = True,
			debug_print_requests: bool = False,
			retry_timer: float = 60
		):
		
		self._debug_print_requests = debug_print_requests
		self.do_caching = do_caching
		self.retry_timer = retry_timer

class Client:
	def __init__(self, token: str = None, config: Optional[ClientConfig] = None , base_url = 'roblox.com'):
		if config is None:
			config = ClientConfig()
		
		self.config = config
		self.cached = {
			'users': {},
			'places': {},
			'universes': {},
			
			'universe_ids': {}
		}
		
		self.fetcher = Fetcher(self)
		self.url_generator = URLGenerator(base_url)
		
		self.economy = EconomyProvider(self)
		self.presence = PresenceProvider(self)
		self.inventory = InventoryProvider(self)
		self.thumbnails = ThumbnailProvider(self)
		self.avatar = AvatarProvider(self)
		self.users = UserProvider(self)
		
		if token:
			self.set_token(token)
	
	def get_cache(self, cache_name: str, index: str):
		if not self.config.do_caching:
			return
		
		sub_cache = self.cached.get(cache_name)
		
		if sub_cache is None:
			print(f'missing subcache {cache_name}')
			
			return
		
		return sub_cache.get(index)
	
	def set_cache(self, cache_name: str, index: str, new_value: Any):
		if not self.config.do_caching:
			return
		
		sub_cache = self.cached.get(cache_name)
		
		if sub_cache is None:
			print(f'missing subcache {cache_name}')
			
			return
		
		sub_cache[index] = new_value
	
	
	def _get_universe_id(self, place_id: int) -> int:
		cached_id = self.get_cache('universe_ids', place_id)
		
		if cached_id:
			return cached_id
		
		universe_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('apis', f'universes/v1/places/{place_id}/universe')
		)
		
		universe_id = universe_data.get('universeId')
		
		self.set_cache('universe_ids', place_id, universe_id)
		
		return universe_id
	
	def set_token(self, token: str):
		self.fetcher.set_cookie('.ROBLOSECURITY', token)
	
	
	def get_User(self, user: UserOrId) -> User:
		user_id = int(user)
		
		cached_user = self.get_cache('users', user_id)
		
		if cached_user:
			return cached_user
		
		new_user = self.users.get_user(user_id=user_id)
		
		self.set_cache('users', user_id, new_user)
		
		return new_user
	
	def get_BaseUser(self, user_id: int) -> BaseUser:
		return self.users.get_base_user(user_id=user_id)
	
	def get_AuthenticatedUser(self, full: bool = True) -> AuthenticatedUser:
		return self.users.get_authenticated_user()
	
	def multiget_Users_usernames(self, usernames: list[str], exclude_banned: bool = True):
		return self.users.multiget_users_usernames(usernames=usernames, exclude_banned=exclude_banned)
	
	def multiget_Users_ids(self, user_ids: list[int], exclude_banned: bool = True):
		return self.users.multiget_users_ids(user_ids=user_ids, exclude_banned=exclude_banned)
	
	
	def get_Group(self, group_id: int) -> Group:
		group_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('groups', f'v1/groups/{group_id}')
		)
		
		return Group(self, group_data)
	
	def get_BaseGroup(self, group_id: int) -> BaseGroup:
		return BaseGroup(self, group_id)
	
	
	def get_Universe(self, universe: UniverseOrId=None, place: PlaceOrId=None) -> Universe:
		universe_id = None
		
		if universe:
			universe_id = int(universe)
		
		if place and not universe_id:
			universe_id = self._get_universe_id(int(place))
		
		cached_universe = self.get_cache('universes', universe_id)
		
		if cached_universe:
			return cached_universe
		
		new_universe = self.multiget_Universes([universe_id])[0]
		
		self.set_cache('universes', universe_id, new_universe)
		
		return new_universe
	
	def get_BaseUniverse(self, universe_id: int) -> BaseUniverse:
		return BaseUniverse(universe_id)
	
	def multiget_Universes(self, universe_ids: list[int]) -> list[Universe]:
		universes_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('games', 'v1/games'),
			params = {'universeIds': universe_ids}
		)
		
		return [Universe(self, data=universe_data) for universe_data in universes_data['data']]
	
	def multiget_Universes_place_ids(self, place_ids: list[int]) -> list[Universe]:
		places = self.multiget_Places(place_ids)
		
		return self.multiget_Universes([place.universe_id for place in places])
	
	
	def get_Place(self, place: PlaceOrId) -> Place:
		if not place:
			return
		
		place_id = int(place)
		
		cached_place = self.get_cache('places', place_id)
		
		if cached_place:
			return cached_place
		
		new_place = self.multiget_Places([place_id])[0]
		
		self.set_cache('places', place_id, new_place)
		
		return new_place
	
	def get_BasePlace(self, place_id: int) -> BasePlace:
		return BasePlace(self, place_id)
	
	def multiget_Places(self, place_ids: list[int]) -> list[Place]:
		places_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('games', 'v1/games/multiget-place-details'),
			params={'placeIds': place_ids}
		)
		
		return [Place(self, place_data) for place_data in places_data]
	
	
	def get_Badge(self, badge_id: int):
		badge_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('badges', f'v1/badges/{badge_id}')
		)
		
		return Badge(self, badge_data)
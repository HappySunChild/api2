from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

from .utility.fetcher import Fetcher
from .utility.url import URLGenerator

from .services.presence import PresenceProvider
from .services.economy import EconomyProvider
from .services.inventory import InventoryProvider
from .services.thumbnail import ThumbnailProvider

from .classes.groups import Group, BaseGroup
from .classes.users import User, BaseUser, AuthenticatedUser
from .classes.places import Place, BasePlace
from .classes.universes import Universe, BaseUniverse
from .classes.badges import Badge

if TYPE_CHECKING:
	from .types import UserOrId, PlaceOrId, UniverseOrId

class ClientConfig:
	def __init__(self,
			allow_partials: bool = True,
			do_caching: bool = True,
			debug_print_requests: bool = False,
			retry_timer: float = 60
		):
		
		self._debug_print_requests = debug_print_requests
		self.do_caching = do_caching
		self.allow_partials = allow_partials
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
	
	
	def _get_universe_id(self, place_id: int):
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
	
	
	def get_User(self, user: UserOrId):
		if isinstance(user, User):
			return user
		
		user_id = int(user)
		
		cached_user = self.get_cache('users', user_id)
		
		if cached_user:
			return cached_user
		
		user_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('users', f'v1/users/{user_id}')
		)
		
		user = User(self, user_data)
		
		self.set_cache('users', user_id, user)
		
		return user
	
	def get_base_User(self, user_id: int):
		return BaseUser(self, user_id)
	
	def get_authenticated_User(self, full: bool = True):
		user_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('users', f'v1/users/authenticated')
		)
		
		if full:
			authenticated_user = AuthenticatedUser(self, {'id': user_data['id']})
			authenticated_user.update_info()
			
			return authenticated_user
		
		return BaseUser(self, user_data['id'])
	
	
	def get_Group(self, group_id: int):
		group_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('groups', f'v1/groups/{group_id}')
		)
		
		return Group(self, group_data)
	
	def get_base_Group(self, group_id: int):
		return BaseGroup(self, group_id)
	
	
	def get_Universe(self, universe: UniverseOrId=None, place: PlaceOrId=None):
		universe_id = int(universe)
		
		if place and not universe_id:
			universe_id = self._get_universe_id(int(place))
		
		cached_universe = self.get_cache('universes', universe_id)
		
		if cached_universe:
			return cached_universe
		
		universe = self.multiget_Universes([universe_id])[0]
		
		self.set_cache('universes', universe_id, universe)
		
		return universe
	
	def get_base_Universe(self, universe_id: int):
		return BaseUniverse(universe_id)
	
	def multiget_Universes(self, universe_ids: list[int]):
		universes_data, _ = self.fetcher.get(
			url=self.url_generator.get_url('games', 'v1/games'),
			params = {'universeIds': universe_ids}
		)
		
		return [Universe(self, data=universe_data) for universe_data in universes_data['data']]
	
	def multiget_Universes_place_ids(self, place_ids: list[int]):
		places = self.multiget_Places(place_ids)
		
		return self.multiget_Universes([place.universe_id for place in places])
	
	
	def get_Place(self, place: PlaceOrId):
		if isinstance(place, Place):
			return place
		
		place_id = int(place)
		
		cached_place = self.get_cache('places', place_id)
		
		if cached_place:
			return cached_place
		
		place = self.multiget_Places([place_id])[0]
		
		self.set_cache('places', place_id, place)
		
		return place
	
	def get_base_Place(self, place_id: int):
		return BasePlace(self, place_id)
	
	def multiget_Places(self, place_ids: list[int]):
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
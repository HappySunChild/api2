from typing import Union

from .classes.badges import Badge, BaseBadge
from .classes.places import Place, BasePlace
from .classes.groups import Group, BaseGroup, GroupMember
from .classes.universes import Universe, BaseUniverse, PartialUniverse
from .classes.users import User, BaseUser, PartialUser, AuthenticatedUser, Friend
from .classes.assets import Asset, BaseAsset

from .utility.fetcher import Fetcher, Page, Pages, PageIterator
from .utility.url import URLGenerator

from .services.economy import EconomyProvider
from .services.inventory import InventoryProvider
from .services.presence import PresenceProvider, Presence
from .services.thumbnail import ThumbnailProvider, Thumbnail, UniverseThumbnails
from .services.avatar import Outfit

from .client import Client, ClientConfig

UserOrId = Union[BaseUser, int]
PlaceOrId = Union[BasePlace, int]
UniverseOrId = Union[BaseUniverse, int]
BadgeOrId = Union[BaseBadge, int]
OutfitOrId = Union[Outfit, int]
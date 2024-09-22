from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..client import Client

class BaseData:
	id = None
	
	def __init__(self, client: Client, id: int) -> None:
		if not id:
			raise Exception('Tried to create BaseData object without an id!')
		
		self.client = client
		self.id = id
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}>'
	
	def __int__(self):
		return self.id
	
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, self.__class__):
			return False
		
		return self.id == other.id
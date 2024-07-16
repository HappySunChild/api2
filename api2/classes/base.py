from __future__ import annotations

class BaseData:
	id = None
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}>'
	
	def __int__(self):
		return self.id
	
	def __eq__(self, other: object) -> bool:
		if isinstance(other, self.__class__):
			return self.id == other.id
		
		return False
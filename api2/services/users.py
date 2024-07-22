# https://users.roblox.com/docs/index.html

from __future__ import annotations
from typing import TYPE_CHECKING

from baseprovider import BaseProvider

class UserProvider(BaseProvider):
	def get_user(self, user_id: int):
		client = self.client
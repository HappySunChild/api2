from enum import Enum, IntEnum

class PresenceType(IntEnum):
	Offline = 0
	Online = 1
	InGame = 2
	InStudio = 3
	Invisible = 4


class ThumbnailState(Enum):
	Completed = 'Completed'
	InReview = 'InReview'
	Pending = 'Pending'
	Error = 'Error'
	Moderated = 'Moderated'
	Blocked = 'Blocked'

class ThumbnailFormat(Enum):
	Png = 'Png',
	Jpeg = 'Jpeg',
	Webp = 'Webp'


class UniverseThumbnailSize(Enum):
	Huge = '768x432'
	Large = '576x324'
	Medium = '480x270'
	Small = '384x216'
	Tiny = '256x144'


class PlaceThumbnailSize(Enum):
	Tiny = '50x50'
	Small = '128x128'
	Medium = '150x150'
	Large = '256x256'
	Huge = '420x420'
	Ginormous = '512x512'

class PlaceThumbnailPolicy(Enum):
	Placeholder = 'PlaceHolder'
	AutoGenerated = 'AutoGenerated'
	ForceAutoGenerated = 'ForceAutoGenerated'


class OutfitThumbnailSize(Enum):
	Normal = '150x150'
	Large = '420x420'


class UserThumbnailSize(Enum):
	Microscopic = '48x48'
	Molecular = '50x50'
	Minuscule = '60x60'
	Tiny = '75x75'
	Small = '100x100'
	Medium = '150x150'
	Decent = '180x180'
	Large = '352x352'
	Huge = '420x420'
	Ginormous = '720x720'

class UserThumbnailType(Enum):
	FullBody = 'avatar'
	Bust = 'avatar-bust'
	Headshot = 'avatar-headshot'


class AvatarType(Enum):
	R15 = 'R15'
	R6 = 'R6'

class OutfitType(Enum):
	All = 'All'
	Avatar = 'Avatar'
	DynamicHead = 'DynamicHead' # what the hell is this

class SortOrder(Enum):
	Ascending = 'Asc'
	Descending = 'Desc'

class AssetType(Enum):
	Image = 1
	Decal = 13
	Video = 62
	Audio = 3
	FontFamily = 73
	
	Mesh = 4
	MeshPart = 40
	Lua = 5
	Place = 9
	Model = 10
	Animation = 24
	Plugin = 38
	
	Gear = 19
	Badge = 21
	GamePass = 34
	
	DynamicHead = 79
	Head = 17
	Face = 18
	Torso = 27
	RightArm = 28
	LeftArm = 29
	LeftLeg = 30
	RightLeg = 31
	Package = 32
	
	HairAccessory = 41
	FaceAccessory = 42
	NeckAccessory = 43
	ShoulderAccessory = 44
	FrontAccessory = 45
	BackAccessory = 46
	WaistAccessory = 47
	EarAccessory = 57
	EyeAccessory = 58
	EyebrowAccessory = 76
	EyelashAccessory = 77
	
	TShirtAccessory = 64
	ShirtAccessory = 65
	PantsAccessory = 66
	JacketAccessory = 67
	SweaterAccessory = 68
	ShortsAccessory = 69	
	LeftShoeAccessory = 70
	RightShoeAccessory = 71
	DressSkirtAccessory = 72
	
	ClimbAnimation = 48
	DeathAnimation = 49 #?
	FallAnimation = 50
	IdleAnimation = 51
	JumpAnimation = 52
	RunAnimation = 53
	SwimAnimation = 54
	WalkAnimation = 55
	PoseAnimation = 56
	EmoteAnimation = 61
	MoodAnimation = 78
	
	Hat = 8
	Shirt = 11
	Pants = 12
	TShirt = 2
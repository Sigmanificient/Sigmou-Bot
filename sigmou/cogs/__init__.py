from .info import InfoCog
from .game import GameCog
from .time import OtherCog

cogs = (InfoCog, GameCog, OtherCog)
__all__ = ('cogs',)

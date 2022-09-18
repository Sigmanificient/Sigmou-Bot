from .game import GameCog
from .info import InfoCog
from .time import OtherCog

cogs = (InfoCog, GameCog, OtherCog)
__all__ = ("cogs",)

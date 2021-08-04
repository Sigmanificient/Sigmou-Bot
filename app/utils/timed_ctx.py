from typing import Tuple

from discord.ext import commands


class TimedCtx(commands.Context):
    """Custom ctx children signature with time for typing purposes."""
    __slots__: Tuple[str] = ('time',)

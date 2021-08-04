from typing import NoReturn

from discord.ext import commands

from app.bot import Bot
from app.utils.embeds import Embed
from app.utils.timed_ctx import TimedCtx


class GameCog(commands.Cog):
    """Game commands."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client


def setup(client: Bot) -> NoReturn:
    client.add_cog(GameCog(client))

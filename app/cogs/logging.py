from typing import NoReturn

from discord.ext import commands

from app.bot import Bot
from app.timed_ctx import TimedCtx
from app.utils.logging import Logger
from app.utils.timer import time


class LoggingCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client
        self.log: Logger = Logger()

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        connect_time: float = time("start", keep=True)
        self.log(f'Logged in as {self.client.user} after {connect_time:,.3f}s')

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        ready_time: float = time("start", keep=True)
        self.log(f'Ready after {ready_time:,.3f}s')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: TimedCtx) -> None:
        self.log(f"Successfully completed {ctx.command.name} by {ctx.author}")


def setup(client: Bot) -> NoReturn:
    client.add_cog(LoggingCog(client))
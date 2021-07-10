from typing import NoReturn

import discord
from discord.ext import commands

from app.bot import Bot
from app.timed_ctx import TimedCtx


class LoggingCog(commands.Cog):
    """Global Error reporting cog."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: TimedCtx, error: Exception) -> None:
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("> Une erreur est survenue sur un des paramètres de la commande")
            return

        await ctx.send(f"**Error report for command `{ctx.command}`**")
        await ctx.send(f"```{error}```")
        await ctx.send(f"```{error!r}```")


def setup(client: Bot) -> NoReturn:
    client.add_cog(LoggingCog(client))
